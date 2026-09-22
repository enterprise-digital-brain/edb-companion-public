[Heading 1] Appendix G — Enterprise structured agent skill standard
[Normal] This appendix defines a book-specific enterprise engineering standard for packaging, evaluating and governing reusable agent skills. It is an author synthesis informed by emerging Agent Skills conventions and contemporary agent-harness practice; it is not presented as an industry standard.
[Normal] A skill is a versioned package of procedural knowledge that an agent runtime can discover and load when a task requires it. The architectural objective is to improve specialised behaviour without copying every procedure, reference and example into every inference context.
[Heading 2] G.1 Progressive disclosure contract
[Normal] The skill package should separate three forms of information because they have different context costs and security implications.
[Normal] The package MUST NOT treat access to a skill as permission to execute a protected capability. Skill selection is a behavioural/context decision; tool authority remains an identity and policy decision enforced by the platform.
[Heading 2] G.2 Reference package layout
[Normal] skills/
 architecture-evidence-review/
 SKILL.md
 references/
 output-contract.md
 evidence-policy.md
 scripts/
 validate_finding.py
 evals/
 activation.jsonl
 task_cases.jsonl
 assertions.py
[Normal] The public Agent Skills format uses SKILL.md plus optional resources. An enterprise package can add governance metadata and evaluation assets so long as the target runtime supports or safely ignores those additions.
[Heading 2] G.3 Recommended SKILL.md
[Normal] ---
name: architecture-evidence-review
description: >
 Review a proposed system against authorised architecture evidence and
 return traceable findings. Use for advisory architecture reviews.
 Do not use to grant formal approval or modify production systems.
version: 1.3.0
owner: enterprise-architecture
risk_class: advisory
---

# Architecture Evidence Review

Use only evidence returned by the authorised architecture retriever.
Return typed Finding objects defined in references/output-contract.md.
Cite at least one evidence identifier for each material finding.
If authoritative sources conflict, return NEEDS_HUMAN_REVIEW.
Do not invoke write-capable infrastructure or repository tools.
Do not represent the result as formal architecture approval.
[Normal] Descriptions should state the objective, method and trigger conditions clearly enough for semantic routing and should include negative cases where neighbouring skills could be confused. Generic phrases such as “produce high-quality work” add little behavioural information and should be removed.
[Heading 2] G.4 Capability and preference skills
[Normal] For lifecycle management, this book distinguishes two categories.
[Normal] A capability skill compensates for a model or harness capability that is not yet reliable: a specialised tracing procedure, code scaffold or analytical method. It should be considered temporary and periodically ablated against newer models or runtimes.
[Normal] A preference skill captures durable organisational intent such as terminology, evidence rules, review criteria, domain playbooks or output contracts. It remains valuable even when foundation models improve because it represents organisation-specific procedural knowledge.
[Normal] The category controls review cadence, not authority. Both types require evaluation and version control.
[Heading 2] G.5 Context-budget rule
[Normal] Do not enforce an arbitrary universal word limit. Context cost depends on tokenisation, runtime architecture and the amount of metadata exposed continuously. Current public guidance for skill authoring emphasises small always-visible metadata, a concise primary skill body and progressive disclosure of deeper resources. The enterprise should set empirical budgets for:
[Caption] Table G.1. Measure and why it matters.
Measure | Why it matters
Activation precision/recall | tests whether the correct skill is discovered
Incremental input tokens | measures marginal inference cost
Instruction adherence | detects dilution or conflicting procedures
Task success | proves the skill adds capability rather than prose
Latency | captures retrieval/loading overhead
Security violations | detects unsafe capability or information use

[Normal] A larger skill that does not improve measured outcomes is context debt.
[Heading 2] G.6 Evaluation harness
[Normal] No production skill should be promoted without an evaluation suite. A useful minimum contains positive activation cases, negative non-activation cases, task-level behavioural cases and deterministic assertions for machine-checkable invariants. Probabilistic cases should be repeated across multiple trials and across the harnesses/models that the enterprise supports.
[Normal] Trajectory checks are especially useful when the skill is intended to enforce procedure. Strict matching is appropriate only when order itself is an invariant. Unordered, subset or superset matching is better where the agent may legitimately choose different paths while still being required to use – or prohibited from exceeding – a known tool set. Semantic trajectory judges should be reserved for aspects that deterministic checks cannot decide reliably.
[Normal] An example evaluation record:
[Normal] skill: architecture-evidence-review
version: 1.3.0
model_profile: reasoning-medium-2026–08
harness: enterprise-agent-runtime-2.4
trials_per_case: 5
metrics:
 activation_precision: 0.98
 activation_recall: 0.96
 evidence_coverage: 0.94
 forbidden_tool_rate: 0.00
 human_escalation_precision: 0.91
release_gate:
 forbidden_tool_rate_max: 0.00
 activation_precision_min: 0.95
 evidence_coverage_min: 0.90
[Normal] The values above are illustrative, not universal production targets.
[Heading 2] G.7 Ablation and retirement
[Normal] A skill is maintained through the lifecycle:
[Normal] author → evaluate → release → observe → ablate → retain | revise | retire.
[Normal] Ablation means running the protected evaluation suite with and without the skill after a meaningful model, harness or orchestration change. If the skill no longer improves the target behaviour, remove it from production context. Retain the evaluation suite. The tests become a regression sentinel that can detect whether a future model again requires the intervention.
[Normal] Retirement should also revoke catalogue entries, cached skill content and any skill-specific resource grants. A retired skill must not remain an undocumented shadow dependency.
[Heading 2] G.8 Security checklist
[Caption] Table G.2. Control question and required property.
Control question | Required property
Can metadata cause accidental or malicious over-triggering? | tested positive and negative activation set
Can a skill expand the caller’s authority? | No; authority is enforced independently by the reference monitor/PEP
Can references cross tenant or classification boundaries? | permission-aware resource resolution
Can scripts perform side effects? | explicit capability classification, signing/provenance and policy checks
Can untrusted content rewrite the skill? | immutable/versioned production artefacts and controlled update path
Can two skills conflict? | precedence/conflict policy and evaluation cases
Is every released skill attributable? | owner, version, source revision and evaluation evidence
Can the skill be removed safely? | ablation, rollback and cache invalidation procedure

[Heading 2] G.9 Architecture decision checklist
[Normal] Use a skill when the behaviour is reusable, conditional, context-sensitive and benefits from progressive disclosure. Prefer deterministic code or a workflow when the procedure is exact, mechanically executable and should not depend on model interpretation. Prefer RAG/knowledge retrieval when the requirement is principally changing factual knowledge rather than procedure. Prefer a policy/rules engine when the requirement expresses mandatory organisational constraints.
[Normal] The goal is not to maximise the number of skills. It is to place procedural knowledge at the narrowest, most testable boundary that preserves the required flexibility.
[Heading 3] References
[Normal] Anthropic. Skills repository and skill-creator guidance. GitHub, accessed 2026.
[Normal] Agent Skills Project. Agent Skills specification. GitHub, accessed 2026.
[Normal] LangChain. AgentEvals. GitHub, accessed 2026.