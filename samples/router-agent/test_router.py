from router import Route, route_request


def test_consequential_action_routes_to_human():
    assert route_request("Approve payment").route == Route.HUMAN


def test_knowledge_requests_route_to_knowledge():
    for text in ("Explain the commit boundary", "What is authority attenuation",
                 "Why did the agent escalate", "Find the supplier record"):
        assert route_request(text).route == Route.KNOWLEDGE


def test_anything_else_routes_to_action():
    assert route_request("Restart the ingestion job").route == Route.ACTION


def test_a_consequential_word_wins_over_a_knowledge_word():
    # "what" would route to knowledge on its own; "payment" must take precedence,
    # because the cost of the two mistakes is not symmetric.
    assert route_request("What payment did we approve").route == Route.HUMAN


def test_routing_is_case_insensitive():
    assert route_request("APPROVE PAYMENT").route == Route.HUMAN
    assert route_request("approve payment").route == Route.HUMAN


def test_every_decision_carries_a_reason():
    for text in ("Approve payment", "Explain this", "Restart the job"):
        assert route_request(text).reason.strip()
