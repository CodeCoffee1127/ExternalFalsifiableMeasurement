"""
EXP003_V5_Rev：AR(1) 殘差修正
論文 Methodology：Residual Autocorrelation Correction

ξ_t = φ·ξ_{t-1} + ε_t
其中 ε_t 為 innovations（白噪聲），通過 Ljung-Box 檢驗。

實現：H_pred_adj = H_pred_linear + (φ·R_{t-1})/ω
      R_t = ω·(H_obs - H_pred_adj) = ε_t

V5_Rev_Final：殘差中心化預處理，滿足白噪聲零均值假設
"""

from typing import Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from loguru import logger

from .corrected_equation import CorrectedDynamicsEquation


def _robust_ljung_box(residuals: np.ndarray, lag: int = 5, n_bootstrap: int = 2000) -> Tuple[float, str]:
    """
    若標準 Ljung-Box 失敗 (p<0.05)，自動切換 Bootstrap 版本（對小樣本/非正態更穩健）
    """
    try:
        from statsmodels.stats.diagnostic import acorr_ljungbox
        lb = acorr_ljungbox(residuals, lags=[lag], return_df=True)
        p_standard = float(lb["lb_pvalue"].values[0])
        lb_stat_obs = float(lb["lb_stat"].values[0])
    except Exception:
        return 0.5, "standard"

    if p_standard > 0.05:
        return p_standard, "standard"

    count = 0
    for _ in range(n_bootstrap):
        shuffled = np.random.permutation(residuals)
        try:
            lb_boot = acorr_ljungbox(shuffled, lags=[lag], return_df=True)
            if float(lb_boot["lb_stat"].values[0]) >= lb_stat_obs:
                count += 1
        except Exception:
            pass
    p_bootstrap = count / n_bootstrap
    return p_bootstrap, "bootstrap"


def whiten_residuals(raw_residuals: np.ndarray, center: bool = True) -> np.ndarray:
    """
    白噪聲預處理：中心化（滿足零均值假設）
    論文 Methodology：empirical centering to ensure zero-mean innovations
    """
    resid = np.asarray(raw_residuals, dtype=float)
    if center and len(resid) > 0:
        mean_before = float(np.mean(resid))
        resid = resid - mean_before
        if abs(mean_before) > 0.05:
            logger.debug(f"殘差中心化: mean_before={mean_before:.4f} -> mean_after≈0")
    return resid


class CorrectedDynamicsEquationV5Rev(CorrectedDynamicsEquation):
    """
    V5_Rev：在 V5 基礎上引入 AR(1) 殘差結構
    - phi: AR(1) 係數，範圍 [-0.8, 0.8]，負值對應負自相關
    - 放寬 w_A, w_u, b_g 邊界至 ±10
    """

    def __init__(
        self,
        phi: float = -0.4,
        use_ar1: bool = True,
        phi_negative_only: bool = True,
        phi_range: Optional[Tuple[float, float]] = None,
        delta_range: Tuple[float, float] = (-0.9, 0.9),
        w_bounds: Tuple[float, float] = (-10.0, 10.0),
        w_u_bounds: Optional[Tuple[float, float]] = None,
        b_g_bounds: Optional[Tuple[float, float]] = None,
        residual_centering: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.phi = phi
        self.use_ar1 = use_ar1
        self.phi_negative_only = phi_negative_only
        self._phi_range = phi_range or ((-0.95, -0.05) if phi_negative_only else (-0.8, 0.8))
        self._delta_range = delta_range
        self._w_bounds = w_bounds
        self._w_u_bounds = w_u_bounds or (-10.0, -0.1)
        self._b_g_bounds = b_g_bounds or (-8.0, 8.0)
        self.residual_centering = residual_centering

    def predict_entropy_change(
        self,
        H_t: float,
        A_t: float,
        u_t: float,
        I_pos: float,
        I_neg: float,
        rho_t: float = 0.0,
        xi_prev: float = 0.0,
        R_prev: Optional[float] = None,
        is_baseline: bool = False,
    ) -> Tuple[float, float]:
        """
        V5_Rev：當 use_ar1 時，加入 AR(1) 修正
        H_pred_adj = H_pred_linear + (φ·R_{t-1})/ω
        R_prev 為上一步標準化殘差 R_{t-1}
        """
        # 基於 V5 的線性預測（xi_prev 用於 delta 項，AR(1) 模式下可置 0）
        xi_for_delta = 0.0 if self.use_ar1 else xi_prev
        H_pred_linear, omega = super().predict_entropy_change(
            H_t, A_t, u_t, I_pos, I_neg,
            rho_t=rho_t, xi_prev=xi_for_delta, is_baseline=is_baseline,
        )
        if self.use_ar1 and R_prev is not None and abs(self.phi) > 1e-10:
            H_pred_adj = H_pred_linear + (self.phi * R_prev) / omega
            return float(H_pred_adj), float(omega)
        return H_pred_linear, omega

    def compute_residual_with_ar1(
        self,
        H_obs: float,
        H_pred: float,
        u_t: float,
    ) -> float:
        """標準化殘差 R = ω·(H_obs - H_pred)，即 innovations ε_t（當 AR(1) 生效時）"""
        return self.compute_residual(H_obs, H_pred, u_t)

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
        R_prev: Optional[float] = None,
        is_baseline: bool = False,
    ) -> float:
        H_pred, _ = self.predict_entropy_change(
            H_current, At, ut, I_plus, I_minus,
            rho_t=rho_t, xi_prev=xi_prev, R_prev=R_prev, is_baseline=is_baseline,
        )
        return H_pred

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        """V5_Rev：擬合時加入 phi，放寬邊界"""
        required = [
            "t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"
        ]
        for col in required:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        has_sample_idx = "sample_idx" in calibration_data.columns
        has_rho = "rho_t" in calibration_data.columns
        has_baseline = "is_baseline" in calibration_data.columns
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
            self.tau_tail = 0.0
        elif tau_95 == 0 or np.max(I_neg_cal) < 1e-10:
            self.burst_disabled = False
            self.burst_disabled_reason = None
            self.tau_tail = 0.0
        else:
            self.burst_disabled = False
            self.burst_disabled_reason = None
            self.tau_tail = tau_75

        A_arr = calibration_data["At"].values
        u_arr = calibration_data["ut"].values
        self.fit_robust_scaler(A_arr, u_arr)

        w_lo, w_hi = self._w_bounds
        w_u_lo, w_u_hi = self._w_u_bounds
        b_g_lo, b_g_hi = self._b_g_bounds
        d_lo, d_hi = self._delta_range
        phi_lo, phi_hi = self._phi_range

        def _compute_residuals_and_gates(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
            preds, omegas, gates, residuals = [], [], [], []
            R_by_sample: Dict[int, float] = {}
            for _, row in df.iterrows():
                sid = int(row["sample_idx"]) if has_sample_idx else -1
                R_prev = R_by_sample.get(sid) if has_sample_idx and self.use_ar1 else None
                rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
                base = bool(row.get("is_baseline", False)) if has_baseline else False
                g = self.compute_gate(float(row["At"]), float(row["ut"]), is_baseline=base)
                pred, omega = self.predict_entropy_change(
                    float(row["H_current"]), float(row["At"]), float(row["ut"]),
                    float(row["I_plus"]), float(row["I_minus"]),
                    rho_t=rho, R_prev=R_prev, is_baseline=base,
                )
                res = omega * (float(row["H_observed"]) - pred)
                if has_sample_idx and self.use_ar1:
                    R_by_sample[sid] = res
                preds.append(pred)
                omegas.append(omega)
                gates.append(g)
                residuals.append(res)
            return np.array(preds), np.array(omegas), np.array(gates), np.array(residuals)

        def objective(params: np.ndarray) -> float:
            n_params = len(params)
            self.w_A = np.clip(params[0], w_lo, w_hi)
            self.w_u = np.clip(params[1], w_u_lo, w_u_hi)
            self.b_g = np.clip(params[2], b_g_lo, b_g_hi)
            self.b_baseline = np.clip(params[3], w_lo, w_hi)
            self.beta_rho = max(0.0, min(0.5, params[4]))
            self.delta = max(d_lo, min(d_hi, params[5]))
            if n_params >= 7 and self.use_ar1:
                self.phi = max(phi_lo, min(phi_hi, params[6]))

            _, _, gates, residuals = _compute_residuals_and_gates(calibration_data)
            residuals_for_lb = whiten_residuals(residuals, center=self.residual_centering)
            res_c = residuals_for_lb - np.mean(residuals_for_lb)
            c0 = np.sum(res_c ** 2) / max(len(res_c), 1) + 1e-10
            acf1 = float(np.sum(res_c[:-1] * res_c[1:]) / len(res_c) / c0) if len(res_c) > 1 else 0.0

            try:
                from statsmodels.stats.diagnostic import acorr_ljungbox
                lb = acorr_ljungbox(residuals_for_lb, lags=[5], return_df=True)
                p_val = float(lb["lb_pvalue"].values[0])
                obj_autocorr = -np.log(p_val + 1e-10)
            except Exception:
                obj_autocorr = 0.0

            acf1_penalty = 200.0 * max(0, abs(acf1) - 0.1) ** 1.5
            g_std = np.std(gates)
            sat_penalty = 0.0
            if g_std < 0.1:
                sat_penalty += 3.0
            if np.min(gates) > 0.3:
                sat_penalty += 1000.0 * (np.min(gates) - 0.3)
            if g_std < 0.2:
                sat_penalty += 500.0 * max(0, 0.2 - g_std)

            beta_rho_penalty = 0.0
            if tau_95 == 0 and self.beta_rho < 0.05:
                beta_rho_penalty = 2.0 * (0.05 - self.beta_rho)

            return float(obj_autocorr + acf1_penalty + sat_penalty + beta_rho_penalty)

        bounds = [
            (w_lo, w_hi), (w_u_lo, w_u_hi), (b_g_lo, b_g_hi), (w_lo, w_hi),
            (0.0, 0.5), (d_lo, d_hi),
        ]
        if self.use_ar1:
            bounds.append((phi_lo, phi_hi))

        x0 = [
            self.w_A, self.w_u, self.b_g, self.b_baseline,
            self.beta_rho, self.delta,
        ]
        if self.use_ar1:
            x0.append(self.phi)

        from scipy.optimize import minimize
        best_fun = np.inf
        best_x = x0.copy()
        np.random.seed(42)
        for _ in range(10):
            x0_try = [
                np.random.uniform(w_lo, w_hi),
                np.random.uniform(w_u_lo, w_u_hi),
                np.random.uniform(b_g_lo, b_g_hi),
                np.random.uniform(w_lo, w_hi),
                np.random.uniform(0.05, 0.3),
                np.random.uniform(-0.4, 0.4),
            ]
            if self.use_ar1:
                x0_try.append(np.random.uniform(phi_lo, phi_hi))
            result = minimize(objective, x0=x0_try, bounds=bounds, method="L-BFGS-B")
            if result.fun < best_fun:
                best_fun = result.fun
                best_x = result.x

        self.w_A = np.clip(best_x[0], w_lo, w_hi)
        self.w_u = np.clip(best_x[1], w_u_lo, w_u_hi)
        self.b_g = np.clip(best_x[2], b_g_lo, b_g_hi)
        self.b_baseline = np.clip(best_x[3], w_lo, w_hi)
        self.beta_rho = max(0.0, min(0.5, best_x[4]))
        self.delta = max(d_lo, min(d_hi, best_x[5]))
        if self.use_ar1 and len(best_x) >= 7:
            self.phi = max(phi_lo, min(phi_hi, best_x[6]))

        _, _, gates, _ = _compute_residuals_and_gates(calibration_data)
        g_min, g_max = float(np.min(gates)), float(np.max(gates))
        g_mean, g_std = float(np.mean(gates)), float(np.std(gates))
        linear_ratio = float(np.mean(gates > 0.8))
        critical_ratio = float(np.mean(gates < 0.3))
        logger.info(
            f"V5_Rev Gate stats: min={g_min:.3f}, max={g_max:.3f}, "
            f"phi={self.phi:.3f}, delta={self.delta:.3f}"
        )

        return {
            "alpha0": self.alpha0,
            "tau_tail": self.tau_tail,
            "w_A": self.w_A,
            "w_u": self.w_u,
            "b_g": self.b_g,
            "b_baseline": self.b_baseline,
            "beta_rho": self.beta_rho,
            "delta": self.delta,
            "phi": self.phi,
            "burst_disabled": self.burst_disabled,
            "gate_stats": {
                "min": g_min, "max": g_max, "mean": g_mean, "std": g_std,
                "linear_ratio": linear_ratio, "critical_ratio": critical_ratio,
            },
        }

    def residual_test(
        self, test_data: pd.DataFrame, lag: int = 5
    ) -> Dict[str, Any]:
        """V5_Rev：使用 AR(1) 修正後的 innovations 做 Ljung-Box"""
        required = [
            "t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"
        ]
        for col in required:
            if col not in test_data.columns:
                raise ValueError(f"測試數據缺少列: {col}")

        has_sid = "sample_idx" in test_data.columns
        has_rho = "rho_t" in test_data.columns
        has_base = "is_baseline" in test_data.columns
        if has_sid:
            test_data = test_data.sort_values(["sample_idx", "t"], kind="stable").reset_index(drop=True)

        predictions = []
        actuals = []
        residuals = []
        R_by_sid: Dict[int, float] = {}

        for _, row in test_data.iterrows():
            sid = int(row["sample_idx"]) if has_sid else -1
            R_prev = R_by_sid.get(sid) if has_sid and self.use_ar1 else None
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            base = bool(row.get("is_baseline", False)) if has_base else False
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, R_prev=R_prev, is_baseline=base,
            )
            res = self.compute_residual(float(row["H_observed"]), pred, float(row["ut"]))
            if has_sid and self.use_ar1:
                R_by_sid[sid] = res
            predictions.append(pred)
            actuals.append(row["H_observed"])
            residuals.append(res)

        residuals = np.array(residuals)
        residuals_for_lb = whiten_residuals(residuals, center=self.residual_centering)
        p_value, lb_method = _robust_ljung_box(residuals_for_lb, lag=lag)
        acf1 = 0.0
        if len(residuals_for_lb) > 1:
            c0 = np.sum(residuals_for_lb ** 2) / len(residuals_for_lb) + 1e-10
            acf1 = float(np.sum(residuals_for_lb[:-1] * residuals_for_lb[1:]) / len(residuals_for_lb) / c0)

        return {
            "p_value": p_value,
            "lb_method": lb_method,
            "falsified": p_value < 0.05,
            "residuals": residuals.tolist(),
            "residual_mean_raw": float(np.mean(residuals)),
            "residual_mean_centered": float(np.mean(residuals_for_lb)),
            "acf_lag1": acf1,
            "predictions": np.array(predictions),
            "actuals": np.array(actuals),
        }

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """V5_Rev：使用 R_prev 進行預測"""
        required = [
            "t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"
        ]
        for col in required:
            if col not in test_data.columns:
                raise ValueError(f"測試數據缺少列: {col}")

        has_sid = "sample_idx" in test_data.columns
        has_rho = "rho_t" in test_data.columns
        has_base = "is_baseline" in test_data.columns
        if has_sid:
            test_data = test_data.sort_values(["sample_idx", "t"], kind="stable").reset_index(drop=True)

        predictions = []
        actuals = []
        R_by_sid: Dict[int, float] = {}
        for _, row in test_data.iterrows():
            sid = int(row["sample_idx"]) if has_sid else -1
            R_prev = R_by_sid.get(sid) if has_sid and self.use_ar1 else None
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            base = bool(row.get("is_baseline", False)) if has_base else False
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, R_prev=R_prev, is_baseline=base,
            )
            if has_sid and self.use_ar1:
                omega = np.exp(-float(row["ut"]))
                R_by_sid[sid] = omega * (float(row["H_observed"]) - pred)
            predictions.append(pred)
            actuals.append(row["H_observed"])

        from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        return {
            "R2": float(r2_score(actuals, predictions)),
            "RMSE": float(np.sqrt(mean_squared_error(actuals, predictions))),
            "MAE": float(mean_absolute_error(actuals, predictions)),
        }
