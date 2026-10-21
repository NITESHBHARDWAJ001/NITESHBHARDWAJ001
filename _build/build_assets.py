"""Generates the SVG artwork used by the profile README.

Run:  python _build/build_assets.py   (from the github-profile folder)
Edit the DATA section below, re-run, commit the files in assets/.
GitHub renders SVG inside <img>, so no web fonts or scripts: system font stacks only.
"""
import os
import textwrap
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

BG, PANEL, INK, MUTED, LINE = "#f1eadc", "#f8f3e8", "#1d1a15", "#5f584b", "#cfc5af"
RED, GREEN, INDIGO, GOLD = "#c9431e", "#1f4d3a", "#22418f", "#b07d12"
TRACK = {"platforms": ("PLATFORMS", RED), "ai": ("AI & DATA", INDIGO), "tools": ("TOOLS", GREEN), "community": ("COMMUNITY", GOLD)}

D = "Georgia, 'Times New Roman', serif"
M = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
B = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def e(s):
    return escape(str(s))


def save(name, w, h, body, defs=""):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
        f"<defs>{defs}</defs>"
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" fill="url(#dots)"/>'
        f"{body}</svg>"
    )
    svg = svg.replace("<defs>", f'<defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.9" fill="{LINE}" opacity="0.55"/></pattern>', 1)
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
        out += f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="none" stroke="{color}" stroke-width="1.2" opacity="0.9"/>'
        out += f'<text x="{cx + w / 2:.1f}" y="{y + 15}" text-anchor="middle" font-family="{M}" font-size="{size}" fill="{color}">{e(s)}</text>'
        cx += w + 7
    return out


def lines(x, y, text, width, size, fill, family=B, lh=1.4, maxlines=3, weight="400"):
    out = ""
    for i, ln in enumerate(textwrap.wrap(text, width)[:maxlines]):
        out += f'<text x="{x}" y="{y + i * size * lh:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}">{e(ln)}</text>'
    return out


# ------------------------------------------------------------------ banner
def banner():
    W, H, PX = 1280, 500, 990
    p = ticket_path(W - 40, H - 40, PX - 20)
    roles = ["full-stack apps", "hiring platforms", "event systems", "data pipelines", "things that scale"]
    cyc = ""
    n = len(roles)
    for i, r in enumerate(roles):
        a, b = i / n, (i + 1) / n
        kt = f"0;{a:.3f};{a + 0.02:.3f};{b - 0.02:.3f};{b:.3f};1"
        cyc += (
            f'<text x="214" y="396" font-family="{M}" font-size="17" font-weight="700" fill="{RED}" opacity="0">{e(r)}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{n * 2.4}s" repeatCount="indefinite"/></text>'
        )
    stub_x = PX + (W - 20 - PX) / 2
    body = f"""
<g transform="translate(24,24)">
  <path d="{p}" fill="{INK}" transform="translate(7,7)" opacity="0.14"/>
  <path d="{p}" fill="{PANEL}" stroke="{INK}" stroke-width="2.2"/>
  <line x1="{PX - 20}" y1="16" x2="{PX - 20}" y2="{H - 56}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 7"><animate attributeName="stroke-dashoffset" from="0" to="-26" dur="1.6s" repeatCount="indefinite"/></line>
  <rect x="0" y="0" width="{PX - 33}" height="9" fill="{RED}" opacity="0.0"/>
</g>
<text x="60" y="84" font-family="{M}" font-size="14" letter-spacing="3" fill="{RED}">THE FULL-STACK SESSIONS  ·  EDITION 2026</text>
<g transform="translate(700,60)">
  <rect x="0" y="0" width="236" height="30" rx="15" fill="{RED}"/>
  <circle cx="18" cy="15" r="5" fill="{PANEL}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/><animate attributeName="r" values="5;3.4;5" dur="1.4s" repeatCount="indefinite"/></circle>
  <text x="32" y="20" font-family="{M}" font-size="12" letter-spacing="1.6" fill="{PANEL}">NOW PLAYING · SITE GURU</text>
</g>
<text x="58" y="208" font-family="{D}" font-size="112" font-weight="700" fill="{INK}" letter-spacing="-3">Nitesh</text>
<text x="58" y="312" font-family="{D}" font-size="112" font-weight="700" fill="{RED}" letter-spacing="-3">Sharma</text>
<rect x="62" y="326" width="0" height="6" fill="{RED}"><animate attributeName="width" from="0" to="420" dur="1.4s" begin="0.3s" fill="freeze" calcMode="spline" keySplines="0.3 0.9 0.4 1" keyTimes="0;1"/></rect>
<text x="60" y="364" font-family="{D}" font-size="23" font-style="italic" fill="{INK}">Software for real events, real hiring and real hospitals.</text>
<text x="60" y="396" font-family="{M}" font-size="13" letter-spacing="1" fill="{MUTED}">NOW WORKING ON</text>
{cyc}
<line x1="52" y1="414" x2="{PX - 52}" y2="414" stroke="{LINE}" stroke-dasharray="4 6"/>
"""
    # info cells
    cells = [("DATE", "Since 2023"), ("VENUE", "Remote · India"), ("TRACKS", "Platforms · AI · Tools"), ("ENTRY", "Always open")]
    for i, (k, v) in enumerate(cells):
        x = 60 + [0, 180, 380, 660][i]
        body += f'<text x="{x}" y="434" font-family="{M}" font-size="10.5" letter-spacing="1.6" fill="{MUTED}">{k}</text>'
        body += f'<text x="{x}" y="452" font-family="{B}" font-size="15" font-weight="700" fill="{INK}">{e(v)}</text>'
    # stub
    body += f"""
<text x="{stub_x}" y="84" text-anchor="middle" font-family="{M}" font-size="13" letter-spacing="3" fill="{MUTED}">ADMIT ONE</text>
<text x="{stub_x}" y="206" text-anchor="middle" font-family="{D}" font-size="126" font-weight="700" fill="{RED}">01</text>
<rect x="{stub_x - 62}" y="228" width="124" height="26" rx="13" fill="none" stroke="{INK}" stroke-width="1.6"/>
<text x="{stub_x}" y="246" text-anchor="middle" font-family="{M}" font-size="11.5" letter-spacing="2" fill="{INK}">ALL ACCESS</text>
{barcode(stub_x - 100, 284, 200, 96, "NITESH SHARMA")}
<text x="{stub_x}" y="412" text-anchor="middle" font-family="{M}" font-size="12" letter-spacing="2" fill="{MUTED}">NS-2026-0001</text>
<text x="{stub_x}" y="436" text-anchor="middle" font-family="{M}" font-size="10.5" letter-spacing="1.4" fill="{MUTED}">B.TECH · IIT MADRAS</text>
"""
    save("banner.svg", W, H, body)


# ------------------------------------------------------------------ section headers
def section(name, no, label, title, sub):
    W, H = 1280, 150
    body = f"""
<text x="40" y="52" font-family="{M}" font-size="14" letter-spacing="3" fill="{RED}">{e(no)}  ·  {e(label.upper())}</text>
<text x="38" y="108" font-family="{D}" font-size="58" font-weight="700" fill="{INK}" letter-spacing="-1.5">{e(title)}</text>
<text x="{W - 40}" y="108" text-anchor="end" font-family="{B}" font-size="17" fill="{MUTED}">{e(sub)}</text>
<line x1="40" y1="132" x2="{W - 40}" y2="132" stroke="{INK}" stroke-width="1.6" stroke-dasharray="6 7"><animate attributeName="stroke-dashoffset" from="0" to="-26" dur="2s" repeatCount="indefinite"/></line>
<circle cx="40" cy="132" r="5" fill="{RED}"/>
"""
    save(name, W, H, body)


# ------------------------------------------------------------------ stats
def stats():
    W, H = 1280, 150
    items = [("28", "projects built"), ("11", "live demos"), ("3", "internships"), ("4", "hackathon podiums"), ("176+", "LeetCode solved")]
    cw = (W - 80) / len(items)
    body = f'<line x1="40" y1="20" x2="{W - 40}" y2="20" stroke="{INK}" stroke-width="1.6"/><line x1="40" y1="{H - 20}" x2="{W - 40}" y2="{H - 20}" stroke="{INK}" stroke-width="1.6"/>'
    for i, (n, l) in enumerate(items):
        x = 40 + i * cw
        if i:
            body += f'<line x1="{x}" y1="38" x2="{x}" y2="{H - 38}" stroke="{LINE}" stroke-dasharray="4 5"/>'
        body += f'<text x="{x + 28}" y="88" font-family="{D}" font-size="58" font-weight="700" fill="{RED}" letter-spacing="-2">{n}</text>'
        body += f'<text x="{x + 30}" y="116" font-family="{M}" font-size="13" letter-spacing="1.4" fill="{MUTED}">{e(l.upper())}</text>'
    save("stats.svg", W, H, body)


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
        body += f'<line x1="40" y1="{y}" x2="{W - 40}" y2="{y}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="6 7"/>'
        body += f'<text x="40" y="{y + 52}" font-family="{D}" font-size="27" font-weight="700" fill="{INK}">{e(when)}</text>'
        body += f'<text x="40" y="{y + 80}" font-family="{M}" font-size="12" letter-spacing="2" fill="{MUTED}">{stage.upper()}</text>'
        if live:
            body += f'<rect x="40" y="{y + 98}" width="170" height="28" rx="14" fill="{RED}"/><circle cx="58" cy="{y + 112}" r="5" fill="{PANEL}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="72" y="{y + 117}" font-family="{M}" font-size="11.5" letter-spacing="1.6" fill="{PANEL}">NOW PLAYING</text>'
        body += f'<text x="360" y="{y + 56}" font-family="{D}" font-size="40" font-weight="700" fill="{INK}" letter-spacing="-1">{e(co)}</text>'
        body += f'<text x="360" y="{y + 82}" font-family="{B}" font-size="16" fill="{RED}" font-weight="600">{e(role)}</text>'
        body += lines(360, y + 112, desc, 105, 15, MUTED, lh=1.45, maxlines=3)
        body += chips(360, y + 176, stack, maxw=860)
    body += f'<line x1="40" y1="{H - 10}" x2="{W - 40}" y2="{H - 10}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="6 7"/>'
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
  <path d="{p}" fill="{INK}" transform="translate(5,5)" opacity="0.14"/>
  <path d="{p}" fill="{PANEL}" stroke="{INK}" stroke-width="2"/>
  <line x1="{PX - 12}" y1="14" x2="{PX - 12}" y2="{H - 38}" stroke="{INK}" stroke-width="1.8" stroke-dasharray="5 6"><animate attributeName="stroke-dashoffset" from="0" to="-22" dur="1.8s" repeatCount="indefinite"/></line>
  <rect x="0" y="0" width="7" height="{H - 24}" fill="{col}" rx="3"/>
</g>
<text x="40" y="52" font-family="{M}" font-size="11" letter-spacing="1.8" fill="{col}">{e(kick)}</text>
<text x="40" y="94" font-family="{D}" font-size="{34 if len(title) < 17 else 29}" font-weight="700" fill="{INK}" letter-spacing="-0.8">{e(title)}</text>
{lines(40, 124, desc, 56, 13.2, MUTED, maxlines=4, lh=1.42)}
{chips(40, 206, stack, color=col, maxw=420, size=10.5)}
<text x="{sx + 12}" y="52" text-anchor="middle" font-family="{M}" font-size="10" letter-spacing="2.4" fill="{MUTED}">ADMIT ONE</text>
<text x="{sx + 12}" y="118" text-anchor="middle" font-family="{D}" font-size="62" font-weight="700" fill="{col}">{num}</text>
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
    cols = [RED, GREEN, INDIGO, GOLD]
    body = f'<text x="40" y="38" font-family="{M}" font-size="12" letter-spacing="3" fill="{MUTED}">TITLE PARTNERS</text><line x1="190" y1="34" x2="{W - 40}" y2="34" stroke="{LINE}" stroke-dasharray="4 6"/>'
    tw = (W - 80 - 3 * 14) / 4
    for i, s in enumerate(title):
        x = 40 + i * (tw + 14)
        body += f'<rect x="{x}" y="54" width="{tw}" height="96" fill="{PANEL}" stroke="{INK}" stroke-width="1.8"/><rect x="{x}" y="54" width="{tw}" height="7" fill="{cols[i]}"/>'
        body += f'<text x="{x + tw / 2}" y="112" text-anchor="middle" font-family="{D}" font-size="31" font-weight="700" fill="{INK}" letter-spacing="-0.6">{e(s)}</text>'
    body += f'<text x="40" y="190" font-family="{M}" font-size="12" letter-spacing="3" fill="{MUTED}">GOLD PARTNERS</text><line x1="190" y1="186" x2="{W - 40}" y2="186" stroke="{LINE}" stroke-dasharray="4 6"/>'
    gw = (W - 80 - 5 * 12) / 6
    for i, s in enumerate(gold):
        x = 40 + i * (gw + 12)
        body += f'<rect x="{x}" y="206" width="{gw}" height="64" fill="{PANEL}" stroke="{INK}" stroke-width="1.5"/><rect x="{x}" y="206" width="5" height="64" fill="{cols[i % 4]}"/>'
        body += f'<text x="{x + gw / 2 + 2}" y="245" text-anchor="middle" font-family="{B}" font-size="19" font-weight="700" fill="{INK}">{e(s)}</text>'
    body += f'<text x="40" y="308" font-family="{M}" font-size="12" letter-spacing="3" fill="{MUTED}">SUPPORTING PARTNERS</text><line x1="250" y1="304" x2="{W - 40}" y2="304" stroke="{LINE}" stroke-dasharray="4 6"/>'
    sw = (W - 80 - 7 * 10) / 8
    for i, s in enumerate(silver):
        r, c = divmod(i, 8)
        x = 40 + c * (sw + 10)
        y = 324 + r * 52
        body += f'<rect x="{x}" y="{y}" width="{sw}" height="42" fill="{PANEL}" stroke="{INK}" stroke-width="1.2"/>'
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
    colors = {"gold": "#d9a520", "bronze": "#b8733a", "rank": GREEN, "exam": RED, "code": INDIGO}
    W, cw, ch = 1280, 398, 104
    H = 3 * (ch + 16) + 20
    body = ""
    for i, (k, t, m, d) in enumerate(items):
        r, c = divmod(i, 3)
        x, y = 40 + c * (cw + 14), 10 + r * (ch + 16)
        col = colors[k]
        body += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{PANEL}" stroke="{INK}" stroke-width="1.6"/>'
        body += f'<path d="M{x + 30} {y + 14}l10 16 10-16" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        body += f'<circle cx="{x + 40}" cy="{y + 60}" r="22" fill="{col}" stroke="{INK}" stroke-width="2.2"/>'
        sym = {"gold": "★", "bronze": "3", "rank": "↗", "exam": "✓", "code": "{ }"}[k]
        body += f'<text x="{x + 40}" y="{y + 68}" text-anchor="middle" font-family="{D}" font-size="22" font-weight="700" fill="{PANEL}">{sym}</text>'
        body += f'<text x="{x + 78}" y="{y + 34}" font-family="{B}" font-size="15.5" font-weight="700" fill="{INK}">{e(t)}</text>'
        body += f'<text x="{x + 78}" y="{y + 54}" font-family="{M}" font-size="10.5" letter-spacing="1.4" fill="{RED}">{e(m)}</text>'
        body += lines(x + 78, y + 76, d, 46, 12.6, MUTED, maxlines=2, lh=1.35)
    save("awards.svg", W, H, body)


# ------------------------------------------------------------------ footer
def footer():
    W, H = 1280, 200
    body = f"""
<line x1="40" y1="24" x2="{W - 40}" y2="24" stroke="{INK}" stroke-width="1.6"/>
<text x="40" y="100" font-family="{D}" font-size="56" font-weight="700" fill="{INK}" letter-spacing="-1.5">See you at the next <tspan fill="{RED}" font-style="italic">edition.</tspan></text>
<text x="40" y="140" font-family="{M}" font-size="13" letter-spacing="2.4" fill="{MUTED}">THANKS FOR ATTENDING  ·  YAMUNANAGAR, INDIA  ·  OPEN TO FULL-TIME ROLES AND FREELANCE WORK</text>
{barcode(W - 340, 56, 300, 90, "SEE YOU NEXT EDITION")}
<text x="{W - 190}" y="170" text-anchor="middle" font-family="{M}" font-size="11" letter-spacing="3" fill="{MUTED}">NS-2026-0001</text>
<line x1="40" y1="{H - 20}" x2="{W - 40}" y2="{H - 20}" stroke="{INK}" stroke-width="1.6"/>
"""
    save("footer.svg", W, H, body)


if __name__ == "__main__":
    banner()
    stats()
    section("h-keynote.svg", "01", "Keynote", "What I do", "the talk in one paragraph")
    section("h-schedule.svg", "02", "Schedule", "Where I've worked", "three internships, back to back")
    section("h-sessions.svg", "03", "Sessions", "Things I've built", "tap a ticket to open the demo")
    section("h-sponsors.svg", "04", "Sponsors", "Powered by", "the tools this programme runs on")
    section("h-awards.svg", "05", "Awards night", "Wins & milestones", "hackathons, exams, open source")
    section("h-checkin.svg", "06", "Check-in desk", "Let's talk", "full-time roles and freelance work")
    schedule()
    tickets()
    stack()
    awards()
    footer()
