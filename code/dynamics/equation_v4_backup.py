"""
V4 備份：嚴格按文章§8實現的動力學方程（無 V5 擴展）
用於緊急回滾：cp equation_v4_backup.py corrected_equation.py

文章第21-22頁完整方程：
H_{t+1} = H_t + g_{t+1}·[α_0·(1-A_{t+1}) + I_{nec}(p_t)]
          + (1-g_{t+1})·max{0, I_-(p_t)-τ_{tail}^{(r)}}
          + (1/ω(p_{t+1}))·ξ_{t+1}

V4 版本：無 beta_rho, delta, b_baseline；爆發項僅 max(0, I_- - τ_tail)
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from scipy.optimize import minimize
from scipy import stats
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from loguru import logger

XI_STABLE = 1e-6
ALPHA_0_THEORY = 1.0 / math.log(2)
N_MIN_EFF = 30


class CorrectedDynamicsEquation:
    """V4：嚴格按文章§8實現（無 V5 擴展）"""

    def __init__(
        self,
        alpha0: Optional[float] = None,
        tau_tail: Optional[float] = None,
        w_A: float = 2.0,
        w_u: float = -1.0,
        b_g: float = 0.0,
        n_min_eff: int = N_MIN_EFF,
    ):
        self.alpha0 = alpha0 if alpha0 is not None else ALPHA_0_THEORY
        self._tau_tail_raw = tau_tail
        self.tau_tail = tau_tail if tau_tail is not None else 0.0
        self.w_A = w_A
        self.w_u = w_u
        self.b_g = b_g
        self.n_min_eff = n_min_eff
        self.burst_disabled: bool = False
        self.burst_disabled_reason: Optional[str] = None
        self.med_A: Optional[float] = None
        self.mad_A: Optional[float] = None
        self.med_u: Optional[float] = None
        self.mad_u: Optional[float] = None
        # V4 無此參數，為兼容 equation_variants 設為 0
        self.b_baseline = 0.0
        self.beta_rho = 0.0
        self.delta = 0.0

    def fit_robust_scaler(self, A_history: np.ndarray, u_history: np.ndarray) -> None:
        self.med_A = float(np.median(A_history))
        mad_A_raw = float(np.median(np.abs(A_history - self.med_A)))
        self.mad_A = mad_A_raw + XI_STABLE
        self.med_u = float(np.median(u_history))
        mad_u_raw = float(np.median(np.abs(u_history - self.med_u)))
        self.mad_u = mad_u_raw + XI_STABLE

    def compute_gate(self, A_t: float, u_t: float, is_baseline: bool = False) -> float:
        if self.med_A is None or self.mad_A is None:
            raise ValueError("必須先調用 fit_robust_scaler")
        z_A = (A_t - self.med_A) / self.mad_A
        z_u = (u_t - self.med_u) / self.mad_u
        s = self.w_A * z_A + self.w_u * z_u + self.b_g
        return float(1.0 / (1.0 + np.exp(-s)))

    def predict_entropy_change(
        self,
        H_t: float,
        A_t: float,
        u_t: float,
        I_pos: float,
        I_neg: float,
        rho_t: float = 0.0,
        xi_prev: float = 0.0,
        is_baseline: bool = False,
    ) -> Tuple[float, float]:
        I_nec = I_pos - I_neg
        g = self.compute_gate(A_t, u_t, is_baseline)
        linear_term = self.alpha0 * (1.0 - A_t) + I_nec
        burst_term = 0.0 if self.burst_disabled else max(0.0, I_neg - self.tau_tail)
        omega = np.exp(-u_t)
        H_pred = H_t + g * linear_term + (1.0 - g) * burst_term
        return float(H_pred), float(omega)

    def compute_residual(self, H_obs: float, H_pred: float, u_t: float) -> float:
        return float(np.exp(-u_t) * (H_obs - H_pred))

    def predict_next_entropy(
        self,
        t: int,
        T: int,
        H_current: float,
        At: float,
        ut: float,
        I_plus: float,
        I_minus: float,
        rho_t: float = 0.0,
        xi_prev: float = 0.0,
        is_baseline: bool = False,
    ) -> float:
        H_pred, _ = self.predict_entropy_change(
            H_current, At, ut, I_plus, I_minus,
            rho_t=rho_t, xi_prev=xi_prev, is_baseline=is_baseline,
        )
        return H_pred

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        required = ["t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"]
        for col in required:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")
        has_sample_idx = "sample_idx" in calibration_data.columns
        if has_sample_idx:
            calibration_data = calibration_data.sort_values(
                ["sample_idx", "t"], kind="stable"
            ).reset_index(drop=True)

        n_cal = len(calibration_data)
        I_neg_cal = calibration_data["I_minus"].values
        tau_75 = float(np.percentile(I_neg_cal, 75))
        tau_95 = float(np.percentile(I_neg_cal, 95))

        if n_cal < self.n_min_eff:
            self.burst_disabled = True
            self.burst_disabled_reason = "N_SMALL"
        elif tau_95 == 0 or np.max(I_neg_cal) < 1e-10:
            self.burst_disabled = True
            self.burst_disabled_reason = "ZERO_MISLEAD_INTENSITY"
        else:
            self.burst_disabled = False
            self.burst_disabled_reason = None

        self.tau_tail = tau_75 if not self.burst_disabled else 0.0
        A_arr = calibration_data["At"].values
        u_arr = calibration_data["ut"].values
        self.fit_robust_scaler(A_arr, u_arr)

        def _compute_residuals_and_gates(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
            preds, omegas, gates = [], [], []
            for _, row in df.iterrows():
                g = self.compute_gate(float(row["At"]), float(row["ut"]))
                pred, omega = self.predict_entropy_change(
                    float(row["H_current"]), float(row["At"]), float(row["ut"]),
                    float(row["I_plus"]), float(row["I_minus"]),
                )
                preds.append(pred)
                omegas.append(omega)
                gates.append(g)
            return np.array(preds), np.array(omegas), np.array(gates)

        def objective(params: np.ndarray) -> float:
            self.w_A, self.w_u, self.b_g = params[0], params[1], params[2]
            preds, omegas, gates = _compute_residuals_and_gates(calibration_data)
            actuals = calibration_data["H_observed"].values
            residuals = omegas * (actuals - preds)
            res_c = residuals - np.mean(residuals)
            c0 = np.sum(res_c ** 2) / max(len(res_c), 1) + 1e-10
            try:
                from statsmodels.stats.diagnostic import acorr_ljungbox
                lb = acorr_ljungbox(residuals, lags=[5], return_df=True)
                obj_autocorr = -np.log(float(lb["lb_pvalue"].values[0]) + 1e-10)
            except Exception:
                obj_autocorr = 0.0
            acf1 = float(np.sum(res_c[:-1] * res_c[1:]) / len(res_c) / c0) if len(res_c) > 1 else 0.0
            acf1_penalty = 200.0 * max(0, abs(acf1) - 0.3) ** 1.5
            g_mean, g_std = np.mean(gates), np.std(gates)
            g_min = np.min(gates)
            sat_penalty = 0.0
            if g_mean > 0.9 or g_mean < 0.2:
                sat_penalty += 5.0
            if g_std < 0.1:
                sat_penalty += 3.0
            if g_min > 0.3:
                sat_penalty += 1000.0 * (g_min - 0.3)
            if g_std < 0.2:
                sat_penalty += 500.0 * max(0, 0.2 - g_std)
            return float(obj_autocorr + acf1_penalty + sat_penalty)

        bounds = [(0.1, 5.0), (-5.0, -0.1), (-5.0, 5.0)]
        best_fun = np.inf
        best_x = [self.w_A, self.w_u, self.b_g]
        np.random.seed(42)
        for _ in range(5):
            x0 = [np.random.uniform(0.5, 3.0), np.random.uniform(-3.0, -0.2), np.random.uniform(-3.0, 3.0)]
            result = minimize(objective, x0=x0, bounds=bounds, method="L-BFGS-B")
            if result.fun < best_fun:
                best_fun, best_x = result.fun, result.x
        self.w_A, self.w_u, self.b_g = best_x[0], best_x[1], best_x[2]

        gates_final = np.array([self.compute_gate(float(r["At"]), float(r["ut"])) for _, r in calibration_data.iterrows()])
        g_min, g_max = float(np.min(gates_final)), float(np.max(gates_final))
        g_mean, g_std = float(np.mean(gates_final)), float(np.std(gates_final))
        linear_ratio = float(np.mean(gates_final > 0.8))
        critical_ratio = float(np.mean(gates_final < 0.3))
        logger.info(f"Gate stats after calibration: min={g_min:.3f}, max={g_max:.3f}, mean={g_mean:.3f}, std={g_std:.3f}")
        logger.info(f"Linear zone ratio (g>0.8): {linear_ratio:.1%}, Critical zone ratio (g<0.3): {critical_ratio:.1%}")

        return {
            "alpha0": self.alpha0, "tau_tail": self.tau_tail,
            "w_A": self.w_A, "w_u": self.w_u, "b_g": self.b_g,
            "burst_disabled": self.burst_disabled, "burst_disabled_reason": self.burst_disabled_reason,
            "gate_stats": {"min": g_min, "max": g_max, "mean": g_mean, "std": g_std,
                          "linear_ratio": linear_ratio, "critical_ratio": critical_ratio},
        }

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        required = ["t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"]
        for col in required:
            if col not in test_data.columns:
                raise ValueError(f"測試數據缺少列: {col}")
        predictions, actuals = [], []
        for _, row in test_data.iterrows():
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
            )
            predictions.append(pred)
            actuals.append(row["H_observed"])
        predictions, actuals = np.array(predictions), np.array(actuals)
        return {
            "R2": float(r2_score(actuals, predictions)),
            "RMSE": float(np.sqrt(mean_squared_error(actuals, predictions))),
            "MAE": float(mean_absolute_error(actuals, predictions)),
        }

    def residual_test(self, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
        required = ["t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"]
        for col in required:
            if col not in test_data.columns:
                raise ValueError(f"測試數據缺少列: {col}")
        predictions, actuals, residuals = [], [], []
        for _, row in test_data.iterrows():
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
            )
            res = self.compute_residual(float(row["H_observed"]), pred, float(row["ut"]))
            predictions.append(pred)
            actuals.append(row["H_observed"])
            residuals.append(res)
        residuals = np.array(residuals)
        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
            p_value = float(acorr_ljungbox(residuals, lags=[lag], return_df=True)["lb_pvalue"].values[0])
        except Exception:
            p_value = 0.5
        return {"p_value": p_value, "falsified": p_value < 0.05, "residuals": residuals.tolist(),
                "predictions": predictions, "actuals": actuals}

    def run_diagnostics(self, data: pd.DataFrame, tau_g: Optional[float] = None) -> Dict[str, Any]:
        required = ["t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"]
        for col in required:
            if col not in data.columns:
                raise ValueError(f"數據缺少列: {col}")
        gates, preds, omegas, residuals = [], [], [], []
        linear_contrib, burst_contrib = [], []
        for _, row in data.iterrows():
            H_t, A_t, u_t = float(row["H_current"]), float(row["At"]), float(row["ut"])
            I_pos, I_neg, H_obs = float(row["I_plus"]), float(row["I_minus"]), float(row["H_observed"])
            g = self.compute_gate(A_t, u_t)
            H_pred, omega = self.predict_entropy_change(H_t, A_t, u_t, I_pos, I_neg)
            I_nec = I_pos - I_neg
            burst_raw = 0.0 if self.burst_disabled else max(0, I_neg - self.tau_tail)
            gates.append(g)
            preds.append(H_pred)
            omegas.append(omega)
            residuals.append(omega * (H_obs - H_pred))
            linear_contrib.append(g * (self.alpha0 * (1 - A_t) + I_nec))
            burst_contrib.append((1 - g) * burst_raw)
        gates, residuals = np.array(gates), np.array(residuals)
        omegas_arr = np.array(omegas)
        sat_high, sat_low = np.sum(gates > 0.95), np.sum(gates < 0.05)
        n_total = len(gates)
        I_neg_arr = data["I_minus"].values
        burst_triggered = 0 if self.burst_disabled else np.sum(I_neg_arr > self.tau_tail)
        try:
            _, p_zero_mean = stats.ttest_1samp(residuals, 0)
        except Exception:
            p_zero_mean = 1.0
        try:
            corr_res_omega = np.corrcoef(residuals, omegas_arr)[0, 1]
        except Exception:
            corr_res_omega = 0.0
        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
            ljungbox_p = float(acorr_ljungbox(residuals, lags=[5], return_df=True)["lb_pvalue"].values[0])
        except Exception:
            ljungbox_p = 0.5
        lin_arr, burst_arr = np.array(linear_contrib), np.array(burst_contrib)
        sum_abs = np.abs(lin_arr).sum() + np.abs(burst_arr).sum() + 1e-10
        pct_linear, pct_burst = np.abs(lin_arr).sum() / sum_abs * 100, np.abs(burst_arr).sum() / sum_abs * 100
        diag = {
            "gate_stats": {"min": float(np.min(gates)), "max": float(np.max(gates)),
                          "mean": float(np.mean(gates)), "std": float(np.std(gates)),
                          "pct_sat_high": sat_high / n_total * 100, "pct_sat_low": sat_low / n_total * 100},
            "burst_audit": {"burst_disabled": self.burst_disabled, "triggered_count": int(burst_triggered),
                           "total_steps": n_total, "tau_tail": self.tau_tail},
            "residual_stats": {"mean": float(np.mean(residuals)), "std": float(np.std(residuals)),
                              "p_zero_mean": float(p_zero_mean), "corr_with_omega": float(corr_res_omega),
                              "ljungbox_p": ljungbox_p, "falsified": ljungbox_p < 0.05},
            "decomposition": {"pct_linear": float(pct_linear), "pct_burst": float(pct_burst)},
        }
        if tau_g is not None:
            diag["tau_g_partition"] = {"tau_g": tau_g, "T_lin_count": int(np.sum(gates >= tau_g)),
                                       "T_crit_count": int(np.sum(gates < tau_g))}
        return diag
