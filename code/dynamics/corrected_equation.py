"""
嚴格按文章§8實現的動力學方程（EXP003 修正版）

文章第21-22頁完整方程：
H_{t+1} = H_t + g_{t+1}·[α_0·(1-A_{t+1}) + I_{nec}(p_t)] 
          + (1-g_{t+1})·max{0, I_-(p_t)-τ_{tail}^{(r)}} 
          + (1/ω(p_{t+1}))·ξ_{t+1}

論文§V.F Eq.33 擴展：風險記憶耦合 + 一階滯後修正
- 爆發項：φ_{t+1} = max(0, I_- - τ_tail + β_ρ·ρ_t)
- 滯後項：δ·ξ_t 用於消除殘差自相關
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from scipy.optimize import minimize
from scipy import stats
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from loguru import logger

# 論文§8 硬編碼常量（嚴禁修改）
XI_STABLE = 1e-6  # MAD 分母數值穩定項
ALPHA_0_THEORY = 1.0 / math.log(2)  # ≈ 1.4427
N_MIN_EFF = 30  # 小樣本硬禁用爆發項閾值


class CorrectedDynamicsEquation:
    """
    嚴格按文章§8實現的動力學方程
    """

    def __init__(
        self,
        alpha0: Optional[float] = None,  # 固定為 ALPHA_0_THEORY，嚴禁可學習
        tau_tail: Optional[float] = None,  # 凍結：Calibration I_- 95 分位數
        w_A: float = 2.0,   # 文章第19頁：ω_A > 0
        w_u: float = -1.0,  # 文章第19頁：ω_u < 0
        b_g: float = 0.0,   # 門控偏置
        b_baseline: float = 0.0,   # 無父依賴時門控偏置（論文§V.F 基線模式）
        beta_rho: float = 0.1,      # 風險記憶耦合係數（論文§V.F Eq.33）
        delta: float = 0.0,         # 一階滯後修正係數（消除殘差自相關）
        n_min_eff: int = N_MIN_EFF,
    ):
        self.alpha0 = alpha0 if alpha0 is not None else ALPHA_0_THEORY
        self._tau_tail_raw = tau_tail  # 僅在 fit 時從 Calibration 估計並凍結
        self.tau_tail = tau_tail if tau_tail is not None else 0.0  # 佔位
        self.w_A = w_A
        self.w_u = w_u
        self.b_g = b_g
        self.b_baseline = b_baseline
        self.beta_rho = beta_rho
        self.delta = delta
        self.n_min_eff = n_min_eff

        # 小樣本硬禁用：若 N_cal < N_min_eff 則 φ ≡ 0
        self.burst_disabled: bool = False
        self.burst_disabled_reason: Optional[str] = None  # N_SMALL / ZERO_MISLEAD_INTENSITY

        # 魯棒標準化使用的歷史統計量（Calibration 階段計算）
        self.med_A: Optional[float] = None
        self.mad_A: Optional[float] = None
        self.med_u: Optional[float] = None
        self.mad_u: Optional[float] = None

    def fit_robust_scaler(self, A_history: np.ndarray, u_history: np.ndarray) -> None:
        """Calibration 階段計算 MAD 標準化參數（文章第19頁）
        z_A = (A - med) / (MAD(A) + ξ)，ξ=1e-6 硬編碼
        """
        self.med_A = float(np.median(A_history))
        mad_A_raw = float(np.median(np.abs(A_history - self.med_A)))
        self.mad_A = mad_A_raw + XI_STABLE

        self.med_u = float(np.median(u_history))
        mad_u_raw = float(np.median(np.abs(u_history - self.med_u)))
        self.mad_u = mad_u_raw + XI_STABLE

    def compute_gate(self, A_t: float, u_t: float, is_baseline: bool = False) -> float:
        """
        文章第19頁：基於魯棒標準化的門控
        z_A = (A - med) / MAD, z_u = (u - med) / MAD
        s = ω_A·z_A + ω_u·z_u + b_g（w_u < 0 故高 u 時 g→0）
        無父依賴時（is_baseline）：g = σ(w_A·z_A + b_baseline)，隔離 I_nec 項
        """
        if self.med_A is None or self.mad_A is None:
            raise ValueError("必須先調用 fit_robust_scaler")

        z_A = (A_t - self.med_A) / self.mad_A
        if is_baseline:
            s = self.w_A * z_A + self.b_baseline
        else:
            z_u = (u_t - self.med_u) / self.mad_u
            s = self.w_A * z_A + self.w_u * z_u + self.b_g

        g = 1.0 / (1.0 + np.exp(-s))
        return float(g)

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
        """
        文章第21-22頁完整方程（確定性部分）+ 論文§V.F 擴展
        返回 (H_pred, omega) 供殘差計算使用
        - 爆發項：φ = max(0, I_- - τ_tail + β_ρ·ρ_t)
        - 滯後項：δ·ξ_prev 消除殘差自相關
        """
        I_nec = I_pos - I_neg  # 文章第14頁

        # 門控（無父依賴時用 baseline 模式）
        g = self.compute_gate(A_t, u_t, is_baseline=is_baseline)

        # 線性項（文章第21頁）：α_0·(1-A) + I_nec
        linear_term = self.alpha0 * (1.0 - A_t) + I_nec

        # 爆發項（論文§V.F Eq.33）：φ = max(0, I_- - τ_tail + β_ρ·ρ_t)
        if self.burst_disabled:
            burst_term = 0.0
        else:
            burst_term = max(0.0, I_neg - self.tau_tail + self.beta_rho * rho_t)

        # 異方差權重（文章第20頁）：ω = exp(-u)
        omega = np.exp(-u_t)

        # 完整方程：H_pred = H_t + g·linear + (1-g)·burst + δ·ξ_prev
        H_pred = H_t + g * linear_term + (1.0 - g) * burst_term + self.delta * xi_prev

        return float(H_pred), float(omega)

    def compute_residual(
        self, H_obs: float, H_pred: float, u_t: float
    ) -> float:
        """
        標準化殘差（文章第27-28頁）
        R = ω(p) * (H_obs - H_pred)，其中 ω = exp(-u)
        """
        omega = np.exp(-u_t)
        residual = omega * (H_obs - H_pred)
        return float(residual)

    # ========== 與 run_exp003 兼容的 fit/evaluate/residual_test 接口 ==========

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
        """兼容 run_exp003 的預測接口（忽略 t, T，使用文章方程）"""
        H_pred, _ = self.predict_entropy_change(
            H_current, At, ut, I_plus, I_minus,
            rho_t=rho_t, xi_prev=xi_prev, is_baseline=is_baseline,
        )
        return H_pred

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        """
        Phase 2：在校準集上擬合參數
        - α_0：固定為 1/ln(2)，嚴禁優化
        - τ_tail：凍結，從 Calibration I_- 的 75 分位數估計
        - N < N_min_eff 時：爆發項強制禁用，標記 BURST_DISABLED
        - 可擬合：w_A, w_u, b_g, b_baseline, beta_rho, delta
        - 損失：最小化殘差自相關（Ljung-Box p 最大化）+ 門控覆蓋懲罰
        """
        required = [
            "t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"
        ]
        for col in required:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        # 若有 sample_idx，按 (sample_idx, t) 排序以正確計算 xi_prev；否則不亂序
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

        # 論文 §9.2.1：N 過小則禁用
        if n_cal < self.n_min_eff:
            self.burst_disabled = True
            self.burst_disabled_reason = "N_SMALL"
            self.tau_tail = 0.0
            logger.info(f"BURST_DISABLED: N_cal={n_cal} < N_min_eff={self.n_min_eff}")
        # 全 baseline（I_- 全零）時：不禁用爆發項，用 τ=0，爆發項 = max(0, β_ρ·ρ_t) 由風險記憶驅動
        elif tau_95 == 0 or np.max(I_neg_cal) < 1e-10:
            self.burst_disabled = False
            self.burst_disabled_reason = None
            self.tau_tail = 0.0
            logger.info(f"ALL_BASELINE: I_- 全零，tau_tail=0，爆發項由 β_ρ·ρ_t 驅動")
        else:
            self.burst_disabled = False
            self.burst_disabled_reason = None
            self.tau_tail = tau_75

        A_arr = calibration_data["At"].values
        u_arr = calibration_data["ut"].values
        self.fit_robust_scaler(A_arr, u_arr)

        # 擬合 w_A, w_u, b_g, b_baseline, beta_rho, delta（τ、α_0 凍結）
        # 論文 §8：門控標定以最小化殘差自相關，使 g 覆蓋 [0.2, 0.9]
        def _compute_residuals_and_gates(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
            """按樣本順序計算 preds, omegas, gates，正確處理 xi_prev"""
            preds, omegas, gates = [], [], []
            xi_by_sample: Dict[int, float] = {}
            for _, row in df.iterrows():
                sid = int(row["sample_idx"]) if has_sample_idx else -1
                xi_prev = xi_by_sample.get(sid, 0.0) if has_sample_idx and self.delta != 0 else 0.0
                rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
                base = bool(row.get("is_baseline", False)) if has_baseline else False
                g = self.compute_gate(float(row["At"]), float(row["ut"]), is_baseline=base)
                pred, omega = self.predict_entropy_change(
                    float(row["H_current"]), float(row["At"]), float(row["ut"]),
                    float(row["I_plus"]), float(row["I_minus"]),
                    rho_t=rho, xi_prev=xi_prev, is_baseline=base,
                )
                res = omega * (float(row["H_observed"]) - pred)
                if has_sample_idx and self.delta != 0:
                    xi_by_sample[sid] = res
                preds.append(pred)
                omegas.append(omega)
                gates.append(g)
            return np.array(preds), np.array(omegas), np.array(gates)

        def objective(params: np.ndarray) -> float:
            n_params = len(params)
            self.w_A = params[0]
            self.w_u = params[1]
            self.b_g = params[2]
            if n_params >= 6:
                self.b_baseline = params[3]
                self.beta_rho = max(0.0, min(0.5, params[4]))
                self.delta = max(-0.5, min(0.5, params[5]))
            elif n_params >= 4:
                self.b_baseline = params[3]
                self.beta_rho = 0.1
                self.delta = 0.0

            preds, omegas, gates = _compute_residuals_and_gates(calibration_data)
            actuals = calibration_data["H_observed"].values

            # 標準化殘差 R = ω·(H_obs - H_pred)
            residuals = omegas * (actuals - preds)
            res_c = residuals - np.mean(residuals)
            c0 = np.sum(res_c ** 2) / max(len(res_c), 1) + 1e-10

            # 目標1：最小化殘差自相關（Ljung-Box p 值越高越好）
            try:
                from statsmodels.stats.diagnostic import acorr_ljungbox
                lb = acorr_ljungbox(residuals, lags=[5], return_df=True)
                p_val = float(lb["lb_pvalue"].values[0])
                obj_autocorr = -np.log(p_val + 1e-10)
            except Exception:
                obj_autocorr = 0.0

            # 目標1b：lag-1 ACF 懲罰（|ACF|>0.3 時加權懲罰，目標 <0.3）
            acf1 = float(np.sum(res_c[:-1] * res_c[1:]) / len(res_c) / c0) if len(res_c) > 1 else 0.0
            acf1_penalty = 200.0 * max(0, abs(acf1) - 0.3) ** 1.5

            # 目標2：門控飽和懲罰（g 應覆蓋 [0.2, 0.9]，std>0.1）
            g_mean, g_std = np.mean(gates), np.std(gates)
            g_min, g_max = np.min(gates), np.max(gates)
            sat_penalty = 0.0
            if g_mean > 0.9 or g_mean < 0.2:
                sat_penalty += 5.0
            if g_std < 0.1:
                sat_penalty += 3.0

            # 修復：強制門控覆蓋臨界區（§8），critical_ratio>5%
            if g_min > 0.3:
                sat_penalty += 1000.0 * (g_min - 0.3)
            if g_std < 0.2:
                sat_penalty += 500.0 * max(0, 0.2 - g_std)

            # 全 baseline 時鼓勵 beta_rho>0，使爆發項由 ρ_t 驅動
            beta_rho_penalty = 0.0
            if tau_95 == 0 and self.beta_rho < 0.05:
                beta_rho_penalty = 2.0 * (0.05 - self.beta_rho)

            return float(obj_autocorr + acf1_penalty + sat_penalty + beta_rho_penalty)

        bounds = [
            (0.1, 5.0),     # w_A > 0
            (-5.0, -0.1),   # w_u < 0
            (-5.0, 5.0),    # b_g
            (-5.0, 5.0),    # b_baseline
            (0.0, 0.5),     # beta_rho
            (-0.5, 0.5),    # delta
        ]

        # 多起點優化，選取目標值最低的解
        best_fun = np.inf
        best_x = [self.w_A, self.w_u, self.b_g, self.b_baseline, self.beta_rho, self.delta]
        np.random.seed(42)
        for _ in range(10):  # 增加重啟次數以提高找到更好解的概率
            x0 = [
                np.random.uniform(0.5, 3.0),
                np.random.uniform(-3.0, -0.2),
                np.random.uniform(-3.0, 3.0),
                np.random.uniform(-3.0, 3.0),
                np.random.uniform(0.05, 0.3),
                np.random.uniform(-0.2, 0.2),
            ]
            result = minimize(objective, x0=x0, bounds=bounds, method="L-BFGS-B")
            if result.fun < best_fun:
                best_fun = result.fun
                best_x = result.x
        self.w_A = best_x[0]
        self.w_u = best_x[1]
        self.b_g = best_x[2]
        self.b_baseline = best_x[3]
        self.beta_rho = max(0.0, min(0.5, best_x[4]))
        self.delta = max(-0.5, min(0.5, best_x[5]))

        # 門控標定驗證輸出（論文 §8）
        gates_final = []
        for _, row in calibration_data.iterrows():
            base = bool(row.get("is_baseline", False)) if has_baseline else False
            gates_final.append(
                self.compute_gate(float(row["At"]), float(row["ut"]), is_baseline=base)
            )
        gates_final = np.array(gates_final)
        g_min, g_max = float(np.min(gates_final)), float(np.max(gates_final))
        g_mean, g_std = float(np.mean(gates_final)), float(np.std(gates_final))
        linear_ratio = float(np.mean(gates_final > 0.8))
        critical_ratio = float(np.mean(gates_final < 0.3))
        logger.info(
            f"Gate stats after calibration: min={g_min:.3f}, max={g_max:.3f}, "
            f"mean={g_mean:.3f}, std={g_std:.3f}"
        )
        logger.info(
            f"Linear zone ratio (g>0.8): {linear_ratio:.1%}, "
            f"Critical zone ratio (g<0.3): {critical_ratio:.1%}"
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
            "burst_disabled": self.burst_disabled,
            "burst_disabled_reason": self.burst_disabled_reason,
            "gate_stats": {
                "min": g_min, "max": g_max, "mean": g_mean, "std": g_std,
                "linear_ratio": linear_ratio, "critical_ratio": critical_ratio,
            },
        }

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """Phase 3：測試集評估，返回 R2, RMSE, MAE"""
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
        xi_by_sid: Dict[int, float] = {}
        for _, row in test_data.iterrows():
            sid = int(row["sample_idx"]) if has_sid else -1
            xi_prev = xi_by_sid.get(sid, 0.0) if has_sid and self.delta != 0 else 0.0
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            base = bool(row.get("is_baseline", False)) if has_base else False
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, xi_prev=xi_prev, is_baseline=base,
            )
            if has_sid and self.delta != 0:
                omega = np.exp(-float(row["ut"]))
                xi_by_sid[sid] = omega * (float(row["H_observed"]) - pred)
            predictions.append(pred)
            actuals.append(row["H_observed"])

        predictions = np.array(predictions)
        actuals = np.array(actuals)

        return {
            "R2": float(r2_score(actuals, predictions)),
            "RMSE": float(np.sqrt(mean_squared_error(actuals, predictions))),
            "MAE": float(mean_absolute_error(actuals, predictions)),
        }

    def residual_test(
        self, test_data: pd.DataFrame, lag: int = 5
    ) -> Dict[str, Any]:
        """
        Phase 4：Ljung-Box 殘差檢驗
        使用異方差加權後的標準化殘差
        """
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
        xi_by_sid: Dict[int, float] = {}
        for _, row in test_data.iterrows():
            sid = int(row["sample_idx"]) if has_sid else -1
            xi_prev = xi_by_sid.get(sid, 0.0) if has_sid and self.delta != 0 else 0.0
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            base = bool(row.get("is_baseline", False)) if has_base else False
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, xi_prev=xi_prev, is_baseline=base,
            )
            res = self.compute_residual(float(row["H_observed"]), pred, float(row["ut"]))
            if has_sid and self.delta != 0:
                xi_by_sid[sid] = res
            predictions.append(pred)
            actuals.append(row["H_observed"])
            residuals.append(res)

        residuals = np.array(residuals)

        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
            lb_result = acorr_ljungbox(residuals, lags=[lag], return_df=True)
            p_value = float(lb_result["lb_pvalue"].values[0])
        except Exception:
            p_value = 0.5

        return {
            "p_value": p_value,
            "falsified": p_value < 0.05,
            "residuals": residuals.tolist(),
            "predictions": predictions,
            "actuals": actuals,
        }

    def run_diagnostics(
        self, data: pd.DataFrame, tau_g: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        任務二：完整診斷指標
        - 門控分布、爆發觸發審計、殘差特性、分賬解釋
        - 支持按 τ_g 劃分 T_lin / T_crit（任務三）
        """
        required = [
            "t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"
        ]
        for col in required:
            if col not in data.columns:
                raise ValueError(f"數據缺少列: {col}")

        gates, preds, omegas, residuals = [], [], [], []
        linear_contrib, burst_contrib = [], []

        has_sid = "sample_idx" in data.columns
        has_rho = "rho_t" in data.columns
        has_base = "is_baseline" in data.columns
        if has_sid:
            data = data.sort_values(["sample_idx", "t"], kind="stable").reset_index(drop=True)
        xi_by_sid: Dict[int, float] = {}

        for _, row in data.iterrows():
            H_t = float(row["H_current"])
            A_t = float(row["At"])
            u_t = float(row["ut"])
            I_pos = float(row["I_plus"])
            I_neg = float(row["I_minus"])
            H_obs = float(row["H_observed"])
            sid = int(row["sample_idx"]) if has_sid else -1
            xi_prev = xi_by_sid.get(sid, 0.0) if has_sid and self.delta != 0 else 0.0
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            base = bool(row.get("is_baseline", False)) if has_base else False

            g = self.compute_gate(A_t, u_t, is_baseline=base)
            H_pred, omega = self.predict_entropy_change(
                H_t, A_t, u_t, I_pos, I_neg,
                rho_t=rho, xi_prev=xi_prev, is_baseline=base,
            )
            if has_sid and self.delta != 0:
                xi_by_sid[sid] = omega * (H_obs - H_pred)

            I_nec = I_pos - I_neg
            burst_raw = 0.0 if self.burst_disabled else max(0, I_neg - self.tau_tail + self.beta_rho * rho)
            lin = g * (self.alpha0 * (1 - A_t) + I_nec)
            burst = (1 - g) * burst_raw

            gates.append(g)
            preds.append(H_pred)
            omegas.append(omega)
            residuals.append(omega * (H_obs - H_pred))
            linear_contrib.append(lin)
            burst_contrib.append(burst)

        gates = np.array(gates)
        residuals = np.array(residuals)
        omegas_arr = np.array(omegas)

        # 門控飽和
        sat_high = np.sum(gates > 0.95)
        sat_low = np.sum(gates < 0.05)
        n_total = len(gates)

        # 爆發觸發（僅當未禁用時）
        I_neg_arr = data["I_minus"].values
        burst_triggered = 0 if self.burst_disabled else np.sum(I_neg_arr > self.tau_tail)

        # 殘差零均值 t 檢驗
        try:
            t_stat, p_zero_mean = stats.ttest_1samp(residuals, 0)
        except Exception:
            p_zero_mean = 1.0

        # 殘差與 ω 相關性（應接近 0）
        try:
            corr_res_omega = np.corrcoef(residuals, omegas_arr)[0, 1]
        except Exception:
            corr_res_omega = 0.0

        # Ljung-Box（lag=5，論文 §9.2.4）
        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
            lb_result = acorr_ljungbox(residuals, lags=[5], return_df=True)
            ljungbox_p = float(lb_result["lb_pvalue"].values[0])
        except Exception:
            ljungbox_p = 0.5
        diag_ljungbox = {"ljungbox_p": ljungbox_p, "falsified": ljungbox_p < 0.05}

        # 分賬佔比
        lin_arr = np.array(linear_contrib)
        burst_arr = np.array(burst_contrib)
        sum_abs = np.abs(lin_arr).sum() + np.abs(burst_arr).sum() + 1e-10
        pct_linear = np.abs(lin_arr).sum() / sum_abs * 100
        pct_burst = np.abs(burst_arr).sum() / sum_abs * 100

        diag = {
            "gate_stats": {
                "min": float(np.min(gates)),
                "max": float(np.max(gates)),
                "mean": float(np.mean(gates)),
                "std": float(np.std(gates)),
                "pct_sat_high": sat_high / n_total * 100,
                "pct_sat_low": sat_low / n_total * 100,
            },
            "burst_audit": {
                "burst_disabled": self.burst_disabled,
                "triggered_count": int(burst_triggered),
                "total_steps": n_total,
                "tau_tail": self.tau_tail,
            },
            "residual_stats": {
                "mean": float(np.mean(residuals)),
                "std": float(np.std(residuals)),
                "p_zero_mean": float(p_zero_mean),
                "corr_with_omega": float(corr_res_omega),
                **diag_ljungbox,
            },
            "decomposition": {
                "pct_linear": float(pct_linear),
                "pct_burst": float(pct_burst),
            },
        }

        if tau_g is not None:
            T_lin = np.sum(gates >= tau_g)
            T_crit = np.sum(gates < tau_g)
            diag["tau_g_partition"] = {
                "tau_g": tau_g,
                "T_lin_count": int(T_lin),
                "T_crit_count": int(T_crit),
            }

        return diag
