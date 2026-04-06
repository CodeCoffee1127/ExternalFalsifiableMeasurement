"""
状态变量计算模块
计算五个可观测状态变量：At, ut, Hv, I±, ρt

I_+, I_- 按論文 §7 父消融定義計算（優先使用 parent_ablation）
"""

import numpy as np
from typing import List, Dict, Tuple, Union, Any, Optional

from cpfc.dependency_extractor import SQLDependencyExtractor


class StateCalculator:
    """
    计算五个可观测状态变量
    """

    def __init__(self, prior_alpha: float = 1.0, prior_beta: float = 1.0):
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.dependency_extractor = SQLDependencyExtractor()

    def compute_At(
        self,
        verification_results: List[Union[bool, object]],
        prior_alpha: float = None,
        prior_beta: float = None
    ) -> float:
        """
        验证一致性（Beta后验均值）

        输入：N个候选的验证结果 [True, False, True, ...]
        输出：At = (α + successes) / (α + β + N)
        """
        alpha = prior_alpha if prior_alpha is not None else self.prior_alpha
        beta = prior_beta if prior_beta is not None else self.prior_beta

        # 支持VerificationResult对象
        successes = sum(
            1 for r in verification_results
            if (r.pass_verification if hasattr(r, 'pass_verification') else r)
        )
        n = len(verification_results)
        if n == 0:
            return 0.5

        posterior_alpha = alpha + successes
        posterior_beta = beta + (n - successes)
        return posterior_alpha / (posterior_alpha + posterior_beta)

    def compute_ut(
        self,
        verification_results: List[Union[bool, object]],
        prior_alpha: float = None,
        prior_beta: float = None
    ) -> float:
        """
        测量不确定性（Beta后验标准差）

        公式：sqrt(αβ / [(α+β)²(α+β+1)])
        """
        alpha = prior_alpha if prior_alpha is not None else self.prior_alpha
        beta = prior_beta if prior_beta is not None else self.prior_beta

        successes = sum(
            1 for r in verification_results
            if (r.pass_verification if hasattr(r, 'pass_verification') else r)
        )
        n = len(verification_results)
        if n == 0:
            return 0.5

        posterior_alpha = alpha + successes
        posterior_beta = beta + (n - successes)
        variance = (posterior_alpha * posterior_beta) / (
            (posterior_alpha + posterior_beta) ** 2 *
            (posterior_alpha + posterior_beta + 1)
        )
        return np.sqrt(max(0, variance))

    def compute_Hv(self, pt: float, epsilon: float = 1e-10) -> float:
        """
        验证熵
        Hv = -[pt·log(pt) + (1-pt)·log(1-pt)]
        """
        pt = np.clip(pt, epsilon, 1 - epsilon)
        return -(pt * np.log2(pt) + (1 - pt) * np.log2(1 - pt))

    def compute_dependency_strength(
        self,
        dependencies: Dict[str, List[str]],
        current_step: str
    ) -> Tuple[float, float]:
        """
        計算 I_+, I_-（結構啟發式，無父消融時使用）
        """
        return self.dependency_extractor.compute_dependency_strength(
            dependencies, current_step
        )

    def compute_parent_ablation_strength(
        self,
        verifier: Any,
        candidates: List[str],
        dependencies: Dict[str, List[str]],
        current_clause: str,
        schema: Optional[dict] = None,
        n_jobs: int = 1,
    ) -> Tuple[float, float]:
        """
        論文 §7：父消融貢獻度 I_+, I_-
        ΔH = H_ablated - H_full，I_+ = sum(max(ΔH,0))，I_- = sum(max(-ΔH,0))
        """
        from .parent_ablation import compute_parent_ablation_strength
        return compute_parent_ablation_strength(
            verifier, candidates, dependencies, current_clause,
            schema=schema, n_jobs=n_jobs,
            prior_alpha=self.prior_alpha, prior_beta=self.prior_beta,
        )

    def compute_rho_t(self, history: List[float]) -> float:
        """
        累积风险记忆
        ρt = 1 - ∏(1 - uk) for k=1 to t
        """
        if not history:
            return 0.0
        return 1 - np.prod([1 - min(max(u, 0), 1) for u in history])
