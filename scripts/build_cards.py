#!/usr/bin/env python3
"""Build the SVG cards shown in the profile README.

    python3 scripts/build_cards.py             # rebuild from the numbers below
    python3 scripts/build_cards.py --refresh   # first pull contributions per year with `gh`

Colors and type follow carlosnava.dev: warm grey paper, near-black ink, one blue.
Every card has a light and a dark file; the README picks one with <picture>.
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
DATA = ROOT / "scripts" / "contributions.json"

THEMES = {
    "light": dict(surface="#f3f3f0", card="#ffffff", line="#dcdcd6", ink="#15171c",
                  muted="#5b606b", accent="#1e50d4", ok="#1f7a4d", ctx="#7d828c"),
    "dark": dict(surface="#111318", card="#1a1d24", line="#2b2f38", ink="#eef0f3",
                 muted="#a3a9b5", accent="#8aa8ff", ok="#5fd394", ctx="#636a78"),
}
SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(n):
    return f"{n:,}"


# ---------------------------------------------------------------- data

def refresh_contributions():
    years = {}
    for y in range(2019, date.today().year + 1):
        q = ('{ viewer { contributionsCollection(from:"%d-01-01T00:00:00Z", to:"%d-12-31T23:59:59Z") '
             '{ contributionCalendar { totalContributions } totalCommitContributions totalPullRequestContributions } } }') % (y, y)
        out = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"], check=True, capture_output=True, text=True).stdout
        c = json.loads(out)["data"]["viewer"]["contributionsCollection"]
        years[str(y)] = dict(total=c["contributionCalendar"]["totalContributions"],
                             commits=c["totalCommitContributions"], prs=c["totalPullRequestContributions"])
    DATA.write_text(json.dumps(dict(as_of=date.today().isoformat(), years=years), indent=2) + "\n")


# ---------------------------------------------------------------- header

ROLES = ["Full-stack engineer.", "Forward deployed engineer.", "AI agents &amp; MCP servers.", "Native iOS in Swift."]


def header(t, stats):
    W, H = 1200, 320
    year = max(stats["years"])
    cur = stats["years"][year]
    term_bg = "#15171c" if t is THEMES["light"] else "#1a1d24"
    term_ink, term_muted, term_accent = "#eef0f3", "#a3a9b5", "#8aa8ff"

    roles = []
    for i, r in enumerate(ROLES):
        roles.append(f'<text class="role r{i}" x="56" y="186">{r}</text>')

    # Terminal lines: (kind, text). Commands are typed, output appears at once.
    lines = [
        ("cmd", "whoami"),
        ("out", "carlos nava · full-stack · 6 yrs · mexico"),
        ("cmd", "ls ~/shipping"),
        ("out", "telecom-ops/   relic/   gym-wigas/"),
        ("cmd", f"gh contributions --year {year}"),
        ("out", f"{fmt(cur['total'])} contributions · {fmt(cur['commits'])} commits · {fmt(cur['prs'])} PRs"),
    ]
    tx, ty, tw, th = 636, 40, 508, 240
    cw = 9.65  # ~0.6em at 16px
    total = 5.2
    t0, parts, clips = 0.5, [], []
    for i, (kind, text) in enumerate(lines):
        y = ty + 78 + i * 26
        if kind == "cmd":
            n = len(text)
            dur = max(0.35, n * 0.045)
            w = 22 + n * cw + 4
            start, end = t0, t0 + dur
            t0 = end + 0.25
            # The clip starts at full width, so the line still shows where SMIL does not run.
            # The animation holds it at 0 until its turn, then opens one character per step.
            kts = ["0"] + [f"{(start + (end - start) * k / n) / total:.4f}" for k in range(n + 1)] + ["1"]
            vals = ["0"] + [f"{22 + k * cw:.1f}" for k in range(n + 1)] + [f"{w:.0f}"]
            clips.append(f'<clipPath id="c{i}"><rect x="{tx + 24}" y="{y - 18}" height="26" width="{w:.0f}">'
                         f'<animate attributeName="width" dur="{total}s" fill="freeze" calcMode="discrete" '
                         f'keyTimes="{";".join(kts)}" values="{";".join(vals)}"/></rect></clipPath>')
            parts.append(f'<g clip-path="url(#c{i})"><text x="{tx + 24}" y="{y}" class="t">'
                         f'<tspan fill="{term_accent}">$</tspan> <tspan fill="{term_ink}">{esc(text)}</tspan></text></g>')
        else:
            at = t0 - 0.1
            parts.append(f'<text x="{tx + 24}" y="{y}" class="t" xml:space="preserve" fill="{term_muted if i < 5 else term_ink}">'
                         f'<animate attributeName="opacity" dur="{total}s" fill="freeze" calcMode="discrete" '
                         f'keyTimes="0;{at/total:.4f};1" values="0;1;1"/>{esc(text)}</text>')
            t0 += 0.35
    cy = ty + 78 + len(lines) * 26
    parts.append(f'<text x="{tx + 24}" y="{cy}" class="t" fill="{term_accent}">$</text>'
                 f'<rect x="{tx + 24 + 2 * cw:.0f}" y="{cy - 15}" width="10" height="19" fill="{term_ink}">'
                 f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')

    n = len(ROLES)
    cycle = 3 * n
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Carlos Nava, full-stack and forward deployed engineer in Mexico</title>
<desc id="desc">Full-stack engineer, forward deployed engineer, AI agents and MCP servers, native iOS in Swift. Open to remote roles and freelance projects. {fmt(cur['total'])} GitHub contributions in {year}.</desc>
<style>
  text {{ font-family: {SANS}; }}
  .t {{ font-family: {MONO}; font-size: 16px; }}
  .role {{ font-size: 32px; font-weight: 600; letter-spacing: -.5px; fill: {t["accent"]}; opacity: 0; animation: role {cycle}s infinite; }}
  {" ".join(f".r{i} {{ animation-delay: {i * 3}s; }}" for i in range(n))}
  @keyframes role {{
    0% {{ opacity: 0; transform: translateY(10px); }}
    {100/n*0.12:.2f}% {{ opacity: 1; transform: translateY(0); }}
    {100/n*0.88:.2f}% {{ opacity: 1; transform: translateY(0); }}
    {100/n:.2f}% {{ opacity: 0; transform: translateY(-10px); }}
    100% {{ opacity: 0; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .role {{ animation: none; }}
    .r0 {{ opacity: 1; }}
  }}
</style>
<defs>{"".join(clips)}
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{t["line"]}"/></pattern>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{t["surface"]}"/>
<rect x="560" width="{W - 560}" height="{H}" fill="url(#dots)" opacity=".9"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["line"]}"/>
<text x="56" y="70" font-size="14" font-weight="600" letter-spacing="2.2" fill="{t["muted"]}">SOFTWARE ENGINEER · MEXICO · EN / ES</text>
<text x="54" y="136" font-size="64" font-weight="600" letter-spacing="-2" fill="{t["ink"]}">Carlos Nava</text>
{"".join(roles)}
<text x="56" y="232" font-size="19" fill="{t["muted"]}">I talk to whoever has the problem,</text>
<text x="56" y="258" font-size="19" fill="{t["muted"]}">then build and run the fix.</text>
<circle cx="62" cy="290" r="5" fill="{t["ok"]}"><animate attributeName="r" values="5;6.5;5" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="76" y="295" font-size="15" fill="{t["ink"]}">Open to remote roles and freelance projects</text>
<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{term_bg}" stroke="{t["line"]}"/>
<circle cx="{tx + 22}" cy="{ty + 22}" r="5.5" fill="#4a505e"/><circle cx="{tx + 40}" cy="{ty + 22}" r="5.5" fill="#4a505e"/><circle cx="{tx + 58}" cy="{ty + 22}" r="5.5" fill="#4a505e"/>
<text x="{tx + tw / 2}" y="{ty + 27}" text-anchor="middle" class="t" font-size="13" fill="{term_muted}">carlos@mexico: ~</text>
<line x1="{tx}" x2="{tx + tw}" y1="{ty + 44}" y2="{ty + 44}" stroke="#2b2f38"/>
{"".join(parts)}
</svg>
'''


# ---------------------------------------------------------------- impact

IMPACT = [
    ("96%", "of activations and recharges|succeed", "Telecom ops platform · 2025–"),
    ("~$1M", "MXN processed|every month", "Telecom ops platform · 2025–"),
    ("60%", "less operating time|for the business", "Telecom ops platform · 2025–"),
    ("80%", "more accurate candidate|classification", "AI recruiting on OpenAI · Alluxi"),
    ("70%", "less manual work with|scraping bots", "Insurance data · Sysy.mx"),
    ("60%", "faster reaction to threats|with SOAR automation", "Cybersecurity · Scitum"),
    ("40%", "of manual warehouse work|automated, backend 30% faster", "Backend · Jüsto"),
    ("50K+", "flight bookings a month,|30% less downtime", "Team lead of 5 · Alluxi"),
]


def impact(t):
    W, cols, pad, gap = 1200, 4, 0, 16
    tw = (W - 2 * pad - (cols - 1) * gap) / cols
    th = 150
    top = 0
    rows = (len(IMPACT) + cols - 1) // cols
    H = top + rows * th + (rows - 1) * gap
    tiles = []
    for i, (val, label, ctx) in enumerate(IMPACT):
        r, c = divmod(i, cols)
        x, y = pad + c * (tw + gap), top + r * (th + gap)
        tiles.append(f'''<g class="tile" style="animation-delay:{i * 90}ms">
  <rect x="{x + .5:.1f}" y="{y + .5}" width="{tw - 1:.1f}" height="{th - 1}" rx="12" fill="{t["card"]}" stroke="{t["line"]}"/>
  <text x="{x + 22:.1f}" y="{y + 56}" font-size="40" font-weight="600" letter-spacing="-1.2" fill="{t["accent"]}">{esc(val)}</text>
  <text x="{x + 22:.1f}" y="{y + 84}" font-size="15" fill="{t["ink"]}">{"".join(f'<tspan x="{x + 22:.1f}" dy="{0 if k == 0 else 20}">{esc(part)}</tspan>' for k, part in enumerate(label.split("|")))}</text>
  <text x="{x + 22:.1f}" y="{y + 130}" font-size="13" fill="{t["muted"]}">{esc(ctx)}</text>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Results I have shipped</title>
<desc id="desc">{esc("; ".join(f"{v} {l.replace(chr(124), chr(32))} ({c})" for v, l, c in IMPACT))}</desc>
<style>
  text {{ font-family: {SANS}; }}
  .tile {{ animation: rise .7s cubic-bezier(.16,1,.3,1) both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: none; }} }}
  @media (prefers-reduced-motion: reduce) {{ .tile {{ animation: none; }} }}
</style>
{"".join(tiles)}
</svg>
'''


# ---------------------------------------------------------------- activity

def activity(t, stats):
    W, H = 1200, 400
    ys = sorted(stats["years"])
    vals = [stats["years"][y]["total"] for y in ys]
    cur_y = ys[-1]
    cur = stats["years"][cur_y]
    as_of = date.fromisoformat(stats["as_of"])
    x0, x1, base, top = 96, 760, 330, 120
    vmax = 3500
    sy = lambda v: base - (base - top) * v / vmax
    band = (x1 - x0) / len(ys)
    bw = 24
    grid = []
    for v in (0, 1000, 2000, 3000):
        y = sy(v)
        grid.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{t["line"]}" stroke-width="1"/>'
                    f'<text x="{x0 - 12}" y="{y + 4.5:.1f}" text-anchor="end" class="tick">{fmt(v)}</text>')
    bars = []
    peak_before = max(range(len(ys) - 1), key=lambda i: vals[i])
    for i, (y, v) in enumerate(zip(ys, vals)):
        cx = x0 + band * (i + .5)
        bx, by = cx - bw / 2, sy(v)
        h = base - by
        r = min(4, h)
        color = t["accent"] if y == cur_y else t["ctx"]
        d = (f"M{bx:.1f},{base} V{by + r:.1f} Q{bx:.1f},{by:.1f} {bx + r:.1f},{by:.1f} H{bx + bw - r:.1f} "
             f"Q{bx + bw:.1f},{by:.1f} {bx + bw:.1f},{by + r:.1f} V{base} Z")
        bars.append(f'<path class="bar" style="animation-delay:{i * 70}ms" d="{d}" fill="{color}"/>')
        bars.append(f'<text x="{cx:.1f}" y="{base + 26}" text-anchor="middle" class="tick">{y}{"*" if y == cur_y else ""}</text>')
        if y == cur_y or i == peak_before:
            bars.append(f'<text x="{cx:.1f}" y="{by - 10:.1f}" text-anchor="middle" class="val">{fmt(v)}</text>')
    tiles = [
        (fmt(cur["total"]), f"contributions in {cur_y}"),
        (fmt(cur["commits"]), "commits"),
        (fmt(cur["prs"]), "pull requests"),
    ]
    kx = 840
    k = []
    for i, (v, l) in enumerate(tiles):
        ky = 132 + i * 86
        k.append(f'<text x="{kx}" y="{ky}" font-size="{44 if i == 0 else 34}" font-weight="600" letter-spacing="-1" fill="{t["ink"]}">{v}</text>'
                 f'<text x="{kx}" y="{ky + 26}" font-size="15" fill="{t["muted"]}">{l}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">GitHub contributions per year</title>
<desc id="desc">{esc(", ".join(f"{y}: {fmt(v)}" for y, v in zip(ys, vals)))}. {cur_y} counted to {as_of:%B %-d}: {fmt(cur["commits"])} commits and {fmt(cur["prs"])} pull requests.</desc>
<style>
  text {{ font-family: {SANS}; }}
  .tick {{ font-size: 13px; fill: {t["muted"]}; font-variant-numeric: tabular-nums; }}
  .val {{ font-size: 14px; font-weight: 600; fill: {t["ink"]}; }}
  .bar {{ transform-box: fill-box; transform-origin: 50% 100%; animation: grow .9s cubic-bezier(.16,1,.3,1) both; }}
  @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
  @media (prefers-reduced-motion: reduce) {{ .bar {{ animation: none; }} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{t["surface"]}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["line"]}"/>
<text x="40" y="54" font-size="21" font-weight="600" fill="{t["ink"]}">Contributions on GitHub, per year</text>
<text x="40" y="80" font-size="14" fill="{t["muted"]}">This account only. Most of it is private work. *{cur_y} counted to {as_of:%B %-d}.</text>
{"".join(grid)}
{"".join(bars)}
<line x1="800" x2="800" y1="110" y2="350" stroke="{t["line"]}"/>
{"".join(k)}
</svg>
'''


# ---------------------------------------------------------------- telecom cover

def telecom():
    W, H = 768, 512
    ink, muted, accent, line, card = "#eef0f3", "#a3a9b5", "#8aa8ff", "#2b2f38", "#1a1d24"

    def chip(x, y, w, label, sub=None, hi=False):
        h = 50 if sub else 38
        s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{card}" stroke="{accent if hi else line}"/>'
             f'<text x="{x + w / 2}" y="{y + (22 if sub else 24)}" text-anchor="middle" font-size="14" font-weight="600" fill="{ink}">{esc(label)}</text>')
        if sub:
            s += f'<text x="{x + w / 2}" y="{y + 40}" text-anchor="middle" font-size="12" fill="{muted}">{esc(sub)}</text>'
        return s

    flow = lambda x1, y1, x2, y2, d=0: (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line}" stroke-width="2"/>'
        f'<line class="pk" style="animation-delay:{d}s" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-dasharray="6 22"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Telecom operations platform</title>
<desc id="desc">96% of SIM activations and prepaid recharges succeed. The owner uses a React and Django platform that talks to carriers over SOAP and an AWS Site-to-Site VPN, with an AI ops agent on the Claude API and MCP.</desc>
<style>
  text {{ font-family: {SANS}; }}
  .pk {{ animation: flow 1.6s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -28; }} }}
  @media (prefers-reduced-motion: reduce) {{ .pk {{ animation: none; }} }}
</style>
<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#232733"/></pattern></defs>
<rect width="{W}" height="{H}" fill="#111318"/>
<rect width="{W}" height="{H}" fill="url(#g)"/>
<text x="44" y="64" font-size="14" font-weight="600" letter-spacing="2.4" fill="{muted}">TELECOM OPERATIONS PLATFORM</text>
<text x="40" y="168" font-size="112" font-weight="600" letter-spacing="-5" fill="{accent}">96%</text>
<text x="44" y="204" font-size="20" fill="{ink}">of SIM activations and recharges succeed</text>
<text x="44" y="232" font-size="16" fill="{muted}">Built solo · ~MXN $1M a month · 60% less operating time</text>
{flow(140, 314, 196, 314, 0)}
{flow(356, 314, 420, 314, .3)}
{flow(580, 314, 620, 314, .6)}
{flow(276, 340, 276, 392, .9)}
{chip(44, 295, 96, "Owner")}
{chip(196, 290, 160, "Ops platform", "Django · React", hi=True)}
{chip(420, 290, 160, "SOAP client", "AWS Site-to-Site VPN")}
{chip(620, 295, 104, "Carriers")}
{chip(186, 392, 180, "AI ops agent", "Claude API · MCP")}
<text x="392" y="414" font-size="13" fill="{muted}">answers from live data;</text>
<text x="392" y="432" font-size="13" fill="{muted}">corrective actions wait for a human</text>
<text x="44" y="484" font-size="13" fill="{muted}">Client under NDA · DDD · TDD · I run production</text>
</svg>
'''


def main():
    if "--refresh" in sys.argv:
        refresh_contributions()
    stats = json.loads(DATA.read_text())
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t, stats))
        (OUT / f"impact-{name}.svg").write_text(impact(t))
        (OUT / f"activity-{name}.svg").write_text(activity(t, stats))
    (OUT / "telecom-cover.svg").write_text(telecom())
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
