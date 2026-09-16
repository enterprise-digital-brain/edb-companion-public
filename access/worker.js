/**
 * Reader access for The Contextual Agentic Enterprise.
 *
 * One Cloudflare Worker, one KV namespace, no server and no database. It mirrors
 * edb_access.py exactly, so an identifier issued here verifies there and vice
 * versa — useful when answering a support message from a laptop.
 *
 * Bindings
 *   LEDGER        KV namespace. Stores redeemed identifiers only: never an order
 *                 reference, never an email address.
 *   EDB_SECRET    secret. Rotating it invalidates every identifier at once.
 *   EDB_EDITION   var, default "1".
 *   EDB_CHALLENGE secret. The expected answer. The question is in CHALLENGE_TEXT
 *                 below and is never printed in the book, so both can change the
 *                 day an answer turns up on a forum.
 *   BUNDLE_URL    var. Where a signed link finally redirects to.
 */

const ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
const AMAZON = /^\d{3}-\d{7}-\d{7}$/;
const OTHER = /^[A-Z0-9][A-Z0-9-]{7,31}$/;
const ID_RX = /^EDB-[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}$/;

const CHALLENGE_TEXT =
  "One question from the book, so we know you have a copy: in Appendix B.2, " +
  "complete the sentence — “The model may propose (a); it cannot manufacture the …”";

// ---------------------------------------------------------------- primitives

async function hmac(secret, message) {
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(message));
  return new Uint8Array(sig);
}

function b32(bytes, length) {
  let n = 0n;
  for (const b of bytes) n = (n << 8n) | BigInt(b);
  let out = "";
  for (let i = 0; i < length; i++) {
    out = ALPHABET[Number(n & 31n)] + out;
    n >>= 5n;
  }
  return out;
}

function constantTimeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// ---------------------------------------------------------------- normalising

function normaliseOrderId(raw) {
  let s = (raw || "").normalize("NFKC").trim().toUpperCase();
  s = s.replace(/[\s‐-―_]+/g, "-").replace(/[^A-Z0-9-]/g, "");
  s = s.replace(/-{2,}/g, "-").replace(/^-+|-+$/g, "");
  if (!s) throw new Error("empty order reference");
  if (AMAZON.test(s)) return s;
  const digits = s.replace(/\D/g, "");
  if (digits.length === 17 && !s.includes("-")) {
    return `${digits.slice(0, 3)}-${digits.slice(3, 10)}-${digits.slice(10)}`;
  }
  if (OTHER.test(s)) return s;
  throw new Error(
    "That does not look like an order reference. An Amazon order ID looks like " +
    "123-1234567-1234567 and is on your order confirmation."
  );
}

function normaliseAnswer(s) {
  return (s || "").normalize("NFKD").toLowerCase()
    .replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "");
}

function tidyIdentifier(raw) {
  let s = (raw || "").normalize("NFKC").trim().toUpperCase().replace(/[^A-Z0-9]/g, "");
  if (s.startsWith("EDB")) s = s.slice(3);
  s = s.replace(/[IL]/g, "1").replace(/O/g, "0").replace(/U/g, "V");
  if (s.length !== 15) throw new Error("An identifier has fifteen characters after EDB-.");
  return `EDB-${s.slice(0, 5)}-${s.slice(5, 10)}-${s.slice(10)}`;
}

// ---------------------------------------------------------------- derivation

async function derive(env, orderId) {
  const canonical = normaliseOrderId(orderId);
  const edition = env.EDB_EDITION || "1";
  return "EDB-" + b32(await hmac(env.EDB_SECRET, `v1|${edition}|${canonical}`), 15)
    .replace(/^(.{5})(.{5})(.{5})$/, "$1-$2-$3");
}

async function signDownload(env, identifier, ttl = 72 * 3600, now = null) {
  const exp = Math.floor((now ?? Date.now() / 1000)) + ttl;
  const sig = b32(await hmac(env.EDB_SECRET, `dl|${tidyIdentifier(identifier)}|${exp}`), 26);
  return { sig, exp };
}

async function checkDownload(env, identifier, exp, sig) {
  if (Math.floor(Date.now() / 1000) > Number(exp)) return false;
  const { sig: expected } = await signDownload(env, identifier, 0, Number(exp));
  return constantTimeEqual(expected, (sig || "").trim().toUpperCase());
}

// ---------------------------------------------------------------- handlers

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

async function handleRegister(request, env) {
  let body;
  try { body = await request.json(); } catch { return json({ error: "Send JSON." }, 400); }

  if (normaliseAnswer(body.answer) === "" ||
      !constantTimeEqual(normaliseAnswer(body.answer), normaliseAnswer(env.EDB_CHALLENGE))) {
    return json({ error: "That is not the answer the book gives. Check Appendix B.2." }, 403);
  }

  let identifier;
  try { identifier = await derive(env, body.order_id); }
  catch (e) { return json({ error: e.message }, 400); }

  // Deterministic derivation means a reader who registers twice gets the same
  // identifier back. Only a different order reference produces a different one.
  const seen = await env.LEDGER.get(identifier, { type: "json" });
  const record = seen || { first_seen: new Date().toISOString(), count: 0 };
  record.count += 1;
  record.last_seen = new Date().toISOString();
  if (record.count > 25) {
    return json({
      error: "This identifier has been used a great many times. If that is not you, " +
             "write to the address in the repository README.",
      identifier,
    }, 429);
  }
  await env.LEDGER.put(identifier, JSON.stringify(record));

  const { sig, exp } = await signDownload(env, identifier);
  const url = new URL(request.url);
  url.pathname = "/download";
  url.search = `?id=${identifier}&exp=${exp}&sig=${sig}`;
  return json({
    identifier,
    download_url: url.toString(),
    expires: new Date(exp * 1000).toISOString(),
    note: "Keep your identifier. It is how you return for later revisions without registering again.",
  });
}

async function handleReturn(request, env) {
  let body;
  try { body = await request.json(); } catch { return json({ error: "Send JSON." }, 400); }
  let identifier;
  try { identifier = tidyIdentifier(body.identifier); }
  catch (e) { return json({ error: e.message }, 400); }

  // An identifier is only known if it has been registered, so an unredeemed
  // guess reveals nothing about whether it would have been valid.
  const seen = await env.LEDGER.get(identifier, { type: "json" });
  if (!seen) return json({ error: "That identifier has not been registered." }, 404);

  const { sig, exp } = await signDownload(env, identifier);
  const url = new URL(request.url);
  url.pathname = "/download";
  url.search = `?id=${identifier}&exp=${exp}&sig=${sig}`;
  return json({ identifier, download_url: url.toString(), expires: new Date(exp * 1000).toISOString() });
}

async function handleDownload(request, env) {
  const url = new URL(request.url);
  const id = url.searchParams.get("id") || "";
  const exp = url.searchParams.get("exp") || "0";
  const sig = url.searchParams.get("sig") || "";
  if (!ID_RX.test(id)) return json({ error: "Malformed identifier." }, 400);
  if (!(await checkDownload(env, id, exp, sig))) {
    return json({ error: "This link has expired. Ask for a new one with your identifier." }, 403);
  }
  return Response.redirect(env.BUNDLE_URL, 302);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/challenge") {
      return json({ question: CHALLENGE_TEXT });
    }
    if (request.method === "POST" && url.pathname === "/register") {
      return handleRegister(request, env);
    }
    if (request.method === "POST" && url.pathname === "/return") {
      return handleReturn(request, env);
    }
    if (request.method === "GET" && url.pathname === "/download") {
      return handleDownload(request, env);
    }
    return json({ error: "Not found." }, 404);
  },
};
