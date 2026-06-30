# Response Letter Phrase Bank

## Category: External Agreement

### For kappa >= 0.60:
- "We have revised the wording to clarify that our annotator agreement represents statistically meaningful external agreement (Cohen's kappa = 0.69 for onset, 0.65 for pattern), not a claim to external ground truth."
- "The annotation protocol used independent blinded annotators with a frozen codebook, constituting a statistically meaningful external reference rather than ground truth labels."
- "We acknowledge the reviewer's concern and have replaced 'ground truth' with 'independent blinded annotation reference' throughout the manuscript."

### For pattern labels:
- "Pattern categories are protocol-defined through a frozen annotation codebook with inter-annotator kappa >= 0.60, representing protocol-defined failure-pattern differentiation rather than mechanism recovery."
- "We characterize observed degradation patterns rather than claiming to recover true failure mechanisms."

## Category: Ordinal vs Cardinal

### For entropy/onset claims:
- "CPFC's onset predictions provide ordinal diagnostic resolution -- rank-order information about degradation timing -- rather than absolute uncertainty quantification."
- "We have clarified that entropy scores serve as ordinal diagnostic indicators, not cardinal uncertainty measures."
- "The within-one-step agreement of 99% supports the interpretation as ordinal resolution, acknowledging inherent step-level granularity."

### For scope claims:
- "Results represent a population-level diagnostic summary based on 100 sampled cases, not individual-chain predictions."
- "We have added caveats limiting claims to within-task-family ordinal pattern stability rather than broad LLM reasoning validity."

## Category: Methodology

### For post-hoc claims:
- "The diagnostic protocol is explicitly post-hoc -- applied after chain generation -- and does not claim real-time failure prediction."
- "Checkpoints are externally checkable against the database schema and verification evidence, supporting reproducible diagnosis."

## Category: Addressing Specific Reviewer Concerns

### Concern: "You claim to recover true failure mechanisms"
Response: "We have revised the manuscript to clarify that CPFC provides protocol-defined failure-pattern differentiation based on externally checkable checkpoints, not mechanism recovery. Pattern labels were established through a frozen annotation codebook with inter-annotator kappa >= 0.60."

### Concern: "Your evaluation is not generalizable"
Response: "We have limited scope claims to within-task-family assessment (chain-of-thought text-to-SQL). The manuscript now explicitly states that results should not be interpreted as architecture-independent or universally applicable."

### Concern: "You confuse entropy with uncertainty"
Response: "We have replaced all references to 'uncertainty' with 'ordinal diagnostic resolution' or 'rank-order diagnostic indicator' as appropriate. The entropy scores are used ordinally to rank cases by estimated degradation risk, not as cardinal uncertainty values."

### Concern: "Individual predictions are not reliable"
Response: "The manuscript now frames results as a population-level diagnostic summary rather than individual-chain predictions. Per-case labels are used for aggregate characterization, not individual diagnosis."

## Standard Phrases

| Situation | Phrase |
|-----------|--------|
| Agree with reviewer | "We thank the reviewer for this constructive observation. We have revised the text accordingly." |
| Clarify limitation | "We have added the following caveat to address this concern: [caveat text]" |
| Replace term | "We have replaced '[old term]' with '[new term]' throughout the manuscript to accurately reflect the scope of our findings." |
| Acknowledge scope | "We acknowledge that our findings are limited to [scope] and have revised the claims accordingly." |
