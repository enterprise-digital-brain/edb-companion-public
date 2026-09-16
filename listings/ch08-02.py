@dataclass
class LoopBudget:
 max_steps: int
 max_elapsed_seconds: int
 max_cost_usd: float
 max_repeated_action: int

@dataclass
class ProgressSignal:
 new_evidence_count: int
 completed_subtasks: int
 state_changed: bool
