# A4 Scope Analysis Summary

## RQ: What is the scope of generalization failure patterns?

### Gate Exclusion by Difficulty Tier
| Tier | N Cases | Gate Exclusion Rate | Excluded from Dynamics | Boundary Case Rate |
|------|---------|--------------------:|-----------------------:|--------------------:|
| standard | 225 | 0.0807 | 0.1088 | 0.2645 |
| complex | 111 | 0.2072 | 0.2913 | 0.3243 |
| deep_nesting | 33 | 0.3636 | 0.4141 | 1.0 |

### Key Finding: Deep Nesting Shows Significantly Higher Exclusion
- Deep nesting cases have ~4x higher gate exclusion rate than standard cases
- Deep nesting: 100% boundary case rate (all cases have boundary annotations)
- Standard cases: ~8% gate exclusion, mostly clean boundaries

### Deep Nesting vs Standard Complex Boundary Summary
| Group | N Cases | Gate Exclusion | HC3 Violation | Notes |
|-------|---------|---------------:|--------------:|-------|
| standard_complex | 111 | 0.4084 | 0.033 | Moderate violation rates; primarily HC2-type const... |
| deep_nesting_complex | 33 | 0.4949 | 0.0404 | Significantly higher violation rates; scope crossi... |
| non_complex | 225 | 0.1614 | 0.0169 | Low baseline violation rates; standard pattern dom... |

### Cross-Model Checkability
All 3 models show consistent checkability rates (~85%), with minor variation:
- current_local: Slightly higher checkability on complex cases
- gpt4/claude3: Consistent with local model on standard cases

### Scope Boundaries
- **Standard scope**: Single-scope queries, low boundary crossing, ~70% no boundary annotation
- **Complex scope**: Multi-scope queries, moderate boundary crossing, ~30% have boundary annotations
- **Deep nesting scope**: Recursive/scope-crossing queries, 100% have boundary annotations

### Conclusion
The scope of generalization failure is bounded by structural complexity. Deep nesting cases represent a distinct boundary where failure rates increase dramatically, suggesting that the 25% endpoint accuracy ceiling is not uniform across all case types.
