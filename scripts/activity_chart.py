#!/usr/bin/env python3
"""Draw the contributions-per-year chart in the profile README.

    python3 scripts/activity_chart.py             # redraw from scripts/contributions.json
    python3 scripts/activity_chart.py --refresh   # first pull fresh totals with `gh`

One series, so no legend: the current year is drawn in carlosnava.dev's blue
and earlier years in grey. The background is transparent so the chart sits on
GitHub's own page; the README picks the light or dark file with <picture>.
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "scripts" / "contributions.json"

THEMES = {
    # muted text >= 4.5:1 and grey bars >= 3:1 on GitHub's white and #0d1117
    "light": dict(grid="#d8dee4", text="#57606a", value="#1f2328", accent="#1e50d4", ctx="#7d828c"),
    "dark": dict(grid="#30363d", text="#9198a1", value="#f0f6fc", accent="#8aa8ff", ctx="#656c76"),
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"


def fmt(n):
    return f"{n:,}"


def refresh():
    years = {}
    for y in range(2019, date.today().year + 1):
        q = ('{ viewer { contributionsCollection(from:"%d-01-01T00:00:00Z", to:"%d-12-31T23:59:59Z") '
             '{ contributionCalendar { totalContributions } totalCommitContributions totalPullRequestContributions } } }') % (y, y)
        out = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"], check=True, capture_output=True, text=True).stdout
        c = json.loads(out)["data"]["viewer"]["contributionsCollection"]
        years[str(y)] = dict(total=c["contributionCalendar"]["totalContributions"],
                             commits=c["totalCommitContributions"], prs=c["totalPullRequestContributions"])
    DATA.write_text(json.dumps(dict(as_of=date.today().isoformat(), years=years), indent=2) + "\n")


def chart(t, stats):
    W, H = 1200, 300
    ys = sorted(stats["years"])
    vals = [stats["years"][y]["total"] for y in ys]
    cur = ys[-1]
    x0, x1, top, base = 64, 1196, 34, 252
    step = 1000
    vmax = (max(vals) // step + 1) * step
    sy = lambda v: base - (base - top) * v / vmax
    band = (x1 - x0) / len(ys)
    bw = 24

    out = []
    for v in range(0, vmax, step):
        y = sy(v)
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{t["grid"]}"/>'
                   f'<text x="{x0 - 14}" y="{y + 5:.1f}" text-anchor="end" class="tick">{fmt(v)}</text>')

    labelled = {len(ys) - 1, max(range(len(ys) - 1), key=lambda i: vals[i])}
    for i, (y, v) in enumerate(zip(ys, vals)):
        cx = x0 + band * (i + .5)
        bx, by = cx - bw / 2, sy(v)
        r = min(4, base - by)
        d = (f"M{bx:.1f},{base} V{by + r:.1f} Q{bx:.1f},{by:.1f} {bx + r:.1f},{by:.1f} H{bx + bw - r:.1f} "
             f"Q{bx + bw:.1f},{by:.1f} {bx + bw:.1f},{by + r:.1f} V{base} Z")
        out.append(f'<path class="bar" style="animation-delay:{i * 60}ms" d="{d}" fill="{t["accent"] if y == cur else t["ctx"]}"/>')
        out.append(f'<text x="{cx:.1f}" y="{base + 30}" text-anchor="middle" class="tick">{y}</text>')
        if i in labelled:
            label = f"{fmt(v)} so far" if y == cur else fmt(v)
            out.append(f'<text x="{cx:.1f}" y="{by - 12:.1f}" text-anchor="middle" class="val">{label}</text>')

    desc = ", ".join(f"{y}: {fmt(v)}" for y, v in zip(ys, vals))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">GitHub contributions per year</title>
<desc id="desc">{desc}. {cur} is counted to {date.fromisoformat(stats["as_of"]):%B %-d}.</desc>
<style>
  text {{ font-family: {SANS}; }}
  .tick {{ font-size: 15px; fill: {t["text"]}; font-variant-numeric: tabular-nums; }}
  .val {{ font-size: 16px; font-weight: 600; fill: {t["value"]}; }}
  .bar {{ transform-box: fill-box; transform-origin: 50% 100%; animation: grow .9s cubic-bezier(.16,1,.3,1) both; }}
  @keyframes grow {{ from {{ transform: scaleY(.04); }} to {{ transform: scaleY(1); }} }}
  @media (prefers-reduced-motion: reduce) {{ .bar {{ animation: none; }} }}
</style>
{"".join(out)}
</svg>
'''


def main():
    if "--refresh" in sys.argv:
        refresh()
    stats = json.loads(DATA.read_text())
    for name, t in THEMES.items():
        (ROOT / "assets" / f"activity-{name}.svg").write_text(chart(t, stats))
    print("wrote assets/activity-light.svg, assets/activity-dark.svg")


if __name__ == "__main__":
    main()
