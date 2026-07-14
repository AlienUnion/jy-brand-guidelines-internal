from __future__ import annotations

import json
import re
from pathlib import Path
from html import escape

import mistune
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
PAGES = ROOT / "pages"
ASSETS = ROOT / "assets"

markdown = mistune.create_markdown(plugins=["table", "strikethrough"])

PAGES.mkdir(exist_ok=True)

PAGE_DEFS = [
    {
        "slug": "constitution",
        "num": "01",
        "title": "品牌憲法",
        "en": "Brand Constitution",
        "file": "10_brand_constitution.md",
        "version": "v1.0",
        "status": "核心已定；標語待拍板",
        "lead": "定義眾悅是誰、相信什麼、為誰服務，以及所有表現層必須服從的核心。",
        "quick": [
            ("個性錨點", "持續進化的內行前輩。懂車、玩過、做過，也持續試新。"),
            ("價值排序", "齊、快、準、安心為恆常；新必須排在準確之後。"),
            ("使用判準", "任何文案與視覺都應能回扣核心，不得由 Logo 或既有風格反向定義品牌。"),
        ],
    },
    {
        "slug": "voice",
        "num": "02",
        "title": "語氣系統",
        "en": "Brand Voice",
        "file": "11_brand_voice.md",
        "version": "v2.0",
        "status": "完成",
        "lead": "讓所有內容保持同一人格，並依溝通情境調整音量，而不是切換成不同品牌。",
        "quick": [
            ("一句話", "先幫使用者判斷，再讓他購買；規格講清楚，不用浮誇承諾。"),
            ("新品公式", "新事物＋驗證動作＋判斷結論，缺一即不合格。"),
            ("絕對紅線", "禁止永久、100%、最、假原廠、療效式或無法證明的宣稱。"),
        ],
    },
    {
        "slug": "color",
        "num": "03",
        "title": "色彩系統",
        "en": "Color System",
        "file": "12_color_system.md",
        "version": "v1.0",
        "status": "完成；萊姆綠待實測決定是否啟用",
        "lead": "以中性骨幹建立可信度，鋼青建立辨識，萊姆綠只承擔受限的進化訊號。",
        "quick": [
            ("比例", "中性約 75%／鋼青約 20%／萊姆綠低於 5%。"),
            ("文字安全", "內文使用墨黑、石墨或深階鋼青；亮階鋼青禁止排文字。"),
            ("訊號色", "萊姆綠只當底，不當字，不作大面積背景。"),
        ],
    },
    {
        "slug": "typography",
        "num": "04",
        "title": "字體系統",
        "en": "Typography",
        "file": "13_typography.md",
        "version": "v1.0",
        "status": "完成",
        "lead": "中英文共用 IBM Plex Sans TC，以單一家族、完整字重與明確層級降低執行差異。",
        "quick": [
            ("唯一字體", "除 Plex 家族外不引入第二套字體。"),
            ("主標做法", "Bold＋4–6 字＋字距微收；禁止水平壓縮。"),
            ("內文規則", "Regular／Text 為主，中文行距至少 1.6 倍。"),
        ],
    },
    {
        "slug": "grid",
        "num": "05",
        "title": "版面網格",
        "en": "Layout Grid",
        "file": "14_layout_grid.md",
        "version": "v1.0",
        "status": "完成",
        "lead": "以 8pt 系統、欄位與留白建立跨畫布可攜的空間紀律。",
        "quick": [
            ("基準", "間距、尺寸與位移使用 8 的倍數；4pt 只作光學微調。"),
            ("欄位", "窄 4–6 欄／中 8 欄／寬 12 欄，跨畫布只調欄數。"),
            ("層級", "只用尺寸、字重、空間建立，不靠裝飾堆疊。"),
        ],
    },
    {
        "slug": "logo",
        "num": "06",
        "title": "Logo 使用規則",
        "en": "Logo Usage",
        "file": "16_logo_usage.md",
        "version": "v1.2",
        "status": "介面契約完成",
        "lead": "定義版式如何容納 Logo、何時切換變體、哪些操作絕對禁止；不反向定義 Logo 造型。",
        "quick": [
            ("必要狀態", "完整版、標記版、單色版、反白版。"),
            ("安全區", "以中文字面高度 x 為單位，四邊至少 1x。"),
            ("禁止", "不可變形、改色、加效果、重繪或低於最小辨識門檻。"),
        ],
    },
    {
        "slug": "iconography",
        "num": "07",
        "title": "圖示與圖形語彙",
        "en": "Iconography & Graphic Vocabulary",
        "file": "17_iconography.md",
        "version": "v1.0",
        "status": "完成；素材庫另建",
        "lead": "建立眾悅圖示的共同文法，而不是用裝飾母題填滿畫面。",
        "quick": [
            ("路線", "線性為主、填色為輔，不設品牌專屬裝飾母題。"),
            ("一致性", "全庫保持單一描邊、轉角、端點與視覺重量。"),
            ("訊號色", "萊姆綠只用於訊號角標，永不作一般圖示填色。"),
        ],
    },
    {
        "slug": "imagery",
        "num": "08",
        "title": "影像風格",
        "en": "Imagery Principles",
        "file": "18_imagery.md",
        "version": "v1.0",
        "status": "原則完成；案例可後補",
        "lead": "以識別／產品軌建立跳出，以實證／過程軌建立可信度，兩軌共享同一套紀律。",
        "quick": [
            ("識別軌", "無事實可標的產品、規格、陳列內容，一律乾淨冷冽。"),
            ("實證軌", "只有具真實過程或實測事實的內容，才允許現場暖調與雜訊。"),
            ("誠實紅線", "前後比較需同條件；不得用素材庫或 AI 影像冒充自家實作。"),
        ],
    },
]

NAV_GROUPS = [
    ("快速入口", [
        ("首頁", "index.html", "home"),
        ("快速檢核", "pages/checks.html", "checks"),
        ("資產中心", "pages/resources.html", "resources"),
    ]),
    ("母法八章", [(f"{p['num']} {p['title']}", f"pages/{p['slug']}.html", p["slug"]) for p in PAGE_DEFS]),
    ("治理", [
        ("狀態與版本", "pages/status.html", "status"),
        ("共用方法論", "pages/methodology.html", "methodology"),
        ("更新紀錄", "pages/changelog.html", "changelog"),
    ]),
]


def rel_prefix(is_root: bool) -> str:
    return "" if is_root else "../"


def build_nav(active: str, is_root: bool) -> str:
    prefix = rel_prefix(is_root)
    groups = []
    for label, items in NAV_GROUPS:
        links = []
        for text, path, key in items:
            href = prefix + path
            num_match = re.match(r"^(\d+)\s+(.*)$", text)
            if num_match:
                label_html = f'<span class="nav-num">{num_match.group(1)}</span><span>{escape(num_match.group(2))}</span>'
            else:
                label_html = f'<span>{escape(text)}</span>'
            links.append(f'<a class="nav-link{" active" if active == key else ""}" href="{href}">{label_html}</a>')
        groups.append(f'<div class="nav-group"><p class="nav-label">{escape(label)}</p>{"".join(links)}</div>')
    return "".join(groups)


def shell(*, active: str, title: str, content: str, is_root: bool = False, breadcrumb: str = "內部 Brand Guidelines") -> str:
    prefix = rel_prefix(is_root)
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="眾悅 Brand Guidelines 內部互動版">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <meta name="theme-color" content="#1a1d21">
  <title>{escape(title)}｜眾悅 Brand Guidelines</title>
  <link rel="icon" href="{prefix}assets/logo/JY_logo_mark_sq_primary.svg" type="image/svg+xml">
  <link rel="preload" href="{prefix}assets/fonts/PlexSansTC-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/PlexSansTC-700.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}assets/css/styles.css">
</head>
<body>
<a class="skip-link" href="#mainContent">跳到主要內容</a>
<div class="app-shell">
  <aside class="sidebar" aria-label="主要導覽">
    <div class="brand-panel">
      <img src="{prefix}assets/logo/JY_logo_full_h_primary.svg" alt="眾悅車品">
      <div class="brand-kicker">Internal Brand System</div>
      <p class="brand-title">Brand Guidelines<br>內部互動版</p>
      <span class="status-badge">Internal Beta · v0.1.0</span>
    </div>
    <div class="side-search"><button class="search-button" data-open-search><span>搜尋規則與資產</span><kbd>/</kbd></button></div>
    <nav class="nav-scroll">{build_nav(active, is_root)}</nav>
    <div class="sidebar-footer">B02 品牌策略部<br>更新：2026/07/13</div>
  </aside>
  <div class="mobile-overlay" data-menu-close></div>
  <main class="main" id="mainContent">
    <header class="topbar">
      <div><button class="icon-button menu-button" data-menu-toggle aria-label="開啟導覽">☰</button> <span class="breadcrumb">{escape(breadcrumb)}</span></div>
      <div class="top-actions">
        <button class="icon-button hide-mobile" data-open-search>搜尋</button>
        <button class="icon-button" data-print>列印</button>
      </div>
    </header>
    {content}
  </main>
</div>
<div class="search-modal" id="searchModal" aria-hidden="true" role="dialog" aria-modal="true" aria-label="全站搜尋">
  <div class="search-dialog">
    <div class="search-head"><input id="globalSearch" type="search" placeholder="搜尋：安全區、萊姆綠、主標、實證…"><button class="search-close" data-close-search aria-label="關閉">✕</button></div>
    <div class="search-results" id="searchResults"><div class="empty-state">輸入章節、規則、色值或關鍵字</div></div>
  </div>
</div>
<div class="toast" id="toast" aria-live="polite"></div>
<script src="{prefix}assets/js/search-index.js"></script>
<script src="{prefix}assets/js/app.js"></script>
</body>
</html>'''


def render_md(path: Path):
    raw = path.read_text(encoding="utf-8")
    raw_wo_title = re.sub(r"^# .+?\n+", "", raw, count=1)
    html = markdown(raw_wo_title)
    soup = BeautifulSoup(html, "html.parser")
    toc = []
    counter = 0
    for heading in soup.find_all(["h2", "h3"]):
        counter += 1
        heading_id = f"section-{counter}"
        heading["id"] = heading_id
        toc.append((heading.name, heading_id, heading.get_text(" ", strip=True)))
    return raw, str(soup), toc


def toc_html(items):
    if not items:
        return ""
    links = []
    for level, hid, text in items:
        links.append(f'<a class="toc-{level}" href="#{hid}">{escape(text)}</a>')
    return f'<aside class="toc"><div class="toc-title">本頁目錄</div>{"".join(links)}</aside>'


def quick_panel(items):
    blocks = "".join(f'<div class="quick-item"><strong>{escape(title)}</strong><p>{escape(text)}</p></div>' for title, text in items)
    return f'<section class="quick-panel"><h2>30 秒快速使用</h2><div class="quick-grid">{blocks}</div></section>'


def page_header(page):
    return f'''<div class="page-kicker">母法第 {int(page['num'])} 章 · {escape(page['en'])}</div>
<h1>{escape(page['title'])}</h1>
<p class="lead">{escape(page['lead'])}</p>
<div class="meta-row"><span><strong>版本</strong> {escape(page['version'])}</span><span><strong>狀態</strong> {escape(page['status'])}</span><span><strong>負責</strong> B02 品牌策略部</span></div>'''


def color_tool():
    colors = [
        ("墨黑 Ink", "#1A1D21", "dark"), ("石墨 Graphite", "#565B61", "dark"),
        ("霧底 Mist", "#F4F7F8", "light"), ("純白 White", "#FFFFFF", "light"),
        ("線框灰 Hairline", "#E3E6E8", "light"), ("亮階鋼青", "#1AA6B7", "light"),
        ("中階鋼青", "#148A9A", "dark"), ("深階鋼青", "#0E6A75", "dark"),
        ("萊姆綠訊號", "#DDF56B", "light"),
    ]
    swatches = "".join(f'<div class="swatch {tone}" style="background:{value}"><button data-copy="{value}">複製</button><strong>{escape(name)}</strong><span>{value}</span></div>' for name, value, tone in colors)
    return f'''<section aria-labelledby="colorTool"><h2 id="colorTool">快速色票</h2><p>點擊即可複製 HEX。色彩用途與禁區仍以本章條文為準。</p><div class="palette">{swatches}</div></section>'''


def typography_tool():
    return '''<section aria-labelledby="typeTool"><h2 id="typeTool">字體即時試排</h2>
<div class="notice info"><div><strong>顯示說明</strong>網站指定 IBM Plex Sans TC；未安裝的電腦會使用系統後備字體。這不改變規範指定字體。</div></div>
<div class="control-panel">
  <div class="control-row">
    <div class="control" style="flex:1"><label for="typeText">試排文字</label><input id="typeText" value="先幫你懂，再讓你買。JY 2026"></div>
    <div class="control"><label for="typeWeight">字重</label><select id="typeWeight"><option value="400">Regular 400</option><option value="450">Text 450</option><option value="500">Medium 500</option><option value="600">SemiBold 600</option><option value="700" selected>Bold 700</option></select></div>
    <div class="control"><label for="typeSize">字級 <span id="typeSizeValue"></span></label><input id="typeSize" type="range" min="16" max="96" value="42"></div>
  </div>
  <div class="preview-box type-preview" id="typePreview"></div>
</div></section>'''


def grid_tool():
    return '''<section aria-labelledby="gridTool"><h2 id="gridTool">欄位示範</h2>
<div class="control-panel"><div class="control-row"><div class="control"><label for="gridCount">欄數</label><select id="gridCount"><option value="4">4 欄｜窄畫布</option><option value="6">6 欄｜窄畫布</option><option value="8" selected>8 欄｜中畫布</option><option value="12">12 欄｜寬畫布</option></select></div></div>
<div class="grid-demo"><div class="grid-columns" id="gridColumns"></div><div class="grid-content"><div class="demo-block"><strong>主要資訊</strong><p>元素比例跨畫布守恆，只有欄數改變。</p></div><div class="demo-block"><strong>次要資訊</strong><p>所有間距取 8pt token。</p></div></div></div></div></section>'''


def logo_tool():
    options = [
        ("JY_logo_full_h_primary.svg", "橫式主色版"), ("JY_logo_full_h_mono.svg", "橫式單色版"), ("JY_logo_full_h_reverse.svg", "橫式反白版"),
        ("JY_logo_full_v_primary.svg", "直式主色版"), ("JY_logo_full_v_mono.svg", "直式單色版"), ("JY_logo_full_v_reverse.svg", "直式反白版"),
        ("JY_logo_mark_sq_primary.svg", "標記主色版"), ("JY_logo_mark_sq_mono.svg", "標記單色版"), ("JY_logo_mark_sq_reverse.svg", "標記反白版"),
    ]
    opts = "".join(f'<option value="{file}">{name}</option>' for file, name in options)
    return f'''<section aria-labelledby="logoTool"><h2 id="logoTool">Logo 預覽器</h2><p>此工具用於快速選擇正確資產與背景狀態，不取代最小尺寸與安全區條文。</p>
<div class="control-panel">
  <div class="control-row">
    <div class="control"><label for="logoAsset">資產</label><select id="logoAsset">{opts}</select></div>
    <div class="control"><label for="logoBackground">背景</label><select id="logoBackground"><option value="">白底</option><option value="dark-bg">深色底</option><option value="teal-bg">鋼青底</option><option value="photo-bg">暖色雜訊模擬</option></select></div>
    <div class="control"><label for="logoSize">顯示寬度</label><input id="logoSize" type="range" min="24" max="520" value="340"></div>
  </div>
  <div class="preview-box logo-preview" id="logoPreview"><img id="logoImage" alt="Logo 預覽"></div>
  <p><a class="download-link" id="logoDownload" href="#" download>下載目前 SVG</a></p>
</div></section>'''


def imagery_placeholders():
    items = [
        ("JY_img_identity_01.webp", "識別／產品軌｜單一產品"),
        ("JY_img_identity_02.webp", "識別／產品軌｜結構或套組"),
        ("JY_img_evidence_01.webp", "實證／過程軌｜施工過程"),
        ("JY_img_evidence_02.webp", "實證／過程軌｜實測結果"),
    ]
    cards = "".join(f'<div class="image-placeholder"><div><strong>{escape(label)}</strong>{escape(file)}<br>1600 × 1200 WebP<br><small>尚未上傳，不影響系統上線</small></div></div>' for file, label in items)
    return f'''<section aria-labelledby="imageryExamples"><h2 id="imageryExamples">影像案例位置</h2><div class="notice warn"><div><strong>非上線阻擋項</strong>影像案例可逐步補入。檔案放入 <code>assets/imagery/</code> 後即可取代占位卡。</div></div><div class="placeholder-grid">{cards}</div></section>'''


def build_guideline_page(page):
    raw, html_content, toc = render_md(CONTENT / page["file"])
    tool = ""
    if page["slug"] == "color": tool = color_tool()
    elif page["slug"] == "typography": tool = typography_tool()
    elif page["slug"] == "grid": tool = grid_tool()
    elif page["slug"] == "logo": tool = logo_tool()
    elif page["slug"] == "imagery": tool = imagery_placeholders()
    inner = f'''<div class="page"><div class="page-grid"><article class="article">{page_header(page)}{quick_panel(page['quick'])}{tool}<div class="content">{html_content}</div></article>{toc_html(toc)}</div></div>'''
    out = shell(active=page["slug"], title=page["title"], content=inner, breadcrumb=f"母法八章 / {page['title']}")
    (PAGES / f"{page['slug']}.html").write_text(out, encoding="utf-8")
    return raw


def build_index():
    cards = "".join(f'''<a class="nav-card" href="pages/{p['slug']}.html"><span class="card-num">{p['num']}</span><h3>{escape(p['title'])}</h3><p>{escape(p['lead'])}</p></a>''' for p in PAGE_DEFS)
    content = f'''<div class="page">
<section class="dashboard-hero">
  <div><div class="page-kicker">眾悅車用精品 JY · Internal Beta</div><h1>先找到正確規則，<br>再開始設計。</h1><p class="lead">提供悅聯內部人員與設計師快速查詢、判斷與下載的 Brand Guidelines。內容以母法八章為核心，通路、工具與產出規格另放子法。</p></div>
  <aside class="hero-side"><div class="eyebrow">CURRENT STATUS</div><h2>母法八章已完成</h2><p>標語、萊姆綠啟用與 Logo 人眼最小尺寸仍屬開放決策；不影響內部版上線。</p><a class="download-link" href="pages/status.html" style="border-color:white;color:white">查看狀態 →</a></aside>
</section>
<h2 class="section-title">母法八章</h2><div class="card-grid">{cards}</div>
<h2 class="section-title">常用工具</h2>
<div class="tool-grid">
  <div class="tool-card"><h3>全站搜尋</h3><p>按 <strong>/</strong> 或 Ctrl／⌘＋K，搜尋規則、禁區、色值與章節。</p><button class="secondary-button" data-open-search>開始搜尋</button></div>
  <div class="tool-card"><h3>快速檢核</h3><p>依色彩、字體、網格、Logo、影像與語氣掃描送審內容。</p><a class="download-link" href="pages/checks.html">開啟檢核</a></div>
  <div class="tool-card"><h3>資產中心</h3><p>預覽並下載 9 個核心 SVG，查看 Logo 子法與待補素材規格。</p><a class="download-link" href="pages/resources.html">前往資產</a></div>
</div>
<div class="notice info" style="margin-top:48px"><div><strong>母法三禁</strong>本網站的母法內容不得綁定通路平台、設計工具或最終產出格式。這三類只進子法。</div></div>
</div>'''
    (ROOT / "index.html").write_text(shell(active="home", title="首頁", content=content, is_root=True), encoding="utf-8")


def build_resources():
    _, child_html, child_toc = render_md(CONTENT / "19_logo_assets_child_rule.md")
    assets = [
        ("橫式主色版", "JY_logo_full_h_primary.svg", "L2 · Primary", False),
        ("橫式單色版", "JY_logo_full_h_mono.svg", "L2 · Mono", False),
        ("橫式反白版", "JY_logo_full_h_reverse.svg", "L2 · Reverse", True),
        ("直式主色版", "JY_logo_full_v_primary.svg", "L3 · Primary", False),
        ("直式單色版", "JY_logo_full_v_mono.svg", "L3 · Mono", False),
        ("直式反白版", "JY_logo_full_v_reverse.svg", "L3 · Reverse", True),
        ("標記主色版", "JY_logo_mark_sq_primary.svg", "L5 · Primary", False),
        ("標記單色版", "JY_logo_mark_sq_mono.svg", "L5 · Mono", False),
        ("標記反白版", "JY_logo_mark_sq_reverse.svg", "L5 · Reverse", True),
    ]
    cards = "".join(f'''<div class="asset-card"><div class="asset-thumb{' dark' if dark else ''}"><img src="../assets/logo/{file}" alt="{escape(name)}"></div><h3>{escape(name)}</h3><p>{escape(meta)}</p><a class="download-link" href="../assets/logo/{file}" download>下載 SVG</a></div>''' for name, file, meta, dark in assets)
    content = f'''<div class="page"><div class="page-grid"><article class="article">
<div class="page-kicker">Resources · 子法與資產</div><h1>資產中心</h1><p class="lead">集中提供可直接使用的官方資產。母法說明「何時可用」，本頁子法說明「檔案如何交付與管理」。</p>
<div class="meta-row"><span><strong>Logo 資產</strong> 9 個 SVG</span><span><strong>影像案例</strong> 可後補</span><span><strong>使用範圍</strong> 內部</span></div>
<div class="notice danger"><div><strong>禁止自行重製</strong>變體是已發放的檔案，不是允許設計師自行重組的操作。</div></div>
<h2>Logo 核心資產</h2><div class="asset-grid">{cards}</div>
<h2>待補影像素材</h2><p>以下素材不影響上線。補入既定路徑後，可逐步取代影像章的占位卡。</p>{imagery_placeholders()}
<hr><div class="content">{child_html}</div></article>{toc_html(child_toc)}</div></div>'''
    (PAGES / "resources.html").write_text(shell(active="resources", title="資產中心", content=content, breadcrumb="資產與子法 / Logo 素材"), encoding="utf-8")
    return (CONTENT / "19_logo_assets_child_rule.md").read_text(encoding="utf-8")


def checklist_group(title, key, items):
    rows = "".join(f'<label class="check-item"><input type="checkbox" value="{escape(str(i))}"><span>{escape(text)}</span></label>' for i, text in enumerate(items, 1))
    return f'''<section><h2>{escape(title)}</h2><div class="checklist" data-checklist="{key}">{rows}</div><div class="check-actions"><button class="secondary-button" data-reset-checklist="{key}">重設本組</button></div></section>'''


def build_checks():
    groups = [
        ("語氣", "voice", ["第一觸點一句內說清楚這是什麼、為什麼相關", "規格與適用條件完整", "新品內容符合新事物＋驗證動作＋判斷結論", "沒有永久、100%、最、假原廠或療效宣稱"]),
        ("色彩", "color", ["中性主導、鋼青識別、萊姆綠低於 5%", "沒有亮階鋼青排文字", "白字只壓深階鋼青", "萊姆綠只當訊號底，沒有當字或大面積背景"]),
        ("字體", "type", ["只使用 IBM Plex 家族", "沒有水平壓縮、垂直拉長或中文斜體", "內文使用 Regular／Text，主標不超長", "中英與數字混排保有適當間距"]),
        ("網格", "grid", ["間距與尺寸符合 8pt 系統", "元素對齊欄位與基線", "單一視覺焦點與單一動線", "層級由尺寸、字重與空間建立，不靠裝飾堆疊"]),
        ("Logo", "logo", ["使用官方 SVG，沒有重繪或自行組合", "色版與背景狀態正確", "安全區未被侵入", "未變形、旋轉、加陰影、外框或漸層", "未低於該變體的最小尺寸"]),
        ("圖示與影像", "visual", ["圖示描邊、轉角與重量一致", "萊姆綠沒有作一般圖示填色", "影像軌道判定正確", "實證內容有真實條件與事實", "沒有以素材庫或 AI 影像冒充自家實作"]),
    ]
    html = "".join(checklist_group(*g) for g in groups)
    content = f'''<div class="page"><div class="page-grid"><article class="article"><div class="page-kicker">Internal Review Tool</div><h1>快速檢核</h1><p class="lead">送審前快速掃描硬性紅線。勾選狀態只保存在目前瀏覽器，不會上傳資料。</p><div class="meta-row"><span><strong>用途</strong> 設計自檢與主管初審</span><span><strong>原則</strong> 紅線項通過率 100%</span></div>{html}</article></div></div>'''
    (PAGES / "checks.html").write_text(shell(active="checks", title="快速檢核", content=content, breadcrumb="內部工具 / 快速檢核"), encoding="utf-8")


def generic_md_page(slug, title, file, active, kicker, lead, breadcrumb):
    raw, html_content, toc = render_md(CONTENT / file)
    content = f'''<div class="page"><div class="page-grid"><article class="article"><div class="page-kicker">{escape(kicker)}</div><h1>{escape(title)}</h1><p class="lead">{escape(lead)}</p><div class="content">{html_content}</div></article>{toc_html(toc)}</div></div>'''
    (PAGES / f"{slug}.html").write_text(shell(active=active, title=title, content=content, breadcrumb=breadcrumb), encoding="utf-8")
    return raw


def build_changelog():
    data = json.loads((ROOT / "data/changelog.json").read_text(encoding="utf-8"))
    blocks = []
    for item in data:
        lis = "".join(f"<li>{escape(x)}</li>" for x in item["items"])
        blocks.append(f'<section><div class="page-kicker">{escape(item["date"])} · {escape(item["type"])}</div><h2>{escape(item["version"])}</h2><ul>{lis}</ul></section>')
    content = f'''<div class="page"><div class="page-grid"><article class="article"><div class="page-kicker">Version History</div><h1>更新紀錄</h1><p class="lead">記錄網站功能與內容版本。母法章節版號與網站版號分開管理。</p><div class="content">{"".join(blocks)}</div></article></div></div>'''
    (PAGES / "changelog.html").write_text(shell(active="changelog", title="更新紀錄", content=content, breadcrumb="治理 / 更新紀錄"), encoding="utf-8")


def build_search_index(raw_docs):
    items = []
    for title, url, text in raw_docs:
        clean = re.sub(r"[`#>*_|\[\]()]", " ", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        snippets = [s.strip() for s in re.split(r"[。！？\n]", clean) if len(s.strip()) > 12]
        if not snippets:
            snippets = [clean[:140]]
        items.append({"title": title, "url": url, "snippet": snippets[0][:120], "text": clean})
    js = "window.JY_SEARCH_INDEX = " + json.dumps(items, ensure_ascii=False) + ";\n"
    (ASSETS / "js/search-index.js").write_text(js, encoding="utf-8")


def main():
    raw_docs = []
    build_index()
    for page in PAGE_DEFS:
        raw = build_guideline_page(page)
        raw_docs.append((page["title"], f"pages/{page['slug']}.html", raw))
    raw_docs.append(("資產中心與 Logo 子法", "pages/resources.html", build_resources()))
    build_checks()
    raw_docs.append(("狀態與版本", "pages/status.html", generic_md_page("status", "狀態與版本", "15_status.md", "status", "Governance Status", "追蹤母法完成度、開放決策、子法待辦與網站載體狀態。", "治理 / 狀態與版本")))
    raw_docs.append(("共用方法論", "pages/methodology.html", generic_md_page("methodology", "共用方法論", "00_shared_methodology.md", "methodology", "Group Methodology", "悅聯全品牌共用的母法／子法邊界、單向依賴、版本治理與驗收方法。", "治理 / 共用方法論")))
    build_changelog()
    raw_docs.extend([
        ("快速檢核", "pages/checks.html", "語氣 色彩 字體 網格 Logo 圖示 影像 送審 自檢 紅線"),
        ("更新紀錄", "pages/changelog.html", (ROOT / "data/changelog.json").read_text(encoding="utf-8")),
    ])
    build_search_index(raw_docs)
    print(f"Built {len(PAGE_DEFS) + 6} pages in {ROOT}")


if __name__ == "__main__":
    main()
