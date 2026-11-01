#!/usr/bin/env python3
"""Build the COSMIC rices gallery from the sibling cosmic-*-theme repos.

Reads each rice's README (title, tagline, pair, palette table, Firefox add-on)
and scripts/switch.sh (MODE), makes small screenshot thumbnails, and writes
index.html. Nothing is typed in by hand: re-run after changing a rice.

  python3 build.py            # rebuild data, thumbnails and index.html
  python3 build.py --data     # print the extracted data only
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOS = HERE.parent
OWNER = "atraxsrc"
BRANCH = "master"
THUMBS = HERE / "thumbs"

ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*!\[#([0-9a-fA-F]{6})\]\([^)]*\)\s*([^|]*?)\s*\|", re.M)
PAIR = re.compile(r"https://github\.com/" + OWNER + r"/(cosmic-[a-z0-9]+-theme)")
AMO = re.compile(r"https://addons\.mozilla\.org/[a-zA-Z-]+/firefox/addon/([a-z0-9-]+)/?")


def lum(h: str) -> float:
    def ch(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(h[i:i + 2]) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def chroma(h: str) -> int:
    v = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return max(v) - min(v)


def rice(repo: Path) -> dict:
    readme = (repo / "README.md").read_text()
    head = readme.split("## Palette", 1)[0]
    name = re.search(r"^# COSMIC · (.+)$", readme, re.M).group(1).strip()
    mode = re.search(r'^MODE="(dark|light)"', (repo / "scripts/switch.sh").read_text(), re.M).group(1)
    pair = next((p for p in PAIR.findall(head) if p != repo.name), None)
    # tagline: the first plain paragraph after the palette image, up to the colon
    para = ""
    for block in head.split("\n\n"):
        b = " ".join(block.split())
        if b and not b.startswith(("<", "#", "!", "[", "---")):
            para = b
            break
    m = re.search(r"COSMIC in (.+?):", para)
    tagline = m.group(1) if m else para.split(":")[0]
    palette = []
    seen = set()
    table = readme.split("## Palette", 1)[1].split("\n## ", 1)[0]
    start = table.index("| Role")  # the first table is the palette; a later one compares the pair
    first_table = table[start:].split("\n\n", 1)[0]
    for role, hexv, label in ROW.findall(first_table):
        hexv = "#" + hexv.upper()
        if hexv in seen:
            continue
        seen.add(hexv)
        palette.append({"role": role.strip(), "hex": hexv,
                        "name": re.sub(r"!\[[^\]]*\]\([^)]*\)", "", label).strip()})
    for prefix in (name, "Tokyo Night Light", "Tokyo Night", name.replace(" Day", "").replace(" Night", "")):
        if tagline.startswith(prefix + " "):
            tagline = tagline[len(prefix) + 1:]
            break
    roles = {p["role"].lower(): p["hex"] for p in palette}
    bg = roles.get("background", palette[0]["hex"])
    others = [p["hex"] for p in palette if p["hex"] != bg]
    text = roles.get("text") or roles.get("foreground")
    if not text or contrast(text, bg) < 4.5:
        text = max(others, key=lambda h: contrast(h, bg))
    # accent: the most colourful swatch that still reads on the background
    readable = [h for h in others if h != text and contrast(h, bg) >= 3] or [text]
    named = [roles.get(k) for k in ("accent", "primary", "gold") if roles.get(k) in readable]
    status = {roles.get(k) for k in ("error", "warning", "success")}
    accent = named[0] if named else max([h for h in readable if h not in status] or readable, key=chroma)
    amo = AMO.search(readme)
    return {
        "repo": repo.name, "name": name, "mode": mode, "pair": pair, "tagline": tagline,
        "palette": palette,
        "bg": bg, "text": text, "accent": accent,
        "amo": amo.group(0) if amo else None,
    }


def collect() -> list[dict]:
    rices = [rice(p) for p in sorted(REPOS.glob("cosmic-*-theme")) if (p / "scripts/switch.sh").is_file()]
    by = {r["repo"]: r for r in rices}
    for r in rices:  # pairing is symmetric: fill a missing side from the other
        if not r["pair"]:
            r["pair"] = next((o["repo"] for o in rices if o["pair"] == r["repo"]), None)
        if r["pair"] and by[r["pair"]]["mode"] == r["mode"]:
            sys.exit(f"error: {r['repo']} and {r['pair']} are both {r['mode']}")
    return rices


def thumbs(rices: list[dict]) -> None:
    THUMBS.mkdir(exist_ok=True)
    for r in rices:
        src = REPOS / r["repo"] / "assets/screenshot.png"
        out = THUMBS / f"{r['repo']}.jpg"
        if out.is_file() and out.stat().st_mtime >= src.stat().st_mtime:
            continue
        subprocess.run(["convert", str(src), "-resize", "960x", "-strip", "-quality", "82",
                        "-interlace", "Plane", str(out)], check=True)


if __name__ == "__main__":
    data = collect()
    if "--data" in sys.argv:
        print(json.dumps(data, indent=1))
        sys.exit()
    thumbs(data)
    import render
    (HERE / "index.html").write_text(render.page(data, OWNER, BRANCH))
    print(f"built index.html: {len(data)} rices, {len(data) // 2} pairs")
