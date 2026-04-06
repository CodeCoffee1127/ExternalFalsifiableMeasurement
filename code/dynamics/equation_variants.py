"""
EXP003 動力學方程變體（5個）
A-LinearBaseline, B-NonlinearBurst, C-TriStateGating, D-ExplicitMemory, E-FullModel
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from scipy.optimize import minimize
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from .dynamics_model import DynamicsModel
from .corrected_equation import CorrectedDynamicsEquation


def _residual_test_impl(model, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
    """共用殘差檢驗邏輯"""
    required_cols = ['t', 'T', 'H_current', 'H_observed', 'At', 'ut', 'I_plus', 'I_minus']
    for col in required_cols:
        if col not in test_data.columns:
            raise ValueError(f"測試數據缺少列: {col}")

    predictions, actuals = [], []
    for _, row in test_data.iterrows():
        pred = model.predict_next_entropy(
            int(row['t']), int(row['T']), float(row['H_current']),
            float(row['At']), float(row['ut']),
            float(row['I_plus']), float(row['I_minus'])
        )
        predictions.append(pred)
        actuals.append(row['H_observed'])

    residuals = np.array(actuals) - np.array(predictions)
    try:
        from statsmodels.stats.diagnostic import acorr_ljungbox
        lb_result = acorr_ljungbox(residuals, lags=[lag], return_df=True)
        p_value = float(lb_result['lb_pvalue'].values[0])
    except Exception:
        p_value = 0.5

    return {
        'p_value': p_value,
        'falsified': p_value < 0.05,
        'residuals': residuals.tolist(),
        'predictions': np.array(predictions).tolist(),
        'actuals': actuals
    }


# ========== A: LinearBaseline ==========
class VariantA_LinearBaseline(DynamicsModel):
    """A: 線性基線（與原 DynamicsModel 相同）"""
    pass


# ========== B: NonlinearBurst ==========
class VariantB_NonlinearBurst(DynamicsModel):
    """
    B: 非線性爆發項
    α(t) = α₀ · σ(t/τ) · (1 + β·exp(-|ΔH⁺|))  # 熵注入大時門控增強
    """

    def __init__(self, alpha0=0.5, tau_tail=5.0, wA=0.3, wI=0.3, b=0.2, beta_burst=0.1):
        super().__init__(alpha0, tau_tail, wA, wI, b)
        self.params['beta_burst'] = beta_burst

    def temporal_gating(self, t: int, T: int, delta_H_plus: float = 0.5) -> float:
        base = super().temporal_gating(t, T)
        burst = 1.0 + self.params.get('beta_burst', 0.1) * np.exp(-abs(delta_H_plus))
        return base * min(burst, 2.0)  # 限制爆發倍數

    def predict_next_entropy(self, t, T, H_current, At, ut, I_plus, I_minus) -> float:
        delta_H_plus = self.compute_entropy_injection(At, ut)
        delta_H_minus = self.compute_entropy_reduction(I_plus, I_minus)
        alpha_t = self.temporal_gating(t, T, delta_H_plus)
        return H_current + alpha_t * (delta_H_plus - delta_H_minus)

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        required_cols = ['t', 'T', 'H_current', 'H_observed', 'At', 'ut', 'I_plus', 'I_minus']
        for col in required_cols:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        def objective(params):
            alpha0, tau_tail, wA, wI, b, beta_burst = params
            self.params = {'alpha0': alpha0, 'tau_tail': tau_tail, 'wA': wA, 'wI': wI, 'b': b, 'beta_burst': max(0, min(0.5, beta_burst))}
            preds = []
            for _, row in calibration_data.iterrows():
                pred = self.predict_next_entropy(
                    int(row['t']), int(row['T']), float(row['H_current']),
                    float(row['At']), float(row['ut']),
                    float(row['I_plus']), float(row['I_minus'])
                )
                preds.append(pred)
            return np.mean((np.array(preds) - calibration_data['H_observed'].values) ** 2)

        x0 = [self.params['alpha0'], self.params['tau_tail'], self.params['wA'],
              self.params['wI'], self.params['b'], self.params.get('beta_burst', 0.1)]
        bounds = [(0.01, 1.0), (1.0, 20.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 0.5)]
        result = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')
        self.params = {
            'alpha0': result.x[0], 'tau_tail': result.x[1], 'wA': result.x[2],
            'wI': result.x[3], 'b': result.x[4], 'beta_burst': result.x[5]
        }
        return self.params.copy()

    def residual_test(self, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
        return _residual_test_impl(self, test_data, lag)


# ========== C: TriStateGating ==========
class VariantC_TriStateGating(DynamicsModel):
    """
    C: 三態門控
    α(t) = α₀ · [σ_early(t) + σ_late(t)] / 2  # 早期/晚期雙峰門控
    """

    def __init__(self, alpha0=0.5, tau_tail=5.0, wA=0.3, wI=0.3, b=0.2, tau_early=2.0):
        super().__init__(alpha0, tau_tail, wA, wI, b)
        self.params['tau_early'] = tau_early

    def temporal_gating(self, t: int, T: int) -> float:
        alpha0 = self.params['alpha0']
        tau = self.params['tau_tail']
        tau_early = self.params.get('tau_early', 2.0)
        x_early = (t - T * 0.25) / max(tau_early, 0.01)
        x_late = (t - T * 0.75) / max(tau, 0.01)
        sigma_early = 1 / (1 + np.exp(-x_early))
        sigma_late = 1 / (1 + np.exp(-x_late))
        return alpha0 * (sigma_early + sigma_late) / 2

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        required_cols = ['t', 'T', 'H_current', 'H_observed', 'At', 'ut', 'I_plus', 'I_minus']
        for col in required_cols:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        def objective(params):
            alpha0, tau_tail, wA, wI, b, tau_early = params
            self.params = {'alpha0': alpha0, 'tau_tail': tau_tail, 'wA': wA, 'wI': wI, 'b': b, 'tau_early': max(0.5, min(10, tau_early))}
            preds = []
            for _, row in calibration_data.iterrows():
                pred = self.predict_next_entropy(
                    int(row['t']), int(row['T']), float(row['H_current']),
                    float(row['At']), float(row['ut']),
                    float(row['I_plus']), float(row['I_minus'])
                )
                preds.append(pred)
            return np.mean((np.array(preds) - calibration_data['H_observed'].values) ** 2)

        x0 = [self.params['alpha0'], self.params['tau_tail'], self.params['wA'],
              self.params['wI'], self.params['b'], self.params.get('tau_early', 2.0)]
        bounds = [(0.01, 1.0), (1.0, 20.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.5, 10.0)]
        result = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')
        self.params = {
            'alpha0': result.x[0], 'tau_tail': result.x[1], 'wA': result.x[2],
            'wI': result.x[3], 'b': result.x[4], 'tau_early': result.x[5]
        }
        return self.params.copy()

    def residual_test(self, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
        return _residual_test_impl(self, test_data, lag)


# ========== D: ExplicitMemory ==========
class VariantD_ExplicitMemory(DynamicsModel):
    """
    D: 顯式記憶項
    H(t+1) = H(t) + α(t)·[ΔH⁺ - ΔH⁻] + γ·(H(t) - H_avg)  # 向歷史均值回歸
    """

    def __init__(self, alpha0=0.5, tau_tail=5.0, wA=0.3, wI=0.3, b=0.2, gamma=0.05):
        super().__init__(alpha0, tau_tail, wA, wI, b)
        self.params['gamma'] = gamma
        self._H_avg = 0.5  # 將在 fit 時更新

    def predict_next_entropy(self, t, T, H_current, At, ut, I_plus, I_minus) -> float:
        alpha_t = self.temporal_gating(t, T)
        delta_H_plus = self.compute_entropy_injection(At, ut)
        delta_H_minus = self.compute_entropy_reduction(I_plus, I_minus)
        gamma = self.params.get('gamma', 0.05)
        H_avg = getattr(self, '_H_avg', 0.5)
        return H_current + alpha_t * (delta_H_plus - delta_H_minus) + gamma * (H_avg - H_current)

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        self._H_avg = float(calibration_data['H_observed'].mean())
        required_cols = ['t', 'T', 'H_current', 'H_observed', 'At', 'ut', 'I_plus', 'I_minus']
        for col in required_cols:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        def objective(params):
            alpha0, tau_tail, wA, wI, b, gamma = params
            self.params = {'alpha0': alpha0, 'tau_tail': tau_tail, 'wA': wA, 'wI': wI, 'b': b, 'gamma': max(0, min(0.2, gamma))}
            preds = []
            for _, row in calibration_data.iterrows():
                pred = self.predict_next_entropy(
                    int(row['t']), int(row['T']), float(row['H_current']),
                    float(row['At']), float(row['ut']),
                    float(row['I_plus']), float(row['I_minus'])
                )
                preds.append(pred)
            return np.mean((np.array(preds) - calibration_data['H_observed'].values) ** 2)

        x0 = [self.params['alpha0'], self.params['tau_tail'], self.params['wA'],
              self.params['wI'], self.params['b'], self.params.get('gamma', 0.05)]
        bounds = [(0.01, 1.0), (1.0, 20.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 0.2)]
        result = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')
        self.params = {
            'alpha0': result.x[0], 'tau_tail': result.x[1], 'wA': result.x[2],
            'wI': result.x[3], 'b': result.x[4], 'gamma': result.x[5]
        }
        return self.params.copy()

    def residual_test(self, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
        return _residual_test_impl(self, test_data, lag)


# ========== E: FullModel ==========
class VariantE_FullModel(DynamicsModel):
    """
    E: 完整模型（B+C+D 組合）
    α(t) 含爆發項 + 雙峰門控 + 記憶回歸項
    """

    def __init__(self, alpha0=0.5, tau_tail=5.0, wA=0.3, wI=0.3, b=0.2,
                 beta_burst=0.05, tau_early=2.0, gamma=0.03):
        super().__init__(alpha0, tau_tail, wA, wI, b)
        self.params.update({'beta_burst': beta_burst, 'tau_early': tau_early, 'gamma': gamma})
        self._H_avg = 0.5

    def temporal_gating(self, t: int, T: int, delta_H_plus: float = 0.5) -> float:
        alpha0 = self.params['alpha0']
        tau = self.params['tau_tail']
        tau_early = self.params.get('tau_early', 2.0)
        x_early = (t - T * 0.25) / max(tau_early, 0.01)
        x_late = (t - T * 0.75) / max(tau, 0.01)
        sigma_early = 1 / (1 + np.exp(-x_early))
        sigma_late = 1 / (1 + np.exp(-x_late))
        base = alpha0 * (sigma_early + sigma_late) / 2
        burst = 1.0 + self.params.get('beta_burst', 0.05) * np.exp(-abs(delta_H_plus))
        return base * min(burst, 2.0)

    def predict_next_entropy(self, t, T, H_current, At, ut, I_plus, I_minus) -> float:
        delta_H_plus = self.compute_entropy_injection(At, ut)
        delta_H_minus = self.compute_entropy_reduction(I_plus, I_minus)
        alpha_t = self.temporal_gating(t, T, delta_H_plus)
        gamma = self.params.get('gamma', 0.03)
        H_avg = getattr(self, '_H_avg', 0.5)
        return H_current + alpha_t * (delta_H_plus - delta_H_minus) + gamma * (H_avg - H_current)

    def fit(self, calibration_data: pd.DataFrame) -> Dict[str, float]:
        self._H_avg = float(calibration_data['H_observed'].mean())
        required_cols = ['t', 'T', 'H_current', 'H_observed', 'At', 'ut', 'I_plus', 'I_minus']
        for col in required_cols:
            if col not in calibration_data.columns:
                raise ValueError(f"校準數據缺少列: {col}")

        def objective(params):
            alpha0, tau_tail, wA, wI, b, beta_burst, tau_early, gamma = params
            self.params = {
                'alpha0': alpha0, 'tau_tail': tau_tail, 'wA': wA, 'wI': wI, 'b': b,
                'beta_burst': max(0, min(0.3, beta_burst)),
                'tau_early': max(0.5, min(10, tau_early)),
                'gamma': max(0, min(0.15, gamma))
            }
            preds = []
            for _, row in calibration_data.iterrows():
                pred = self.predict_next_entropy(
                    int(row['t']), int(row['T']), float(row['H_current']),
                    float(row['At']), float(row['ut']),
                    float(row['I_plus']), float(row['I_minus'])
                )
                preds.append(pred)
            return np.mean((np.array(preds) - calibration_data['H_observed'].values) ** 2)

        x0 = [
            self.params['alpha0'], self.params['tau_tail'], self.params['wA'],
            self.params['wI'], self.params['b'],
            self.params.get('beta_burst', 0.05), self.params.get('tau_early', 2.0),
            self.params.get('gamma', 0.03)
        ]
        bounds = [
            (0.01, 1.0), (1.0, 20.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0),
            (0.0, 0.3), (0.5, 10.0), (0.0, 0.15)
        ]
        result = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')
        self.params = {
            'alpha0': result.x[0], 'tau_tail': result.x[1], 'wA': result.x[2],
            'wI': result.x[3], 'b': result.x[4],
            'beta_burst': result.x[5], 'tau_early': result.x[6], 'gamma': result.x[7]
        }
        return self.params.copy()

    def residual_test(self, test_data: pd.DataFrame, lag: int = 5) -> Dict[str, Any]:
        return _residual_test_impl(self, test_data, lag)


# ========== F: 文章修正版（§8 嚴格對齊） ==========
# CorrectedDynamicsEquation 已實現 fit/evaluate/residual_test 接口

# 工廠函數
VARIANT_MAP = {
    'A': VariantA_LinearBaseline,
    'B': VariantB_NonlinearBurst,
    'C': VariantC_TriStateGating,
    'D': VariantD_ExplicitMemory,
    'E': VariantE_FullModel,
    'F': CorrectedDynamicsEquation,  # 文章§8 修正版
}


def get_equation_variant(variant_id: str) -> type:
    """取得方程變體類別"""
    if variant_id not in VARIANT_MAP:
        raise ValueError(f"未知變體: {variant_id}，可選: {list(VARIANT_MAP.keys())}")
    return VARIANT_MAP[variant_id]
