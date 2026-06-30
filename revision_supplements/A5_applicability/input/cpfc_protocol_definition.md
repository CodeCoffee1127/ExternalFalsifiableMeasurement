# CPFC Protocol Definition

## Overview

The Checklist-Protocol-Fit-Condition (CPFC) protocol defines four necessary conditions (P1-P4) that must be satisfied for a task domain to be eligible for ordinal validation-entropy analysis. These conditions ensure that the verification process is structured, externally grounded, and methodologically sound.

## P1: Discrete Checkpointability

A task must decompose into a finite set of discrete, verifiable checkpoints. Each checkpoint must have an unambiguous binary or categorical outcome that can be independently assessed without requiring subjective interpretation of the full solution context.

**Rationale**: Without discrete checkpoints, it is impossible to construct a meaningful checkpoint-frequency table, which is the foundational data structure for ordinal verification-entropy computation.

## P2: External Rule Availability

There must exist a publicly available, domain-expert-validated rule set (reference implementation, grading rubric, or verifier specification) against which checkpoint outcomes can be checked. The rules must be external to the model being evaluated.

**Rationale**: External rules provide the objective standard against which model outputs are judged. Without external rules, verification collapses into self-reference or subjective judgment.

## P3: Ordinal Categorical Reducibility

Checkpoint failure types must be reducible to a finite set of ordered categories. The ordering must reflect a substantively meaningful severity or complexity gradient (e.g., trivial omission < structural error < fundamental misunderstanding).

**Rationale**: The ordinal structure enables the use of non-parametric rank-based statistics and prevents inappropriate cardinal interpretations of verification-entropy values.

## P4: Post-Hoc Availability

Checkpoint-level outcomes must be observable after model generation completes, without requiring access to the model's internal states, activations, or generation trajectory.

**Rationale**: Post-hoc availability ensures that the protocol can be applied to black-box models and aligns with standard evaluation practices in LLM benchmarking.

## Protocol Satisfaction

All four conditions (P1-P4) are necessary. A domain satisfies CPFC if and only if all four conditions are met. Partial satisfaction does not confer eligibility for ordinal validation-entropy analysis.
