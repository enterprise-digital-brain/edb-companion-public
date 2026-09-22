from evaluate import exact_match


def test_identical_strings_match():
    result = exact_match("COMMITTED", "COMMITTED")
    assert result.passed and result.score == 1.0


def test_comparison_ignores_case_and_surrounding_space():
    assert exact_match(" Committed ", "committed").passed


def test_different_strings_do_not_match():
    result = exact_match("COMMITTED", "REJECTED")
    assert not result.passed and result.score == 0.0
    assert result.reason == "Output differs"


def test_an_empty_expectation_does_not_pass_everything():
    assert not exact_match("", "something").passed
