[Heading 1] Appendix C — Architecture decision guide and example ADRs
[Normal] Agentic systems benefit from explicit Architecture Decision Records (ADRs) because many important choices are not visible in source code: why a task is agentic, why a model may call a tool, why a tenant has dedicated storage, or why human approval is required.
[Heading 2] C.1 Minimal ADR template
[Normal] Title
[Code Block] Status: Proposed / Accepted / Superseded / Deprecated
[Code Block] Context: What problem, constraints and assumptions create the decision?
[Code Block] Decision: What will be done?
[Normal] Alternatives considered: What credible alternatives were rejected and why?
[Normal] Consequences: Positive, negative and operational consequences.
[Normal] Security and privacy: Trust boundaries, identities, data and residual risk.
[Code Block] Evaluation: What evidence will show that the decision works?
[Normal] Revisit triggers: What changes would justify reopening the decision?
[Heading 2] C.2 ADR — use an agent or deterministic workflow?
[Normal] Context. Support engineers investigate integration failures. The relevant diagnostic step varies with message content and system history.
[Normal] Decision. Use a bounded investigation agent for evidence gathering and hypothesis generation; use a deterministic workflow for ticket state, permission checks, escalation and remediation approval.
[Normal] Alternative: fully deterministic runbook. Rejected because incidents have too many semantic variants and engineers regularly deviate from fixed diagnostic paths.
[Normal] Alternative: autonomous remediation agent. Rejected initially because production change authority is high consequence and evidence is not yet sufficient.
[Normal] Consequences. Higher flexibility during investigation, while remediation remains predictable. Additional model/evaluation/observability cost.
[Normal] Evaluation. Time to defensible hypothesis, evidence coverage, unnecessary tool calls, escalation accuracy, incident outcomes.
[Heading 2] C.3 ADR — RAG versus fine-tuning for enterprise policy knowledge
[Normal] Context. Policies change monthly and require source attribution.
[Normal] Decision. Use permission-aware retrieval to supply policy knowledge. Fine-tuning may later be considered for stable output conventions or specialised classification, not for current policy facts.
[Normal] Why. Retrieval supports freshness, revocation and attribution.
[Normal] Trade-off. Retrieval quality and indexing lifecycle become operational dependencies.
[Normal] Revisit. If task-specific behaviour remains inconsistent despite strong prompting/evaluation, consider adaptation methods while retaining RAG for current facts.
[Heading 2] C.4 ADR — shared or dedicated vector stores?
[Normal] Context. A SaaS platform serves multiple enterprise tenants with confidential documents.
[Normal] Decision. Use pooled compute but dedicated vector indexes and encryption keys for regulated tenants; lower-risk internal tenants may use shared infrastructure with mandatory tenant filtering.
[Normal] Alternatives. Dedicated full environment for every tenant rejected initially for cost; global shared index rejected for high-sensitivity customers.
[Normal] Evidence. Cross-tenant security tests, operational recovery tests, cost per tenant.
[Heading 2] C.5 ADR — MCP gateway before enterprise APIs
[Normal] Context. Agents need access to numerous internal APIs, including legacy-backed services.
[Normal] Decision. Expose only approved task-oriented capabilities through an MCP governance gateway. Existing APIs remain behind domain adapters; raw OpenAPI transformation is permitted only for APIs assessed as already agent-safe.
[Normal] Reason. MCP standardises capability access but does not make broad enterprise APIs least-privileged.
[Normal] Revisit. When API estate adopts standard side-effect/security metadata.
[Heading 2] C.6 ADR — A2A for cross-domain specialists
[Normal] Context. Separate business domains operate specialist agents with distinct ownership and deployments.
[Normal] Decision. Use A2A task delegation for cross-domain work; local specialists within one workflow may continue using internal framework calls.
[Normal] Reason. A2A adds value at organisational/runtime boundaries where independent identity, capability discovery and versioning matter.
[Normal] Trade-off. Protocol/federation complexity and context-fragmentation risk.
[Heading 2] C.7 ADR — human approval binding
[Normal] Context. Agent prepares a production configuration change.
[Normal] Decision. Human approves canonical structured payload; approval stores hash/digest and expires after 20 minutes. Commit service rejects any changed payload.
[Normal] Rejected alternative. Approve a natural-language summary then regenerate the command afterwards.
[Normal] Reason. Prevents mismatch between reviewed intent and executed action.
[Heading 2] C.8 ADR — historical replay support
[Normal] Context. Risk recommendations may be challenged months later.
[Normal] Decision. Store evidence references, source/effective dates, feature/model/policy versions, material tool results and workflow events. Do not store raw chain-of-thought.
[Normal] Consequence. Additional evidence/telemetry storage and lifecycle controls; improved assurance and regression testing.
[Heading 2] C.9 ADR — legacy ERP integration
[Normal] Context. ERP API uses a privileged technical account and has complex, unstable semantics.
[Normal] Decision. Place an anti-corruption/capability adapter in front. Agent receives narrow read/prepare operations. Commit requires policy and human approval. Downstream credential stays in adapter.
[Normal] Alternative. Generic database tool rejected because it bypasses ERP business rules.
[Heading 2] C.10 Architecture decision checklist
[Normal] Before approving an agentic design, answer:
[List Bullet] What business problem requires probabilistic reasoning?
[List Bullet] Which portions can remain deterministic?
[List Bullet] What is the authoritative system of record?
[List Bullet] What knowledge is required and who owns it?
[List Bullet] How is tenant/identity applied before retrieval?
[List Bullet] Which tools are needed and what side-effect class does each have?
[List Bullet] Where is workflow state stored?
[List Bullet] What is the loop termination/progress rule?
[List Bullet] What happens after a timeout or partial commit?
[List Bullet] What human judgement remains material?
[List Bullet] What evidence is stored?
[List Bullet] How will the feature be evaluated before and after production?
[List Bullet] How can it be contained or rolled back?
[List Bullet] What is the cost per resolved outcome?
[List Bullet] What architectural condition would cause this decision to be revisited?