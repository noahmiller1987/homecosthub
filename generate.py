#!/usr/bin/env python3
"""
HomeCostHub — pSEO generator (Plan B niche #1).
Generates "How much does [trade] cost in [city]" pages from a dataset.
4 trades x 5 metros = 20 pages + index + sitemap + robots. Static HTML, no build.

Scale plan: add cities to CITIES / trades to TRADES and re-run -> hundreds of pages.
DOMAIN is the only thing to swap once a domain is chosen (founder gate).
"""
import os, html, json

DOMAIN = "https://homecosthub.vercel.app"   # PLACEHOLDER — swap once founder picks a domain
BRAND = "HomeCostHub"
OUT = os.path.join(os.path.dirname(__file__), "web")
YEAR = "2026"

def money(n):
    return "$" + format(int(round(n / 50.0) * 50), ",")

def rng(lo, hi, idx):
    return f"{money(lo*idx)}–{money(hi*idx)}"

# ---------------------------------------------------------------- TRADES
TRADES = {
  "roof-replacement": {
    "noun": "roof replacement", "a": "a roof replacement",
    "kw": "roof replacement cost",
    "lo": 9000, "hi": 18000, "basis": "for a typical 2,000 sq ft single-family home",
    "intro": "Replacing a roof is one of the biggest exterior projects a homeowner takes on, and the price swings widely with material, roof size, pitch, and how many old layers have to be torn off.",
    "table_title": "Cost by roofing material",
    "table": [
      ("Asphalt shingle (3-tab / architectural)", 9000, 16000),
      ("Standing-seam metal", 16000, 30000),
      ("Clay or concrete tile", 18000, 40000),
      ("Wood shake", 20000, 35000),
    ],
    "factors": [
      ("Roof size (“squares”)", "Roofers price in 100 sq ft “squares.” A bigger or multi-story roof means more material and labor."),
      ("Material", "Asphalt is cheapest; metal, tile, and shake cost two to four times as much but last far longer."),
      ("Pitch & complexity", "Steep, cut-up roofs with lots of valleys, dormers, and skylights are slower and riskier to work on."),
      ("Tear-off & decking", "Stripping old layers and replacing rotted plywood decking adds labor and disposal cost."),
      ("Permits & labor rates", "Local permit fees and crew wages vary a lot by metro — the single biggest reason the same roof costs more in one city than another."),
    ],
    "faqs": [
      ("How much does a roof replacement cost in {city}?",
       "In {city}, replacing the roof on a typical single-family home runs about {range}, depending mainly on the material and the size and pitch of the roof. Asphalt shingle is the budget end; metal and tile sit at the top."),
      ("How long does a new roof last?",
       "Asphalt shingles last about 15–30 years, metal roofs 40–70 years, and tile 50+ years. Spending more on material usually buys you decades of extra life and fewer repairs."),
      ("What are the signs I need a new roof?",
       "Curling or missing shingles, granules collecting in gutters, daylight or water stains in the attic, sagging, and an age past 20 years are the common signals it is time to replace rather than patch."),
      ("Does home insurance cover roof replacement?",
       "Insurance typically covers sudden damage from a covered event like a storm or fallen tree, but not wear-and-tear or age. Document damage with photos and get an inspection before filing."),
    ],
  },
  "hvac-installation": {
    "noun": "HVAC installation", "a": "an HVAC installation",
    "kw": "HVAC installation cost",
    "lo": 7000, "hi": 14000, "basis": "for a full central system in an average home",
    "intro": "Installing or replacing a central heating and cooling system is a major mechanical job priced by system size (tonnage), efficiency rating, and the condition of your existing ductwork.",
    "table_title": "Cost by system type",
    "table": [
      ("Central AC only", 5500, 12000),
      ("AC + furnace (full system)", 8000, 16000),
      ("Heat pump", 6000, 14000),
      ("Ductless mini-split (multi-zone)", 5000, 15000),
    ],
    "factors": [
      ("System size (tonnage)", "Bigger homes need more cooling capacity. An oversized or undersized unit wastes money and wears out faster, so proper sizing matters."),
      ("Efficiency (SEER2)", "Higher-efficiency units cost more up front but cut monthly energy bills — often worth it in hot climates with long cooling seasons."),
      ("Ductwork", "Replacing or sealing old, leaky ducts adds cost; a ductless mini-split avoids ducts entirely."),
      ("Brand & equipment", "Premium brands and variable-speed equipment run higher than builder-grade units."),
      ("Permits & labor rates", "Mechanical permits and local install-crew wages drive much of the metro-to-metro price difference."),
    ],
    "faqs": [
      ("How much does HVAC installation cost in {city}?",
       "A full central HVAC system in {city} typically costs {range}. AC-only replacements land lower; high-efficiency systems with new ductwork sit at the top of the range."),
      ("How long does an HVAC install take?",
       "A straightforward replacement is usually a 1–2 day job. Adding or rerouting ductwork, or a first-time install, can stretch it to several days."),
      ("Is a higher SEER2 rating worth it?",
       "In hot, long-summer climates the energy savings from a higher-SEER2 unit can pay back the premium over the system's life. In mild climates the payback is slower."),
      ("How long does an AC unit last?",
       "Central AC units typically last 12–18 years and furnaces 15–20. Rising repair bills, uneven cooling, or a unit over 15 years old are signs it is time to replace."),
    ],
  },
  "kitchen-remodel": {
    "noun": "kitchen remodel", "a": "a kitchen remodel",
    "kw": "kitchen remodel cost",
    "lo": 15000, "hi": 45000, "basis": "for a mid-range remodel",
    "intro": "Kitchen remodels span an enormous range — from a cosmetic refresh to a gut renovation that moves walls and plumbing. Scope, cabinetry, and finishes drive nearly all of the cost.",
    "table_title": "Cost by remodel tier",
    "table": [
      ("Minor / cosmetic (paint, hardware, counters)", 10000, 20000),
      ("Mid-range (new cabinets, counters, appliances)", 25000, 45000),
      ("Major / upscale (layout change, custom)", 50000, 100000),
    ],
    "factors": [
      ("Scope", "A cosmetic refresh costs a fraction of a full gut. Moving the sink, range, or walls triggers plumbing, electrical, and permits."),
      ("Cabinets", "Cabinetry is usually the single biggest line item — stock, semi-custom, and custom can differ by 3–4x."),
      ("Countertops & appliances", "Quartz, granite, and pro-grade appliances add up quickly versus laminate and standard models."),
      ("Layout & structural changes", "Removing walls, relocating utilities, or expanding the footprint adds labor, permits, and engineering."),
      ("Finishes & labor rates", "Tile, lighting, flooring choices and local contractor wages set whether you land at the low or high end."),
    ],
    "faqs": [
      ("How much does a kitchen remodel cost in {city}?",
       "A mid-range kitchen remodel in {city} typically runs {range}. Cosmetic refreshes cost less; major layout changes with custom cabinetry run well above it."),
      ("Does a kitchen remodel add resale value?",
       "Kitchens are among the highest-ROI remodels, with minor and mid-range projects generally recouping more of their cost than high-end gut jobs at resale."),
      ("How long does a kitchen remodel take?",
       "A cosmetic update can be 1–2 weeks; a mid-range remodel 4–6 weeks; a major renovation with layout changes 8–12 weeks or more once permits and custom orders are factored in."),
      ("What is the most expensive part of a kitchen remodel?",
       "Cabinetry is usually the largest single cost, followed by countertops and appliances. Layout changes that move plumbing or electrical add the most unexpected expense."),
    ],
  },
  "water-heater-replacement": {
    "noun": "water heater replacement", "a": "a water heater replacement",
    "kw": "water heater replacement cost",
    "lo": 1200, "hi": 3500, "basis": "installed, for a standard home",
    "intro": "Replacing a water heater is a smaller but essential project. The biggest cost drivers are whether you choose a traditional tank or a tankless unit, the fuel type, and any code upgrades the install triggers.",
    "table_title": "Cost by water heater type",
    "table": [
      ("Tank — gas", 1200, 2800),
      ("Tank — electric", 1100, 2500),
      ("Tankless — gas", 3000, 6000),
      ("Heat-pump / hybrid", 2500, 5000),
    ],
    "factors": [
      ("Tank vs tankless", "Tankless units cost more up front but last longer and save space and energy; tanks are cheaper to install."),
      ("Fuel type", "Gas, electric, and heat-pump models differ in unit price and in the venting or wiring they require."),
      ("Capacity", "Larger households need 50–80 gallon tanks or higher-output tankless units, raising the price."),
      ("Code upgrades", "An install can trigger an expansion tank, new venting, a drain pan, or seismic strapping — each adds cost."),
      ("Labor & permits", "Plumbing permits and local labor rates account for much of the difference between metros."),
    ],
    "faqs": [
      ("How much does it cost to replace a water heater in {city}?",
       "In {city}, a standard tank water heater replacement runs about {range} installed. Tankless and hybrid heat-pump units cost more up front but last longer and cut energy bills."),
      ("Is a tankless water heater worth it?",
       "Tankless units cost more to install but last 20+ years, never run out of hot water, and lower energy use. The payback is best for households with high or steady hot-water demand."),
      ("How long does a water heater replacement take?",
       "A like-for-like tank swap is usually a 2–3 hour job. Switching fuel types or going tankless takes longer because of new venting, gas lines, or wiring."),
      ("How long does a water heater last?",
       "Tank water heaters last about 8–12 years and tankless units 20+. Rusty water, rumbling, leaks, or an age past 10 years mean it is time to plan a replacement."),
    ],
  },
}

# ---------------------------------------------------------------- CITIES
CITIES = {
  "sacramento": {"name": "Sacramento, CA", "idx": 1.08,
    "note": "Sacramento's hot, dry summers make cooling and roofing systems work hard, and California's Title 24 energy code can push HVAC and re-roof projects toward higher-efficiency (and pricier) options. Labor rates sit above the national average, and city/county permits add time and cost."},
  "san-jose": {"name": "San Jose, CA", "idx": 1.40,
    "note": "San Jose carries some of the highest contractor labor rates in the country, plus strict California permitting and seismic requirements. Expect prices well above the national average across every home project here — demand and the cost of living both run hot."},
  "fresno": {"name": "Fresno, CA", "idx": 0.96,
    "note": "Fresno's Central Valley location means lower labor costs than coastal California metros, but brutal summer heat makes air conditioning essential and hard-working. It is one of the more affordable California markets for home projects while still under California's permit and energy rules."},
  "san-diego": {"name": "San Diego, CA", "idx": 1.22,
    "note": "San Diego's mild coastal climate is easy on equipment, but salt air can accelerate corrosion on rooftop HVAC and metal roofing. The high cost of living and California permitting keep project prices above the national average."},
  "phoenix": {"name": "Phoenix, AZ", "idx": 1.02,
    "note": "Phoenix's extreme desert heat makes air conditioning the most critical system in the home, often requiring larger tonnage and tile or foam roofing built for sun. Arizona permitting is generally lighter and faster than California's, keeping labor competitive."},
}

# ---------------------------------------------------------------- TEMPLATE
def page_html(tslug, t, cslug, c):
    idx = c["idx"]; cn = c["name"]; city_short = cn.split(",")[0]
    headline_range = rng(t["lo"], t["hi"], idx)
    slug = f"how-much-does-{tslug}-cost-in-{cslug}"
    url = f"{DOMAIN}/{slug}"
    title = f"How Much Does {t['noun'].title()} Cost in {city_short}? ({YEAR} Prices)"
    desc = (f"{t['noun'].title()} in {cn} typically costs {headline_range} {t['basis']}. "
            f"See {YEAR} price ranges, what drives the cost, and how to get local quotes.")
    rows = "".join(
        f'<tr class="border-b border-slate-200"><td class="py-2 pr-4">{html.escape(label)}</td>'
        f'<td class="py-2">{rng(lo,hi,idx)}</td></tr>'
        for (label, lo, hi) in t["table"])
    factors = "".join(
        f'<li><strong>{html.escape(f0)}:</strong> {html.escape(f1)}</li>'
        for (f0, f1) in t["factors"])
    faq_pairs = [(q.format(city=city_short), a.format(city=city_short, range=headline_range))
                 for (q, a) in t["faqs"]]
    faq_html = "".join(
        f'<div class="border-b border-slate-200 py-4"><h3 class="font-bold text-lg mb-1">{html.escape(q)}</h3>'
        f'<p class="text-slate-700">{html.escape(a)}</p></div>'
        for (q, a) in faq_pairs)
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for (q,a) in faq_pairs]}
    article_ld = {"@context":"https://schema.org","@type":"Article",
        "headline":title,"datePublished":"2026-06-16","dateModified":"2026-06-16",
        "author":{"@type":"Organization","name":BRAND},
        "publisher":{"@type":"Organization","name":BRAND,"url":DOMAIN},"description":desc}
    # other cities for this trade (internal links)
    other_cities = "".join(
        f'<a href="/how-much-does-{tslug}-cost-in-{oc}" class="text-emerald-700 underline">{CITIES[oc]["name"].split(",")[0]}</a>'
        + (", " if i < len(CITIES)-1 else "")
        for i, oc in enumerate(CITIES) )
    other_trades = "".join(
        f'<li><a href="/how-much-does-{ot}-cost-in-{cslug}" class="text-emerald-700 underline">{TRADES[ot]["noun"].title()} in {city_short}</a></li>'
        for ot in TRADES if ot != tslug)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}" />
<meta property="og:title" content="{html.escape(title)}" />
<meta property="og:description" content="{html.escape(desc)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<link rel="canonical" href="{url}" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E\U0001F3E0%3C/text%3E%3C/svg%3E" />
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>body{{font-family:Inter,system-ui,sans-serif}}</style>
<script type="application/ld+json">{json.dumps(article_ld)}</script>
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
</head>
<body class="antialiased text-slate-900 bg-white">
<header class="border-b border-slate-200 sticky top-0 bg-white/80 backdrop-blur z-50">
  <div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
    <a href="/" class="font-bold text-xl">\U0001F3E0 {BRAND}</a>
    <a href="/" class="text-sm text-slate-600 hover:text-slate-900">All cost guides</a>
  </div>
</header>
<article class="max-w-3xl mx-auto px-6 py-12">
  <div class="text-emerald-700 text-sm font-semibold uppercase tracking-wider mb-3">{YEAR} cost guide · {html.escape(cn)}</div>
  <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight leading-tight mb-4">How much does {t['noun']} cost in {html.escape(city_short)}?</h1>
  <p class="text-xl text-slate-600 leading-relaxed mb-6">In {html.escape(cn)}, {t['a']} typically costs <strong>{headline_range}</strong> {t['basis']}. {html.escape(t['intro'])}</p>

  <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-6 my-6">
    <p class="font-semibold text-emerald-900 mb-2">Get free {t['noun']} quotes from vetted {html.escape(city_short)} pros</p>
    <p class="text-slate-700 mb-4">Compare a few local quotes before you commit — prices for the same job vary widely between contractors.</p>
    <a href="#quote" data-affiliate="lead-gen-slot" class="inline-block bg-emerald-600 text-white font-semibold px-5 py-2.5 rounded-lg hover:bg-emerald-700">Compare local quotes →</a>
  </div>

  <h2 class="text-2xl font-bold mt-10 mb-3">{html.escape(t['table_title'])} in {html.escape(city_short)}</h2>
  <p class="text-slate-700 mb-3">These ranges are adjusted for {html.escape(city_short)} labor and permit costs:</p>
  <div class="overflow-x-auto my-4">
    <table class="w-full text-base border-collapse">
      <thead><tr class="border-b-2 border-slate-300 text-left"><th class="py-2 pr-4">Type</th><th class="py-2">{html.escape(city_short)} price range</th></tr></thead>
      <tbody class="align-top">{rows}</tbody>
    </table>
  </div>
  <p class="text-sm text-slate-500 italic">Estimates for {YEAR}; actual quotes vary by home, scope, and contractor. Always get written bids.</p>

  <h2 class="text-2xl font-bold mt-10 mb-3">What drives {t['noun']} cost</h2>
  <ul class="list-disc pl-6 space-y-2 text-lg leading-relaxed">{factors}</ul>

  <h2 class="text-2xl font-bold mt-10 mb-3">{html.escape(city_short)} cost factors</h2>
  <p class="text-lg leading-relaxed text-slate-700">{html.escape(c['note'])}</p>

  <h2 class="text-2xl font-bold mt-10 mb-4">Frequently asked questions</h2>
  {faq_html}

  <div class="bg-slate-900 text-white rounded-2xl p-8 mt-10" id="quote">
    <div class="text-emerald-400 text-sm font-semibold uppercase tracking-wider mb-2">Ready to start?</div>
    <h3 class="text-2xl font-bold mb-3">Get matched with vetted {html.escape(city_short)} {t['noun']} pros and compare free quotes.</h3>
    <a href="#" data-affiliate="lead-gen-slot" class="inline-block bg-white text-slate-900 font-semibold px-5 py-2.5 rounded-lg hover:bg-slate-100">Compare local quotes →</a>
  </div>

  <h2 class="text-xl font-bold mt-10 mb-3">{t['noun'].title()} costs in other cities</h2>
  <p class="text-slate-700 mb-4">{other_cities}</p>
  <h2 class="text-xl font-bold mt-6 mb-3">Other project costs in {html.escape(city_short)}</h2>
  <ul class="list-disc pl-6 space-y-1">{other_trades}</ul>

  <p class="text-sm text-slate-500 mt-8 italic">Published 2026-06-16. Cost ranges are general {YEAR} estimates for guidance only, not quotes. Get written bids from licensed local contractors.</p>
</article>
<footer class="border-t border-slate-200 mt-12">
  <div class="max-w-5xl mx-auto px-6 py-8 text-sm text-slate-500 flex flex-col sm:flex-row gap-3 justify-between">
    <div>© {YEAR} {BRAND}. Home project cost guides.</div>
    <a href="/" class="hover:text-slate-900">All cost guides</a>
  </div>
</footer>
</body>
</html>
"""

# ---------------------------------------------------------------- INDEX
def index_html():
    cards = ""
    for tslug, t in TRADES.items():
        links = "".join(
            f'<a href="/how-much-does-{tslug}-cost-in-{cslug}" class="block px-3 py-2 rounded-lg hover:bg-emerald-50 text-emerald-700">{CITIES[cslug]["name"]} →</a>'
            for cslug in CITIES)
        cards += (f'<div class="border border-slate-200 rounded-2xl p-6">'
                  f'<h2 class="text-2xl font-bold mb-1">{t["noun"].title()} cost</h2>'
                  f'<p class="text-slate-600 mb-3">{YEAR} price ranges by city.</p>'
                  f'<div class="grid sm:grid-cols-2 gap-1">{links}</div></div>')
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{BRAND} — Home Project Cost Guides by City ({YEAR})</title>
<meta name="description" content="Real {YEAR} cost ranges for roof replacement, HVAC, kitchen remodels and water heaters — adjusted by city, with what drives the price and how to get local quotes." />
<link rel="canonical" href="{DOMAIN}/" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E\U0001F3E0%3C/text%3E%3C/svg%3E" />
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>body{{font-family:Inter,system-ui,sans-serif}}</style>
</head><body class="antialiased text-slate-900 bg-white">
<header class="border-b border-slate-200"><div class="max-w-5xl mx-auto px-6 py-4 font-bold text-xl">\U0001F3E0 {BRAND}</div></header>
<section class="max-w-3xl mx-auto px-6 pt-16 pb-8 text-center">
  <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">What does it really cost?</h1>
  <p class="text-xl text-slate-600">Straight {YEAR} price ranges for the home projects people actually budget for — adjusted city by city, with what drives the cost and how to get local quotes.</p>
</section>
<section class="max-w-5xl mx-auto px-6 pb-20"><div class="grid md:grid-cols-2 gap-6">{cards}</div></section>
<footer class="border-t border-slate-200"><div class="max-w-5xl mx-auto px-6 py-8 text-sm text-slate-500">© {YEAR} {BRAND}. Cost ranges are general estimates for guidance only, not quotes.</div></footer>
</body></html>
"""

# ---------------------------------------------------------------- WRITE
def main():
    pages = []
    for tslug, t in TRADES.items():
        for cslug, c in CITIES.items():
            slug = f"how-much-does-{tslug}-cost-in-{cslug}"
            with open(os.path.join(OUT, slug + ".html"), "w") as f:
                f.write(page_html(tslug, t, cslug, c))
            pages.append(slug)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(index_html())
    # sitemap
    urls = [f"{DOMAIN}/"] + [f"{DOMAIN}/{p}" for p in pages]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pri = "1.0" if u.endswith("/") else "0.8"
        sm += f"  <url><loc>{u}</loc><lastmod>2026-06-16</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority></url>\n"
    sm += "</urlset>\n"
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(sm)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print(f"generated {len(pages)} city-trade pages + index + sitemap + robots into {OUT}")
    print("trades:", list(TRADES), "| cities:", list(CITIES))

if __name__ == "__main__":
    main()
