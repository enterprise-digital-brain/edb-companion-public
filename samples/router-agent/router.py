from dataclasses import dataclass
from enum import Enum


class Route(str, Enum):
    KNOWLEDGE = "knowledge"
    ACTION = "action"
    HUMAN = "human"


@dataclass(frozen=True)
class RoutingDecision:
    route: Route
    reason: str


def route_request(text: str) -> RoutingDecision:
    value = text.lower()
    if any(word in value for word in ("approve", "payment", "delete", "transfer")):
        return RoutingDecision(Route.HUMAN, "Potentially consequential action.")
    if any(word in value for word in ("find", "explain", "what", "why")):
        return RoutingDecision(Route.KNOWLEDGE, "Knowledge-oriented request.")
    return RoutingDecision(Route.ACTION, "Operational request.")


if __name__ == "__main__":
    print(route_request("Explain the Zero Trust agent boundary"))
