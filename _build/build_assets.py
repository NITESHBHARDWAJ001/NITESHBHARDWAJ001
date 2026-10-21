"""Generates the SVG artwork used by the profile README (dark theme, matched to GitHub dark).

Run:  python _build/build_assets.py   (from the github-profile folder)
Edit the DATA sections below, re-run, commit the files in assets/.
GitHub renders SVG inside <img>, so no web fonts or scripts: system font stacks only.
The live GitHub numbers are produced separately by _build/fetch_stats.py (runs in a GitHub Action).
"""
import os
import textwrap
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

BG, PANEL, PANEL2, INK, MUTED, LINE = "#0d1117", "#161b22", "#1c2330", "#e6edf3", "#8b949e", "#30363d"
CYAN, CORAL, GOLD, VIOLET, MINT = "#2ee6d6", "#ff6b6b", "#ffd93d", "#a78bfa", "#7ee787"
TRACK = {"platforms": ("PLATFORMS", CYAN), "ai": ("AI & DATA", VIOLET), "tools": ("TOOLS", GOLD), "community": ("COMMUNITY", CORAL)}

D = "'Segoe UI', 'SF Pro Display', -apple-system, Roboto, Helvetica, Arial, sans-serif"
M = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
B = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

GLOW = '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
SOFT = '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'


def e(s):
    return escape(str(s))


def save(name, w, h, body, defs=""):
    """Dark card with a faint grid and two soft colour washes, like a panel on GitHub dark."""
    bg = (
        f'<defs>{GLOW}{SOFT}'
        f'<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{LINE}" stroke-width="0.6" opacity="0.45"/></pattern>'
        f'<radialGradient id="wa" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(0 0) scale({w * 0.55} {h * 1.2})"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="wb" cx="1" cy="1" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({w} {h}) scale({w * 0.5} {h * 1.1})"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f"{defs}</defs>"
        f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#grid)"/>'
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#wa)"/>'
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#wb)"/>'
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
        f'{bg}{body}<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/></svg>'
    )
    with open(os.path.join(OUT, name), "w", encoding="utf8") as f:
        f.write(svg)
    print("wrote", name)


def barcode(x, y, w, h, seed, color=INK):
    hv, bars, pos = 7, [], 0
    for i in range(46):
        hv = (hv * 31 + ord(seed[i % len(seed)]) + i) % 9973
        wd = 1 + hv % 3
        if i % 2 == 0:
            bars.append((pos, wd))
        pos += wd
    k = w / pos
    return "".join(f'<rect x="{x + p * k:.2f}" y="{y}" width="{wd * k:.2f}" height="{h}" fill="{color}"/>' for p, wd in bars)


def ticket_path(w, h, px, r=14, n=13):
    return (
        f"M{r},0 H{px - n} A{n},{n} 0 0 0 {px + n},0 H{w - r} Q{w},0 {w},{r} V{h - r} Q{w},{h} {w - r},{h} "
        f"H{px + n} A{n},{n} 0 0 0 {px - n},{h} H{r} Q0,{h} 0,{h - r} V{r} Q0,0 {r},0 Z"
    )


def chips(x, y, items, color=MUTED, maxw=10**6, size=11):
    out, cx = "", x
    cw = size * 0.62
    for s in items:
        w = len(s) * cw + 20
        if cx + w - x > maxw:
            break
        out += f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity="0.08" stroke="{color}" stroke-width="1.2" opacity="0.95"/>'
        out += f'<text x="{cx + w / 2:.1f}" y="{y + 15}" text-anchor="middle" font-family="{M}" font-size="{size}" fill="{color}">{e(s)}</text>'
        cx += w + 7
    return out


def lines(x, y, text, width, size, fill, family=B, lh=1.4, maxlines=3, weight="400"):
    out = ""
    for i, ln in enumerate(textwrap.wrap(text, width)[:maxlines]):
        out += f'<text x="{x}" y="{y + i * size * lh:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}">{e(ln)}</text>'
    return out


def dash(x1, y1, x2, y2, color=LINE, sw=1.6, dur=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-dasharray="6 7"><animate attributeName="stroke-dashoffset" from="0" to="-26" dur="{dur}s" repeatCount="indefinite"/></line>'


# ------------------------------------------------------------------ banner
def banner():
    W, H, PX = 1280, 500, 990
    p = ticket_path(W - 40, H - 40, PX - 20)
    roles = ["full-stack apps", "hiring platforms", "event systems", "data pipelines", "things that scale"]
    n = len(roles)
    cyc = ""
    for i, r in enumerate(roles):
        a, b = i / n, (i + 1) / n
        kt = f"0;{a:.3f};{a + 0.02:.3f};{b - 0.02:.3f};{b:.3f};1"
        cyc += (
            f'<text x="214" y="396" font-family="{M}" font-size="17" font-weight="700" fill="{CYAN}" opacity="0">{e(r)}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{n * 2.4}s" repeatCount="indefinite"/></text>'
        )
    sx = PX + (W - 20 - PX) / 2
    body = f"""
<g transform="translate(24,24)">
  <path d="{p}" fill="{PANEL}" stroke="{CYAN}" stroke-width="2" filter="url(#soft)"/>
  <path d="{p}" fill="{PANEL}" fill-opacity="0.6" stroke="{CYAN}" stroke-width="2"/>
  {dash(PX - 20, 16, PX - 20, H - 56, CYAN, 2, 1.6)}
</g>
<g opacity="0.9"><rect x="0" y="40" width="170" height="{H - 80}" fill="{CYAN}" opacity="0.07"><animate attributeName="x" from="-200" to="{W}" dur="5.5s" repeatCount="indefinite"/></rect></g>
<text x="60" y="84" font-family="{M}" font-size="14" letter-spacing="3" fill="{CYAN}">THE FULL-STACK SESSIONS  ·  EDITION 2026</text>
<g transform="translate(700,60)">
  <rect x="0" y="0" width="236" height="30" rx="15" fill="{CORAL}" filter="url(#soft)"/>
  <circle cx="18" cy="15" r="5" fill="{BG}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/><animate attributeName="r" values="5;3.4;5" dur="1.4s" repeatCount="indefinite"/></circle>
  <text x="32" y="20" font-family="{M}" font-size="12" font-weight="700" letter-spacing="1.6" fill="{BG}">NOW PLAYING · SITE GURU</text>
</g>
<text x="58" y="208" font-family="{D}" font-size="108" font-weight="800" fill="{INK}" letter-spacing="-4">Nitesh</text>
<text x="58" y="312" font-family="{D}" font-size="108" font-weight="800" fill="{CYAN}" letter-spacing="-4" filter="url(#glow)">Sharma</text>
<rect x="62" y="328" width="0" height="5" rx="2.5" fill="{CORAL}"><animate attributeName="width" from="0" to="420" dur="1.4s" begin="0.3s" fill="freeze" calcMode="spline" keySplines="0.3 0.9 0.4 1" keyTimes="0;1"/></rect>
<text x="60" y="366" font-family="{D}" font-size="23" fill="{INK}">Software for real events, real hiring and real hospitals.</text>
<text x="60" y="396" font-family="{M}" font-size="13" letter-spacing="1" fill="{MUTED}">NOW WORKING ON</text>
{cyc}
{dash(52, 414, PX - 52, 414, LINE, 1, 3)}
"""
    cells = [("DATE", "Since 2023"), ("VENUE", "Remote · India"), ("TRACKS", "Platforms · AI · Tools"), ("ENTRY", "Always open")]
    for i, (k, v) in enumerate(cells):
        x = 60 + [0, 180, 380, 660][i]
        body += f'<text x="{x}" y="438" font-family="{M}" font-size="10.5" letter-spacing="1.6" fill="{MUTED}">{k}</text>'
        body += f'<text x="{x}" y="456" font-family="{B}" font-size="15" font-weight="700" fill="{INK}">{e(v)}</text>'
    body += f"""
<text x="{sx}" y="84" text-anchor="middle" font-family="{M}" font-size="13" letter-spacing="3" fill="{MUTED}">ADMIT ONE</text>
<text x="{sx}" y="206" text-anchor="middle" font-family="{D}" font-size="124" font-weight="800" fill="{CORAL}" filter="url(#glow)">01</text>
<rect x="{sx - 62}" y="228" width="124" height="26" rx="13" fill="none" stroke="{CYAN}" stroke-width="1.6"/>
<text x="{sx}" y="246" text-anchor="middle" font-family="{M}" font-size="11.5" letter-spacing="2" fill="{CYAN}">ALL ACCESS</text>
{barcode(sx - 100, 284, 200, 96, "NITESH SHARMA", INK)}
<text x="{sx}" y="412" text-anchor="middle" font-family="{M}" font-size="12" letter-spacing="2" fill="{MUTED}">NS-2026-0001</text>
<text x="{sx}" y="436" text-anchor="middle" font-family="{M}" font-size="10.5" letter-spacing="1.4" fill="{MUTED}">B.TECH · IIT MADRAS</text>
"""
    save("banner.svg", W, H, body)


# ------------------------------------------------------------------ section headers
def section(name, no, label, title, sub, col=CYAN):
    W, H = 1280, 150
    body = f"""
<text x="40" y="52" font-family="{M}" font-size="14" letter-spacing="3" fill="{col}">{e(no)}  ·  {e(label.upper())}</text>
<text x="38" y="108" font-family="{D}" font-size="54" font-weight="800" fill="{INK}" letter-spacing="-1.5">{e(title)}</text>
<text x="{W - 40}" y="108" text-anchor="end" font-family="{B}" font-size="17" fill="{MUTED}">{e(sub)}</text>
{dash(40, 132, W - 40, 132, col, 1.6, 2)}
<circle cx="40" cy="132" r="5" fill="{col}" filter="url(#soft)"/>
"""
    save(name, W, H, body)


# ------------------------------------------------------------------ static stats (about me, not from GitHub)
def stats():
    W, H = 1280, 150
    items = [("28", "projects built", CYAN), ("11", "live demos", CORAL), ("3", "internships", GOLD), ("4", "hackathon podiums", VIOLET), ("176+", "LeetCode solved", MINT)]
    cw = (W - 80) / len(items)
    body = ""
    for i, (n, l, c) in enumerate(items):
        x = 40 + i * cw
        if i:
            body += f'<line x1="{x}" y1="34" x2="{x}" y2="{H - 34}" stroke="{LINE}" stroke-dasharray="4 5"/>'
        body += f'<text x="{x + 28}" y="86" font-family="{D}" font-size="56" font-weight="800" fill="{c}" letter-spacing="-2" filter="url(#soft)">{n}</text>'
        body += f'<text x="{x + 30}" y="116" font-family="{M}" font-size="13" letter-spacing="1.4" fill="{MUTED}">{e(l.upper())}</text>'
    save("stats.svg", W, H, body)


# ------------------------------------------------------------------ about: code editor + terminal
def about():
    W, H = 1280, 470
    L = 40
    code = [
        [("const ", CORAL), ("nitesh", CYAN), (" = {", INK)],
        [("  now", "#79c0ff"), (": ", INK), ('"Full Stack Developer Intern @ Site Guru"', "#a5d6ff"), (",", INK)],
        [("  since", "#79c0ff"), (": ", INK), ('"15 Jun 2026"', "#a5d6ff"), (",", INK)],
        [("  before", "#79c0ff"), (": [", INK), ('"Qgenii EdTech"', "#a5d6ff"), (", ", INK), ('"Bharati Expoads"', "#a5d6ff"), ("],", INK)],
        [("  studying", "#79c0ff"), (": [", INK), ('"B.Tech CSE, SIET"', "#a5d6ff"), (", ", INK), ('"BS Data Science, IIT Madras"', "#a5d6ff"), ("],", INK)],
        [("  completed", "#79c0ff"), (": ", INK), ('"BSc Programming & Data Science (May 2026)"', "#a5d6ff"), (",", INK)],
        [("  builds", "#79c0ff"), (": [", INK), ('"events"', "#a5d6ff"), (", ", INK), ('"hiring"', "#a5d6ff"), (", ", INK), ('"multi-tenant SaaS"', "#a5d6ff"), (", ", INK), ('"real-time video"', "#a5d6ff"), ("],", INK)],
        [("  openTo", "#79c0ff"), (": ", INK), ('"full-time roles + freelance projects"', "#a5d6ff"), (",", INK)],
        [("};", INK)],
    ]
    body = f"""
<rect x="{L}" y="30" width="800" height="{H - 60}" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>
<rect x="{L}" y="30" width="800" height="42" rx="12" fill="{PANEL2}"/><rect x="{L}" y="58" width="800" height="14" fill="{PANEL2}"/>
<circle cx="{L + 24}" cy="51" r="6.5" fill="#ff5f56"/><circle cx="{L + 46}" cy="51" r="6.5" fill="#ffbd2e"/><circle cx="{L + 68}" cy="51" r="6.5" fill="#27c93f"/>
<rect x="{L + 100}" y="40" width="130" height="32" rx="6" fill="{PANEL}"/><rect x="{L + 100}" y="69" width="130" height="3" fill="{CYAN}"/>
<text x="{L + 165}" y="61" text-anchor="middle" font-family="{M}" font-size="13" fill="{INK}">nitesh.ts</text>
"""
    y0 = 112
    for i, row in enumerate(code):
        y = y0 + i * 34
        body += f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{0.5 + i * 0.45:.2f}s" fill="freeze"/>'
        body += f'<text x="{L + 22}" y="{y}" font-family="{M}" font-size="15" fill="{MUTED}" opacity="0.6">{i + 1}</text>'
        x = L + 64
        spans = "".join(f'<tspan fill="{c}">{e(t)}</tspan>' for t, c in row)
        body += f'<text x="{x}" y="{y}" font-family="{M}" font-size="17" xml:space="preserve">{spans}</text></g>'
    last_y = y0 + (len(code) - 1) * 34
    body += f'<rect x="{L + 64 + 22}" y="{last_y - 16}" width="9" height="20" fill="{CYAN}" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.5;0.52;1" dur="1.1s" begin="4.8s" repeatCount="indefinite"/></rect>'
    TX, TW = 870, 370
    body += f"""
<rect x="{TX}" y="30" width="{TW}" height="{H - 60}" rx="12" fill="#0a0e14" stroke="{LINE}" stroke-width="1.5"/>
<rect x="{TX}" y="30" width="{TW}" height="42" rx="12" fill="{PANEL2}"/><rect x="{TX}" y="58" width="{TW}" height="14" fill="{PANEL2}"/>
<text x="{TX + 20}" y="57" font-family="{M}" font-size="13" fill="{MUTED}">terminal</text>
"""
    term = [
        ("$ ", "node nitesh.ts", INK),
        ("> ", "shipping   Event Karwalo  ✓", MINT),
        ("> ", "shipping   TalentSphere   ✓", MINT),
        ("> ", "building   Site Guru SaaS", CYAN),
        ("> ", "learning   Data Science", VIOLET),
        ("> ", "status     open to work", GOLD),
    ]
    for i, (pre, t, c) in enumerate(term):
        y = 112 + i * 34
        body += f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{5.2 + i * 0.6:.2f}s" fill="freeze"/>'
        body += f'<text x="{TX + 22}" y="{y}" font-family="{M}" font-size="14.5" xml:space="preserve"><tspan fill="{CORAL}">{e(pre)}</tspan><tspan fill="{c}">{e(t)}</tspan></text></g>'
    body += f'<rect x="{TX + 22}" y="{112 + 6 * 34 - 16}" width="9" height="18" fill="{GOLD}" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.5;0.52;1" dur="1.1s" begin="9s" repeatCount="indefinite"/></rect>'
    save("about.svg", W, H, body)


# ------------------------------------------------------------------ schedule (experience)
def schedule():
    rows = [
        ("15 Jun 2026 — Now", "Stage 03", "Site Guru", "Full Stack Developer Intern", True,
         "Remote. Backend of a live SaaS product plus client work: REST APIs, auth, real-time video calling, live streaming, chat, forums and Razorpay. Designed and built the TalentSphere hiring platform from the first commit.",
         ["Node.js", "Express", "MySQL / MariaDB", "Vue.js", "WebRTC", "Socket.IO", "Razorpay"]),
        ("Jul 2025 — Apr 2026", "Stage 02", "Qgenii EdTech", "MERN Stack Developer Intern", False,
         "Part of a five-developer team building an EdTech and job-portal platform. Shipped the Contest Engine, Course Flow, Hiring Flow and Admin Dashboard on my own, and cut API response times by about 40%.",
         ["MongoDB", "Express", "React", "Node.js", "Socket.IO", "Docker"]),
        ("Jul 2025 — Dec 2025", "Stage 01", "Bharati Expoads", "Full Stack Developer Intern", False,
         "Built a CRM and business-automation platform that moved the whole company off MS Teams: hierarchical RBAC, automated reports, about 65% less manual work and a zero-downtime migration.",
         ["PostgreSQL", "Express", "React", "Node.js", "JWT"]),
    ]
    RH, W = 224, 1280
    H = RH * len(rows) + 30
    body = ""
    for i, (when, stage, co, role, live, desc, stack) in enumerate(rows):
        y = 20 + i * RH
        body += dash(40, y, W - 40, y, LINE, 1.4, 3)
        body += f'<text x="40" y="{y + 54}" font-family="{D}" font-size="25" font-weight="800" fill="{INK}">{e(when)}</text>'
        body += f'<text x="40" y="{y + 82}" font-family="{M}" font-size="12" letter-spacing="2" fill="{MUTED}">{stage.upper()}</text>'
        if live:
            body += f'<rect x="40" y="{y + 100}" width="170" height="28" rx="14" fill="{CORAL}" filter="url(#soft)"/><circle cx="58" cy="{y + 114}" r="5" fill="{BG}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="72" y="{y + 119}" font-family="{M}" font-size="11.5" font-weight="700" letter-spacing="1.6" fill="{BG}">NOW PLAYING</text>'
        body += f'<text x="360" y="{y + 58}" font-family="{D}" font-size="38" font-weight="800" fill="{INK}" letter-spacing="-1">{e(co)}</text>'
        body += f'<text x="360" y="{y + 84}" font-family="{B}" font-size="16" fill="{CYAN}" font-weight="600">{e(role)}</text>'
        body += lines(360, y + 114, desc, 105, 15, MUTED, lh=1.45, maxlines=3)
        body += chips(360, y + 178, stack, color=CYAN if live else MUTED, maxw=860)
    save("schedule.svg", W, H, body)


# ------------------------------------------------------------------ project tickets
PROJECTS = [
    ("event-karwalo", "Event Karwalo", "EVENT OPERATING SYSTEM", "platforms", "Plan. Organize. Manage. Done. Forms, offline QR check-in, a public page builder, teams and judging, plus a vendor marketplace with bidding, quotes and payments.", ["React 19", "TypeScript", "Prisma", "PostgreSQL"]),
    ("talentsphere", "TalentSphere", "HIRING PLATFORM · SITE GURU", "platforms", "AI-powered talent platform for candidates, employers, agencies and institutions: job matching, ATS, campus drives, WebRTC video interviews and offers.", ["Vue.js", "Node.js", "WebRTC", "MariaDB"]),
    ("ai-hiring-flow", "AI Hiring Flow", "RECRUITMENT + AI INTERVIEWER", "ai", "An AI interviewer plans topics from the job and resume, follows up on weak answers and writes a structured hire report. Judge0 coding tests and proctoring.", ["React", "TypeScript", "Prisma", "Socket.IO"]),
    ("sunrise-hop", "Sunrise HOP", "AI-ENABLED HEALTH SYSTEM", "ai", "Hospital platform on a lifetime patient timeline. Offline risk engine with three on-device models, Hindi voice input, OCR, and a chatbot that calls a real calculation.", ["React 19", "Express", "Groq", "Docker"]),
    ("assetflow", "AssetFlow ERP", "MULTI-TENANT SAAS", "platforms", "Asset and resource management with QR-tagged assets, approval chains, bookings and audits. The tenant id always comes from the JWT, never the client.", ["React", "TypeScript", "Prisma", "PostgreSQL"]),
    ("seat-allocation", "Exam Seat Allocator", "IN USE AT COLLEGE", "tools", "Seat-by-seat exam plans and fair invigilation rosters, built for my college and used there. Deterministic engine with an independent validator and 102 tests.", ["TypeScript", "React", "Express", "IndexedDB"]),
    ("portlify", "Portlify", "AI PORTFOLIO BUILDER", "ai", "Build, share and discover portfolios. An LLM drafts the content, a drag-and-drop editor shapes it, and one click deploys it to Vercel.", ["React", "Node.js", "MongoDB", "Groq"]),
    ("autofill", "Smart Autofill", "BROWSER EXTENSION", "tools", "Privacy-first Manifest V3 extension: fills web forms from a profile kept on your device, with in-browser OCR, resume parsing and encrypted backups.", ["WXT", "React 19", "TypeScript", "Dexie"]),
    ("image-quality", "Image Quality Scorer", "COMPUTER VISION", "ai", "Scores an image 0 to 100 and flags blur, exposure and noise using a locally trained model. No external vision API; the README reports its weak spots.", ["FastAPI", "OpenCV", "scikit-learn", "React"]),
    ("leadflow", "LeadFlow CRM", "LEAD MANAGEMENT", "platforms", "Admins see the whole pipeline, employees only their own leads, with an immutable audit trail on every status change. Swagger docs, tests and Docker.", ["React", "TypeScript", "Prisma", "Docker"]),
    ("siet-admin", "SIET Hackathon Admin", "COLLEGE HACKATHON PORTAL", "community", "Control room for SIET's internal hackathon: registrations, problem statements, a 100-point judging rubric with live ranking, Sheets sync and Excel export.", ["React", "Express", "Sheets API", "ExcelJS"]),
    ("codecrafter", "CodeCrafter", "DAILY CHALLENGE PORTAL", "community", "Daily coding contest for the club. Solutions are verified against real LeetCode submissions, with streak rules, a leaderboard and QR-verified PDF certificates.", ["TypeScript", "Express", "Supabase", "Zod"]),
]


def tickets():
    W, H, PX = 620, 262, 478
    for i, (pid, title, kick, cat, desc, stack) in enumerate(PROJECTS):
        label, col = TRACK[cat]
        p = ticket_path(W - 24, H - 24, PX - 12, r=12, n=12)
        sx = PX - 12 + (W - 24 - (PX - 12)) / 2
        num = f"{i + 1:02d}"
        body = f"""
<g transform="translate(12,12)">
  <path d="{p}" fill="{PANEL}" stroke="{col}" stroke-width="1.8" stroke-opacity="0.85"/>
  <path d="{p}" fill="none" stroke="{col}" stroke-width="3" stroke-opacity="0.18" filter="url(#soft)"/>
  {dash(PX - 12, 14, PX - 12, H - 38, col, 1.8, 1.8)}
  <rect x="0" y="12" width="5" height="{H - 48}" fill="{col}" rx="2.5" filter="url(#soft)"/>
</g>
<text x="40" y="52" font-family="{M}" font-size="11" letter-spacing="1.8" fill="{col}">{e(kick)}</text>
<text x="40" y="94" font-family="{D}" font-size="{33 if len(title) < 17 else 28}" font-weight="800" fill="{INK}" letter-spacing="-0.8">{e(title)}</text>
{lines(40, 124, desc, 56, 13.2, MUTED, maxlines=4, lh=1.42)}
{chips(40, 206, stack, color=col, maxw=420, size=10.5)}
<text x="{sx + 12}" y="52" text-anchor="middle" font-family="{M}" font-size="10" letter-spacing="2.4" fill="{MUTED}">ADMIT ONE</text>
<text x="{sx + 12}" y="118" text-anchor="middle" font-family="{D}" font-size="60" font-weight="800" fill="{col}" filter="url(#soft)">{num}</text>
<rect x="{sx + 12 - 50}" y="132" width="100" height="22" rx="11" fill="none" stroke="{col}" stroke-width="1.4"/>
<text x="{sx + 12}" y="147" text-anchor="middle" font-family="{M}" font-size="9.5" letter-spacing="1.6" fill="{col}">{e(label)}</text>
{barcode(sx + 12 - 52, 170, 104, 42, pid, INK)}
<text x="{sx + 12}" y="230" text-anchor="middle" font-family="{M}" font-size="9" letter-spacing="1.6" fill="{MUTED}">SESSION {num}</text>
"""
        save(f"ticket-{pid}.svg", W, H, body)


# ------------------------------------------------------------------ sponsors wall
def stack():
    W = 1280
    title = ["TypeScript", "Node.js", "React", "PostgreSQL"]
    gold = ["Vue.js", "Express", "Prisma", "MongoDB", "Python", "Docker"]
    silver = ["Socket.IO", "WebRTC", "WebSockets", "MySQL", "MariaDB", "FastAPI", "Flask", "Tailwind", "Zustand", "TanStack Query", "Zod", "JWT", "Razorpay", "Groq", "OpenAI API", "Claude API", "scikit-learn", "OpenCV", "Capacitor", "Vitest", "Git", "Supabase", "IndexedDB", "C++"]
    cols = [CYAN, CORAL, GOLD, VIOLET]
    body = f'<text x="40" y="38" font-family="{M}" font-size="12" letter-spacing="3" fill="{MUTED}">TITLE PARTNERS</text><line x1="190" y1="34" x2="{W - 40}" y2="34" stroke="{LINE}" stroke-dasharray="4 6"/>'
    tw = (W - 80 - 3 * 14) / 4
    for i, s in enumerate(title):
        x = 40 + i * (tw + 14)
        c = cols[i]
        body += f'<rect x="{x}" y="54" width="{tw}" height="96" fill="{PANEL}" stroke="{c}" stroke-width="1.6" stroke-opacity="0.8" rx="8"/><rect x="{x}" y="54" width="{tw}" height="5" fill="{c}" rx="2" filter="url(#soft)"/>'
        body += f'<text x="{x + tw / 2}" y="112" text-anchor="middle" font-family="{D}" font-size="30" font-weight="800" fill="{INK}" letter-spacing="-0.6">{e(s)}</text>'
    body += f'<text x="40" y="190" font-family="{M}" font-size="12" letter-spacing="3" fill="{MUTED}">GOLD PARTNERS</text><line x1="190" y1="186" x2="{W - 40}" y2="186" stroke="{LINE}" stroke-dasharray="4 6"/>'
    gw = (W - 80 - 5 * 12) / 6
    for i, s in enumerate(gold):
        x = 40 + i * (gw + 12)
        c = cols[i % 4]
        body += f'<rect x="{x}" y="206" width="{gw}" height="64" fill="{PANEL}" stroke="{LINE}" stroke-width="1.4" rx="8"/><rect x="{x}" y="214" width="4" height="48" fill="{c}" rx="2"/>'
        body += f'<text x="{x + gw / 2 + 2}" y="245" text-anchor="middle" font-family="{B}" font-size="19" font-weight="700" fill="{INK}">{e(s)}</text>'
    body += f'<text x="40" y="308" font-family="{M}" font-size="12" letter-spacing="3" fill="{MUTED}">SUPPORTING PARTNERS</text><line x1="250" y1="304" x2="{W - 40}" y2="304" stroke="{LINE}" stroke-dasharray="4 6"/>'
    sw = (W - 80 - 7 * 10) / 8
    for i, s in enumerate(silver):
        r, c = divmod(i, 8)
        x = 40 + c * (sw + 10)
        y = 324 + r * 52
        body += f'<rect x="{x}" y="{y}" width="{sw}" height="42" fill="{PANEL}" stroke="{LINE}" stroke-width="1.2" rx="6"/>'
        body += f'<text x="{x + sw / 2}" y="{y + 26}" text-anchor="middle" font-family="{M}" font-size="13" fill="{INK}">{e(s)}</text>'
    save("stack.svg", W, 324 + 3 * 52 + 12, body)


# ------------------------------------------------------------------ awards
def awards():
    items = [
        ("gold", "Winner, MERN Marketers Hackathon", "CDAC DELHI · 1ST PLACE", "A production-ready full-stack build in under 24 hours."),
        ("bronze", "3rd Prize, SIC Project Hackathon", "PODIUM", "A solution built around real social impact."),
        ("rank", "Top 20, Hackelipse", "100+ TEAMS", "National ranking in a high-intensity hackathon."),
        ("rank", "Top 50, Odoo Hackathon 2025", "850+ TEAMS", "Placed among the top fifty teams globally."),
        ("exam", "GATE 2026 qualified", "NATIONAL EXAM", "Core CS and engineering fundamentals."),
        ("exam", "NDA written exam, three times", "NATIONAL EXAM", "Cleared on three consecutive attempts."),
        ("code", "GSSoC and Winter of Code", "OPEN SOURCE", "Contributor in two community programmes."),
        ("code", "HackerRank 4-star, DSA", "90TH PERCENTILE", "Plus 176+ LeetCode problems solved."),
        ("exam", "Samsung Innovation Campus", "AI & ML CERTIFICATION", "Applied AI and machine-learning programme."),
    ]
    colors = {"gold": GOLD, "bronze": "#e08a4f", "rank": MINT, "exam": CORAL, "code": VIOLET}
    W, cw, ch = 1280, 398, 104
    H = 3 * (ch + 16) + 20
    body = ""
    for i, (k, t, m, d) in enumerate(items):
        r, c = divmod(i, 3)
        x, y = 40 + c * (cw + 14), 10 + r * (ch + 16)
        col = colors[k]
        body += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{PANEL}" stroke="{LINE}" stroke-width="1.4" rx="10"/>'
        body += f'<rect x="{x}" y="{y + 14}" width="4" height="{ch - 28}" fill="{col}" rx="2" filter="url(#soft)"/>'
        body += f'<circle cx="{x + 44}" cy="{y + 52}" r="24" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="2"/>'
        sym = {"gold": "★", "bronze": "3", "rank": "↗", "exam": "✓", "code": "{ }"}[k]
        body += f'<text x="{x + 44}" y="{y + 60}" text-anchor="middle" font-family="{D}" font-size="22" font-weight="800" fill="{col}">{sym}</text>'
        body += f'<text x="{x + 82}" y="{y + 34}" font-family="{B}" font-size="15.5" font-weight="700" fill="{INK}">{e(t)}</text>'
        body += f'<text x="{x + 82}" y="{y + 54}" font-family="{M}" font-size="10.5" letter-spacing="1.4" fill="{col}">{e(m)}</text>'
        body += lines(x + 82, y + 76, d, 46, 12.6, MUTED, maxlines=2, lh=1.35)
    save("awards.svg", W, H, body)


# ------------------------------------------------------------------ footer
def footer():
    W, H = 1280, 200
    body = f"""
<text x="40" y="104" font-family="{D}" font-size="54" font-weight="800" fill="{INK}" letter-spacing="-1.5">See you at the next <tspan fill="{CYAN}" filter="url(#glow)">edition.</tspan></text>
<text x="40" y="146" font-family="{M}" font-size="13" letter-spacing="2.4" fill="{MUTED}">THANKS FOR ATTENDING  ·  YAMUNANAGAR, INDIA  ·  OPEN TO FULL-TIME ROLES AND FREELANCE WORK</text>
{barcode(W - 340, 56, 300, 90, "SEE YOU NEXT EDITION", INK)}
<text x="{W - 190}" y="172" text-anchor="middle" font-family="{M}" font-size="11" letter-spacing="3" fill="{MUTED}">NS-2026-0001</text>
{dash(40, 24, W - 40, 24, CYAN, 1.4, 3)}
"""
    save("footer.svg", W, H, body)


def build_all():
    banner()
    stats()
    section("h-keynote.svg", "01", "Keynote", "What I do", "the talk in one paragraph", CYAN)
    section("h-schedule.svg", "02", "Schedule", "Where I've worked", "three internships, back to back", CORAL)
    section("h-sessions.svg", "03", "Sessions", "Things I've built", "tap a ticket to open the demo", GOLD)
    section("h-sponsors.svg", "04", "Sponsors", "Powered by", "the tools this programme runs on", VIOLET)
    section("h-awards.svg", "05", "Awards night", "Wins & milestones", "hackathons, exams, open source", MINT)
    section("h-checkin.svg", "06", "Check-in desk", "Let's talk", "full-time roles and freelance work", CYAN)
    about()
    schedule()
    tickets()
    stack()
    awards()
    footer()


if __name__ == "__main__":
    build_all()
