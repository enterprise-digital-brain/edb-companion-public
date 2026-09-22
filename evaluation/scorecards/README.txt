[Heading 1] Appendix E — Enterprise model, router and memory benchmark scorecards
[Normal] This appendix provides reusable templates for evaluating a public, private or domain-adapted model inside the CAE Intelligence Fabric. It deliberately avoids declaring a permanent “best model”. The purpose is to make model choice a reproducible architecture decision.
[Heading 2] E.1 Task-envelope template
[Caption] Table E.1. Field and record.
Field | Record
Capability role | e.g. contract_evidence_synthesis
Business outcome | decision/review this capability supports
Task family | extraction / classification / synthesis / planning / tool use / multimodal / critique
Consequence class | low / medium / high / critical
Data classification | public / internal / confidential / restricted
Residency / sovereignty | approved regions or private deployment requirement
Modalities | text / image / audio / code / structured data
Required affordances | tools, structured output, long context, streaming, computer use
Quality floor | task-specific acceptance criterion
Reliability floor | repeated-trial success / schema success
Latency SLO | p50/p95 target
Cost budget | per request / per resolved outcome
Human route | escalation or mandatory approval condition
Prohibited behaviour | actions, data flows, unsupported claims

[Normal] A benchmark result without this envelope is difficult to operationalise because it does not say what the model was expected to do.
[Heading 2] E.2 Candidate-model scorecard
[Normal] Use raw metrics plus a decision narrative. Do not hide material regressions inside a weighted average.
[Heading 2] E.3 Classification and regression extensions
[Normal] For classifiers, record macro F1, weighted F1, per-class recall, confusion matrix and calibration when probabilities drive routing or decisions. Accuracy alone is inadequate for imbalanced high-risk classes.
[Normal] For continuous predictions, record MAE, RMSE and domain-appropriate interval quality. When prediction intervals are used, measure empirical coverage and interval width. A narrow interval that misses frequently is not confidence; it is miscalibration.
[Heading 2] E.4 Generative and agentic evaluation
[Normal] Open-ended tasks need an acceptance envelope rather than exact-string matching. Define observable criteria such as evidence coverage, factual consistency with authorised sources, policy alignment, actionability and appropriate uncertainty.
[Normal] Agent roles add trajectory properties. A benchmark should record whether success was achieved through an acceptable path. Examples of unacceptable success include using a forbidden tool, leaking cross-tenant context, performing an unapproved write and then compensating it, or completing only after a retry storm that violates the cost budget.
[Normal] Repeated trials are essential. For a binary end-to-end success variable:
[Code Block] [ \hat{p}=\frac{s}{n}. ]
[Normal] Record (n) and an uncertainty interval. Do not compare 0.91 with 0.92 as meaningful if each number came from a handful of stochastic executions.
[Heading 2] E.5 Router benchmark scorecard
[Caption] Table E.2. Router measure and definition / purpose.
Router measure | Definition / purpose
Admissibility accuracy | Never selects a candidate violating security/residency/capability constraints
Quality regret | Difference from best admissible candidate on the task
Cost saving | Saving relative to agreed baseline (e.g. always-frontier)
Latency regret | Additional latency relative to best admissible route
Unsafe-route rate | Protected cases sent to uncertified/inappropriate route
Model recall | Whether router considered a candidate capable of meeting the target
Escalation rate | Fraction routed to stronger model/human
Route entropy | Concentration/diversity of model use; useful for diagnosing collapse
Drift stability | Performance as task distribution changes
Fallback correctness | Behaviour during provider/model unavailability

[Normal] A production router should expose a reason code describing why a route was selected: security_constraint, modality, quality_floor, budget, latency, fallback, learned_preference. This is more useful operationally than opaque probability alone.
[Heading 2] E.6 Internal/domain model promotion gate
[Normal] Record at least three evaluation sets:
[Normal] Target suite – capability the adaptation is intended to improve.
[Normal] Retention suite - historical/general capabilities that must not regress beyond tolerance.
[Normal] Security suite – identity/tool/context/injection and unsafe-action behaviours that must remain within policy.
[Normal] Suggested release record:
[Normal] candidate: domain-model-r17
base_model: immutable-base-id
intended_role: specialist_domain_extraction
target_suite:
 version: domain-v12
 gain: +0.047
retention_suite:
 version: enterprise-core-v9
 max_forgetting: 0.012
security_suite:
 version: agent-sec-v6
 mandatory_failures: 0
shadow:
 days: 14
 task_success_delta: +0.021
 cost_delta: -0.18
 unsafe_route_delta: 0.0
promotion:
 decision: approved_for_specialist_role
 fallback: workhorse-model-profile-v5
[Normal] The release is role scoped. A model can be excellent for extraction without being approved for planning or production side effects.
[Heading 2] E.7 Memory benchmark scorecard
[Caption] Table E.3. Dimension and test.
Dimension | Test
Write precision | correct accept/reject/scope decision for candidate memories
Positive recall | retrieve authorised relevant memory
Negative recall | correctly return no memory
Temporal correctness | exclude expired/superseded state
Conflict handling | surface/resolve contradictions by policy
Provenance | preserve source and authority
Tenant/purpose isolation | prohibited retrieval rate
Deletion/forgetting | revocation propagation
Contribution | quality/time/cost delta vs no-memory baseline

[Normal] Run a long-context baseline where feasible. If persistent memory adds little quality but substantial privacy/operational risk, long-context or session state may be the better architecture.
[Heading 2] E.8 Continual-learning scorecard
[Normal] For staged adaptation, retain a performance matrix (R_{i,j}). Track target gain, average retained performance, forgetting, backward/forward transfer where meaningful, calibration shift, security regression and operational trajectory change.
[Normal] A simple forgetting measure:
[Code Block] [ F_j=\max_{i<T}R_{i,j}-R_{T,j}. ]
[Normal] The promotion decision should explicitly state whether a regression is accepted, constrained to a narrower route, or blocks the release.
[Heading 2] E.9 Model-selection ADR template
[Normal] Decision: Which model/configuration is certified for which role?
Context: Task envelope, current production baseline and constraints.
Candidates: Exact immutable model/version/configuration identifiers.
Evidence: Public benchmarks, local benchmark version, repeated trials and shadow data.
Trade-offs: Quality, reliability, security, latency, cost, portability and operational burden.
Decision: Primary, fallback, abstention/human route.
Known limitations: Failure classes, unsupported modalities, data restrictions.
Review triggers: Provider/model change, cost change, drift, tool/context change, incident, scheduled review.
Owner: Model role owner / review board.
[Heading 2] E.10 Benchmark anti-patterns
[Normal] A benchmark programme is weak when it chooses a model from vendor charts alone, mixes test and optimisation data, evaluates only average quality, runs stochastic agent tasks once, ignores security and tool behaviour, compares models under different retrieval/tool environments, reports token price rather than cost per completed outcome, or allows a provider alias to change without re-certification.
[Normal] The enterprise question is not “Which model is smartest?” It is:
[Normal] Which certified configuration delivers the required outcome for this task envelope with acceptable reliability, security, latency and total cost – and what route should be used when it does not?