class MemoryCandidate(BaseModel):
    subject_id: str
    statement: str
    memory_class: Literal["episodic", "semantic"]
    source_ref: str
    tenant_id: str
    purpose_scope: set[str]
    effective_at: datetime
    expires_at: datetime | None = None

class MemoryDecision(BaseModel):
    accepted: bool
    target_store: Literal["episodic", "semantic", "quarantine"]
    reason: str
