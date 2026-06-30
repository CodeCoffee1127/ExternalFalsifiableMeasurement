# When CPFC Does NOT Apply

## Explicit Non-Applicability Conditions

The CPFC protocol does NOT apply, and ordinal validation-entropy analysis is NOT justified, in the following circumstances:

### 1. Open-Ended Generation Tasks
Tasks like creative writing, open-domain dialogue, or story generation lack discrete checkpoints. There is no external rule set for evaluating stylistic choices, and outcomes are not categorically reducible.

**Examples**: Poetry generation, free-form conversation, essay writing without rubric.

### 2. Subjective Evaluation Tasks
Tasks where human judgment is the only viable evaluation criterion and no expert-validated rubric exists.

**Examples**: Humor generation, emotional appropriateness, aesthetic quality assessment.

### 3. Procedural Tasks Without Post-Hoc Verification
Tasks where correctness can only be determined by observing the generation process, not the final output.

**Examples**: Interactive debugging, multi-turn negotiation, real-time strategy execution.

### 4. Continuous Output Spaces
Tasks with continuous outputs that cannot be discretized without loss of substantive meaning.

**Examples**: Regression value prediction, embedding space traversal, control signal generation.

### 5. Self-Referential Verification
Tasks where the only available verification standard is the model's own output or an internal consistency check.

**Examples**: Self-consistency decoding evaluation, bootstrap-based confidence estimation.

### 6. Domains Without Expert-Validated External Rules
Even if a task seems structured, if no domain expert has validated a rule set, P2 is violated.

**Examples**: Novel programming languages without specification, informal protocol implementations.

## Important Distinction

The absence of CPFC applicability in these domains does not mean the domains are unimportant or that LLM evaluation is impossible. It means that **ordinal validation-entropy specifically** is not the appropriate methodological tool. Other evaluation approaches (human evaluation, reference-based metrics, task-specific benchmarks) remain valid.

## When Partial Satisfaction Occurs

If some but not all P1-P4 conditions are satisfied, the task does NOT qualify for ordinal validation-entropy analysis. Partial satisfaction is treated as non-applicability. Future work may develop extensions or relaxations of CPFC for specific partial-satisfaction scenarios, but such extensions are beyond the scope of this paper.
