class ModelCapability(BaseModel):
    model_id: str
    roles: set[str]
    modalities: set[str]
    supports_tools: bool
    max_data_classification: str
    residency: set[str]
    estimated_cost_class: Literal["low", "medium", "high"]

class ModelRequest(BaseModel):
    task_family: str
    risk_class: str
    data_classification: str
    modality: str
    quality_floor: float
    latency_budget_ms: int
    cost_budget_usd: float
    requires_tools: bool = False
