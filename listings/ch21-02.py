class MemoryAssertion(BaseModel):
    assertion_id: str
    subject_id: str
    predicate: str
    value: Any
    memory_class: Literal["episodic", "semantic", "procedural"]
    source_ref: str
    authority: str
    confidence: float | None
    valid_from: datetime | None
    valid_to: datetime | None
    tenant_id: str
    purpose_scope: set[str]
    supersedes: list[str] = Field(default_factory=list)
