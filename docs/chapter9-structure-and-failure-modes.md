### 9.2 Prompt chaining
Structure
Break work into sequential stages with typed outputs:
extract -> normalise -> analyse -> render
Each stage may be a model call or deterministic function.
Failure modes
Early errors can cascade. Long chains increase latency. If every stage repeats the entire context, token cost can grow quickly.

### 9.3 Router
Structure
A router classifies the request into a controlled set of destinations.
The classification can be deterministic for obvious cases and model-based for semantic cases. The destination list remains fixed by configuration.
Failure modes
Misrouting can become systemic because every request passes through the router. Measure route accuracy separately. Provide a safe fallback for uncertain classification.

### 9.5 Planner–Executor
Structure
The Planner converts a goal into a structured task graph. Each step identifies its purpose, dependencies, required tool, expected result and potential side effects.
Before execution, a deterministic Plan Validator checks:
whether the requested tools are approved;
whether the plan contains invalid dependencies or cycles;
whether step, time and cost limits are respected;
whether preconditions can be satisfied; and
whether each action falls within the principal’s delegated authority.
The Executor then performs approved steps in dependency order, using only the permissions needed for the current action. Execution evidence and policy decisions are recorded for every step.
A planner may propose an action, but it cannot authorise that action. For example, during an incident investigation, the planner may recommend rolling back a deployment. The validator may permit diagnostic steps while holding the rollback for human approval.
Figure 9.2. Planner, validator and executor: separating the authority to decompose work from the authority to perform it.
Failure modes
Plans may depend on assumptions that later prove false. The executor should therefore recheck preconditions before acting and permit bounded re-planning when circumstances change.
Re-planning must not expand the original authority boundary. Limit the number of attempts, plan size, execution time and cost to prevent endless regeneration. Require evidence-based completion conditions so that neither the planner nor the executor can declare success without proof.
Use this pattern when the goal is understood but the sequence of actions must be discovered dynamically. If the sequence is already stable, a deterministic workflow is usually simpler and easier to govern.

### 9.6 Planner–Executor–Critic
Structure
The Planner creates an authorised task graph, and the Executor performs its approved steps. The Critic then evaluates the resulting artefact against explicit criteria such as:
evidence coverage and source quality;
internal contradictions;
policy compliance;
completeness;
unresolved uncertainty; and
alignment with the original objective.
The critic may accept the result, request one bounded revision or route the case to human review. It should not rewrite the goal, expand the workflow’s authority or create an unlimited correction loop.
For example, an incident-analysis workflow may complete every diagnostic step but recommend a rollback without sufficient evidence linking the deployment to the failure. The critic can identify that gap and require further evidence before the recommendation is released.
Failure modes
 The critic may approve weak work, repeatedly request cosmetic revisions or introduce new unsupported claims. Use measurable acceptance criteria, revision limits and escalation rules.
Use this pattern when the cost of an incomplete or poorly supported output justifies an additional review stage.

### 9.7 ReAct-style tool use
Structure
At each iteration, the agent determines its next information need, selects a tool from an approved capability set and submits a structured request. The runtime validates the call, executes it and returns the observation to the agent.
The model does not receive arbitrary access to external systems. Tool permissions, input schemas, execution limits and side-effect policies are enforced outside the model. Every request, observation and policy decision is recorded.
For example, during an incident investigation, the agent may inspect service metrics, use the result to identify a failure window and then retrieve only the logs and deployment records relevant to that period.
Failure modes
The agent may repeat calls, chase irrelevant evidence, misuse observations or continue investigating without measurable progress. Apply tool allowlists, iteration and cost limits, duplicate-call detection, no-progress rules and evidence-based stopping conditions.
Use this pattern for investigations in which each observation changes the next information need. Avoid it for stable business processes whose sequence and data sources are already known; a deterministic workflow will usually be clearer and cheaper.

### 9.8 Retrieval agent
Structure
The agent analyses the question, selects permitted knowledge sources and issues one or more targeted queries. It may reformulate queries, follow graph relationships or request structured records as evidence gaps become visible.
Retrieval stops when the evidence criteria are satisfied, the retrieval budget is exhausted or further progress requires access the principal does not possess.
For example, an agent investigating a supplier-risk decision may retrieve the supplier record, follow its contractual and ownership relationships, examine relevant risk policies and search recent assurance findings before constructing an answer.
Failure modes
The agent may over-retrieve, repeatedly reformulate equivalent queries or mistake retrieval volume for evidence quality. Set limits on subqueries, elapsed time and cost, and terminate when successive searches add no material evidence.
Retrieval must remain permission-aware. The agent cannot remove access-control filters, cross tenancy boundaries or infer that inaccessible evidence supports its conclusion. Evaluate the pattern using evidence coverage, source quality, answer accuracy and retrieval cost—not answer fluency alone.
Use this pattern when answering the question requires iterative evidence discovery. For predictable lookups against a known source, conventional retrieval is simpler and more efficient.

### 9.9 Evaluator-optimiser
Structure
The Evaluator-Optimiser pattern creates a bounded feedback loop: generate, evaluate, revise and evaluate again. The evaluator applies an explicit rubric and returns structured findings. The optimiser revises only the failed dimensions, and the loop ends when the acceptance threshold or iteration limit is reached.
Failure modes
An evaluator may reward superficial rubric compliance or reproduce the generator’s errors, particularly when both roles use the same model and evidence. Use deterministic tests where possible, cap revisions and escalate unresolved failures. Do not present self-evaluation as independent assurance.

### 9.10 Guardian / policy agent
Structure
A Guardian performs semantic policy analysis and returns a typed assessment containing relevant obligations, risk indicators, ambiguity and recommended handling. Mandatory rules remain enforced by a deterministic policy or access-control layer.
Example
A procurement agent proposes a contract variation. The Guardian compares free-text clauses with approved guidance and flags an ambiguous liability term. A deterministic rule separately prevents commitments above the principal’s delegated threshold.
Failure modes
The principal anti-pattern is treating a Guardian as the sole authorisation mechanism. Model output may inform a policy decision, but it must not replace identity checks, mandatory constraints or approval controls.

### 9.11 Approval gate
Structure
The workflow pauses durably before the side effect. An authorised person receives the proposed action, supporting evidence, uncertainty and risk summary. The approval is bound to an immutable representation or digest of the exact action payload and expires after a defined period.
Failure modes
Approval becomes theatre when evidence is incomplete, payloads can change after review or requests are too frequent to examine properly. Preserve payload binding, decision provenance, expiry and explicit rejection semantics.

### 9.12 Maker-checker
Structure
The Maker creates the proposal and evidence package. A Checker evaluates it using separate authority and, where practical, independent evidence or validation criteria. The Checker may be a human, deterministic service or model-assisted reviewer operating behind an independent control boundary.
Failure modes
Two agents using the same model, context, credentials and evidence do not provide meaningful independence. Distinct role names are not a substitute for separate authority and control.

### 9.13 Checkpoint and resume
Structure
Persist workflow state, artefacts and evidence after meaningful transitions. On restart, reconcile external state and resume from the last committed checkpoint using the versioned workflow definition that created it.
Failure modes
Blindly replaying the last step can duplicate side effects. Resume logic must inspect recorded intent and external state before deciding whether to retry, continue or escalate.

### 9.14 Bounded retry and circuit breaker
Structure
Retry only errors classified as transient, using maximum attempts, backoff and jitter. A circuit breaker stops requests to an unhealthy dependency after a threshold and routes work to a defined fallback, queue or escalation path.
Failure modes
An agent may switch among alternative tools and multiply load across the estate. Enforce retry, concurrency and tool budgets at workflow level, not only per connector.

### 9.15 Saga / compensating action
Structure
Define a compensating action for each committed step where feasible. If a later step fails, the workflow runs compensation in a controlled order or escalates with an explicit record of residual state.
Failure modes
Compensation is not always rollback. An email cannot reliably be unsent and a disclosed decision may have lasting effects. Classify actions as reversible, compensatable or irreversible before execution.

### 9.16 Evidence-first response
Structure
Construct an evidence package before generating the final explanation. Each material finding references evidence identifiers carrying source, authority, validity and provenance information. The response generator explains the evidence record rather than inventing support while drafting.
Failure modes
Citation presence does not prove support. Validate that evidence actually entails the claim, record contradictory sources and prevent inaccessible or expired evidence from being silently reused.

### 9.17 Confidence-gated escalation
Structure
A decision function combines task-specific calibration, evidence quality, source agreement, policy and explicit uncertainty indicators. Cases are automated only within validated operating bounds; the remainder are routed to human review or a safer workflow.
Failure modes
Self-reported model confidence is not sufficient. Thresholds can drift as data and operating conditions change, so calibration and escalation outcomes require continuing evaluation.