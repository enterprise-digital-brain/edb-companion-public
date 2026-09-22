# Reader access

How a buyer of *The Contextual Agentic Enterprise* gets a unique identifier and the
extended material. One Cloudflare Worker, one KV namespace, one static page. No
server, no database, nothing to pay for at this scale.

## The constraint that shapes everything

**Every KDP copy is printed identically.** Amazon does not do variable-data printing
and does not give authors buyer details, so a unique code cannot be printed in the
book and codes cannot be emailed out. The identifier has to be *earned at
redemption*, not distributed.

That is what this does. The reader proves purchase, and their identifier is derived
from that proof.

## How an identifier is made

```
identifier = EDB - base32( HMAC-SHA256(EDB_SECRET, "v1|<edition>|<order id>") )
```

Deterministic derivation, which buys three things:

- **No issuance database.** The same order reference always yields the same
  identifier, so a reader who loses theirs registers again and gets it back.
- **Nothing to steal.** There is no list of valid codes anywhere. Validity is
  computed, not looked up.
- **One-line revocation.** Rotating `EDB_SECRET` invalidates every identifier at
  once. That is the response to a leak.

The ledger stores redeemed identifiers only — never an order reference, never an
email address. The identifier is a one-way function of the order reference and
cannot be turned back into it, so the KV namespace holds nothing worth stealing.

Crockford Base32 drops I, L, O and U, so nothing is misread over the phone or
mistyped off a screen; `tidy()` repairs the usual substitutions anyway.

## The two gates

**Proof of purchase.** An order reference, format-checked and normalised so that
spacing and case cannot manufacture a second identity. Amazon's 3-7-7 shape is
recognised; other retailers pass a looser rule so nobody who bought elsewhere is
shut out. This gives one-identifier-per-purchase. It does not prove authenticity —
nothing free can — but a reused reference is visible in the ledger.

**A question from the book.** The answer lives in `EDB_CHALLENGE`, the question in
`CHALLENGE_TEXT` in `worker.js`. **Neither is printed in the book.** That is the
point: the day an answer appears on a forum, change both and redeploy. Nothing on
paper goes stale.

## Files

| File | What it is |
|---|---|
| `worker.js` | The Worker: `/challenge`, `/register`, `/return`, `/download` |
| `edb_access.py` | The same scheme in Python, for support and for issuing by hand |
| `test_edb_access.py` | Tests for the Python side |
| `index.html` | The redemption page, for GitHub Pages |
| `wrangler.toml` | Worker configuration |

`worker.js` and `edb_access.py` produce byte-identical identifiers. Verify after any
change:

```bash
EDB_SECRET=… python3 -c "import edb_access; print(edb_access.derive('114-8352901-7654321'))"
```

## Setting it up

```bash
# 1. the ledger
npx wrangler kv namespace create LEDGER      # put the id in wrangler.toml

# 2. the secrets — generate a real one, do not invent it by hand
openssl rand -base64 48 | npx wrangler secret put EDB_SECRET
npx wrangler secret put EDB_CHALLENGE        # the expected answer, lower case

# 3. deploy
npx wrangler deploy
```

Then publish `index.html` with GitHub Pages from `edb-companion-public`, and set
`API` at the bottom of it to the deployed Worker URL.

Finally, build the extended bundle and attach it as a release asset, and point
`BUNDLE_URL` at it:

```bash
zip -r edb-extended.zip edb-code-lab edb-codevault-iac edb-templates
gh release create extended-v1 edb-extended.zip --repo enterprise-digital-brain/edb-companion-public
```

## What the book prints

One address, and only one:

```
https://github.com/enterprise-digital-brain/edb-companion-public
```

The redemption page, the errata and any change of arrangements are linked from that
repository's README. A printed page cannot be corrected; a README can. Every other
link is behind the one address, so a change of host, form or provider costs a commit
rather than a reprint.

## What this does and does not do

It stops casual copying and gives every buyer something of their own. It will not
stop a determined sharer, and it is not meant to — the honest reason to register a
reader is to be able to send them a fix, not to police them.

The material the book actually teaches from is public, deliberately. A public
companion repository sells more copies than a locked one protects.
