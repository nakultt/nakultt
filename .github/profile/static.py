"""Build the static profile images (hero, link buttons, project cards, recognition, stack).

Edit the copy below, then regenerate and commit assets/:

    python .github/profile/static.py
"""

from __future__ import annotations

import math

from common import CAP, EASE_IN_OUT, EASE_OUT, ROOT, THEMES, Doc, f, measure, onoff, pct, rrect

ASSETS = ROOT / "assets"
LINE = 'fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'

# ---------------------------------------------------------------- copy

NAME = "Nakul T"
COMPANY = "Ragworks.AI"
LEAD = "Backend AI developer building"
ROLLING = ["agentic AI systems.", "GraphRAG memory engines.", "edge vision for road safety.", "MCP-powered pipelines."]
META = [("pin", "Coimbatore, India"), ("cap", "B.Tech AI & DS · KPR IET"), ("trophy", "6× first place")]
NODES = ["LLM", "MCP", "RAG", "Memory", "Tools", "Vision"]

LINKS = {  # slug: (label, icon); the first one is the primary call to action
    "portfolio": ("Portfolio", "globe"),
    "linkedin": ("LinkedIn", "briefcase"),
    "leetcode": ("LeetCode", "code"),
    "kaggle": ("Kaggle", "chart"),
}

PROJECTS = [
    {"slug": "cortex", "name": "Cortex", "tag": "GraphRAG", "art": "graph",
     "desc": "Long-term memory for LLMs on a knowledge graph.",
     "metrics": [("150 ms", "retrieval, down from 1.2 s"), ("−25%", "LLM API spend")],
     "stack": "Neo4j · Qdrant · Groq · Kubernetes"},
    {"slug": "pacer", "name": "PACER", "tag": "Edge AI", "art": "road",
     "desc": "Real-time traffic-violation detection at the edge.",
     "metrics": [("30+ FPS", "YOLO26n on a Raspberry Pi"), ("−85%", "memory, ONNX to NCNN")],
     "stack": "YOLO26n · NCNN · FastAPI · Gemini Vision"},
    {"slug": "sosmesh", "name": "SOS Mesh", "tag": "Offline-first", "art": "mesh",
     "desc": "Disaster alerts relayed phone to phone, no internet.",
     "metrics": [("−45%", "network congestion"), ("Multi-hop", "BLE + Wi-Fi Direct relay")],
     "stack": "Kotlin · BLE · Wi-Fi Direct · MongoDB"},
    {"slug": "more", "name": "More on GitHub", "tag": "50+ repos", "art": "repos",
     "desc": "Agents, computer vision, full-stack and ML builds.",
     "cta": "Browse all repositories",
     "stack": "Python · TypeScript · Kotlin · Dart"},
]
REPOS = ["DriftSense", "VeriTransit", "GajaAlert", "crop-disease-detection", "locus", "facefinder",
         "FactChecker", "lifeline-core", "Catalyst", "FireSense", "MultiVision", "rabbitmq-gitops",
         "interviewer", "shoproute", "ClimateAct", "TrainRDR", "SmartServe", "Routy",
         "Shoty", "WFLOW", "Heart-Disease-Prediction", "ERP", "MoE", "AutoNotify"]

STATS = [("6", "First-place wins"), ("9", "Podium finishes"), ("3", "Finalist spots"),
         ("1", "Published patent"), ("200+", "LeetCode solved")]

STACK = [
    ("Languages", ["Python", "TypeScript", "Java", "C", "R", "MATLAB"]),
    ("GenAI", ["LangChain", "LangGraph", "LlamaIndex", "MCP", "RAG", "Hugging Face", "Ollama"]),
    ("ML & vision", ["TensorFlow", "OpenCV", "YOLO", "CNN", "LSTM"]),
    ("Backend & web", ["FastAPI", "Node.js", "Express", "React", "Next.js", "Tailwind CSS", "D3.js"]),
    ("Data", ["PostgreSQL", "MongoDB", "Redis", "MySQL", "Neo4j", "Qdrant", "ChromaDB"]),
    ("DevOps", ["Docker", "Kubernetes", "GitHub Actions", "Jenkins", "Linux", "DVC", "AWS"]),
]

# ---------------------------------------------------------------- icons

ICONS = {
    "pin": '<path d="M0-7a5.5 5.5 0 0 1 5.5 5.5c0 4.2-5.5 9.5-5.5 9.5s-5.5-5.3-5.5-9.5A5.5 5.5 0 0 1 0-7z"/>'
           '<circle cy="-1.5" r="1.7"/>',
    "cap": '<path d="M-8.5-1.5 0-5.5l8.5 4L0 2.5z"/><path d="M-4.8.6v3.3c2.8 1.9 6.8 1.9 9.6 0V.6"/>',
    "trophy": '<path d="M-4.5-6.5h9v4.3a4.5 4.5 0 0 1-9 0z"/>'
              '<path d="M-4.5-4.8h-2.8a3 3 0 0 0 3.2 3.8M4.5-4.8h2.8a3 3 0 0 1-3.2 3.8M0 2.3v3.4M-3.2 6.5h6.4"/>',
    "globe": '<circle r="7.2"/><path d="M-7.2 0h14.4M0-7.2c2.8 2.3 2.8 12.1 0 14.4M0-7.2c-2.8 2.3-2.8 12.1 0 14.4"/>',
    "briefcase": '<rect x="-7.5" y="-4.5" width="15" height="11" rx="2.2"/>'
                 '<path d="M-3-4.5V-6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 3-6v1.5M-7.5.8h15"/>',
    "code": '<path d="m-3.6-5.4-4.4 5.4 4.4 5.4M3.6-5.4 8 0l-4.4 5.4M1.4-7.4-1.4 7.4"/>',
    "chart": '<path d="M-7 7h14M-4.5 3.5V0M0 3.5V-6M4.5 3.5v-6"/>',
    "arrow": '<path d="M-3.6 3.6 3.6-3.6M-2.2-3.6h5.8v5.8"/>',
    "repo": '<path d="M-4-5.5h7.5v9.5H-3a1 1 0 0 0-1 1zm0 10.5a1 1 0 0 1 1-1h6.5v1.5H-3a1 1 0 0 1-1-1z"/>',
}
SPARKLE = "M0-14C1.5-4.7 4.7-1.5 14 0 4.7 1.5 1.5 4.7 0 14-1.5 4.7-4.7 1.5-14 0-4.7-1.5-1.5-4.7 0-14Z"


def icon(name: str, x: float, y: float, color: str, scale: float = 1) -> str:
    s = f" scale({scale:g})" if scale != 1 else ""
    return f'<g transform="translate({f(x)} {f(y)}){s}" stroke="{color}" {LINE}>{ICONS[name]}</g>'


def frame(t: dict, w: int, h: int, r: int = 16) -> str:
    """Card surface: page-coloured fill and a hairline border."""
    return rrect(.5, .5, w - 1, h - 1, r - .5, fill=t["canvas"], stroke=t["border"])


def grid(d: Doc, t: dict, w: float, h: float, cx: float, cy: float, radius: float, step: int = 40,
         gid: str = "grid") -> str:
    """Blueprint grid that fades out radially around (cx, cy)."""
    d.defs.append(
        f'<pattern id="{gid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse" '
        f'x="{f(cx % step)}" y="{f(cy % step)}"><path d="M{step} 0H0V{step}" fill="none" '
        f'stroke="{t["grid"]}" stroke-opacity="{t["gridAlpha"]}"/></pattern>'
        f'<radialGradient id="{gid}Fade" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" r="{f(radius)}">'
        f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="{gid}Mask"><rect width="{f(w)}" height="{f(h)}" fill="url(#{gid}Fade)"/></mask>'
    )
    return f'<rect width="{f(w)}" height="{f(h)}" fill="url(#{gid})" mask="url(#{gid}Mask)"/>'


def chip(d: Doc, label: str, x: float, cy: float, *, fg: str, bg: str, line: str | None = None,
         size: float = 11, anchor: str = "start") -> str:
    """Small mono label in a rounded rectangle; x is its left edge (or right edge if anchor=end)."""
    w = measure(label, size, 500, "mono") + 14
    if anchor == "end":
        x -= w
    return (rrect(x, cy - 10, w, 20, 5, fill=bg, stroke=line)
            + d.text(label, x + 7, cy + CAP * size / 2, size, 500, "mono", fill=fg))


# ---------------------------------------------------------------- hero

def hero(theme: str) -> Doc:
    t = THEMES[theme]
    W, H, X0 = 1200, 440, 72
    d = Doc(W, H, f"{NAME}, backend AI developer at {COMPANY}",
            f"{LEAD} {', '.join(p.rstrip('.') for p in ROLLING)}.")
    hub_x, hub_y = 912, 220
    d.css.append(
        f".rise{{animation:rise 1s {EASE_OUT} both}}@keyframes rise{{from{{opacity:0;transform:translateY(12px)}}}}"
        f".fade{{animation:fade 1.6s {EASE_OUT} .35s both}}@keyframes fade{{from{{opacity:0}}}}"
        ".ping{animation:ping 2.8s cubic-bezier(0,0,.2,1) infinite}"
        "@keyframes ping{0%{transform:scale(1);opacity:.6}70%,100%{transform:scale(2.6);opacity:0}}"
        ".spin{animation:spin 60s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
        ".pulse{stroke-dasharray:10 200;stroke-dashoffset:10;animation:pulse 6s infinite both}"
        f"@keyframes pulse{{0%{{stroke-dashoffset:10;animation-timing-function:{EASE_IN_OUT}}}11%,100%{{stroke-dashoffset:-100}}}}"
        ".lit{opacity:0;animation:lit 6s infinite both}"
        "@keyframes lit{0%,9%{opacity:0}13%{opacity:1}36%{opacity:1}46%,100%{opacity:0}}"
    )

    b = d.body
    b.append(frame(t, W, H))
    d.defs.append(f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    b.append(f'<g clip-path="url(#frame)" class="fade">{grid(d, t, W, H, hub_x, hub_y, 330)}</g>')

    # status pill: "Currently at Ragworks.AI"
    lead, size = "Currently at ", 16
    lead_w = measure(lead, size, 500)
    pill_w = 36 + lead_w + measure(COMPANY, size, 500) + 18
    b.append(f'<g class="rise" style="animation-delay:.05s">'
             + rrect(X0, 60, pill_w, 36, 18, fill=t["subtle"], stroke=t["border"])
             + f'<g transform="translate({X0 + 18} 78)" fill="{t["success"]}"><circle r="3.5" class="ping"/><circle r="3.5"/></g>'
             + d.text(lead, X0 + 34, 78 + CAP * size / 2, size, 500, fill=t["muted"])
             + d.text(COMPANY, X0 + 34 + lead_w, 78 + CAP * size / 2, size, 500, fill=t["fg"]) + "</g>")

    # name: display weight, tight tracking, a soft vertical tone
    size, base = 104, 210
    name = d.text(NAME, X0 - 5, base, size, 600, tracking=-.045, fill="#fff")
    d.defs.append(f'<linearGradient id="head" gradientUnits="userSpaceOnUse" x1="0" y1="{base - 76}" x2="0" y2="{base + 4}">'
                  f'<stop offset="0" stop-color="{t["headTop"]}"/><stop offset="1" stop-color="{t["headBottom"]}"/></linearGradient>'
                  f'<mask id="nameMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{name}</mask>')
    b.append(f'<g class="rise" style="animation-delay:.12s"><rect x="{X0 - 10}" y="{base - 90}" width="560" height="120" '
             f'fill="url(#head)" mask="url(#nameMask)"/></g>')

    # lead line + a phrase that rolls through what I build
    size, base, slot, lift = 30, 272, 2.8, 44
    total = slot * len(ROLLING)
    d.css.append(
        f".roll{{opacity:0;animation:roll {total:g}s infinite both}}.roll:first-child{{opacity:1}}"
        f"@keyframes roll{{0%{{opacity:0;transform:translateY({lift}px);animation-timing-function:{EASE_OUT}}}"
        f"{pct(.7, total)}{{opacity:1;transform:none}}"
        f"{pct(slot - .25, total)}{{opacity:1;transform:none;animation-timing-function:cubic-bezier(.7,0,.84,0)}}"
        f"{pct(slot + .2, total)},100%{{opacity:0;transform:translateY(-{lift}px)}}}}"
    )
    d.defs.append(f'<clipPath id="rollClip"><rect x="{X0 - 6}" y="{base + 9}" width="640" height="48"/></clipPath>')
    phrases = "".join(f'<g class="roll" style="animation-delay:{.6 + i * slot:g}s">'
                      f'{d.text(p, X0, base + 43, size, 500, tracking=-.015, fill=t["fg"])}</g>'
                      for i, p in enumerate(ROLLING))
    b.append(f'<g class="rise" style="animation-delay:.22s">{d.text(LEAD, X0, base, size, 400, tracking=-.015, fill=t["muted"])}'
             f'<g clip-path="url(#rollClip)">{phrases}</g></g>')

    # meta row
    x, items = X0, []
    for name_, label in META:
        items.append(icon(name_, x + 8, 382, t["faint"], 1.1) + d.text(label, x + 26, 388, 17, 400, fill=t["muted"]))
        x += 26 + measure(label, 17) + 34
    b.append(f'<g class="rise" style="animation-delay:.32s">{"".join(items)}</g>')

    # agent hub: a core that calls each tool in turn
    orbit = 148
    pts = [(orbit * math.cos(math.radians(-90 + 60 * i)), orbit * math.sin(math.radians(-90 + 60 * i)))
           for i in range(len(NODES))]
    hub = [f'<circle r="{orbit}" fill="none" stroke="{t["hair"]}"/>']
    for i, (px, py) in enumerate(pts):
        line = f"M0 0L{f(px)} {f(py)}"
        hub.append(f'<path d="{line}" stroke="{t["border"]}"/>'
                   f'<path d="{line}" pathLength="100" stroke="{t["accent"]}" stroke-width="2" stroke-linecap="round" '
                   f'class="pulse" style="animation-delay:{1.2 + i}s"/>')
    hub.append(f'<circle r="66" fill="none" stroke="{t["border"]}" stroke-dasharray="2 6" class="spin"/>'
               f'<circle r="48" fill="{t["canvas"]}" stroke="{t["hair"]}"/>'
               f'<circle r="34" fill="{t["fg"]}"/><path d="{SPARKLE}" fill="{t["canvas"]}"/>')
    for i, ((px, py), label) in enumerate(zip(pts, NODES)):
        w = 32 + measure(label, 15, 500, "mono") + 14
        x0, y0, ty = px - w / 2, py - 17, py + CAP * 7.5
        hub.append(rrect(x0, y0, w, 34, 9, fill=t["subtle"], stroke=t["border"])
                   + f'<circle cx="{f(x0 + 16)}" cy="{f(py)}" r="3.2" fill="{t["faint"]}"/>'
                   + d.text(label, x0 + 28, ty, 15, 500, "mono", fill=t["muted"])
                   + f'<g class="lit" style="animation-delay:{1.2 + i}s">'
                   + rrect(x0, y0, w, 34, 9, fill=t["subtle"], stroke=t["accent"])
                   + f'<circle cx="{f(x0 + 16)}" cy="{f(py)}" r="3.2" fill="{t["accent"]}"/>'
                   + d.text(label, x0 + 28, ty, 15, 500, "mono", fill=t["fg"]) + "</g>")
    b.append(f'<g transform="translate({hub_x} {hub_y})"><g class="fade">{"".join(hub)}</g></g>')
    return d


# ---------------------------------------------------------------- link buttons

def button(theme: str, slug: str) -> Doc:
    t = THEMES[theme]
    label, glyph = LINKS[slug]
    primary = slug == next(iter(LINKS))
    H, size = 40, 15
    tw = measure(label, size, 500)
    W = math.ceil(16 + 16 + 10 + tw + 12 + 10 + 16)
    bg, ink, line, soft = ((t["fg"], t["canvas"], t["fg"], t["canvas"]) if primary
                           else (t["subtle"], t["fg"], t["border"], t["muted"]))
    d = Doc(W, H, label)
    d.body += [rrect(.5, .5, W - 1, H - 1, 8, fill=bg, stroke=line),
               icon(glyph, 24, 20, soft),
               d.text(label, 42, 20 + CAP * size / 2, size, 500, fill=ink),
               icon("arrow", 42 + tw + 17, 20, soft)]
    return d


# ---------------------------------------------------------------- project cards

def art_graph(d: Doc, t: dict) -> str:
    """Cortex: a query walks the knowledge graph and comes back as a cache hit."""
    T = 6.0
    pos = {"q": (46, 80), "a": (128, 38), "b": (118, 118), "h": (196, 130), "c": (214, 70), "i": (262, 22),
           "d": (300, 108), "e": (348, 42), "f": (386, 94), "j": (444, 134), "g": (462, 62)}
    edges = ["qb", "ab", "ai", "bh", "bc", "hd", "ci", "ie", "de", "ef", "fj", "jg", "eg"]
    route = "qacdfg"
    out = []
    for u, v in edges:
        out.append(f'<path d="M{f(pos[u][0])} {f(pos[u][1])}L{f(pos[v][0])} {f(pos[v][1])}" stroke="{t["border"]}"/>')
    pts = [pos[k] for k in route]
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total_len, start, end = sum(seg), .6, 2.3
    poly = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
    for u, v in zip(route, route[1:]):
        out.append(f'<path d="M{f(pos[u][0])} {f(pos[u][1])}L{f(pos[v][0])} {f(pos[v][1])}" stroke="{t["border"]}"/>')
    d.css.append(f".route{{stroke-dasharray:100;animation:route {T:g}s linear infinite}}"
                 f"@keyframes route{{0%,{pct(start, T)}{{stroke-dashoffset:100;opacity:1}}{pct(end, T)}{{stroke-dashoffset:0}}"
                 f"{pct(4.7, T)}{{opacity:1}}{pct(5.2, T)},100%{{stroke-dashoffset:0;opacity:0}}}}")
    out.append(f'<path d="{poly}" pathLength="100" stroke="{t["accent"]}" stroke-width="2" stroke-linejoin="round" '
               f'stroke-linecap="round" fill="none" class="route"/>')
    acc = 0.0
    size = {"q": 7, "g": 7, "h": 4, "i": 4, "j": 4}
    for key, (x, y) in pos.items():
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{size.get(key, 5.5)}" fill="{t["subtle"]}" '
                   f'stroke="{t["muted"] if key in "qg" else t["faint"]}" stroke-width="1.5"/>')
    for i, key in enumerate(route):
        if i:
            acc += seg[i - 1]
        on = start + (end - start) * acc / total_len
        x, y = pos[key]
        d.css.append(onoff(f"n{i}", T, on - .05, 4.7, .25) + f".n{i}{{animation:n{i} {T:g}s infinite both}}")
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{size.get(key, 5.5)}" fill="{t["accent"]}" class="n{i}"/>')
    out.append(d.text("query", pos["q"][0], pos["q"][1] + 26, 11, 500, "mono", anchor="middle", fill=t["faint"]))
    d.css.append(onoff("hit", T, end + .05, 4.7, .3) + f".hit{{animation:hit {T:g}s infinite both}}")
    out.append(f'<g class="hit">{chip(d, "cache hit · 150 ms", pos["g"][0] + 26, pos["g"][1] - 34, fg=t["accent"], bg=t["canvas"], line=t["border"], anchor="end")}</g>')
    return "".join(out)


def art_road(d: Doc, t: dict) -> str:
    """PACER: an edge camera locks on to a vehicle and its plate."""
    W, H, hy = 504, 152, 26
    vx = 252
    out = [f'<path d="M36 {H}L{vx - 8} {hy}M{W - 36} {H}L{vx + 8} {hy}M0 {hy}H{W}" stroke="{t["border"]}"/>',
           f'<path d="M{vx} {hy}V{H}" stroke="{t["faint"]}" stroke-width="2" class="lane"/>']
    d.css.append(".lane{stroke-dasharray:8 10;animation:lane .9s linear infinite}@keyframes lane{to{stroke-dashoffset:-18}}"
                 ".scan{animation:scan 3.6s cubic-bezier(.45,0,.55,1) infinite}"
                 f"@keyframes scan{{0%{{transform:translateY({hy}px);opacity:0}}12%{{opacity:.5}}88%{{opacity:.5}}"
                 f"100%{{transform:translateY({H}px);opacity:0}}}}"
                 ".rec{animation:rec 1.4s steps(1) infinite}@keyframes rec{50%{opacity:.25}}"
                 f".lock{{animation:lock 3.6s {EASE_OUT} infinite}}@keyframes lock{{0%{{transform:scale(1.12);opacity:0}}"
                 "14%{transform:scale(1);opacity:1}86%{opacity:1}100%{opacity:1}}")
    # car, rear view
    cx, base = 196, 130
    car = (f'<path d="M{cx - 34} {base - 40}l9-22h50l9 22" fill="{t["subtle"]}"/>'
           + rrect(cx - 48, base - 42, 96, 34, 9, fill=t["subtle"])
           + rrect(cx - 44, base - 9, 16, 9, 2.5, fill=t["muted"], stroke="none")
           + rrect(cx + 28, base - 9, 16, 9, 2.5, fill=t["muted"], stroke="none")
           + rrect(cx - 42, base - 34, 15, 6, 2, fill=t["danger"], stroke="none", fill_opacity=".85")
           + rrect(cx + 27, base - 34, 15, 6, 2, fill=t["danger"], stroke="none", fill_opacity=".85")
           + rrect(cx - 14, base - 23, 28, 10, 2, fill=t["canvas"]))
    out.append(f'<g stroke="{t["muted"]}" stroke-width="1.5" stroke-linejoin="round">{car}</g>')
    # detection: corner brackets around the car, a box on the plate, labels
    bx0, by0, bx1, by1 = cx - 58, base - 76, cx + 58, base + 4
    mx, my = (bx0 + bx1) / 2, (by0 + by1) / 2
    hw, hh, k = (bx1 - bx0) / 2, (by1 - by0) / 2, 12
    brackets = "".join(f"M{f(sx * hw)} {f(sy * (hh - k))}V{f(sy * hh)}H{f(sx * (hw - k))}"
                       for sx in (-1, 1) for sy in (-1, 1))
    out.append(f'<g transform="translate({f(mx)} {f(my)})"><g class="lock"><path d="{brackets}" stroke="{t["accent"]}" '
               f'stroke-width="2" fill="none" stroke-linecap="round"/>'
               f'{rrect(-17, base - 25 - my, 34, 14, 2.5, fill="none", stroke=t["accent"], stroke_width=1.5)}</g></g>')
    out.append(chip(d, "vehicle 0.97", bx0, by0 - 14, fg=t["canvas"], bg=t["accent"]))
    out.append(chip(d, "plate · OCR", cx + 64, base - 18, fg=t["accent"], bg=t["canvas"], line=t["border"]))
    # HUD
    out.append(f'<circle cx="22" cy="14" r="3.5" fill="{t["danger"]}" class="rec"/>'
               + d.text("REC", 32, 14 + CAP * 5.5, 11, 500, "mono", fill=t["muted"])
               + d.text("30 FPS · NCNN", W - 16, 14 + CAP * 5.5, 11, 500, "mono", anchor="end", fill=t["muted"]))
    out.append(f'<g class="scan"><rect x="0" y="-1" width="{W}" height="2" fill="{t["accent"]}" opacity=".7"/></g>')
    return "".join(out)


def art_mesh(d: Doc, t: dict) -> str:
    """SOS Mesh: an alert hops between phones until one of them reaches the internet."""
    T = 6.5
    phones = [(54, 98), (126, 44), (172, 116), (254, 70), (334, 120), (382, 52)]
    cloud = (458, 100)
    links = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    route = [0, 2, 3, 5]
    nodes = phones + [cloud]
    out = [f'<path d="M{f(phones[a][0])} {f(phones[a][1])}L{f(phones[b][0])} {f(phones[b][1])}" stroke="{t["border"]}"/>'
           for a, b in links]
    out.append(f'<path d="M{f(phones[5][0])} {f(phones[5][1])}L{f(cloud[0])} {f(cloud[1])}" stroke="{t["border"]}" '
               f'stroke-dasharray="3 4"/>')
    hops = list(zip(route, route[1:] + [6]))
    times = []
    for k, (a, b) in enumerate(hops):
        s = .7 + k * .55
        e = s + .45
        times.append(e)
        (x0, y0), (x1, y1) = nodes[a], nodes[b]
        d.css.append(f"@keyframes h{k}{{0%,{pct(s, T)}{{stroke-dashoffset:100;opacity:1}}{pct(e, T)}{{stroke-dashoffset:0}}"
                     f"{pct(5, T)}{{opacity:1}}{pct(5.5, T)},100%{{stroke-dashoffset:0;opacity:0}}}}"
                     f".h{k}{{stroke-dasharray:100;animation:h{k} {T:g}s infinite both}}")
        out.append(f'<path d="M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}" pathLength="100" stroke="{t["accent"]}" stroke-width="2" '
                   f'stroke-linecap="round" class="h{k}"/>')
    lit = {route[0]: .45, **{b: e for (_, b), e in zip(hops, times)}}
    for x, y in phones:
        out.append(rrect(x - 7.5, y - 12, 15, 24, 3.5, fill=t["subtle"], stroke=t["muted"], stroke_width=1.5)
                   + f'<path d="M{f(x - 2.5)} {f(y + 8)}h5" stroke="{t["muted"]}" stroke-width="1.5" stroke-linecap="round"/>')
    for i, on in lit.items():
        x, y = nodes[i]
        color = t["danger"] if i == route[0] else t["accent"]
        d.css.append(onoff(f"l{i}", T, on, 5, .2) + f".l{i}{{animation:l{i} {T:g}s infinite both}}"
                     f"@keyframes r{i}{{0%,{pct(on, T)}{{transform:scale(.6);opacity:0}}{pct(on + .05, T)}{{opacity:.7}}"
                     f"{pct(on + 1, T)},100%{{transform:scale(2.4);opacity:0}}}}.r{i}{{animation:r{i} {T:g}s infinite both}}")
        out.append(f'<g transform="translate({f(x)} {f(y)})"><circle r="13" fill="none" stroke="{color}" stroke-width="1.5" '
                   f'class="r{i}"/></g>')
        if i < len(phones):
            out.append(f'<g class="l{i}">' + rrect(x - 7.5, y - 12, 15, 24, 3.5, fill=t["subtle"], stroke=color, stroke_width=1.5)
                       + f'<path d="M{f(x - 2.5)} {f(y + 8)}h5" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/></g>')
    cloud_path = (f"M{f(cloud[0] - 14)} {f(cloud[1] + 9)}a7 7 0 0 1-.6-14 9.5 9.5 0 0 1 18.2-2.6A6.6 6.6 0 0 1 "
                  f"{f(cloud[0] + 14)} {f(cloud[1] + 9)}z")
    out.append(f'<path d="{cloud_path}" fill="{t["subtle"]}" stroke="{t["muted"]}" stroke-width="1.5" stroke-linejoin="round"/>'
               f'<path d="{cloud_path}" fill="{t["subtle"]}" stroke="{t["accent"]}" stroke-width="1.5" stroke-linejoin="round" class="l6"/>')
    out.append(chip(d, "SOS", phones[0][0] - 17, phones[0][1] - 30, fg=t["canvas"], bg=t["danger"]))
    out.append(d.text("offline", phones[0][0], phones[0][1] + 31, 11, 500, "mono", anchor="middle", fill=t["faint"]))
    d.css.append(onoff("ok", T, times[-1] + .05, 5, .3) + f".ok{{animation:ok {T:g}s infinite both}}")
    out.append(f'<g class="ok">{chip(d, "delivered", cloud[0] + 30, cloud[1] - 34, fg=t["accent"], bg=t["canvas"], line=t["border"], anchor="end")}</g>')
    return "".join(out)


def art_repos(d: Doc, t: dict) -> str:
    """More: a slow scroll through other repositories."""
    W, H, row = 504, 152, 26
    rows = math.ceil(len(REPOS) / 2)
    d.defs.append(f'<g id="repoIcon" fill="none" stroke="{t["faint"]}" stroke-width="1.3" stroke-linejoin="round">'
                  f'{ICONS["repo"]}</g>'
                  f'<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                  f'<stop offset=".25" stop-color="#fff"/><stop offset=".75" stop-color="#fff"/>'
                  f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                  f'<mask id="edgeMask"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>')
    d.css.append(f".scroll{{animation:scroll {rows * 2.2:g}s linear infinite}}"
                 f"@keyframes scroll{{to{{transform:translateY(-{rows * row}px)}}}}")
    items = []
    for copy in range(2):
        for i, name in enumerate(REPOS):
            x = 34 + (i % 2) * 240
            y = 18 + (copy * rows + i // 2) * row
            items.append(f'<use href="#repoIcon" x="{x}" y="{y}"/>'
                         + d.text(name, x + 14, y + CAP * 6.5, 13, 400, "mono", fill=t["muted"]))
    return f'<g mask="url(#edgeMask)"><g class="scroll">{"".join(items)}</g></g>'


ART = {"graph": art_graph, "road": art_road, "mesh": art_mesh, "repos": art_repos}


def card(theme: str, p: dict) -> Doc:
    t = THEMES[theme]
    W, H, X = 520, 360, 28
    d = Doc(W, H, p["name"], f'{p["desc"]} {p["stack"]}')
    b = d.body
    b.append(rrect(.5, .5, W - 1, H - 1, 14, fill=t["canvas"], stroke=t["border"]))
    d.defs.append('<clipPath id="panel"><rect x="8" y="8" width="504" height="152" rx="9"/></clipPath>')
    b.append(rrect(8.5, 8.5, 503, 151, 8.5, fill=t["subtle"], stroke=t["hair"]))
    b.append(f'<g clip-path="url(#panel)"><g transform="translate(8 8)">'
             f'{grid(d, t, 504, 152, 252, 76, 300, 24, "pgrid")}{ART[p["art"]](d, t)}</g></g>')

    title_base = 210
    b.append(d.text(p["name"], X, title_base, 26, 600, tracking=-.02, fill=t["fg"]))
    tag = p["tag"].upper()
    tag_w = measure(tag, 12, 500, "mono", .06) + 20
    cy = title_base - CAP * 26 / 2
    b.append(rrect(W - X - tag_w, cy - 12, tag_w, 24, 6, fill=t["subtle"], stroke=t["border"])
             + d.text(tag, W - X - tag_w + 10, cy + CAP * 6, 12, 500, "mono", tracking=.06, fill=t["muted"]))
    b.append(d.text(p["desc"], X, 239, 16, 400, fill=t["muted"]))

    if "metrics" in p:
        for i, (value, label) in enumerate(p["metrics"]):
            x = X + i * 236
            b.append(d.text(value, x, 283, 24, 600, tracking=-.02, fill=t["fg"])
                     + d.text(label, x, 304, 14, 400, fill=t["muted"]))
    else:
        cta_w = measure(p["cta"], 16, 500)
        b.append(d.text(p["cta"], X, 290, 16, 500, fill=t["fg"]) + icon("arrow", X + cta_w + 14, 284.5, t["fg"]))
    b.append(f'<path d="M{X} 320.5H{W - X}" stroke="{t["hair"]}"/>')
    b.append(d.text(p["stack"], X, 345, 13, 400, "mono", fill=t["faint"]))
    return d


# ---------------------------------------------------------------- recognition

def recognition(theme: str) -> Doc:
    t = THEMES[theme]
    W, H = 1200, 168
    col = W / len(STATS)
    d = Doc(W, H, "Recognition", ", ".join(f"{v} {label.lower()}" for v, label in STATS))
    d.css.append(f".rise{{animation:rise 1s {EASE_OUT} both}}@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}}}")
    b = d.body
    b.append(frame(t, W, H))
    for i, (value, label) in enumerate(STATS):
        x = i * col + 36
        if i:
            b.append(f'<path d="M{f(i * col)} 36V{H - 36}" stroke="{t["hair"]}"/>')
        b.append(f'<g class="rise" style="animation-delay:{.08 * i:g}s">'
                 + d.text(value, x, 94, 54, 600, tracking=-.04, fill=t["fg"])
                 + d.text(label, x, 128, 18, 400, fill=t["muted"]) + "</g>")
    return d


def stack(theme: str) -> Doc:
    t = THEMES[theme]
    W, X_CHIPS, ROW, size = 1200, 286, 58, 17
    H = 40 + ROW * len(STACK) + 12
    d = Doc(W, H, "Stack", "; ".join(f"{group}: {', '.join(items)}" for group, items in STACK))
    d.css.append(f".rise{{animation:rise .9s {EASE_OUT} both}}@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}}}")
    b = d.body
    b.append(frame(t, W, H))
    for r, (group, items) in enumerate(STACK):
        cy = 46 + r * ROW + 18
        if r:
            b.append(f'<path d="M48 {f(cy - ROW / 2)}H{W - 48}" stroke="{t["hair"]}"/>')
        row = [d.text(group.upper(), 56, cy + CAP * 7.5, 15, 500, "mono", tracking=.06, fill=t["muted"])]
        x = X_CHIPS
        for item in items:
            w = measure(item, size, 500) + 30
            row.append(rrect(x, cy - 18, w, 36, 8, fill=t["subtle"], stroke=t["border"])
                       + d.text(item, x + 15, cy + CAP * size / 2, size, 500, fill=t["fg"]))
            x += w + 10
        b.append(f'<g class="rise" style="animation-delay:{.06 * r:g}s">{"".join(row)}</g>')
    return d


def main() -> None:
    for theme in THEMES:
        hero(theme).save(ASSETS / f"hero-{theme}.svg")
        recognition(theme).save(ASSETS / f"recognition-{theme}.svg")
        stack(theme).save(ASSETS / f"stack-{theme}.svg")
        for slug in LINKS:
            button(theme, slug).save(ASSETS / f"link-{slug}-{theme}.svg")
        for p in PROJECTS:
            card(theme, p).save(ASSETS / f"card-{p['slug']}-{theme}.svg")
    for path in sorted(ASSETS.glob("*.svg")):
        print(f"{path.stat().st_size:>8,}  {path.name}")


if __name__ == "__main__":
    main()
