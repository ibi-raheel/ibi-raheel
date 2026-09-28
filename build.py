"""Build the GitHub profile README: a hero banner and uniform project cards as
SVG, in the ibiraheel.com visual language (near-black panels, lime accent)."""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

BG, PANEL, LINE = "#0b0c10", "#111318", "#23262f"
FG, MUTED, DIM, LIME = "#ecedf1", "#a3a9b6", "#7d8494", "#c8f560"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def text_width(s, size):
    w = 0.0
    for ch in s:
        if ch in "il.,:;'|!1 ()":
            w += 0.30
        elif ch in "mwMW@":
            w += 0.86
        elif ch.isupper():
            w += 0.66
        elif ch.isdigit():
            w += 0.57
        else:
            w += 0.52
    return w * size


def wrap(s, size, width, max_lines):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if text_width(trial, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    if len(lines) > max_lines:
        raise ValueError(f"too long for {max_lines} lines: {s!r}")
    return lines


def t(x, y, s, size, fill, weight=400, family=SANS, anchor="start", spacing=0, extra=""):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{escape(s)}</text>')


def banner():
    W, H = 1280, 420
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Muhammad Ibrahim Raheel. 16 AI agents shipped.">',
         "<defs>",
         '<pattern id="dots" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="#ffffff" fill-opacity=".07"/></pattern>',
         f'<radialGradient id="glow" cx="18%" cy="30%" r="55%"><stop offset="0" stop-color="{LIME}" stop-opacity=".16"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/></radialGradient>',
         f'<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
         "<style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 2.4s ease-in-out infinite}</style>",
         "</defs>",
         f'<rect width="{W}" height="{H}" rx="28" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" rx="28" fill="url(#dots)"/>',
         f'<rect width="{W}" height="{H}" rx="28" fill="url(#glow)"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="27" fill="none" stroke="#1c1f27" stroke-width="2"/>']

    p.append(t(56, 70, "MUHAMMAD IBRAHIM RAHEEL", 15, DIM, 500, MONO, spacing=3.5))
    p.append(f'<rect x="360" y="57" width="1.5" height="16" fill="{LINE}"/>')
    p.append(f'<circle class="pulse" cx="384" cy="65" r="4.5" fill="{LIME}"/>')
    p.append(t(398, 70, "BUILDING IN PUBLIC · 2026", 15, DIM, 500, MONO, spacing=3.5))

    p.append(t(44, 300, "16", 236, LIME, 700, SANS, spacing=-12, extra=' filter="url(#soft)"'))
    p.append(t(336, 206, "AI agents", 58, FG, 600, SANS, spacing=-1.5))
    p.append(t(336, 270, "shipped", 58, FG, 600, SANS, spacing=-1.5))
    p.append(t(56, 370, "6× HACKATHON WINNER  ·  FOUNDER, SLATE CRE  ·  DREXEL '26", 14, MUTED, 500, MONO, spacing=2.2))

    x0, w = 676, 548
    tag = "Voice agents that answer real phones, autonomous systems that run on a schedule, and products built end to end with agentic workflows."
    for i, line in enumerate(wrap(tag, 22, w, 3)):
        p.append(t(x0, 146 + i * 33, line, 22, MUTED, 400))

    top, th = 268, 104
    p.append(f'<rect x="{x0}" y="{top}" width="{w}" height="{th}" rx="16" fill="{LINE}"/>')
    tiles = [("VOICE", "AGENTS", "4"), ("AUTONOMOUS", "AGENTS", "7"), ("AGENT-BUILT", "PRODUCTS", "5")]
    tw = (w - 2) / 3
    for i, (a, b, v) in enumerate(tiles):
        tx = x0 + i * (tw + 1)
        rx = ' rx="16"' if i in (0, 2) else ""
        p.append(f'<rect x="{tx + (1 if i == 0 else 0):.1f}" y="{top + 1}" width="{tw - (1 if i != 1 else 0):.1f}" height="{th - 2}"{rx} fill="#12141a"/>')
        if i == 0:
            p.append(f'<rect x="{tx + tw - 16:.1f}" y="{top + 1}" width="16" height="{th - 2}" fill="#12141a"/>')
        if i == 2:
            p.append(f'<rect x="{tx:.1f}" y="{top + 1}" width="16" height="{th - 2}" fill="#12141a"/>')
        p.append(t(tx + 22, top + 30, a, 12, DIM, 500, MONO, spacing=2.2))
        p.append(t(tx + 22, top + 47, b, 12, DIM, 500, MONO, spacing=2.2))
        p.append(t(tx + 22, top + 86, v, 32, FG, 500, MONO))
    p.append("</svg>")
    open(os.path.join(OUT, "banner.svg"), "w").write("\n".join(p))


CARDS = [
    ("vault", "01", "AI AGENT", "SEP 2026", "GalaxyGate Track winner: 2,746 messages in, 94 tokens out",
     "for anyone re-explaining the same project to every AI tool", "Vault Librarian",
     "Memory that follows you across every model and agent"),
    ("ai-receptionist-v2", "02", "VOICE AGENT", "MAR 2026", "Every call answered, every lead captured",
     "for Rapid Restore, a water-damage restoration company in Philadelphia", "Emotion-aware AI dispatcher",
     "Hears how the caller feels, adapts its voice, captures the lead"),
    ("aria-os", "03", "AI AGENT", "APR–MAY 2026", "139 personalised outreach messages sent, 174 people tracked",
     "for one operator running five agents on a schedule", "Aria OS",
     "No framework, no database: markdown files are the state"),
    ("leaseiq", "04", "AI AGENT", "MAY 2026", "$15,538 a year found in two real leases",
     "for retail tenants and the brokers who represent them", "LeaseIQ",
     "A forensic audit of what the tenant should not be paying"),
    ("caferadar", "05", "AI AGENT", "MAR–APR 2026", "1,911 products and 6 commodity indexes tracked",
     "for a café owner buying from three suppliers", "CafeRadar",
     "Nightly supplier scrapers plus commodity indexes"),
    ("arcadia", "06", "AI PLATFORM", "APR–MAY 2026", "MVP shipped in six phases, then eight more",
     "for creators who want a world, not a Discord", "Arcadia",
     "A 2.5D multiplayer world with an AI scribe that writes courses"),
]


def card(slug, n, cat, date, head, who, name, tag):
    W, H = 800, 470
    pad, inner = 52, 800 - 104
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(name)}: {escape(head)}">',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="26" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>',
         f'<path d="M22 50V22h28M{W-22} {H-50}v28h-28" fill="none" stroke="{LIME}" stroke-opacity=".6" stroke-width="2.5" stroke-linecap="round"/>']
    p.append(t(pad, 78, n, 18, LIME, 600, MONO, spacing=2))
    p.append(t(pad + 44, 78, cat, 16, DIM, 500, MONO, spacing=3))
    p.append(t(W - pad, 78, date, 16, DIM, 500, MONO, anchor="end", spacing=3))
    y = 152
    for line in wrap(head, 40, inner, 3):
        p.append(t(pad, y, line, 40, FG, 650, SANS, spacing=-0.8))
        y += 49
    y += 2
    for line in wrap(who, 24, inner, 2):
        p.append(t(pad, y, line, 24, MUTED, 400))
        y += 32
    p.append(f'<rect x="{pad}" y="356" width="{inner}" height="1.5" fill="{LINE}"/>')
    p.append(t(pad, 400, name, 26, FG, 600))
    p.append(t(pad, 434, tag, 21, DIM, 400))
    p.append(t(W - pad, 414, "→", 32, LIME, 500, anchor="end"))
    p.append("</svg>")
    open(os.path.join(OUT, f"card-{slug}.svg"), "w").write("\n".join(p))


if __name__ == "__main__":
    banner()
    for c in CARDS:
        card(*c)
    print("built", 1 + len(CARDS), "svgs")
