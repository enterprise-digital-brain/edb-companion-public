# The Contextual Agentic Enterprise — companion repository

Companion material for **The Contextual Agentic Enterprise: From systems of record to
governed AI agents and enterprise outcomes**, by Hanif Karimi. Published under the
Enterprise Digital Brain programme.

This is the one address printed in the book. Everything else is reached from here, so
that a change of host or arrangement costs a commit rather than a reprint.

## Everything the book points at — public, no registration

| Path | What it is | Where the book points at it |
|---|---|---|
| [`docs/adr/`](docs/adr/) | Ten worked Architecture Decision Records, a minimal template and the decision checklist | Appendix C |
| [`evaluation/scorecards/`](evaluation/scorecards/) | Task envelope, candidate-model, router, memory and continual-learning scorecards; benchmark anti-patterns | Appendix E |
| [`docs/cloud-mapping/`](docs/cloud-mapping/) | Vendor-neutral responsibilities mapped to AWS and Azure, with the portable seams called out | Appendix F |
| [`skills/`](skills/) | The structured agent skill standard: package layout, SKILL.md, evaluation harness, lifecycle, checklists | Appendix G |
| [`listings/`](listings/) | The fourteen code listings abridged in the text, in full | The *Listing abridged* notes |
| [`samples/`](samples/) | Runnable examples | Chapters 9 and 17 |

Four appendices live here rather than in the book because they are templates you fill
in, or a cloud mapping that changes faster than a printed page can. The arguments they
rest on are in the chapters; only the forms moved.

## Reader access to the extended material

The code laboratory, the Terraform definitions and the enterprise template set are for
readers who bought the book.

Every printed copy is identical — Amazon does not do variable-data printing and gives
authors no buyer details — so a code cannot be printed in the book or emailed out. You
earn an identifier instead, at **[the registration page](access/)**, with your order
reference and one question answerable from a copy of the book.

Your identifier looks like `EDB-XXXXX-XXXXX-XXXXX`. Keep it: it is how you come back
for later revisions without registering again.

We store your identifier and nothing else — not your order reference, not your email
address. The identifier is a one-way function of your order reference and cannot be
turned back into it. [`access/`](access/) contains the whole implementation, so you can
check that claim rather than take it on trust. That seemed the least this book could do.

## Errata

Corrections to the printed text are in [`docs/errata.md`](docs/errata.md). If you find
something, open an issue — corrections are credited.

## Resource IDs

Book examples use stable identifiers such as `EDB-C07-PAT01`. These stay stable when an
implementation is updated, so a reference in the printed text keeps resolving.

## Working on this repository

```bash
python -m pytest            # configuration is in pyproject.toml
python tools/check_book_pointers.py
```

`tools/check_book_pointers.py` fails the build if a path the printed book names has
gone missing. It is the book's own argument about conformance applied to the book
itself: the manifest is the specification, the repository is the execution, CI is the
check. **Never delete a path an edition still in print refers to.** Add a redirect
instead.

## Security

Never commit credentials, tokens, private keys, customer data, or reader entitlement
data. `EDB_SECRET` and `EDB_CHALLENGE` are deployment secrets and belong nowhere in
git. See [SECURITY.md](SECURITY.md).

## Licence

Code is MIT (see [LICENSE](LICENSE)). The prose of the book, and the appendix text
reproduced here, remain © Hanif Karimi.
