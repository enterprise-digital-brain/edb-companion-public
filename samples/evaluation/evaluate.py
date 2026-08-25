from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    passed: bool
    score: float
    reason: str


def exact_match(expected: str, actual: str) -> Evaluation:
    passed = expected.strip().casefold() == actual.strip().casefold()
    return Evaluation(
        passed=passed,
        score=1.0 if passed else 0.0,
        reason="Exact normalized match" if passed else "Output differs",
    )
