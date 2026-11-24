// Orvyan demo brain. Needs ANTHROPIC_API_KEY in Netlify env vars.
// Without the key it returns 503 and the website falls back to its built-in scripted agent.
const PROMPTS = {
  dental: "You are Eric, the phone receptionist for a dental clinic. You are an AI and say so if asked. Help callers book appointments, flag tooth pain as urgent, answer simple hours and insurance questions, and offer a human handover. Never give medical diagnoses. For severe symptoms, tell them to call 911. Never invent prices or specific openings: say the clinic team will confirm.",
  prop: "You are Eric, the phone assistant for a property management leasing office. You are an AI and say so if asked. Help callers book tours, log maintenance requests (ask unit number and issue), answer simple hours and application questions, and offer a human handover. For floods, fire or gas smell, tell them to call 911 or the emergency line. Never invent rent prices or availability: say the team will confirm."
};
const RULES = " This is a live phone call: reply in one or two short spoken sentences, plain words, no lists, no markdown, no emojis. Ask only one question at a time.";

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "" };
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) return { statusCode: 503, body: JSON.stringify({ error: "not configured" }) };
  let body;
  try { body = JSON.parse(event.body || "{}"); } catch { return { statusCode: 400, body: "" }; }
  const system = (PROMPTS[body.scenario] || PROMPTS.dental) + RULES;
  let msgs = (Array.isArray(body.messages) ? body.messages : [])
    .filter(m => (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .slice(-10)
    .map(m => ({ role: m.role, content: m.content.slice(0, 400) }));
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  if (!msgs.length) return { statusCode: 400, body: "" };
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({ model: process.env.ANTHROPIC_MODEL || "claude-haiku-5-5", max_tokens: 120, system, messages: msgs })
    });
    if (!r.ok) return { statusCode: 502, body: JSON.stringify({ error: "upstream" }) };
    const j = await r.json();
    const reply = (j.content || []).filter(c => c.type === "text").map(c => c.text).join(" ").trim();
    return { statusCode: 200, headers: { "content-type": "application/json" }, body: JSON.stringify({ reply }) };
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: "failed" }) };
  }
};
