from router import Route, route_request


def test_consequential_action_routes_to_human():
    assert route_request("Approve payment").route == Route.HUMAN
