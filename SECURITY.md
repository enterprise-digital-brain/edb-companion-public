# Security

## Reporting

Report anything security-relevant by opening a [private security advisory][adv] rather
than a public issue. Expect an acknowledgement within a week.

[adv]: https://github.com/enterprise-digital-brain/edb-companion-public/security/advisories/new

## What lives here, and what must not

This repository is public and contains the reader-access implementation. That is
deliberate: a reader can check how their data is handled rather than take it on trust.

What must never be committed:

- `EDB_SECRET` or `EDB_CHALLENGE`. Both are deployment secrets, set with
  `wrangler secret put`.
- Reader identifiers, order references or email addresses.
- Cloud credentials, tokens, private keys or customer data.

## The access scheme, stated plainly

A reader identifier is `HMAC-SHA256(EDB_SECRET, "v1|<edition>|<order id>")` in Crockford
Base32. It is derived, never issued from a list, so there is no table of valid codes to
leak. The ledger stores redeemed identifiers only, and an identifier cannot be reversed
into the order reference it came from.

Rotating `EDB_SECRET` invalidates every identifier at once. That is the intended
response to a leak, and readers can re-register to obtain their new one.

The scheme deters casual sharing and gives every buyer something of their own. It does
not defeat a determined sharer, and is not claimed to.
