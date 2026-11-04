#!/usr/bin/env python3
"""Generates the Orvyan Tech v3 multi-page site into ./site/"""
import pathlib, os, re, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "site"
OUT.mkdir(exist_ok=True)

SITE = "https://www.orvyantech.com"
WHATSAPP = "https://wa.me/917972928086"
EMAIL = "orvyan.ai@gmail.com"
FORM = "https://formtorch.com/f/t2vo9j93fa"

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("how-it-works.html", "How it works"),
    ("industries.html", "Industries"),
    ("pricing.html", "Pricing"),
    ("faq.html", "FAQ"),
]

ICON = {
    "spark": '<path d="M12 3.5 13.7 9l5.5 1.7-5.5 1.7L12 17.9l-1.7-5.5L4.8 10.7 10.3 9 12 3.5Z"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12Z"/>',
    "bolt": '<path d="M13 3 5 13h5l-1 8 8-10h-5l1-8Z"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v2.2M12 18.8V21M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M3 12h2.2M18.8 12H21M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6"/>',
    "check": '<path d="M4 12.5 9 17.5 20 6.5"/>',
    "arrow": '<path d="M5 12h13M12.5 6l6 6-6 6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/>',
    "shield": '<path d="M12 3.5 19 6v6c0 4.2-3 7-7 8.5-4-1.5-7-4.3-7-8.5V6l7-2.5Z"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.4 3.8 5.4 3.8 8.5S14.5 18.1 12 20.5C9.5 18.1 8.2 15.1 8.2 12S9.5 5.9 12 3.5Z"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7 8 6 8-6"/>',
}


def icon(name, cls=""):
    return (
        '<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
        % (cls, ICON[name])
    )


def head(title, desc, canonical, extra=""):
    og = SOURCE_NAME = title
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{canonical}">
<meta name="theme-color" content="#08090c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Orvyan Tech">
<meta property="og:title" content="{og}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{canonical}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://formtorch.com" crossorigin>
<link rel="preload" href="assets/css/site.css" as="style">
<link rel="stylesheet" href="assets/css/site.css">
<link rel="preconnect" href="https://www.googletagmanager.com">
{extra}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GD2M58Q7JF"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}
gtag('js',new Date());gtag('config','G-GD2M58Q7JF');
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="index.html"><span class="brand-chip"><img src="assets/img/logo.svg" alt="" width="22" height="22"></span> Orvyan Tech</a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="Main">
      {nav_links(canonical)}
    </nav>
    <a class="cta" href="contact.html">Book a consultation {icon('arrow')}</a>
  </div>
</header>
<main id="main">
"""


CURRENT = {"page": ""}


def nav_links(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return "".join(out)


FOOT = f"""</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><span class="brand-chip"><img src="assets/img/logo.svg" alt="" width="22" height="22"></span> Orvyan Tech</a>
        <p style="color:#98a2ad;font-size:.92rem;margin-top:12px;max-width:34ch">
          AI agents, voice agents and workflow automation, built around the tools your business already runs on.
        </p>
        <p style="color:#6d7681;font-size:.85rem">Based in India. Working remote-first.</p>
      </div>
      <div>
        <h4>Services</h4>
        <a href="services.html#agents">AI agents</a>
        <a href="services.html#workflows">Workflow automation</a>
        <a href="services.html#growth">Leads and growth</a>
        <a href="services.html#advise">Build and advise</a>
      </div>
      <div>
        <h4>Company</h4>
        <a href="how-it-works.html">How it works</a>
        <a href="industries.html">Industries</a>
        <a href="pricing.html">Pricing</a>
        <a href="faq.html">FAQ</a>
      </div>
      <div>
        <h4>Contact</h4>
        <a href="contact.html">Book a consultation</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> Orvyan Tech. All rights reserved.</span>
      <span class="pillars">
        <a href="privacy-policy.html">Privacy policy</a>
        <a href="terms-of-service.html">Terms of service</a>
      </span>
    </div>
  </div>
</footer>
<aside class="wa-dock min" id="waDock" aria-label="Chat with Orvyan Tech on WhatsApp">
  <div class="wa-head">
    <span class="wa-ava"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.5 14.1c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1a11 11 0 0 1-4.4-3.1c-1-1.2-1.6-2.4-1.6-3.2 0-.7.4-1.4.8-1.7.2-.2.4-.2.6-.2h.5c.2 0 .3 0 .5.4l.6 1.5c.1.2 0 .4-.1.5l-.4.5c-.1.2-.2.3 0 .5.4.7 1.5 1.9 2.4 2.3.2.1.4.1.5 0l.6-.7c.1-.2.3-.2.5-.1l1.5.7c.2.1.4.2.4.4 0 .1 0 .5-.1.9Z"/></svg></span>
    <div><strong>Orvyan Tech</strong><small>Replies instantly, 24/7</small></div>
    <button class="wa-min" type="button" aria-label="Minimise chat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg></button>
  </div>
  <div class="wa-body">
    <div class="wa-msg in">Hi, this is Orvyan Tech. Tell us what eats your team's time and we will say what can be automated.</div>
    <div class="wa-msg in">Voice agents, WhatsApp bots, n8n workflows, CRM follow up.</div>
    <div class="wa-msg me">Can you look at our clinic booking flow?</div>
  </div>
  <a class="wa-cta" href="{WHATSAPP}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.5 14.1c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1a11 11 0 0 1-4.4-3.1c-1-1.2-1.6-2.4-1.6-3.2 0-.7.4-1.4.8-1.7.2-.2.4-.2.6-.2h.5c.2 0 .3 0 .5.4l.6 1.5c.1.2 0 .4-.1.5l-.4.5c-.1.2-.2.3 0 .5.4.7 1.5 1.9 2.4 2.3.2.1.4.1.5 0l.6-.7c.1-.2.3-.2.5-.1l1.5.7c.2.1.4.2.4.4 0 .1 0 .5-.1.9Z"/></svg>Open WhatsApp</a>
</aside>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def flow_card():
    return f"""
      <div class="flow-card reveal d2">
        <div class="flow-head"><span>One appointment enquiry</span><span class="badge-live">Live example</span></div>
        <div class="step"><div class="num">1</div><div><h4>Customer messages on WhatsApp</h4>
          <div class="bubble">&ldquo;Can I book a slot for tomorrow evening?&rdquo;</div></div></div>
        <div class="step"><div class="num">2</div><div><h4>AI agent replies</h4>
          <div class="bubble reply">&ldquo;Tomorrow at 5:30 pm is free. Should I book it for you?&rdquo;</div></div></div>
        <div class="step"><div class="num">3</div><div><h4>Booking is saved</h4>
          <p>Added to your calendar and CRM, with the customer&rsquo;s details.</p></div></div>
        <div class="step"><div class="num">4</div><div><h4>Reminder goes out</h4>
          <p>Your team steps in only if the customer asks for a person.</p></div></div>
      </div>"""


def cta_band(title, text, primary=("contact.html", "Book a free consultation"), secondary=(WHATSAPP, "Message us on WhatsApp")):
    return f"""
<section><div class="wrap"><div class="cta-band reveal">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    <a class="cta" href="{primary[0]}">{primary[1]} {icon('arrow')}</a>
    <a class="cta ghost" href="{secondary[0]}"{' target="_blank" rel="noopener"' if secondary[0].startswith('http') else ''}>{secondary[1]}</a>
  </div>
</div></div></section>"""


def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")


# ----------------------------------------------------------------- index
def page_index():
    h = head(
        "Orvyan Tech | AI agents, voice agents and workflow automation",
        "Orvyan Tech builds AI agents, voice agents, WhatsApp bots and n8n workflow automation for businesses, creators and individuals. Book a free consultation.",
        "index.html",
    )
    h += f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow reveal"><i></i> AI agents &middot; Voice &middot; n8n workflows</span>
      <h1 class="display reveal d1">AI agents and automations that <span class="grad">answer, follow up</span> and keep work moving.</h1>
      <p class="lede reveal d2">We build voice agents, WhatsApp bots and n8n workflows around the tools and habits your business already has. No rip and replace, no new platform to learn.</p>
      <div class="hero-actions reveal d3">
        <a class="cta" href="contact.html">Book a free consultation {icon('arrow')}</a>
        <a class="cta ghost" href="{WHATSAPP}" target="_blank" rel="noopener">Message us on WhatsApp</a>
      </div>
      <div class="trust reveal d4">
        <span>{icon('globe')} Based in India</span>
        <span>{icon('bolt')} Remote-first</span>
        <span>{icon('clock')} Reply within 24 hours</span>
      </div>
    </div>
    {flow_card()}
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <span>WhatsApp</span><span>n8n</span><span>Make</span><span>Zapier</span><span>HubSpot</span><span>Shopify</span><span>Google Workspace</span><span>Airtable</span><span>Notion</span><span>Slack</span><span>OpenAI</span><span>Twilio</span>
    <span>WhatsApp</span><span>n8n</span><span>Make</span><span>Zapier</span><span>HubSpot</span><span>Shopify</span><span>Google Workspace</span><span>Airtable</span><span>Notion</span><span>Slack</span><span>OpenAI</span><span>Twilio</span>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">What we build</span>
      <h2>Four kinds of systems, one goal: work that finishes itself.</h2>
      <p>Everything is built around the tools you already use: WhatsApp, Google Workspace, your CRM and your website.</p>
    </div>
    <div class="grid g4">
      <a class="card reveal" href="services.html#agents"><div class="ico">{icon('chat')}</div>
        <h3>AI agents</h3><p>Answer, qualify and book on the channels your customers already use.</p>
        <span class="link-more">Explore {icon('arrow')}</span></a>
      <a class="card reveal d1" href="services.html#workflows"><div class="ico">{icon('gear')}</div>
        <h3>Workflow automation</h3><p>Ops and internal busywork, routed and resolved without a human in the middle.</p>
        <span class="link-more">Explore {icon('arrow')}</span></a>
      <a class="card reveal d2" href="services.html#growth"><div class="ico">{icon('bolt')}</div>
        <h3>Leads and growth</h3><p>Capture, enrich, follow up and book, before the lead cools down.</p>
        <span class="link-more">Explore {icon('arrow')}</span></a>
      <a class="card reveal d3" href="services.html#advise"><div class="ico">{icon('spark')}</div>
        <h3>Build and advise</h3><p>Custom integrations, internal tools and a clear plan for what to automate next.</p>
        <span class="link-more">Explore {icon('arrow')}</span></a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">Why it works</span>
      <h2>Automation that fits your business, not the other way round.</h2>
    </div>
    <div class="grid g3">
      <div class="card reveal"><div class="ico">{icon('bolt')}</div><h3>Live in days, not quarters</h3>
        <p>Simple workflows go live in a few days. Bigger agents take two to four weeks, and you see progress every week.</p></div>
      <div class="card reveal d1"><div class="ico">{icon('shield')}</div><h3>Your data stays yours</h3>
        <p>Encrypted connections, secure credential storage and role-based access. Nothing leaves your stack that does not need to.</p></div>
      <div class="card reveal d2"><div class="ico">{icon('chat')}</div><h3>A team that stays reachable</h3>
        <p>Documentation, a walkthrough and a real person to call after launch. No black box, no disappearing act.</p></div>
    </div>
  </div>
</section>

{cta_band("Tell us what eats your week.", "A short call is enough for us to tell you what can be automated, what cannot, and what it would cost.")}
"""
    write("index.html", h + FOOT)


# -------------------------------------------------------------- services
SERVICE_GROUPS = [
    ("agents", "Agents that talk to customers",
     "Answer, qualify and book, on the channels your customers already use.",
     [("AI agents", "Agents that answer questions, qualify leads and take action around the clock across support, sales and internal operations."),
      ("Voice agents", "Inbound and outbound calls handled end to end, with summaries and next steps written back to your CRM."),
      ("WhatsApp AI agents", "Conversations inside WhatsApp, with catalogues, booking and human handover when the customer asks for it."),
      ("Chatbots", "Website chat that answers from your own content instead of guessing, and hands off when it should."),
      ("Customer support AI", "Ticket triage, first replies and knowledge lookups, so your team only sees what needs a person.")]),
    ("workflows", "Workflows that run themselves",
     "Internal work that moves between tools, without someone copying and pasting between tabs.",
     [("AI automation", "Document reading, summarising, categorising and routing, built into the systems you already run."),
      ("Workflow automation", "n8n, Make and Zapier builds that connect your stack and keep it in sync."),
      ("Ops and internal workflows", "Onboarding, approvals, reporting and handoffs, made visible and repeatable."),
      ("Appointment booking", "Availability, booking, reminders and rescheduling handled in one path, with fewer no-shows.")]),
    ("growth", "Leads and growth",
     "Capture, follow up and book, before the lead cools down.",
     [("Lead generation and CRM automation", "New enquiries enriched, scored and routed to the right person with the right context."),
      ("Email automation", "Sequences that read like a person wrote them, with replies triaged automatically."),
      ("Social media automation", "Content scheduling, comment triage and reporting without touching four dashboards.")]),
    ("advise", "Build and advise",
     "Sometimes the right answer is a system. Sometimes it is a decision.",
     [("Custom integrations", "Two systems that were never meant to talk to each other, connected properly."),
      ("Custom AI solutions", "Internal tools and agents shaped around how your team actually works."),
      ("AI consulting", "A review of your operations, a ranked list of what to automate, and a plan you can act on.")]),
]


def page_services():
    h = head(
        "Services | Orvyan Tech",
        "AI agents, voice agents, WhatsApp bots, workflow automation, lead generation and custom integrations built for your existing stack.",
        "services.html",
    )
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / Services</p>
  <h1>Services</h1>
  <p>Four groups of work, one principle: your existing tools stay, and the gaps between them get closed.</p>
</div></section>
"""
    for gid, title, blurb, items in SERVICE_GROUPS:
        cards = "".join(
            f'<div class="card reveal d{min(i,3)}"><h3>{n}</h3><p>{d}</p></div>'
            for i, (n, d) in enumerate(items)
        )
        h += f"""
<section id="{gid}"><div class="wrap">
  <div class="sec-head reveal">
    <span class="kicker">{title}</span>
    <h2>{title}</h2>
    <p>{blurb}</p>
  </div>
  <div class="grid g3">{cards}</div>
</div></section>
"""
    h += cta_band("Not sure which one you need?", "Describe the task that keeps repeating. We will tell you what it takes to remove it.")
    write("services.html", h + FOOT)


# ---------------------------------------------------------- how it works
STEPS = [
    ("A free consultation", "Thirty minutes on your process, your tools and the points where work stalls. No deck, no pressure."),
    ("A written scope and quote", "What we will build, what it will touch, what it costs and how long it takes. You approve before anything starts."),
    ("Build in the open", "You see working versions early. Weekly updates, and a staging link you can click at any point."),
    ("Launch, document, hand over", "We run it live together, write the documentation and walk your team through it. Then we stay reachable."),
]


def page_how():
    h = head(
        "How it works | Orvyan Tech",
        "A free consultation, a written scope, a build you can watch, and a proper handover. Here is exactly how an Orvyan Tech project runs.",
        "how-it-works.html",
    )
    steps = "".join(
        f'<div class="p-step reveal d{min(i,3)}"><div class="num"></div><div><h3>{t}</h3><p>{d}</p></div></div>'
        for i, (t, d) in enumerate(STEPS)
    )
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / How it works</p>
  <h1>How a project runs</h1>
  <p>Three things you should never have to guess with an automation partner: what is being built, what it costs, and when it lands.</p>
</div></section>

<section><div class="wrap">
  <div class="process">{steps}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head reveal"><span class="kicker">Timelines</span><h2>What to expect, honestly</h2></div>
  <div class="grid g3">
    <div class="card reveal"><h3>Simple workflow</h3><p>A form, a sheet and two tools talking. Usually live within a few days.</p></div>
    <div class="card reveal d1"><h3>AI agent</h3><p>Knowledge, guardrails, channel setup and testing. Typically two to four weeks.</p></div>
    <div class="card reveal d2"><h3>Multi tool system</h3><p>Several integrations, permissions and a rollout plan. Scoped after the consultation.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head reveal"><span class="kicker">Included</span><h2>What you get at handover</h2></div>
  <div class="grid g4">
    <div class="card reveal"><div class="ico">{icon('check')}</div><h3>Working build</h3><p>Live in your accounts, on your credentials.</p></div>
    <div class="card reveal d1"><div class="ico">{icon('check')}</div><h3>Documentation</h3><p>What each step does and how to change it.</p></div>
    <div class="card reveal d2"><div class="ico">{icon('check')}</div><h3>Walkthrough</h3><p>A session with the people who will run it.</p></div>
    <div class="card reveal d3"><div class="ico">{icon('check')}</div><h3>Support window</h3><p>A defined period for fixes after launch.</p></div>
  </div>
</div></section>

{cta_band("Start with the consultation.", "It is free, it takes thirty minutes, and you leave with a clear idea of what to automate first.")}
"""
    write("how-it-works.html", h + FOOT)


# ------------------------------------------------------------ industries
INDUSTRIES = [
    ("Clinics and healthcare", "Appointment enquiries answered in seconds on WhatsApp, bookings written straight into the calendar, reminders that cut no-shows.", "chat"),
    ("E-commerce", "Order status, returns, product questions and abandoned carts handled without a queue of copy-paste replies.", "bolt"),
    ("Agencies and studios", "New business enquiries qualified, briefs collected, and internal reporting assembled on a schedule.", "gear"),
    ("Real estate", "Viewing requests matched to availability, follow-ups sent on time, and every lead logged with context.", "globe"),
    ("Coaching and creators", "DMs, forms and calls triaged into a single pipeline, with content and email follow-up on autopilot.", "spark"),
    ("Professional services", "Client onboarding, document collection, approvals and status updates that no longer live in someone's inbox.", "shield"),
]


def page_industries():
    h = head(
        "Industries | Orvyan Tech",
        "Where automation pays back fastest: clinics, e-commerce, agencies, real estate, coaching and professional services.",
        "industries.html",
    )
    cards = "".join(
        f'<div class="card reveal d{min(i%4,3)}"><div class="ico">{icon(ic)}</div><h3>{n}</h3><p>{d}</p></div>'
        for i, (n, d, ic) in enumerate(INDUSTRIES)
    )
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / Industries</p>
  <h1>Industries</h1>
  <p>The same pattern shows up everywhere: a person asks something, someone else has to look it up, and the answer arrives late. That gap is what we remove.</p>
</div></section>

<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>

<section class="band"><div class="wrap">
  <div class="sec-head reveal"><span class="kicker">Outside the list</span><h2>If your work has a repeatable step, it qualifies</h2>
  <p>No size is too small to start. We have built for solo operators and for teams of forty. The question is not the industry, it is whether the same task happens more than once a week.</p></div>
  <div class="hero-actions"><a class="cta" href="contact.html">Ask about your case {icon('arrow')}</a></div>
</div></section>
"""
    write("industries.html", h + FOOT)


# --------------------------------------------------------------- pricing
def page_pricing():
    h = head(
        "Pricing | Orvyan Tech",
        "How Orvyan Tech prices AI agents and automation: scoped after a free consultation, with clear tiers and no surprise invoices.",
        "pricing.html",
    )
    plans = [
        ("Starter", "One workflow or one agent", "For a single, well-defined task that repeats every day.",
         ["One automation or agent", "Up to two tools connected", "Testing and launch support", "Documentation and walkthrough"], False),
        ("Core", "A connected system", "For an agent plus the workflows that feed it.",
         ["AI agent on one channel", "Multiple workflow steps", "CRM or calendar integration", "Human handover rules", "Support window after launch"], True),
        ("Custom", "Built around your operation", "For several integrations, voice, or internal tooling.",
         ["Multi channel agents", "Voice or WhatsApp at scale", "Custom integrations and internal tools", "Rollout plan and team training"], False),
    ]
    cards = ""
    for name, sub, desc, feats, feature in plans:
        li = "".join(f"<li>{icon('check')} <span>{f}</span></li>" for f in feats)
        cards += f"""
    <div class="price-card reveal {'feature' if feature else ''}">
      <div class="tier">{sub}</div>
      <h3>{name}</h3>
      <p class="quote">{desc}</p>
      <ul>{li}</ul>
      <a class="cta {'ghost' if not feature else ''}" href="contact.html">Get a quote</a>
    </div>"""
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / Pricing</p>
  <h1>Pricing</h1>
  <p>Every project is quoted after a free consultation, because the price depends on how many workflows, which tools and whether an agent is involved. What does not change is the structure.</p>
</div></section>

<section><div class="wrap"><div class="grid g3">{cards}</div>
  <p class="form-note" style="margin-top:18px">Consultation is free. You approve a written scope and quote before any work starts.</p>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head reveal"><span class="kicker">What moves the number</span><h2>Four things decide the price</h2></div>
  <div class="grid g4">
    <div class="card reveal"><h3>Number of workflows</h3><p>One clean path costs less than five that branch into each other.</p></div>
    <div class="card reveal d1"><h3>Tools involved</h3><p>Native integrations are quick. Systems without an API take longer.</p></div>
    <div class="card reveal d2"><h3>Channel</h3><p>Web chat is simplest, WhatsApp and voice add setup and compliance work.</p></div>
    <div class="card reveal d3"><h3>Volume and edge cases</h3><p>High traffic and unusual cases need more guardrails and testing.</p></div>
  </div>
</div></section>

{cta_band("Want a number for your case?", "Tell us the process and the tools. You get a written quote with scope, price and timeline.")}
"""
    write("pricing.html", h + FOOT)


# ------------------------------------------------------------------- faq
FAQS = [
    ("What kind of businesses do you work with?",
     "Startups, agencies, local businesses, creators, healthcare providers, e-commerce brands and individuals who want to automate repetitive work. No size is too small to start."),
    ("How much does it cost?",
     "It depends on the number of workflows, the tools involved and whether an AI agent is needed. Every project starts with a free consultation, after which you get a clear quote for the scope we agree on."),
    ("How long does it take to build an automation?",
     "Simple workflows can go live within a few days. More involved AI agents or multi tool integrations typically take two to four weeks, depending on scope."),
    ("Do I need technical knowledge to use what you build?",
     "No. We design systems to be easy to manage day to day, and we provide documentation and a walkthrough so your team is comfortable running them."),
    ("Which tools can you integrate with?",
     "Most modern platforms: n8n, Make, Zapier, WhatsApp, Slack, Google Workspace, Shopify, HubSpot, Notion, Airtable and custom APIs, among others."),
    ("Is my data secure?",
     "We use encrypted connections, secure credential storage and role-based access, and can design the system so sensitive data never leaves your own infrastructure."),
    ("What happens after launch?",
     "You get documentation, a walkthrough session and a support window for fixes. After that you can run it yourself or keep us on a monthly arrangement."),
]


def page_faq():
    h = head(
        "FAQ | Orvyan Tech",
        "Answers on scope, pricing, timelines, tools, security and what happens after an Orvyan Tech automation goes live.",
        "faq.html",
    )
    items = "".join(
        f'<details class="faq reveal"{" open" if i == 0 else ""}><summary>{q}</summary><p class="a">{a}</p></details>'
        for i, (q, a) in enumerate(FAQS)
    )
    import json
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS
        ],
    }
    extra = '<script type="application/ld+json">' + json.dumps(schema, indent=2) + "</script>"
    h = head(
        "FAQ | Orvyan Tech",
        "Answers on scope, pricing, timelines, tools, security and what happens after an Orvyan Tech automation goes live.",
        "faq.html",
        extra=extra,
    )
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / FAQ</p>
  <h1>Frequently asked questions</h1>
  <p>If your question is not here, WhatsApp is usually faster than email.</p>
</div></section>

<section><div class="wrap" style="max-width:820px">{items}</div></section>

{cta_band("Still deciding?", "Send the messy version of your process. We will tell you what is worth automating first.")}
"""
    write("faq.html", h + FOOT)


# --------------------------------------------------------------- contact
def page_contact():
    h = head(
        "Contact | Orvyan Tech",
        "Book a free consultation with Orvyan Tech. Tell us what you want automated and we reply within 24 hours.",
        "contact.html",
    )
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / Contact</p>
  <h1>Book a free consultation</h1>
  <p>Thirty minutes, no obligation. Tell us the task that keeps repeating and we will tell you whether automation is worth it.</p>
</div></section>

<section style="padding-top:0"><div class="wrap hero-grid">
  <form class="form-shell reveal" action="{FORM}" method="post">
    <div class="row2">
      <div class="field"><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="row2">
      <div class="field"><label for="company">Business name</label><input id="company" name="company" type="text" autocomplete="organization"></div>
      <div class="field"><label for="interest">What do you need?</label>
        <select id="interest" name="interest">
          <option>AI agent</option><option>Voice agent</option><option>WhatsApp automation</option>
          <option>Workflow automation</option><option>Lead generation</option><option>Not sure yet</option>
        </select>
      </div>
    </div>
    <div class="field"><label for="message">What would you like to automate?</label>
      <textarea id="message" name="message" required placeholder="A sentence or two is enough."></textarea></div>
    <input type="hidden" name="source" value="orvyantech.com">
    <button class="cta" type="submit" style="width:100%;justify-content:center">Send request {icon('arrow')}</button>
    <p class="form-note">We reply within 24 hours. If the form does not go through, email {EMAIL} or message us on WhatsApp.</p>
  </form>

  <div class="stack-30 reveal d2">
    <div class="card"><div class="ico">{icon('chat')}</div><h3>WhatsApp</h3>
      <p>Fastest route if you just have a question.</p>
      <a class="link-more" href="{WHATSAPP}" target="_blank" rel="noopener">Message us {icon('arrow')}</a></div>
    <div class="card"><div class="ico">{icon('mail')}</div><h3>Email</h3>
      <p>{EMAIL}</p>
      <a class="link-more" href="mailto:{EMAIL}">Write to us {icon('arrow')}</a></div>
    <div class="card"><div class="ico">{icon('clock')}</div><h3>Response time</h3>
      <p>Within 24 hours, Monday to Saturday. Based in India, working remote-first.</p></div>
  </div>
</div></section>
"""
    write("contact.html", h + FOOT)


# ------------------------------------------------------- legal pages
def page_legal(slug, title, body):
    h = head(f"{title} | Orvyan Tech", f"{title} for Orvyan Tech.", slug)
    paras = "".join(f"<p>{p}</p>" for p in body)
    h += f"""
<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> / {title}</p>
  <h1>{title}</h1>
  <div style="color:#9aa3ad;max-width:760px">{paras}</div>
</div></section>
"""
    write(slug, h + FOOT)


def page_privacy():
    raw = pathlib.Path(__file__).parent.joinpath("content/privacy.html").read_text(encoding="utf-8")
    write("privacy-policy.html", head("Privacy policy | Orvyan Tech",
        "How Orvyan Tech collects, uses and protects the information you share when you contact us.",
        "/privacy-policy.html") + '<main id="main"><div class="wrap"><article class="doc legal">' + raw + '</article></div>' + FOOT)


def page_terms():
    raw = pathlib.Path(__file__).parent.joinpath("content/terms.html").read_text(encoding="utf-8")
    write("terms-of-service.html", head("Terms of service | Orvyan Tech",
        "The terms that cover use of the Orvyan Tech website and the early stages of any engagement.",
        "/terms-of-service.html") + '<main id="main"><div class="wrap"><article class="doc legal">' + raw + '</article></div>' + FOOT)


SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">
  <url><loc>https://www.orvyantech.com/</loc><priority>1.0</priority></url>
  <url><loc>https://www.orvyantech.com/services.html</loc><priority>0.9</priority></url>
  <url><loc>https://www.orvyantech.com/how-it-works.html</loc><priority>0.8</priority></url>
  <url><loc>https://www.orvyantech.com/industries.html</loc><priority>0.7</priority></url>
  <url><loc>https://www.orvyantech.com/pricing.html</loc><priority>0.9</priority></url>
  <url><loc>https://www.orvyantech.com/faq.html</loc><priority>0.7</priority></url>
  <url><loc>https://www.orvyantech.com/contact.html</loc><priority>0.8</priority></url>
  <url><loc>https://www.orvyantech.com/privacy-policy.html</loc><priority>0.3</priority></url>
  <url><loc>https://www.orvyantech.com/terms-of-service.html</loc><priority>0.3</priority></url>
</urlset>
""".replace("http://www.sitemap.org/schemas/sitemap/0.9", "http://www.sitemaps.org/schemas/sitemap/0.9")

ORG_SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Orvyan Tech",
  "url": "https://www.orvyantech.com/",
  "email": "orvyan.ai@gmail.com",
  "telephone": "+91-79729-28086",
  "description": "AI agents, voice agents, WhatsApp bots and n8n workflow automation for businesses, creators and individuals.",
  "areaServed": "Worldwide",
  "address": { "@type": "PostalAddress", "addressCountry": "IN" }
}
</script>
"""


if __name__ == "__main__":
    page_index(); page_services(); page_how(); page_industries()
    page_pricing(); page_faq(); page_contact(); page_privacy(); page_terms()
    (OUT / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://www.orvyantech.com/sitemap.xml\n", encoding="utf-8")
    (OUT / "_redirects").write_text("/*    /index.html   200\n", encoding="utf-8")

    # inject organisation schema into index
    idx = OUT / "index.html"
    txt = idx.read_text(encoding="utf-8")
    if "ProfessionalService" not in txt:
        txt = txt.replace("</head>", ORG_SCHEMA + "</head>")
        idx.write_text(txt, encoding="utf-8")

    print("pages:", sorted(p.name for p in OUT.glob("*.html")))
