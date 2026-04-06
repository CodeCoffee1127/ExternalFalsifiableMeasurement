from .dynamics_model import DynamicsModel
from .corrected_equation import CorrectedDynamicsEquation
from .equation_variants import (
    get_equation_variant,
    VARIANT_MAP,
    VariantA_LinearBaseline,
    VariantB_NonlinearBurst,
    VariantC_TriStateGating,
    VariantD_ExplicitMemory,
    VariantE_FullModel,
)

__all__ = [
    "CorrectedDynamicsEquation",
    "DynamicsModel",
    "get_equation_variant",
    "VARIANT_MAP",
    "VariantA_LinearBaseline",
    "VariantB_NonlinearBurst",
    "VariantC_TriStateGating",
    "VariantD_ExplicitMemory",
    "VariantE_FullModel",
]
