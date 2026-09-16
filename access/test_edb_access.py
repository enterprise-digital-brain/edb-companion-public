# -*- coding: utf-8 -*-
"""Tests for the reader identifier scheme. Run with: python3 -m pytest -q"""
import os
import time

os.environ.setdefault("EDB_SECRET", "test-secret-at-least-32-characters-long!!")

import edb_access as a  # noqa: E402

ORDER = "114-8352901-7654321"


def test_identifier_is_stable_and_well_formed():
    first = a.derive(ORDER)
    assert a.ID_RX.match(first)
    assert a.derive(ORDER) == first, "a reader who registers twice must get the same identifier"


def test_spacing_and_case_do_not_create_a_second_identity():
    assert a.derive("  114 8352901 7654321  ") == a.derive(ORDER)
    assert a.derive("11483529017654321") == a.derive(ORDER)


def test_a_different_order_gives_a_different_identifier():
    assert a.derive("114-8352901-7654322") != a.derive(ORDER)


def test_identifier_survives_being_typed_back_badly():
    ident = a.derive(ORDER)
    mangled = ident.lower().replace("-", " ").replace("0", "O")
    assert a.tidy(mangled) == ident
    assert a.matches(mangled, ORDER)


def test_rotating_the_secret_invalidates_everything():
    before = a.derive(ORDER)
    os.environ["EDB_SECRET"] = "a-completely-different-secret-value-32ch!"
    try:
        assert a.derive(ORDER) != before
    finally:
        os.environ["EDB_SECRET"] = "test-secret-at-least-32-characters-long!!"


def test_rubbish_order_references_are_refused():
    for bad in ("", "   ", "nope", "1234"):
        try:
            a.normalise_order_id(bad)
        except a.AccessError:
            continue
        raise AssertionError(f"accepted {bad!r}")


def test_download_links_expire():
    ident = a.derive(ORDER)
    sig, exp = a.sign_download(ident, ttl_seconds=60)
    assert a.check_download(ident, exp, sig)
    assert not a.check_download(ident, exp, sig, now=exp + 1)


def test_a_download_link_is_bound_to_its_identifier():
    sig, exp = a.sign_download(a.derive(ORDER))
    assert not a.check_download(a.derive("114-8352901-7654322"), exp, sig)


def test_the_challenge_ignores_punctuation_and_case():
    assert a.check_challenge("  Complete, mediation. ", "complete mediation")
    assert not a.check_challenge("", "complete mediation")
    assert not a.check_challenge("something else", "complete mediation")
