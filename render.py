"""HTML for the COSMIC rices gallery. Called by build.py; no dependencies."""
from html import escape as e

EXTRAS = [
    ("cosmic-icon-themes", "Icon themes", "Recoloured Kanagawa icon packs, one per rice, in several folder colours."),
    ("firefox-frosted-glass-cosmic", "Frosted glass Firefox", "A Firefox patch that lets COSMIC blur the desktop behind the window."),
]

CSS = """
:root{--bg:#0f0f11;--panel:#18181b;--line:#2c2c31;--fg:#e7e5e1;--dim:#9b9a96;--focus:#f2c14e;
--mono:ui-monospace,"JetBrains Mono","Fira Code",Menlo,Consolas,monospace;
--sans:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,Ubuntu,sans-serif}
*{box-sizing:border-box}
html{color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:2px solid var(--focus);outline-offset:3px;border-radius:6px}
.wrap{max-width:1280px;margin:0 auto;padding:0 16px}
header{padding:56px 0 28px}
.eyebrow{font:500 12px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
h1{font-size:clamp(34px,6vw,60px);line-height:1.02;letter-spacing:-.035em;margin:14px 0 14px;font-weight:650}
.lede{max-width:680px;color:var(--dim);font-size:18px;margin:0}
.bar{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between;
padding:16px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:28px;
position:sticky;top:0;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);z-index:5}
.count{font:13px var(--mono);color:var(--dim)}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--panel)}
.seg button{all:unset;cursor:pointer;font:500 13px var(--mono);padding:6px 14px;border-radius:999px;color:var(--dim)}
.seg button[aria-pressed=true]{background:var(--fg);color:var(--bg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,360px),1fr));gap:20px;padding:28px 0 64px}
.card{border-radius:16px;overflow:hidden;border:1px solid var(--line);transition:transform .2s ease,box-shadow .2s ease}
.card:hover{transform:translateY(-2px);box-shadow:0 14px 40px -18px rgba(0,0,0,.7)}
.half{display:none;background:var(--c-bg);color:var(--c-fg);height:100%;flex-direction:column}
.card[data-show=dark] .half[data-mode=dark],.card[data-show=light] .half[data-mode=light]{display:flex}
.shot{display:block;aspect-ratio:16/9;background:var(--c-bg);overflow:hidden;border-bottom:1px solid color-mix(in srgb,var(--c-fg) 14%,transparent)}
.shot img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease}
.shot:hover img{transform:scale(1.025)}
.body{padding:18px 18px 16px;display:flex;flex-direction:column;gap:12px;flex:1}
.top{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
h2{margin:0;font-size:24px;letter-spacing:-.02em;font-weight:650}
h2::after{content:"";display:block;width:28px;height:3px;border-radius:2px;background:var(--c-accent);margin-top:8px}
.flip{all:unset;cursor:pointer;font:500 12px var(--mono);padding:5px 10px;border-radius:999px;white-space:nowrap;
border:1px solid color-mix(in srgb,var(--c-fg) 30%,transparent);color:var(--c-fg)}
.flip:hover{border-color:var(--c-accent)}
.tag{margin:0;color:color-mix(in srgb,var(--c-fg) 78%,var(--c-bg));font-size:15px}
.swatches{display:flex;flex-wrap:wrap;gap:6px;padding:0;margin:0;list-style:none}
.swatches button{all:unset;cursor:pointer;width:26px;height:26px;border-radius:7px;background:var(--s);
box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--c-fg) 22%,transparent);position:relative}
.swatches button:hover,.swatches button:focus-visible{transform:translateY(-2px)}
.links{display:flex;flex-wrap:wrap;gap:8px 16px;margin-top:auto;font:500 13px var(--mono)}
.links a{text-decoration:none;color:var(--c-accent)}
.links a:hover{text-decoration:underline}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);opacity:0;
background:var(--fg);color:var(--bg);font:500 13px var(--mono);padding:8px 14px;border-radius:999px;
transition:all .2s ease;pointer-events:none;z-index:9}
.toast.on{opacity:1;transform:translateX(-50%)}
.extras{border-top:1px solid var(--line);padding:36px 0 12px}
.extras h3{font:500 12px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin:0 0 16px}
.extras ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:16px}
.extras li{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}
.extras a{font-weight:600;text-decoration:none}.extras a:hover{text-decoration:underline}
.extras p{margin:6px 0 0;color:var(--dim);font-size:14px}
footer{color:var(--dim);font:13px var(--mono);padding:28px 0 48px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = """
const cards=[...document.querySelectorAll('.card')];
const seg=[...document.querySelectorAll('.seg button')];
function setAll(mode){cards.forEach(c=>c.dataset.show=mode);seg.forEach(b=>b.setAttribute('aria-pressed',b.dataset.mode===mode));
try{localStorage.setItem('rices-mode',mode)}catch(_){}}
let start='dark';try{start=localStorage.getItem('rices-mode')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark')}catch(_){}
setAll(start);
seg.forEach(b=>b.addEventListener('click',()=>setAll(b.dataset.mode)));
document.querySelectorAll('.flip').forEach(b=>b.addEventListener('click',()=>{
const c=b.closest('.card');c.dataset.show=c.dataset.show==='dark'?'light':'dark';
c.querySelector(`.half[data-mode=${c.dataset.show}] .flip`).focus()}));
const toast=document.querySelector('.toast');let t;
document.querySelectorAll('.swatches button').forEach(b=>b.addEventListener('click',async()=>{
let msg=b.dataset.hex+' copied';try{await navigator.clipboard.writeText(b.dataset.hex)}catch(_){msg=b.dataset.hex}
toast.textContent=msg;toast.classList.add('on');clearTimeout(t);t=setTimeout(()=>toast.classList.remove('on'),1400)}));
"""


def half(r, other, owner, branch):
    full = f"https://raw.githubusercontent.com/{owner}/{r['repo']}/{branch}/assets/screenshot.png"
    repo = f"https://github.com/{owner}/{r['repo']}"
    sw = "".join(
        f'<li><button type="button" style="--s:{p["hex"]}" data-hex="{p["hex"]}" '
        f'title="{e(p["role"])} {p["hex"]}" aria-label="Copy {e(p["role"])} {p["hex"]}"></button></li>'
        for p in r["palette"])
    links = [f'<a href="{repo}">Repository</a>', f'<a href="{repo}#setup">Install</a>']
    if r["amo"]:
        links.append(f'<a href="{e(r["amo"])}">Firefox add-on</a>')
    flip = (f'<button type="button" class="flip" aria-label="Show {e(other["name"])}, the '
            f'{other["mode"]} half">{"☀ " if other["mode"] == "light" else "☾ "}{e(other["name"])}</button>') if other else ""
    return f"""
      <div class="half" data-mode="{r['mode']}" style="--c-bg:{r['bg']};--c-fg:{r['text']};--c-accent:{r['accent']}">
        <a class="shot" href="{full}" aria-label="Full-size screenshot of {e(r['name'])}">
          <img src="thumbs/{r['repo']}.jpg" width="960" height="540" loading="lazy" alt="Pop!_OS COSMIC desktop with the {e(r['name'])} theme">
        </a>
        <div class="body">
          <div class="top"><h2>{e(r['name'])}</h2>{flip}</div>
          <p class="tag">{e(r['tagline'][:1].upper() + r['tagline'][1:])}</p>
          <ul class="swatches" aria-label="{e(r['name'])} palette">{sw}</ul>
          <div class="links">{''.join(links)}</div>
        </div>
      </div>"""


def page(rices, owner, branch):
    by = {r["repo"]: r for r in rices}
    pairs = []
    for r in rices:
        if r["mode"] == "dark":
            pairs.append((r, by.get(r["pair"])))
    pairs.sort(key=lambda p: p[0]["name"].lower())
    cards = "".join(
        f'\n    <article class="card" data-show="dark" aria-label="{e(d["name"])} and {e(l["name"] if l else "")}">'
        f'{half(d, l, owner, branch)}{half(l, d, owner, branch) if l else ""}\n    </article>'
        for d, l in pairs)
    extras = "".join(
        f'<li><a href="https://github.com/{owner}/{slug}">{e(t)}</a><p>{e(d)}</p></li>' for slug, t, d in EXTRAS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>COSMIC Rices</title>
<meta name="description" content="{len(pairs)} paired dark and light themes for the COSMIC desktop on Pop!_OS: desktop, terminals, shell, editors, browsers and apps.">
<meta name="theme-color" content="#0f0f11">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eyebrow">Pop!_OS · COSMIC desktop</div>
    <h1>COSMIC Rices</h1>
    <p class="lede">{len(pairs)} themes, each with a dark and a light half. One rice recolours the whole
    desktop: COSMIC itself, terminals, shell, editors, Firefox, Brave, GTK and Qt apps, cursors and wallpapers.</p>
  </header>
  <div class="bar">
    <span class="count">{len(rices)} rices · {len(pairs)} pairs</span>
    <div class="seg" role="group" aria-label="Show every rice as">
      <button type="button" data-mode="dark" aria-pressed="true">☾ Night</button>
      <button type="button" data-mode="light" aria-pressed="false">☀ Day</button>
    </div>
  </div>
  <main class="grid">{cards}
  </main>
  <section class="extras">
    <h3>Also for COSMIC</h3>
    <ul>{extras}</ul>
  </section>
  <footer>Generated from the theme repositories. Click a swatch to copy its colour; click a screenshot for full size.</footer>
</div>
<div class="toast" role="status" aria-live="polite"></div>
<script>{JS}</script>
</body>
</html>
"""
