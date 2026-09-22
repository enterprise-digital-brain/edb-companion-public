# -*- coding: utf-8 -*-
"""Prove that worker.js and edb_access.py still derive the same identifier.

Two implementations of one scheme drift silently, and the failure is invisible until
a reader is told their identifier is wrong. This runs both over the same inputs and
compares.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "access"))

CASES = [
    "114-8352901-7654321",
    "  114 8352901 7654321  ",
    "11483529017654321",
    "702-1111111-2222222",
    "D01-9876543-1234567",
    "ORDER-ABC-123456789",
]

NODE = r"""
const A = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
const crypto = require("crypto");
const AMAZON = /^\d{3}-\d{7}-\d{7}$/;
const OTHER = /^[A-Z0-9][A-Z0-9-]{7,31}$/;
function b32(bytes, len){ let n=0n; for(const b of bytes) n=(n<<8n)|BigInt(b);
  let o=""; for(let i=0;i<len;i++){ o=A[Number(n&31n)]+o; n>>=5n; } return o; }
function norm(raw){
  let s=(raw||"").normalize("NFKC").trim().toUpperCase();
  s=s.replace(/[\s‐-―_]+/g,"-").replace(/[^A-Z0-9-]/g,"");
  s=s.replace(/-{2,}/g,"-").replace(/^-+|-+$/g,"");
  if(!s) throw new Error("empty");
  if(AMAZON.test(s)) return s;
  const d=s.replace(/\D/g,"");
  if(d.length===17 && !s.includes("-")) return `${d.slice(0,3)}-${d.slice(3,10)}-${d.slice(10)}`;
  if(OTHER.test(s)) return s;
  throw new Error("bad order reference");
}
const secret = process.env.EDB_SECRET;
const edition = process.env.EDB_EDITION || "1";
const out = {};
for (const c of JSON.parse(process.argv[1])) {
  const mac = crypto.createHmac("sha256", secret)
    .update(`v1|${edition}|${norm(c)}`).digest();
  out[c] = "EDB-" + b32(mac,15).replace(/^(.{5})(.{5})(.{5})$/,"$1-$2-$3");
}
console.log(JSON.stringify(out));
"""


def main() -> int:
    import edb_access

    if not os.environ.get("EDB_SECRET"):
        print("EDB_SECRET is not set", file=sys.stderr)
        return 2

    node = subprocess.run(
        ["node", "-e", NODE, json.dumps(CASES)],
        capture_output=True, text=True, env=os.environ,
    )
    if node.returncode != 0:
        print(node.stderr, file=sys.stderr)
        return 2
    js = json.loads(node.stdout)

    bad = []
    for case in CASES:
        py = edb_access.derive(case)
        if py != js[case]:
            bad.append(f"  {case!r}\n      python {py}\n      worker {js[case]}")

    if bad:
        print("worker.js and edb_access.py disagree:\n", file=sys.stderr)
        print("\n".join(bad), file=sys.stderr)
        return 1

    print(f"Both implementations agree on all {len(CASES)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
