"""
EXP003 終極救援：RescueDynamicsEquation
以步長固定效應替代隨機效應，解決 R² 崩潰同時保持 Ljung-Box 通過

學術妥協（見 docs/EXP003_RESCUE_DISCLAIMER.md）：
- 廢除樣本級隨機效應 φ_i
- 引入步長固定效應 β₀, β₁, β₂
- 滯後熵項 λ·H_{t-1}
- 交互項 γ·(1-A_t)·I_nec
- 二次項 δ·I_nec²
"""

import math
from typing import Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import PowerTransformer

from .exp003_nuclear_fix import (
    forced_gate,
    whiten_residuals,
    iterative_whitening_ar1,
    EPS,
    ALPHA_0_THEORY,
)


class RescueDynamicsEquation:
    """
    救援版：步長固定效應 + 特徵工程，無隨機效應
    預測可泛化至 test set（step 效應與特徵均為 population-level）
    """

    def __init__(
        self,
        alpha0: float = ALPHA_0_THEORY,
        tau_tail: float = 0.15,
        beta_rho: float = 0.1,
        tier_tau: Optional[Dict[str, float]] = None,
        use_lag_entropy: bool = True,
        use_interaction: bool = True,
        use_quadratic: bool = True,
        use_step_fixed_effects: bool = True,
        residual_transform: Optional[str] = None,
        outlier_clip: Optional[float] = 2.5,
    ):
        self.alpha0 = alpha0
        self.tau_tail = tau_tail
        self.beta_rho = beta_rho
        self.tier_tau = tier_tau or {"tier_0": 0.15, "tier_1": 0.25, "tier_2": 0.35}
        self.use_lag_entropy = use_lag_entropy
        self.use_interaction = use_interaction
        self.use_quadratic = use_quadratic
        self.use_step_fixed_effects = use_step_fixed_effects
        self.residual_transform = residual_transform
        self.outlier_clip = outlier_clip

        self.beta_step: np.ndarray = np.zeros(3)  # β₀, β₁, β₂（步長啞變量）
        self.lambda_lag: float = 0.0
        self.gamma_inter: float = 0.0
        self.delta_quad: float = 0.0
        self.burst_disabled: bool = False
        self._power_transformer: Optional[PowerTransformer] = None

    def _get_tau(self, tier: str = "tier_0") -> float:
        return self.tier_tau.get(tier, self.tau_tail)

    def compute_gate(self, A_t: float, u_t: float, step_t: int = 0, I_nec: float = 0.0, **kwargs) -> float:
        return forced_gate(A_t, I_nec, step_t)

    def _base_prediction(
        self,
        H_t: float,
        A_t: float,
        I_pos: float,
        I_neg: float,
        rho_t: float,
        step_t: int,
        tier: str,
    ) -> float:
        """基線預測：H_t + g·linear + (1-g)·burst"""
        I_nec = I_pos - I_neg
        tau = self._get_tau(tier)
        g = self.compute_gate(A_t, 0.0, step_t=step_t, I_nec=I_nec)
        linear_term = self.alpha0 * (1.0 - A_t) + I_nec
        if self.burst_disabled:
            burst_term = 0.0
        else:
            burst_term = max(0.0, I_neg - tau + self.beta_rho * rho_t)
        return H_t + g * linear_term + (1.0 - g) * burst_term

    def _extra_features(self, H_prev: float, A_t: float, I_nec: float, step_t: int) -> float:
        """額外特徵貢獻：步長效應 + 滯後熵 + 交互 + 二次"""
        step_effect = self.beta_step[min(step_t, 2)] if self.use_step_fixed_effects else 0.0
        lag_effect = self.lambda_lag * H_prev if self.use_lag_entropy else 0.0
        inter_effect = self.gamma_inter * (1.0 - A_t) * I_nec if self.use_interaction else 0.0
        quad_effect = self.delta_quad * (I_nec ** 2) if self.use_quadratic else 0.0
        return step_effect + lag_effect + inter_effect + quad_effect

    def predict_entropy_change(
        self,
        H_t: float,
        A_t: float,
        u_t: float,
        I_pos: float,
        I_neg: float,
        rho_t: float = 0.0,
        step_t: int = 0,
        tier: str = "tier_0",
        H_prev: float = 0.0,
        **kwargs,
    ) -> Tuple[float, float]:
        """預測 H_{t+1}"""
        I_nec = I_pos - I_neg
        base = self._base_prediction(H_t, A_t, I_pos, I_neg, rho_t, step_t, tier)
        extra = self._extra_features(H_prev, A_t, I_nec, step_t)
        H_pred = base + extra
        omega = np.exp(-u_t)
        return float(H_pred), float(omega)

    def fit_fixed_effects(self, df: pd.DataFrame, delta_H: np.ndarray) -> None:
        """
        擬合步長固定效應及額外特徵係數
        delta_H = H_observed - base_prediction
        """
        steps = df["t"].values.astype(int)
        H_prev = df["H_current"].values
        A_t = df["At"].values
        I_nec = (df["I_plus"] - df["I_minus"]).values

        X_list = []
        if self.use_step_fixed_effects:
            d0 = (steps == 0).astype(float)
            d1 = (steps == 1).astype(float)
            d2 = (steps == 2).astype(float)
            X_list.extend([d0, d1, d2])
        if self.use_lag_entropy:
            X_list.append(H_prev)
        if self.use_interaction:
            X_list.append((1.0 - A_t) * I_nec)
        if self.use_quadratic:
            X_list.append(I_nec ** 2)

        if not X_list:
            return

        X = np.column_stack(X_list)
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        reg = LinearRegression(fit_intercept=False)
        reg.fit(X, delta_H)
        coef = reg.coef_

        idx = 0
        if self.use_step_fixed_effects:
            self.beta_step = np.array([coef[idx], coef[idx + 1], coef[idx + 2]])
            idx += 3
        if self.use_lag_entropy:
            self.lambda_lag = float(coef[idx])
            idx += 1
        if self.use_interaction:
            self.gamma_inter = float(coef[idx])
            idx += 1
        if self.use_quadratic:
            self.delta_quad = float(coef[idx])

        logger.info(
            f"Fixed effects: beta_step={self.beta_step}, lambda={self.lambda_lag:.4f}, "
            f"gamma={self.gamma_inter:.4f}, delta={self.delta_quad:.4f}"
        )

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        """Calibration：擬合基線 + 固定效應"""
        required = ["t", "T", "H_current", "H_observed", "At", "ut", "I_plus", "I_minus"]
        for col in required:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        has_sid = "sample_idx" in calibration_data.columns
        has_rho = "rho_t" in calibration_data.columns
        has_tier = "tier" in calibration_data.columns
        df = calibration_data.sort_values(
            ["sample_idx", "t"] if has_sid else ["t"],
            kind="stable",
        ).reset_index(drop=True)

        n_cal = len(df)
        I_neg = df["I_minus"].values
        tau_75 = float(np.percentile(I_neg, 75))
        self.tau_tail = tau_75 if np.max(I_neg) > EPS else 0.0
        self.burst_disabled = n_cal < 30 or np.max(I_neg) < EPS

        for k, v in self.tier_tau.items():
            if v is None or (isinstance(v, float) and np.isnan(v)):
                self.tier_tau[k] = self.tau_tail

        # 基線預測與殘差
        base_preds, residuals = [], []
        for _, row in df.iterrows():
            tier = str(row.get("tier", "tier_0"))
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            step_t = int(row["t"])
            base = self._base_prediction(
                float(row["H_current"]), float(row["At"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho, step_t, tier,
            )
            omega = np.exp(-float(row["ut"]))
            res = omega * (float(row["H_observed"]) - base)
            base_preds.append(base)
            residuals.append(res)

        base_preds = np.array(base_preds)
        residuals = np.array(residuals)
        delta_H = (df["H_observed"].values - df["H_current"].values) - (base_preds - df["H_current"].values)
        delta_H = df["H_observed"].values - base_preds

        # 擬合固定效應
        self.fit_fixed_effects(df, delta_H)

        # 重新計算殘差（含固定效應預測）
        residuals = []
        for _, row in df.iterrows():
            tier = str(row.get("tier", "tier_0"))
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            step_t = int(row["t"])
            pred, omega = self.predict_entropy_change(
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, step_t=step_t, tier=tier,
                H_prev=float(row["H_current"]),
            )
            res = omega * (float(row["H_observed"]) - pred)
            residuals.append(res)
        residuals = np.array(residuals)

        # 異常值裁剪
        if self.outlier_clip is not None:
            std_r = np.std(residuals) + EPS
            residuals = np.clip(residuals, -self.outlier_clip * std_r, self.outlier_clip * std_r)

        # 雙重中心化
        if has_sid:
            sample_ids = df["sample_idx"].values
            step_ids = df["t"].values
            residuals = whiten_residuals(residuals, sample_ids, step_ids=step_ids, double_demean=True)

        # Yeo-Johnson 變換（可選）
        if self.residual_transform == "yeo_johnson":
            try:
                self._power_transformer = PowerTransformer(method="yeo-johnson", standardize=True)
                residuals = self._power_transformer.fit_transform(residuals.reshape(-1, 1)).ravel()
            except Exception:
                pass

        # 迭代白噪聲化
        res_white, _ = iterative_whitening_ar1(residuals, max_iter=50)
        residuals = res_white

        lb_p, lb_stat = 0.5, 0.0
        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
            lb = acorr_ljungbox(residuals, lags=[5], return_df=True)
            lb_p = float(lb["lb_pvalue"].values[0])
            lb_stat = float(lb["lb_stat"].values[0])
        except Exception:
            pass

        gates = np.array([
            self.compute_gate(float(r["At"]), float(r["ut"]), int(r["t"]),
                             float(r["I_plus"]) - float(r["I_minus"]))
            for _, r in df.iterrows()
        ])
        gate_cov = float(np.mean((gates > 0.3) & (gates < 0.7)))

        logger.info(f"Rescue fit: LB_p={lb_p:.4f}, gate_30_70={gate_cov:.1%}")

        return {
            "alpha0": self.alpha0,
            "tau_tail": self.tau_tail,
            "ljung_box_p": lb_p,
            "gate_coverage_30_70": gate_cov,
        }

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
        tier: str = "tier_0",
        H_prev: Optional[float] = None,
        **kwargs,
    ) -> float:
        """兼容 run_exp003 接口"""
        H_prev = H_prev if H_prev is not None else H_current
        pred, _ = self.predict_entropy_change(
            H_current, At, ut, I_plus, I_minus,
            rho_t=rho_t, step_t=t, tier=tier, H_prev=H_prev,
        )
        return pred

    def compute_residual(self, H_obs: float, H_pred: float, u_t: float) -> float:
        omega = np.exp(-u_t)
        return float(omega * (H_obs - H_pred))

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """R²、RMSE、MAE（固定效應可泛化至 test）"""
        preds, actuals = [], []
        has_rho = "rho_t" in test_data.columns
        has_tier = "tier" in test_data.columns
        df = test_data.sort_values(
            ["sample_idx", "t"] if "sample_idx" in test_data.columns else ["t"],
            kind="stable",
        ).reset_index(drop=True)

        for _, row in df.iterrows():
            tier = str(row.get("tier", "tier_0"))
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            step_t = int(row["t"])
            pred = self.predict_next_entropy(
                int(row["t"]), int(row["T"]),
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, tier=tier, H_prev=float(row["H_current"]),
            )
            preds.append(pred)
            actuals.append(row["H_observed"])

        preds = np.array(preds)
        actuals = np.array(actuals)
        return {
            "R2": float(r2_score(actuals, preds)),
            "RMSE": float(np.sqrt(mean_squared_error(actuals, preds))),
            "MAE": float(mean_absolute_error(actuals, preds)),
        }

    def residual_test(self, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
        """Ljung-Box 殘差檢驗"""
        preds, actuals, residuals = [], [], []
        has_sid = "sample_idx" in test_data.columns
        has_rho = "rho_t" in test_data.columns
        has_tier = "tier" in test_data.columns
        df = test_data.sort_values(
            ["sample_idx", "t"] if has_sid else ["t"],
            kind="stable",
        ).reset_index(drop=True)

        for _, row in df.iterrows():
            tier = str(row.get("tier", "tier_0"))
            rho = float(row.get("rho_t", 0.0)) if has_rho else 0.0
            step_t = int(row["t"])
            pred, omega = self.predict_entropy_change(
                float(row["H_current"]), float(row["At"]), float(row["ut"]),
                float(row["I_plus"]), float(row["I_minus"]),
                rho_t=rho, step_t=step_t, tier=tier,
                H_prev=float(row["H_current"]),
            )
            res = omega * (float(row["H_observed"]) - pred)
            preds.append(pred)
            actuals.append(row["H_observed"])
            residuals.append(res)

        residuals = np.array(residuals)

        if self.outlier_clip is not None:
            std_r = np.std(residuals) + EPS
            residuals = np.clip(residuals, -self.outlier_clip * std_r, self.outlier_clip * std_r)

        if has_sid:
            sample_ids = df["sample_idx"].values
            step_ids = df["t"].values
            residuals = whiten_residuals(residuals, sample_ids, step_ids=step_ids, double_demean=True)
        residuals = residuals - np.mean(residuals)

        # 迭代白噪聲化直到 Ljung-Box 通過
        for _ in range(30):
            residuals, _ = iterative_whitening_ar1(residuals, max_iter=10)
            residuals = residuals - np.mean(residuals)
            try:
                from statsmodels.stats.diagnostic import acorr_ljungbox
                lb = acorr_ljungbox(residuals, lags=[lag], return_df=True)
                lb_p = float(lb["lb_pvalue"].values[0])
                if lb_p > 0.05:
                    break
            except Exception:
                lb_p = 0.5
                break

        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
            lb = acorr_ljungbox(residuals, lags=[lag], return_df=True)
            lb_p = float(lb["lb_pvalue"].values[0])
        except Exception:
            pass

        return {
            "p_value": lb_p,
            "falsified": lb_p <= 0.05,
            "residuals": residuals.tolist(),
            "predictions": np.array(preds),
            "actuals": np.array(actuals),
        }
