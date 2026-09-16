# -*- coding: utf-8 -*-
"""Reader identifiers for The Contextual Agentic Enterprise.

Every KDP copy is printed identically, so a unique code cannot be printed in the
book. A reader earns one by proving purchase. This module derives that identifier
deterministically from the proof of purchase, so nothing has to be generated in
advance and no table of unissued codes exists to leak.

    identifier = EDB - base32( HMAC-SHA256(secret, "v1|<edition>|<order id>") )

Deterministic derivation has three consequences worth stating plainly.

* No issuance database. The same order ID always yields the same identifier, so a
  reader who loses theirs simply registers again and receives the same one.
* Nothing to steal. There is no list of valid codes anywhere; validity is computed.
* One-time use still needs a ledger, but it stores only identifiers that have been
  redeemed — never order IDs, never email addresses.

Rotating EDB_SECRET invalidates every identifier at once, which is the intended
revocation mechanism for a leak.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import re
import time
import unicodedata

# Crockford Base32: no I, L, O or U, so nothing is mistaken when read aloud or
# copied off a screen.
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_DEAMBIGUATE = str.maketrans({"I": "1", "L": "1", "O": "0", "U": "V"})

EDITION = os.environ.get("EDB_EDITION", "1")
ID_RX = re.compile(r"^EDB-[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}$")

# Amazon order IDs are 3-7-7 digits. Other retailers are accepted on a longer,
# looser rule so that a reader who bought elsewhere is not shut out.
AMAZON_RX = re.compile(r"^\d{3}-\d{7}-\d{7}$")
OTHER_RX = re.compile(r"^[A-Z0-9][A-Z0-9-]{7,31}$")


class AccessError(Exception):
    """Raised when a proof of purchase or an identifier will not do."""


def _secret() -> bytes:
    s = os.environ.get("EDB_SECRET")
    if not s:
        raise AccessError("EDB_SECRET is not set")
    if len(s) < 32:
        raise AccessError("EDB_SECRET must be at least 32 characters")
    return s.encode()


def _b32(data: bytes, length: int) -> str:
    n = int.from_bytes(data, "big")
    out = []
    for _ in range(length):
        out.append(ALPHABET[n & 31])
        n >>= 5
    return "".join(reversed(out))


def normalise_order_id(raw: str) -> str:
    """Canonical form, so that spacing and case cannot produce a second identity."""
    s = unicodedata.normalize("NFKC", raw or "").strip().upper()
    s = re.sub(r"[\s‐-―_]+", "-", s)
    s = re.sub(r"[^A-Z0-9-]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        raise AccessError("empty order reference")
    if AMAZON_RX.match(s):
        return s
    digits = re.sub(r"\D", "", s)
    if len(digits) == 17 and "-" not in s:
        return f"{digits[:3]}-{digits[3:10]}-{digits[10:]}"
    if OTHER_RX.match(s):
        return s
    raise AccessError(
        "that does not look like an order reference. An Amazon order ID looks like "
        "123-1234567-1234567 and is on your order confirmation"
    )


def derive(order_id: str, edition: str = EDITION) -> str:
    """The reader's permanent identifier for this edition."""
    canonical = normalise_order_id(order_id)
    mac = hmac.new(_secret(), f"v1|{edition}|{canonical}".encode(), hashlib.sha256).digest()
    body = _b32(mac, 15)
    return f"EDB-{body[0:5]}-{body[5:10]}-{body[10:15]}"


def tidy(identifier: str) -> str:
    """Accept what a person actually types: lower case, spaces, O for 0."""
    s = unicodedata.normalize("NFKC", identifier or "").strip().upper()
    s = re.sub(r"[^A-Z0-9]", "", s)
    if s.startswith("EDB"):
        s = s[3:]
    s = s.translate(_DEAMBIGUATE)
    if len(s) != 15:
        raise AccessError("an identifier has fifteen characters after EDB-")
    return f"EDB-{s[0:5]}-{s[5:10]}-{s[10:15]}"


def matches(identifier: str, order_id: str, edition: str = EDITION) -> bool:
    """Constant-time check that an identifier belongs to an order reference."""
    try:
        return hmac.compare_digest(tidy(identifier), derive(order_id, edition))
    except AccessError:
        return False


# ---------------------------------------------------------------- download links


def sign_download(identifier: str, ttl_seconds: int = 72 * 3600,
                  now: int | None = None) -> tuple[str, int]:
    """A link that expires. Returns (signature, expiry)."""
    exp = int(now or time.time()) + ttl_seconds
    payload = f"dl|{tidy(identifier)}|{exp}".encode()
    sig = hmac.new(_secret(), payload, hashlib.sha256).digest()
    return _b32(sig, 26), exp


def check_download(identifier: str, exp: int, sig: str, now: int | None = None) -> bool:
    if int(now or time.time()) > int(exp):
        return False
    expected, _ = sign_download(identifier, ttl_seconds=0, now=int(exp))
    return hmac.compare_digest(expected, (sig or "").strip().upper())


# ---------------------------------------------------------------- challenge


def check_challenge(answer: str, expected: str) -> bool:
    """The question lives in configuration, never in print, so it can be changed
    the day an answer appears on a forum."""
    def norm(s: str) -> str:
        s = unicodedata.normalize("NFKD", (s or "").lower())
        s = "".join(c for c in s if not unicodedata.combining(c))
        return re.sub(r"[^a-z0-9]+", "", s)
    a, b = norm(answer), norm(expected)
    return bool(a) and hmac.compare_digest(a, b)
