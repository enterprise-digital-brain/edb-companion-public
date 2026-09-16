# -*- coding: utf-8 -*-
"""Fail the build if a path the printed book points at has gone missing.

The book gives one address and then names paths beneath it. A printed page cannot
be corrected, so a path that disappears here becomes a dead end in every copy ever
sold. This is the book's own argument about conformance applied to the book: the
manifest below is the specification, the repository is the execution, and CI is the
conformance check.

Add to MANIFEST whenever a new edition prints a new path. Never remove an entry for
a path an edition still in print refers to.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# path -> where it is printed
MANIFEST: dict[str, str] = {
    "docs/adr/": "Appendix C stub, and the Companion repository page in the front matter",
    "evaluation/scorecards/": "Appendix E stub, and the front matter",
    "docs/cloud-mapping/": "Appendix F stub, and the front matter",
    "skills/": "Appendix G stub, and the front matter",
    "listings/": "the front matter, and fourteen 'Listing abridged' notes",
    "listings/ch05-01.yaml": "chapter 5, abridged listing",
    "listings/ch08-01.py": "chapter 8, abridged listing",
    "listings/ch08-02.py": "chapter 8, abridged listing",
    "listings/ch12-01.json": "chapter 12, the canonical Agentic Flow Mining event",
    "listings/ch15-01.yaml": "chapter 15, abridged listing",
    "listings/ch15-02.py": "chapter 15, abridged listing",
    "listings/ch15-03.txt": "chapter 15, abridged listing",
    "listings/ch15-04.yaml": "chapter 15, abridged listing",
    "listings/ch17-01.yaml": "chapter 17, abridged listing",
    "listings/ch21-01.json": "chapter 21, abridged listing",
    "listings/ch21-02.py": "chapter 21, abridged listing",
    "listings/ch25-01.yaml": "chapter 25, abridged listing",
    "listings/ch25-02.py": "chapter 25, abridged listing",
    "listings/ch25-03.py": "chapter 25, abridged listing",
}

# The README is the only page the book routes readers onward through, so these have
# to be reachable from it or the single printed address leads nowhere useful.
README_MUST_MENTION = ["docs/adr", "listings", "access", "errata"]


def main() -> int:
    problems: list[str] = []

    for path, printed_in in MANIFEST.items():
        target = ROOT / path
        if path.endswith("/"):
            if not target.is_dir():
                problems.append(f"missing directory  {path:<32} printed in {printed_in}")
            elif not any(target.iterdir()):
                problems.append(f"empty directory    {path:<32} printed in {printed_in}")
        elif not target.is_file():
            problems.append(f"missing file       {path:<32} printed in {printed_in}")
        elif target.stat().st_size == 0:
            problems.append(f"empty file         {path:<32} printed in {printed_in}")

    readme = (ROOT / "README.md")
    if not readme.is_file():
        problems.append("missing README.md — the one printed address resolves to it")
    else:
        text = readme.read_text(encoding="utf-8").lower()
        for token in README_MUST_MENTION:
            if token not in text:
                problems.append(f"README.md no longer mentions {token!r}")

    if problems:
        print("Book pointers do not resolve:\n", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(
            "\nEvery one of these is printed in a book that cannot be corrected.\n"
            "Restore the path, or add a redirect, before merging.",
            file=sys.stderr,
        )
        return 1

    print(f"All {len(MANIFEST)} printed pointers resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
