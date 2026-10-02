"""Render the contribution activity panel from live GitHub data.

A playhead sweeps through the year and each day lights up in proportion to its
activity, leaving a fading trail; then the best day and the current streak light
up together with their stats in the header.

    python .github/profile/activity.py [--user nakultt] [--out dist]

Authenticates with GITHUB_TOKEN, falling back to `gh auth token` locally.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from common import CAP, ROOT, THEMES, Doc, f, measure, onoff, pct, rrect

QUERY = """
query($login: String!, $from: DateTime, $to: DateTime) {
  user(login: $login) {
    createdAt
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date weekday contributionCount } }
      }
    }
  }
}"""
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

# layout
W, H = 1200, 376
X_L, X_R = 80, 1120
CELL, PITCH = 15, 19
X_GRID, Y_GRID = X_R - 53 * PITCH + 4, 174

# timeline (seconds): sweep one week every STEP, hold, then fade and loop
STEP, HOLD, LOOP = .1, 2.6, 9.5
GLOW = (0, .35, .55, .8, 1)  # accent strength per level


@dataclass
class Day:
    date: dt.date
    count: int
    col: int
    row: int


def token() -> str:
    if value := os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
        return value
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def graphql(**variables) -> dict:
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    request = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token()}", "User-Agent": "nakultt-profile"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def fetch(user: str):
    """Last-year calendar plus every day since the account was created."""
    data = graphql(login=user)
    cal = data["contributionsCollection"]["contributionCalendar"]
    days = [Day(dt.date.fromisoformat(d["date"]), d["contributionCount"], col, d["weekday"])
            for col, week in enumerate(cal["weeks"]) for d in week["contributionDays"]]
    history: dict[dt.date, int] = {}
    start = dt.datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    while start < now:
        end = min(start + dt.timedelta(days=365), now)
        chunk = graphql(login=user, **{"from": start.isoformat(), "to": end.isoformat()})
        for week in chunk["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                history[dt.date.fromisoformat(d["date"])] = d["contributionCount"]
        start = end
    for day in days:
        history[day.date] = day.count
    return cal["totalContributions"], days, history


def streaks(days: list[Day], history: dict[dt.date, int]) -> tuple[int, int]:
    """Current streak (today may still be empty) and longest streak ever."""
    current, recent = 0, days if days[-1].count else days[:-1]
    for day in reversed(recent):
        if not day.count:
            break
        current += 1
    longest = run = 0
    prev = None
    for date in sorted(history):
        consecutive = prev is not None and (date - prev).days == 1
        run = (run + 1 if consecutive else 1) if history[date] else 0
        longest, prev = max(longest, run), date
    return current, max(longest, current)


def levels(days: list[Day]) -> dict[dt.date, int]:
    """Quartiles of active days, so a few huge days don't flatten the rest."""
    active = sorted(d.count for d in days if d.count)
    if not active:
        return {d.date: 0 for d in days}
    cuts = [active[int(q * (len(active) - 1))] for q in (.25, .5, .75)]
    return {d.date: 0 if not d.count else 1 + sum(d.count > c for c in cuts) for d in days}


def short(date: dt.date) -> str:
    return f"{MONTHS[date.month - 1]} {date.day}"


def cell_x(col: int) -> float:
    return X_GRID + col * PITCH


def cell_y(row: int) -> float:
    return Y_GRID + row * PITCH


def render(theme: str, user: str, total: int, days: list[Day], current: int, longest: int) -> Doc:
    t = THEMES[theme]
    best = max(days, key=lambda d: (d.count, d.date))
    d = Doc(W, H, f"{user}: {total:,} contributions in the last year",
            f"Current streak {current} days, longest streak {longest} days, best day {best.count} on {short(best.date)}.")
    b = d.body
    b.append(rrect(.5, .5, W - 1, H - 1, 15.5, fill=t["canvas"], stroke=t["border"]))

    # timeline: the playhead crosses one week per STEP, then the highlights hold
    cols = days[-1].col + 1
    end = cols * STEP
    hold_end = end + HOLD
    d.css.append(onoff("best", LOOP, best.col * STEP + .15, hold_end) + f".hl-best{{opacity:0;animation:best {LOOP:g}s infinite}}"
                 + onoff("streak", LOOP, end, hold_end) + f".hl-streak{{opacity:0;animation:streak {LOOP:g}s infinite}}")

    # header: total on the left, streak stats on the right
    b.append(d.text("CONTRIBUTION ACTIVITY", X_L, 60, 14, 500, "mono", tracking=.08, fill=t["muted"]))
    figure = f"{total:,}"
    b.append(d.text(figure, X_L - 2, 116, 50, 600, tracking=-.035, fill=t["fg"])
             + d.text("contributions in the last year", X_L + measure(figure, 50, 600, tracking=-.035) + 14, 116, 19,
                      400, fill=t["muted"]))
    stats = [("Current streak", f"{current} day{'s' * (current != 1)}", "hl-streak", t["success"]),
             ("Longest streak", f"{longest} day{'s' * (longest != 1)}", None, None),
             (f"Best day · {short(best.date)}", f"{best.count}", "hl-best", t["accent"])]
    block = 172
    for i, (label, value, hl, color) in enumerate(stats):
        x = X_R - (len(stats) - i) * block + 30
        b.append(f'<path d="M{f(x - 30)} 44V122" stroke="{t["hair"]}"/>'
                 + d.text(label, x, 70, 16, 400, fill=t["muted"])
                 + d.text(value, x, 112, 32, 600, tracking=-.03, fill=t["fg"]))
        if hl:
            b.append(f'<g class="{hl}">{d.text(value, x, 112, 32, 600, tracking=-.03, fill=color)}</g>')

    # calendar: month labels, weekday labels, cells
    seen = -9
    for day in days:
        if day.date.day <= 7 and day.row == 0 and day.col - seen > 2 and day.col < 51:
            b.append(d.text(MONTHS[day.date.month - 1], cell_x(day.col), Y_GRID - 14, 15, 400, fill=t["muted"]))
            seen = day.col
    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b.append(d.text(label, X_GRID - 12, cell_y(row) + CELL / 2 + CAP * 7.5, 15, 400, anchor="end", fill=t["faint"]))
    lv = levels(days)
    b.append("".join(rrect(cell_x(day.col), cell_y(day.row), CELL, CELL, 3.5, fill=t["levels"][lv[day.date]])
                     for day in days))
    b.append(sweep(d, t, days, lv, end))

    # the best day and the current streak, ringed while their stats light up
    ring = lambda day, color: rrect(cell_x(day.col) - 3, cell_y(day.row) - 3, CELL + 6, CELL + 6, 6, fill="none",
                                    stroke=color, stroke_width=2)
    b.append(f'<g class="hl-best">{ring(best, t["accent"])}</g>')
    run = [day for day in days if day.count][-current:] if current else []
    b.append(f'<g class="hl-streak">{"".join(ring(day, t["success"]) for day in run)}</g>')

    # footer: refresh note, legend
    fy = H - 30
    b.append(f'<circle cx="{X_L + 4}" cy="{f(fy - 5.3)}" r="4" fill="{t["success"]}"/>'
             + d.text(f"Refreshed daily · {short(days[-1].date)}, {days[-1].date.year}", X_L + 18, fy, 15, 400, fill=t["muted"]))
    x = X_R - 5 * PITCH + 4
    b.append(d.text("Less", x - 10, fy, 15, 400, anchor="end", fill=t["muted"])
             + "".join(rrect(x + i * PITCH, fy - 13, CELL - 2, CELL - 2, 3, fill=c) for i, c in enumerate(t["levels"]))
             + d.text("More", x + 5 * PITCH + 3, fy, 15, 400, fill=t["muted"]))
    return d


def sweep(d: Doc, t: dict, days: list[Day], lv: dict[dt.date, int], end: float) -> str:
    """Playhead that crosses the year; each week flashes as it passes and decays into a trail."""
    last = cell_x(days[-1].col) + CELL + 6
    d.css.append(
        f"@keyframes flash{{0%{{opacity:0}}1.6%{{opacity:1}}16%,100%{{opacity:0}}}}"
        f".wk{{opacity:0;animation:flash {LOOP:g}s infinite both}}"
        f"@keyframes head{{0%{{transform:translateX({f(cell_x(0) - 6)}px);opacity:0}}2%{{opacity:1}}"
        f"{pct(end, LOOP)}{{transform:translateX({f(last)}px);opacity:1}}"
        f"{pct(end + .35, LOOP)},100%{{transform:translateX({f(last)}px);opacity:0}}}}"
        f".head{{opacity:0;animation:head {LOOP:g}s linear infinite}}"
    )
    by_col: dict[int, list[Day]] = {}
    for day in days:
        if day.count:
            by_col.setdefault(day.col, []).append(day)
    out = []
    for col, members in sorted(by_col.items()):
        rects = "".join(rrect(cell_x(col), cell_y(m.row), CELL, CELL, 3.5, fill=t["accent"],
                              fill_opacity=f"{GLOW[lv[m.date]]:g}") for m in members)
        out.append(f'<g class="wk" style="animation-delay:{col * STEP:.2f}s">{rects}</g>')
    out.append(f'<g class="head"><rect x="-1" y="{Y_GRID - 6}" width="2" height="{7 * PITCH + 8}" rx="1" '
               f'fill="{t["accent"]}"/><circle cy="{Y_GRID - 6}" r="3.5" fill="{t["accent"]}"/></g>')
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--user", default="nakultt")
    parser.add_argument("--out", default=str(ROOT / "dist"))
    args = parser.parse_args()
    total, days, history = fetch(args.user)
    current, longest = streaks(days, history)
    for theme in THEMES:
        path = render(theme, args.user, total, days, current, longest).save(Path(args.out) / f"activity-{theme}.svg")
        print(f"{path.stat().st_size:>8,}  {path}")
    print(f"total={total} current={current} longest={longest}")


if __name__ == "__main__":
    main()
