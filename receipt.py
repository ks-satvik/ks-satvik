"""
Prints receipt.svg: an animated thermal-printer receipt of my work.

Run by .github/workflows/receipt.yml every morning, so the date, ticket
number and "NOW BUILDING" list (3 latest pushed repos) stay current.
Uses only the standard library.
Add a line in build() when you publish a paper or ship a project.
"""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from xml.sax.saxutils import escape

USER = "ks-satvik"
FIRST_DAY = date(2024, 2, 16)   # first contribution on GitHub; ticket # = days since
FALLBACK_REPO = "footnote"

# QR code for https://scholar.google.com/citations?user=cb0Qe1sAAAAJ (version 4, ECC M)
QR = [
    "111111100011001010111101001111111",
    "100000100101100110100100101000001",
    "101110101111001100001100001011101",
    "101110101110000000010111001011101",
    "101110101101001110101111101011101",
    "100000101011001000001100101000001",
    "111111101010101010101010101111111",
    "000000001001000010000111100000000",
    "101111100100111001100010101111100",
    "011110010100110011111111001101101",
    "101010101011011111101100000010110",
    "110100011011110000111111011011110",
    "101001100010101110100011110011001",
    "100101000110010101101101001001011",
    "111100100010101111001000011001010",
    "111111001110100100100101111001100",
    "101101110100101101000000110110001",
    "010000010100001010111101011101101",
    "110101100101000110101110110110110",
    "101011010010110010111110110111100",
    "111000110101011000110001110011010",
    "110010010001001110101011011001001",
    "100011110011100001101010000010010",
    "100010010010011010000100011011101",
    "100011101100010001000011111111010",
    "000000001101011001111100100010111",
    "111111100110110111001101101010110",
    "100000101001110111111111100011110",
    "101110101101110010010010111111000",
    "101110101011111101101111010010111",
    "101110101000101111001010101101000",
    "100000100010100100010111000010100",
    "111111101101010101000010101101010",
]

# ---------------------------------------------------------------------------
# Live data (falls back to static values so the receipt never breaks)
# ---------------------------------------------------------------------------

def live_data():
    tz = timezone(timedelta(hours=-7))  # Arizona: MST all year, no DST
    now = datetime.now(tz)
    data = {
        "date": now.strftime("%d %b %Y").upper(),
        "time": now.strftime("%H:%M") + " MST",
        "day": (now.date() - FIRST_DAY).days,
        "recent": [(FALLBACK_REPO, "")],
    }
    try:
        req = urllib.request.Request(
            f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=15",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "receipt-printer"},
        )
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=15) as r:
            repos = json.load(r)
        recent = []
        for repo in repos:
            if repo.get("fork") or repo.get("archived") or repo["name"].lower() == USER.lower():
                continue
            pushed = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
            name = repo["name"] if len(repo["name"]) <= 26 else repo["name"][:25] + "…"
            recent.append((name, ago(now - pushed)))
            if len(recent) == 3:
                break
        if recent:
            data["recent"] = recent
    except Exception as e:  # network/API trouble: keep the fallback
        print(f"live data unavailable, using fallback: {e}", file=sys.stderr)
    return data


def ago(delta):
    s = max(0, int(delta.total_seconds()))
    if s < 3600:
        return "just now"
    if s < 86400:
        return f"{s // 3600}h ago"
    if s < 86400 * 60:
        return f"{s // 86400}d ago"
    return f"{s // (86400 * 30)}mo ago"


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

W = 440
PX0, PX1 = 40, 400            # paper edges
LX, RX = PX0 + 24, PX1 - 24   # text column
CX = W / 2
LINE = 19
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"
INK, MUTED, FAINT, PAPER = "#1c1b19", "#6f6b62", "#a19c90", "#fcfbf7"


class Receipt:
    def __init__(self):
        self.els = []
        self.y = 78

    def text(self, x, y, s, anchor="start", size=13, weight="normal", fill=INK, spacing=None, cite=None):
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        c = (f'<tspan font-size="8.5" dy="-5" fill="{FAINT}" font-weight="normal">&#160;[{cite}]</tspan>'
             if cite else "")
        self.els.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{sp}>{escape(s)}{c}</text>'
        )

    def center(self, s, **kw):
        self.text(CX, self.y, s, anchor="middle", **kw)
        self.y += LINE

    def row(self, left, right="", indent=0, bold=False, muted_right=False, size=13, cite=None, muted_left=False):
        w = "bold" if bold else "normal"
        self.text(LX + indent, self.y, left, size=size, weight=w, cite=cite, fill=MUTED if muted_left else INK)
        if right:
            self.text(RX, self.y, right, anchor="end", size=size, weight=w, fill=MUTED if muted_right else INK)
        self.y += LINE

    def rule(self, style="dash", gap=14):
        yy = self.y - LINE / 2 + 2
        dash = ' stroke-dasharray="4 3"' if style in ("dash", "double") else ""
        self.els.append(f'<line x1="{LX}" y1="{yy}" x2="{RX}" y2="{yy}" stroke="{INK}" stroke-width="1"{dash}/>')
        if style == "double":
            self.els.append(f'<line x1="{LX}" y1="{yy+4}" x2="{RX}" y2="{yy+4}" stroke="{INK}" stroke-width="1"{dash}/>')
        self.y += gap

    def space(self, h=8):
        self.y += h


def build(d):
    r = Receipt()

    # header
    r.center("RECEIPT OF WORK", size=19, weight="bold", spacing="2")
    r.space(1)
    r.center("KUMAR SATVIK CHAUDHARY", weight="bold")
    r.center("ML/NLP RESEARCH · ARIZONA STATE UNIV.", fill=MUTED, size=11.5)
    r.space(5)
    r.row(f"{d['date']}", f"{d['time']}", size=11.5, muted_right=True, muted_left=True)
    r.row(f"TICKET #{d['day']:04d}", "TEMPE, AZ", size=11.5, muted_right=True, muted_left=True)
    r.rule(gap=15)

    # research: papers only
    r.row("RESEARCH", "VENUE", bold=True)
    r.row("SMoA", "PAKDD '25", indent=8, cite=1)
    r.row("CyberBOT", "CIKM '25", indent=8, cite=2)
    r.row("+ BEST DEMO PAPER AWARD", indent=22, size=11, muted_left=True)
    r.row("EssayCBM", "ECML-PKDD '26", indent=8, cite=3)
    r.row("Trustworthy Edu. survey", "SSRN '26", indent=8, cite=4)
    r.row("REC-CBM", "SDM '26", indent=8, cite=5)
    r.row("+ AI4GOOD @ ICML '26", indent=22, size=11, muted_left=True)
    r.space(9)

    # education
    r.row("EDUCATION", "", bold=True)
    r.row("Arizona State University", indent=8, cite=6)
    r.row("MS Computer Science", "MAY '27", indent=16, size=12, muted_right=True)
    r.row("+ ACCELERATED", indent=30, size=11, muted_left=True)
    r.row("BS Computer Science", "MAY '26", indent=16, size=12, muted_right=True)
    r.row("+ DATA SCIENCE MINOR", indent=30, size=11, muted_left=True)
    r.row("GPA", "4.00", indent=16, size=12)
    r.space(9)

    # projects
    r.row("PROJECTS", "", bold=True)
    r.row("Footnote", "citation-grounded RAG", indent=8, cite=7, muted_right=True, size=12.5)
    r.row("Tally", "self-correcting SQL agent", indent=8, cite=8, muted_right=True, size=12.5)
    r.row("Voot", "AI accounts payable", indent=8, cite=9, muted_right=True, size=12.5)
    r.space(9)

    # live, refreshed daily
    r.row("NOW BUILDING", "UPDATED", bold=True)
    for name, when in d["recent"]:
        r.row(name, when or "in progress", indent=8, muted_right=True, size=12.5)
    r.space(2)
    r.rule(gap=15)

    r.row("TOTAL", "SHOWS HIS WORK", bold=True, size=15.5)
    r.space(1)
    r.rule(gap=18)

    # QR block: code on the left, caption on the right
    mod = 3
    qr_size = len(QR) * mod
    qx, qy = LX + 6, r.y - 6
    path = []
    for j, line in enumerate(QR):
        i = 0
        while i < len(line):
            if line[i] == "1":
                k = i
                while k < len(line) and line[k] == "1":
                    k += 1
                path.append(f"M{qx + i*mod:.1f} {qy + j*mod:.1f}h{(k-i)*mod:.1f}v{mod}h-{(k-i)*mod:.1f}z")
                i = k
            else:
                i += 1
    r.els.append(f'<path d="{"".join(path)}" fill="{INK}" shape-rendering="crispEdges"/>')
    tx = qx + qr_size + 18
    cy = qy + qr_size / 2
    r.text(tx, cy - 22, "SCAN FOR SOURCES", weight="bold", size=12.5, spacing="0.5")
    r.text(tx, cy - 3, "every claim on this", size=11.5, fill=MUTED)
    r.text(tx, cy + 13, "receipt is cited.", size=11.5, fill=MUTED)
    r.text(tx, cy + 31, "refs [1]-[9] below ↓", size=11.5, fill=MUTED)
    r.y = qy + qr_size + 26

    r.center("THANK YOU · COME AGAIN", weight="bold", size=13, spacing="1.2")
    r.center("reprinted daily by github actions", size=10, fill=FAINT)
    return r


def zigzag(x0, x1, y, tooth, depth, reverse=False):
    pts, x, down = [], x1 if reverse else x0, True
    step = -tooth / 2 if reverse else tooth / 2
    while (x > x0) if reverse else (x < x1):
        x = max(x0, x + step) if reverse else min(x1, x + step)
        pts.append(f"{x:.1f},{y + (depth if down else 0):.1f}" if reverse else f"{x:.1f},{y - (depth if down else 0):.1f}")
        down = not down
    return pts


def render(d):
    r = build(d)
    top, bottom = 22, r.y - 4
    H = int(bottom + 28)

    pts = [f"{PX0},{top}"] + zigzag(PX0, PX1, top, 11, 5) + [f"{PX1},{bottom}"]
    pts += zigzag(PX0, PX1, bottom, 11, 6, reverse=True) + [f"{PX0},{top}"]
    paper = " ".join(pts)
    travel = bottom + 12

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Receipt of work: Kumar Satvik Chaudhary</title>
<desc id="d">An animated receipt printing out of a thermal printer. Research: SMoA (PAKDD 2025); CyberBOT (CIKM 2025, Best Demo Paper award); EssayCBM (ECML-PKDD 2026); Trustworthy Education in the Era of Generative AI survey (SSRN 2026); REC-CBM (SDM 2026, AI4Good at ICML 2026). Education: Arizona State University, MS Computer Science (accelerated, May 2027), BS Computer Science with a Data Science minor (May 2026), GPA 4.00. Projects: Footnote, Tally, Voot. Now building: {escape(", ".join(n for n, _ in d["recent"]))}. Total: shows his work. A QR code links to Google Scholar.</desc>
<style>
  .feed {{ animation: feed 3.6s steps(52, end) .5s both; }}
  .led  {{ animation: blink .3s steps(2, jump-none) .5s 13 both; }}
  @keyframes feed {{ from {{ transform: translateY(-{travel}px); }} to {{ transform: translateY(0); }} }}
  @keyframes blink {{ from {{ fill: #34342f; }} to {{ fill: #4ade80; }} }}
  @media (prefers-reduced-motion: reduce) {{ .feed, .led {{ animation: none; }} }}
</style>
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
  <clipPath id="sheet"><polygon points="{paper}"/></clipPath>
  <filter id="shadow" x="-15%" y="-5%" width="130%" height="112%">
    <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity=".22"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/>
    <feColorMatrix values="0 0 0 0 .45  0 0 0 0 .42  0 0 0 0 .36  0 0 0 .07 0"/>
  </filter>
  <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#46463f"/><stop offset=".55" stop-color="#2b2b27"/><stop offset="1" stop-color="#1f1f1c"/>
  </linearGradient>
  <linearGradient id="curl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000" stop-opacity=".05"/><stop offset=".08" stop-color="#000" stop-opacity="0"/>
    <stop offset=".92" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".06"/>
  </linearGradient>
</defs>
<g clip-path="url(#frame)">
  <g class="feed">
    <g filter="url(#shadow)"><polygon points="{paper}" fill="{PAPER}"/></g>
    <g clip-path="url(#sheet)">
      <rect x="{PX0}" y="{top-6}" width="{PX1-PX0}" height="{bottom-top+12}" filter="url(#grain)"/>
      <rect x="{PX0}" y="{top-6}" width="{PX1-PX0}" height="{bottom-top+12}" fill="url(#curl)"/>
    </g>
    <g font-family="{FONT}">{"".join(r.els)}</g>
  </g>
</g>
<rect x="14" y="0" width="{W-28}" height="36" rx="10" fill="url(#body)"/>
<rect x="14" y="1" width="{W-28}" height="1.2" rx=".6" fill="#fff" opacity=".12"/>
<rect x="{PX0-8}" y="27" width="{PX1-PX0+16}" height="5" rx="2.5" fill="#0c0c0b"/>
<text x="34" y="19" font-family="{FONT}" font-size="8.5" fill="#8d8a80" letter-spacing="2.5">KSC-THERMAL · 80MM</text>
<circle class="led" cx="{W-36}" cy="15" r="3.6" fill="#4ade80"/>
<circle cx="{W-52}" cy="15" r="3.6" fill="#34342f"/>
</svg>
'''


if __name__ == "__main__":
    svg = render(live_data())
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipt.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"printed {out}")
