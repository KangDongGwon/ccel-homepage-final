# CCEL homepage, DK final drafts (261110): three themes (Awesomic, Intercom, Mercury) over one shared function layer.
#   function layer : Jinuk's ccel-s1 (github.com/jinukmoon/ccel-s1, cloned 261110 into ../_ref_261110/ccel-s1):
#                    _shared/content.js (all lab data), assets/site.js + per-page JS, the five inner pages.
#   home layout    : Kiheon's C draft (qheosldia-lab.github.io/ccel-preview/C.html) sections, rebuilt from content.js.
#   design + motion: ours (mockups_261012/build_mockups.py tokens, 261026 scroll motion), src/*.css, src/*.js.
# Output: <theme>/index.html + the five inner pages, _shared/ once at the top, index.html = comparison page.
# Rebuild: python build_final.py   (then open index.html through a local server; file:// breaks on the '#' in the path)
import io, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(os.path.dirname(HERE), "_ref_261110", "ccel-s1")
MOCK = os.path.join(os.path.dirname(HERE), "mockups_261012", "img")
SRC = os.path.join(HERE, "src")
LENIS = "https://unpkg.com/lenis@1.1.20/dist/lenis.min.js"
GF = "https://fonts.googleapis.com/css2?"
INNER = ["professor.html", "members.html", "research.html", "publications.html", "contact.html"]
JS = ["site.js", "professor.js", "people.js", "research.js", "pubs.js", "contact.js"]
KO = "'S-CoreDream', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

THEMES = [
 dict(key="awesomic", label="Awesomic", hero="hero_particle.jpg",
   note="밝은 회색 바탕에 주황·자홍 빛, 둥근 흰 카드, 서체 Bricolage Grotesque + DM Sans",
   fonts=GF + "family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap",
   vars=f"""--ccel-font:'DM Sans',{KO};--dfont:'Bricolage Grotesque',{KO};
   --bg:#f1f1f3;--page:radial-gradient(1100px 700px at 92% 0%,rgba(255,90,0,.36),transparent 62%),radial-gradient(900px 640px at -6% 18%,rgba(254,69,226,.20),transparent 60%),radial-gradient(1000px 900px at 100% 48%,rgba(255,160,60,.18),transparent 60%),radial-gradient(900px 900px at 0% 80%,rgba(254,69,226,.12),transparent 60%),linear-gradient(170deg,#fff3e8 0%,#f6f4f6 40%,#f1e8f5 100%);
   --ink:#09090b;--navy:#09090b;--navy-deep:#09090b;--muted:#52525b;--rule:#e4e4e7;--rule-strong:#d4d4d8;--band:#f4f4f5;
   --accent:#ff5a00;--accent-ink:#c2410c;--surface:#fff;--surface-2:#f4f4f5;--hdr-bg:#fff;--hdr-line:rgba(9,9,11,.06);
   --r-card:28px;--r-btn:14px;--w-display:700;--track:-.03em;--display:clamp(38px,4.4vw,62px);
   --pill-bg:#ff5a00;--pill-ink:#fff;--tile-bg:linear-gradient(140deg,#ff7a1a 0%,#e0389f 100%);--join-bg:linear-gradient(135deg,#ff5a00 0%,#e0389f 100%);--join-ink:#fff;--ftr-bg:#09090b""",
   css="""
.hero{background:#fff;border:1px solid var(--rule);border-radius:36px;padding:52px;margin-top:20px;box-shadow:0 4px 24px rgba(0,0,0,.05)}
.hero-media{border-radius:24px}
.home .sec.panel>.wrap>.box{background:rgba(255,255,255,.72);border:1px solid rgba(9,9,11,.06);border-radius:36px;padding:52px;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.rlist{border-top:0}.rlist li{border-bottom-color:var(--rule)}.rlist a{border-radius:18px}
.newslist li::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--accent);margin-right:12px;vertical-align:middle}
.newslist li p{display:inline}
.joinbox .btn{border-color:rgba(255,255,255,.6)}
.page-head h1{font-size:clamp(40px,5vw,72px);font-weight:700}
.page-head .wrap{background:#fff;border:1px solid var(--rule);border-radius:36px;padding:44px 52px;margin-top:20px;box-shadow:0 4px 24px rgba(0,0,0,.04)}
.inner>.wrap,.inner>section>.wrap{background:rgba(255,255,255,.78);border-radius:36px;margin-top:20px;margin-bottom:20px;padding-top:12px;padding-bottom:12px}
.cite-thumb img,.mrow-photo,.mrow-photo img,.area-fig img,.profile-photo img,.group-photo img{border-radius:18px}
.subnav [aria-selected="true"],.site-nav a[aria-current="page"]{border-bottom-color:var(--accent)}
@media(max-width:768px){.hero,.page-head .wrap{padding:26px;border-radius:24px}.home .sec.panel>.wrap>.box{padding:26px;border-radius:24px}}
"""),
 dict(key="intercom", label="Intercom", hero="hero_lattice.jpg",
   note="크림·리넨 바탕, 아주 큰 제목과 검은 가는 선, 서체 Schibsted Grotesk",
   fonts=GF + "family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..900&display=swap",
   vars=f"""--ccel-font:'Schibsted Grotesk',{KO};--dfont:'Schibsted Grotesk',{KO};
   --bg:#f4f1ec;--page:radial-gradient(1100px 700px at 100% 0%,rgba(0,7,203,.18),transparent 62%),radial-gradient(900px 640px at -6% 30%,rgba(226,150,90,.18),transparent 60%),radial-gradient(1000px 900px at 104% 70%,rgba(0,7,203,.10),transparent 60%),linear-gradient(180deg,#fcfbf9 0%,#f1ebe1 50%,#e6dccd 100%);
   --ink:#111;--navy:#111;--navy-deep:#111;--muted:#585858;--rule:#d9d5ce;--rule-strong:#111;--band:#efe9df;
   --accent:#0007cb;--accent-ink:#0007cb;--surface:#fbfaf8;--surface-2:#efe9df;--hdr-bg:#f7f4ef;--hdr-line:#d9d5ce;
   --r-card:4px;--r-btn:4px;--w-display:500;--track:-.04em;--display:clamp(46px,7.4vw,112px);
   --pill-bg:transparent;--pill-ink:#111;--tile-bg:linear-gradient(140deg,#0007cb 0%,#00035a 100%);--join-bg:#111;--join-ink:#f4f1ec;--ftr-bg:#111""",
   css="""
.hero{grid-template-columns:1fr;gap:40px;padding-top:56px}
.hero h1{max-width:12.5em;line-height:.98}
.hero .lead{margin:0;font-size:20px;max-width:30em}
.hero-text{display:grid;grid-template-columns:minmax(0,1fr);gap:28px}
.hero-media img{aspect-ratio:21/9}
.pill{border:1px solid #111;padding:5px 12px;margin-bottom:0;justify-self:start}
.stats{border-top:1px solid #111}
.home h2{font-size:clamp(40px,5vw,76px);letter-spacing:-.045em}
.rlist{border-top:1px solid #111}.rt{font-size:clamp(22px,2.3vw,34px)}
.rlist a:hover{background:#111;color:#f4f1ec}.rlist a:hover .rt,.rlist a:hover .rn,.rlist a:hover .rk,.rlist a:hover .rarrow{color:#f4f1ec}
.scard .simg{border-radius:2px}.selgrid{border-top:1px solid #111;padding-top:24px}
.newslist li:first-child{border-top-color:#111}
.page-head h1{font-size:clamp(52px,8vw,128px);letter-spacing:-.05em;line-height:.95}
.page-head:has(.profile) h1,.profile h1{font-size:clamp(36px,4.2vw,60px);letter-spacing:-.04em;line-height:1.05}
.page-head{border-bottom:1px solid #111}
.site-nav a[aria-current="page"],.subnav [aria-selected="true"]{border-bottom-color:#111}
.ghead,.vhead{border-bottom-color:#111}
.btn.primary:hover{background:var(--accent);border-color:var(--accent)}
"""),
 dict(key="mercury", label="Mercury", hero="hero_lattice.jpg",
   note="코발트 빛 어두운 남색, 사진 위에 얇고 넓은 제목, 서체 Archivo(넓은 폭) + Inter",
   fonts=GF + "family=Archivo:wdth,wght@62..125,100..900&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
   vars=f"""--ccel-font:'Inter',{KO};--dfont:'Archivo',{KO};--stretch:118%;
   --bg:#171721;--page:radial-gradient(1300px 760px at 74% -4%,rgba(82,102,235,.55),transparent 64%),radial-gradient(900px 640px at -8% 26%,rgba(140,82,235,.26),transparent 60%),radial-gradient(1100px 900px at 106% 60%,rgba(82,102,235,.24),transparent 60%),radial-gradient(900px 800px at 10% 92%,rgba(60,150,235,.18),transparent 60%),linear-gradient(180deg,#23233f 0%,#171721 40%,#0d0d14 100%);
   --ink:#ededf3;--navy:#fff;--navy-deep:#0d0d14;--muted:#b9b9c6;--rule:rgba(112,112,125,.35);--rule-strong:rgba(160,160,180,.5);--band:#1e1e2a;
   --accent:#8f9cf5;--accent-ink:#b4bdfa;--surface:#1e1e2a;--surface-2:#272735;--on-strong:#0d0d14;--hdr-bg:#171721;--hdr-line:rgba(112,112,125,.3);
   --r-card:12px;--r-btn:32px;--w-display:300;--track:0;--display:clamp(36px,4.2vw,64px);
   --btn-bg:#5266eb;--btn-ink:#fff;--tile-bg:linear-gradient(140deg,#5266eb 0%,#2b2f78 100%);--pill-bg:rgba(255,255,255,.1);--pill-ink:#fff;--join-bg:linear-gradient(160deg,#5266eb 0%,#3a3f9e 100%);--join-ink:#fff;
   --ftr-bg:#0d0d14;--logo-filter:grayscale(1) brightness(0) invert(1)""",
   css="""
a{color:#c9d0ff;text-decoration-color:rgba(201,208,255,.35)}
.site-nav a{color:#d4d4de}.site-nav a:hover,.site-nav a[aria-current="page"]{color:#fff}
.brand{background:#fff;border-radius:8px;padding:5px 9px}
.hero{display:block;min-height:calc(100vh - var(--hdr));padding:0;margin:0 calc(50% - 50vw);border-radius:0}
.hero-media{position:absolute;inset:0;border-radius:0}
.hero-media img{height:100%!important;aspect-ratio:auto}
.hero-media::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,13,20,.25) 0%,rgba(13,13,20,.55) 55%,#171721 100%),linear-gradient(90deg,rgba(13,13,20,.65) 0%,transparent 70%)}
.hero-text{position:relative;z-index:1;max-width:calc(1240px + 2*var(--gut));margin:0 auto;padding:16vh var(--gut) 0}
.hero h1{max-width:13em}
.hero .lead{color:#d6d6e0}
.stats{position:relative;z-index:1;max-width:calc(1240px + 2*var(--gut));margin:9vh auto 0;padding:28px var(--gut) 40px;border-top:0}
.stats::before{content:"";position:absolute;left:var(--gut);right:var(--gut);top:0;border-top:1px solid var(--rule-strong)}
.js [data-ri]{clip-path:none}
.btn{background:#272735;border-color:#272735;color:#fff}
.rlist a:hover{background:rgba(143,156,245,.1)}
.scard .simg:not(.is-tile){background:#272735}
.home .sec.alt{background:linear-gradient(180deg,transparent,rgba(30,30,42,.6) 20%,rgba(30,30,42,.6) 80%,transparent)}
.covers .track img{border-color:transparent}
.partners .track img{filter:none;opacity:1;background:#fff;padding:8px 14px;height:46px;border-radius:8px}
.filters input[type="search"],.filters select{color:var(--ink);border-color:var(--rule-strong)}
.cite-thumb img,.cover-grid img{border-color:transparent}
.profile-photo img{background:#272735}
"""),
]

HOME = """<!doctype html>
<html lang="en" class="t-{key}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>CCEL · {label}</title>
{head}
</head>
<body class="home">
<div class="progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
{header}
<main id="main">
  <div class="wrap">
    <section class="hero" id="top">
      <div class="hero-text">
        <p class="pill">Seoul National University · Materials Science and Engineering</p>
        <h1>Catalysts and energy materials, designed with AI, simulation, and experiment</h1>
        <p class="lead" id="tagline"></p>
        <div class="cta"><a class="btn primary" href="research.html">Explore research</a><a class="btn" href="publications.html">Publications</a></div>
      </div>
      <figure class="hero-media"><img src="../_shared/dk/{hero}" alt="" width="1600" height="1000"></figure>
      <div class="stats" id="stats"></div>
    </section>
  </div>

  <section class="sec panel" id="approach"><div class="wrap"><div class="box approach">
    <div><p class="eyebrow">Our approach</p><h2>Design, predict, validate</h2><p id="approach-text"></p><a class="btn" href="research.html">How we work</a></div>
    <img src="../_shared/dk/approach.jpg" alt="Research loop: AI, computational materials design, experimental validation and analysis" loading="lazy">
  </div></div></section>

  <section class="sec research alt" id="research"><div class="wrap">
    <div class="sec-top"><h2>Research</h2><a class="btn" href="research.html">All research areas</a></div>
    <ol class="rlist" id="rlist"></ol>
  </div></section>
  <div class="rpeek" aria-hidden="true"><img alt=""></div>

  <section class="sec panel"><div class="wrap"><div class="box two">
    <div><div class="sec-top"><h2>News</h2></div><ul class="newslist" id="news"></ul></div>
    <aside class="joinbox" id="join"><p class="eyebrow">Open positions</p><h3>Join CCEL</h3><p id="join-ko" lang="ko"></p><a class="btn" id="join-mail" href="#"></a></aside>
  </div></div></section>

  <section class="sec selected"><div class="wrap">
    <div class="sec-top"><h2>Selected publications</h2><a class="btn" href="publications.html#selected">All selected</a></div>
    <div class="selgrid" id="selgrid"></div>
  </div></section>

  <section class="sec covers alt"><div class="wrap">
    <div class="sec-top"><h2>Journal covers</h2><a class="btn" id="cov-all" href="publications.html#covers">All covers</a></div>
  </div>
    <div class="marquee"><div class="track" id="cov1"></div></div>
    <div class="marquee rev"><div class="track" id="cov2"></div></div>
  </section>

  <section class="sec partners"><div class="wrap"><p class="eyebrow">Funding and partners</p></div>
    <div class="marquee"><div class="track" id="spon"></div></div>
  </section>

  <section class="sec panel"><div class="wrap"><div class="box about">
    <div><p class="eyebrow">About CCEL</p><h2 lang="ko">계산촉매 및 첨단소재설계 연구실</h2><p id="about-ko" lang="ko"></p></div>
    <div class="films" id="films"></div>
  </div></div></section>
</main>
<footer class="site-ftr" id="site-ftr"></footer>
<script src="../_shared/content.js"></script>
<script src="assets/site.js"></script>
<script src="../_shared/dk/home.js"></script>
<script src="../_shared/dk/motion.js"></script>
</body>
</html>
"""

def head(t):
    return (f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="{t["fonts"]}">\n'
            '<link rel="stylesheet" href="../_shared/brand/brand.css">\n<link rel="stylesheet" href="assets/site.css">\n'
            '<link rel="stylesheet" href="../_shared/dk/bridge.css">\n<link rel="stylesheet" href="../_shared/dk/home.css">\n'
            '<link rel="stylesheet" href="assets/theme.css">\n'
            "<script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('js')</script>\n"
            f'<script defer src="{LENIS}"></script>')

def header_from(page_html, current):
    m = re.search(r'<header class="site-hdr">.*?</header>', page_html, flags=re.S)
    h = m.group(0).replace('src="_shared/', 'src="../_shared/').replace(' aria-current="page"', '')
    return h.replace(f'<a href="{current}">', f'<a href="{current}" aria-current="page">')

def inner_page(src, t):
    s = src.replace('href="_shared/', 'href="../_shared/').replace('src="_shared/', 'src="../_shared/')
    s = re.sub(r'<link rel="stylesheet" href="\.\./_shared/brand/brand\.css">\s*<link rel="stylesheet" href="assets/site\.css">',
               head(t), s, count=1)
    s = re.sub(r'<title>(.*?) · CCEL</title>', lambda m: f'<title>{m.group(1)} · CCEL {t["label"]}</title>', s)
    s = s.replace('<body>', f'<body class="page t-{t["key"]}">\n<div class="progress" aria-hidden="true"></div>', 1)
    s = s.replace('</body>', '<script src="../_shared/dk/motion.js"></script>\n</body>', 1)
    assert "../_shared/dk/bridge.css" in s, "head swap failed"
    return s

def compare(ts):
    tabs = "".join(f'<button data-key="{t["key"]}" data-note="{t["note"]}">{t["label"]}</button>' for t in ts)
    pages = "".join(f'<option value="{p}">{p.split(".")[0].capitalize()}</option>' for p in ["index.html"] + INNER)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>CCEL 강동권 최종안 3종</title><style>
:root{{--bar:#13235B;--on:#f0b429}}
body{{margin:0;font-family:'Malgun Gothic',system-ui,sans-serif;background:#eee;display:flex;flex-direction:column;height:100vh}}
.bar{{display:flex;gap:8px;align-items:center;padding:10px 14px;background:var(--bar);color:#fff;flex-wrap:wrap}}
.bar b{{margin-right:10px}} button,select,a.open{{border:0;border-radius:6px;padding:8px 14px;font:inherit;font-size:13px;cursor:pointer;background:#2b3d7c;color:#fff;text-decoration:none}}
button.on{{background:var(--on);color:var(--bar);font-weight:700}} #note{{margin-left:auto;font-size:13px;opacity:.9}}
iframe{{flex:1;border:0;width:100%;background:#fff}}</style></head><body>
<div class="bar"><b>CCEL 최종안 3종 (강동권)</b>{tabs}<select id="pg" aria-label="쪽">{pages}</select><a class="open" id="open" target="_blank">새 창</a><span id="note"></span></div>
<iframe id="f" title="시안"></iframe>
<script>const b=[...document.querySelectorAll('button')],f=document.getElementById('f'),n=document.getElementById('note'),pg=document.getElementById('pg'),op=document.getElementById('open');let cur=b[0];
function go(x){{cur=x;b.forEach(y=>y.classList.toggle('on',y===x));const u=x.dataset.key+'/'+pg.value;f.src=u;op.href=u;n.textContent=x.dataset.note;}}
b.forEach(x=>x.onclick=()=>go(x));pg.onchange=()=>go(cur);go(b[0]);
document.addEventListener('keydown',e=>{{if(e.target.tagName==='SELECT')return;const i=b.indexOf(cur);if(e.key==='ArrowRight')go(b[(i+1)%b.length]);if(e.key==='ArrowLeft')go(b[(i+b.length-1)%b.length]);}});</script></body></html>"""

def build():
    # shared layer, once: Jinuk's data/images/fonts (without the S-series scroll frames) + our parts
    sh = os.path.join(HERE, "_shared")
    if os.path.isdir(sh): shutil.rmtree(sh)
    shutil.copytree(os.path.join(REF, "_shared"), sh, ignore=shutil.ignore_patterns("scroll", "content.json"))
    os.makedirs(os.path.join(sh, "dk"))
    for f in ("hero_particle.jpg", "hero_lattice.jpg", "hero_helix.jpg", "approach.jpg"):
        shutil.copy2(os.path.join(MOCK, f), os.path.join(sh, "dk", f))
    for f in ("bridge.css", "home.css", "home.js", "motion.js"):
        shutil.copy2(os.path.join(SRC, f), os.path.join(sh, "dk", f))
    for t in THEMES:
        d = os.path.join(HERE, t["key"])
        if os.path.isdir(d): shutil.rmtree(d)
        for f in JS:
            s = rd(os.path.join(REF, "assets", f))
            if f == "site.js": s = s.replace("var SHARED = '_shared/';", "var SHARED = '../_shared/';")
            wr(os.path.join(d, "assets", f), s)
        shutil.copy2(os.path.join(REF, "assets", "site.css"), os.path.join(d, "assets", "site.css"))
        wr(os.path.join(d, "assets", "theme.css"), f"/* DK theme: {t['label']} — tokens, then layout switches */\n:root{{{t['vars']}}}\n{t['css']}")
        for p in INNER:
            wr(os.path.join(d, p), inner_page(rd(os.path.join(REF, p)), t))
        hdr = header_from(rd(os.path.join(REF, "members.html")), "index.html")
        wr(os.path.join(d, "index.html"), HOME.format(key=t["key"], label=t["label"], head=head(t), header=hdr, hero=t["hero"]))
        wr(os.path.join(d, "robots.txt"), "User-agent: *\nDisallow: /\n")
    wr(os.path.join(HERE, "index.html"), compare(THEMES))
    wr(os.path.join(HERE, ".nojekyll"), "")
    print("built", len(THEMES), "themes in", HERE)

if __name__ == "__main__":
    build()
