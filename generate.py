#!/usr/bin/env python3
"""
HomeCostHub — pSEO generator (Plan B niche #1).
Generates "How much does [trade] cost in [city]" pages from a dataset.
4 trades x 5 metros = 20 pages + index + sitemap + robots. Static HTML, no build.

Scale plan: add cities to CITIES / trades to TRADES and re-run -> hundreds of pages.
DOMAIN is the only thing to swap once a domain is chosen (founder gate).
"""
import os, html, json

DOMAIN = "https://homecostcheck.com"   # live
BRAND = "HomeCostCheck"
GSC_VERIFY = "google85e6075b23385072.html"  # Google Search Console HTML-file verification (keep forever)
GSC_META = '<meta name="google-site-verification" content="2iO-r2Nf6_z4VdB0ddZifN9SKbcQXi1FrWdE1_GD6mQ" />'
OUT = os.path.join(os.path.dirname(__file__), "web")
YEAR = "2026"

# ---------------------------------------------------------------- LEAD-GEN / MONETIZATION
# Every "Compare local quotes" CTA points to a real, working external lead-gen destination.
# Interim = Thumbtack deep links (verified HTTP 200, no auth, genuinely useful to the visitor).
# To MONETIZE: once a paid home-services affiliate is approved (Modernize / Networx / Angi
# Leads / QuinStreet), set LEADGEN_AFFILIATE to its deep-link template and re-run — every page
# switches to the paid link. {tt} = thumbtack slug, {zip} = primary city zip, {trade} = trade slug.
LEADGEN_AFFILIATE = ""   # e.g. "https://modernize.com/r/PARTNERID?service={trade}&zip={zip}"
TT_SLUG = {
    "roof-replacement": "roofing",
    "hvac-installation": "hvac",
    "kitchen-remodel": "kitchen-remodeling",
    "water-heater-replacement": "water-heater-installation",
    "bathroom-remodel": "bathroom-remodeling",
    "window-replacement": "window-installation",
    "interior-painting": "interior-painting",
    "flooring-installation": "flooring-installation",
    "electrical-panel-upgrade": "electrical",
    "solar-panel-installation": "solar-panel-installation",
    "fence-installation": "fence-installation",
    "garage-door-replacement": "garage-door-installation",
}
def leadgen_url(tslug, czip=""):
    tt = TT_SLUG.get(tslug, "")
    if LEADGEN_AFFILIATE:
        return html.escape(LEADGEN_AFFILIATE.format(tt=tt, zip=czip, trade=tslug))
    return f"https://www.thumbtack.com/k/{tt}/near-me/"

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
  "bathroom-remodel": {
    "noun": "bathroom remodel", "a": "a bathroom remodel",
    "kw": "bathroom remodel cost",
    "lo": 12000, "hi": 25000, "basis": "for a mid-range full bathroom",
    "intro": "Bathroom remodels run from a fixture-and-tile refresh to a full gut that relocates plumbing. Tile work, fixtures, and whether the layout changes drive most of the price.",
    "table_title": "Cost by remodel scope",
    "table": [
      ("Cosmetic refresh (fixtures, paint, vanity)", 5000, 10000),
      ("Mid-range full bath (tile, tub/shower, vanity)", 12000, 25000),
      ("Major / primary bath (layout change, custom)", 28000, 60000),
    ],
    "factors": [
      ("Scope", "A fixture-and-paint refresh costs a fraction of a full gut. Moving the toilet, tub, or shower triggers plumbing and permits."),
      ("Tile & surfaces", "Floor and wall tile labor is one of the biggest line items; natural stone and intricate patterns cost more to set."),
      ("Fixtures & vanity", "Toilets, tubs, showers, faucets, and vanities span budget to luxury and add up fast."),
      ("Plumbing & layout", "Relocating fixtures or converting a tub to a walk-in shower adds labor, materials, and inspection."),
      ("Labor rates", "Local plumber, tile-setter, and contractor wages set whether you land at the low or high end."),
    ],
    "faqs": [
      ("How much does a bathroom remodel cost in {city}?",
       "A mid-range full bathroom remodel in {city} typically runs {range}. Cosmetic refreshes cost less; primary-bath gut jobs with layout changes run well above it."),
      ("Does a bathroom remodel add resale value?",
       "Bathrooms are a strong-ROI remodel, and mid-range updates generally recoup more of their cost at resale than high-end luxury renovations."),
      ("How long does a bathroom remodel take?",
       "A cosmetic refresh can be done in about a week; a mid-range full bath usually takes 2–3 weeks, and a gut with layout changes 4–6 weeks once permits and tile work are factored in."),
      ("What is the most expensive part of a bathroom remodel?",
       "Tile labor and plumbing changes are usually the biggest costs, followed by the shower or tub and the vanity."),
    ],
  },
  "window-replacement": {
    "noun": "window replacement", "a": "a window replacement",
    "kw": "window replacement cost",
    "lo": 5000, "hi": 15000, "basis": "to replace about 10 windows",
    "intro": "Window replacement is usually priced per window and then by the whole-home count. Frame material, glass package, and whether it is a simple retrofit or a full-frame install drive the cost.",
    "table_title": "Cost per window by material (installed)",
    "table": [
      ("Vinyl", 400, 900),
      ("Aluminum", 450, 1000),
      ("Fiberglass", 600, 1300),
      ("Wood", 800, 1800),
    ],
    "factors": [
      ("Number of windows", "Whole-home replacements are priced per window, so the count is the biggest driver of the total."),
      ("Frame material", "Vinyl is the budget choice; fiberglass and wood cost more but offer better looks and longevity."),
      ("Glass package", "Double- vs triple-pane and low-E coatings raise the price but cut energy loss."),
      ("Size & style", "Large picture, bay, bow, and custom-shaped windows cost more than standard double-hungs."),
      ("Install type & labor", "Full-frame replacement costs more than a retrofit insert, and local labor rates move the total."),
    ],
    "faqs": [
      ("How much does window replacement cost in {city}?",
       "Replacing about 10 windows in {city} typically runs {range}, depending mainly on the frame material and glass package. Vinyl is the budget end; wood and fiberglass sit higher."),
      ("Are new windows worth the cost?",
       "Energy-efficient windows lower heating and cooling bills and improve comfort and noise; the payback is strongest in climates with long heating or cooling seasons."),
      ("How long does window replacement take?",
       "Most crews replace 8–15 windows in a single day. Full-frame replacements and custom sizes take longer."),
      ("How long do replacement windows last?",
       "Quality vinyl and fiberglass windows last about 20–40 years; wood windows can last longer with maintenance. Drafts, condensation between panes, and difficulty operating them are signs to replace."),
    ],
  },
  "interior-painting": {
    "noun": "interior painting", "a": "an interior paint job",
    "kw": "interior painting cost",
    "lo": 2500, "hi": 6000, "basis": "to paint the interior of a 2,000 sq ft home",
    "intro": "Interior painting is priced by square footage and surface count. How many rooms, the condition of the walls, ceiling and trim detail, and paint quality set the price.",
    "table_title": "Cost by project scope",
    "table": [
      ("Single room", 350, 800),
      ("Whole 2,000 sq ft interior", 2500, 6000),
      ("Cabinets / trim / detail work", 1000, 3500),
    ],
    "factors": [
      ("Square footage", "More wall area means more paint and labor — the main driver of the total."),
      ("Surfaces", "Ceilings, trim, doors, and accent walls each add labor beyond the basic wall coat."),
      ("Prep & repair", "Patching, sanding, priming, and covering old dark colors add hours before any finish coat goes on."),
      ("Paint quality", "Premium, low-VOC, and specialty finishes cost more per gallon but cover better and last longer."),
      ("Labor rates", "Local painter wages are the biggest reason the same job costs more in one metro than another."),
    ],
    "faqs": [
      ("How much does interior painting cost in {city}?",
       "Painting the interior of a typical 2,000 sq ft home in {city} runs about {range}, depending on the number of surfaces, prep needed, and paint quality."),
      ("How long does it take to paint a house interior?",
       "A single room takes a day; a full 2,000 sq ft interior usually takes 3–5 days including prep and drying between coats."),
      ("How often should you repaint a home interior?",
       "Most interiors need repainting every 5–10 years, sooner for high-traffic areas, kitchens, and kids' rooms."),
      ("Is it cheaper to paint yourself?",
       "DIY saves on labor but costs your time and risks an uneven finish on ceilings, trim, and tall walls. For a whole-home job most people hire out the prep-heavy work."),
    ],
  },
  "flooring-installation": {
    "noun": "flooring installation", "a": "a flooring installation",
    "kw": "flooring installation cost",
    "lo": 3000, "hi": 12000, "basis": "for about 1,000 sq ft installed",
    "intro": "New flooring is priced by material and square footage, plus the cost of removing the old floor and prepping the subfloor. Material choice is the single biggest factor.",
    "table_title": "Cost by material (1,000 sq ft installed)",
    "table": [
      ("Laminate / luxury vinyl plank", 3000, 7000),
      ("Engineered wood", 5000, 12000),
      ("Solid hardwood", 8000, 15000),
      ("Tile", 7000, 20000),
    ],
    "factors": [
      ("Material", "Laminate and vinyl plank are the budget choices; hardwood and tile cost two to three times as much."),
      ("Square footage", "Total area is the main driver; larger jobs sometimes earn a lower per-foot rate."),
      ("Subfloor prep", "Leveling, repairing, or replacing a damaged subfloor adds labor before installation."),
      ("Old-floor removal", "Tearing out and hauling away existing flooring adds cost, especially glued-down tile."),
      ("Patterns & stairs", "Diagonal layouts, borders, and staircases are slower and raise the labor rate."),
    ],
    "faqs": [
      ("How much does flooring installation cost in {city}?",
       "Installing about 1,000 sq ft of new flooring in {city} runs about {range}, depending mainly on the material. Laminate and vinyl plank are cheapest; hardwood and tile sit at the top."),
      ("What is the cheapest flooring to install?",
       "Laminate and luxury vinyl plank are the most affordable durable options and are often DIY-friendly, which is why they are the most popular budget choices."),
      ("How long does flooring installation take?",
       "A 1,000 sq ft job typically takes 1–3 days depending on the material and how much subfloor prep and removal is needed."),
      ("Can I install flooring myself?",
       "Floating laminate and vinyl plank are common DIY projects; hardwood, tile, and glue-down floors are best left to a pro for a lasting, level result."),
    ],
  },
  "electrical-panel-upgrade": {
    "noun": "electrical panel upgrade", "a": "an electrical panel upgrade",
    "kw": "electrical panel upgrade cost",
    "lo": 2000, "hi": 4000, "basis": "to upgrade to 200-amp service",
    "intro": "Upgrading an electrical panel boosts your home's capacity for modern loads like EV chargers, heat pumps, and additions. Cost depends on the new amperage and whether the service entrance also needs work.",
    "table_title": "Cost by scope",
    "table": [
      ("Panel replacement (same amperage)", 1300, 2500),
      ("Upgrade to 200-amp service", 2000, 4000),
      ("Upgrade + new service mast/meter", 3000, 6000),
    ],
    "factors": [
      ("Target amperage", "Going from 100 to 200 amps (or higher) means a bigger panel and often a new service entrance."),
      ("Panel location & access", "A cramped or far-from-the-meter location makes the job slower and pricier."),
      ("Service entrance", "Upgrading the mast, meter, and utility connection adds cost beyond the panel itself."),
      ("Code corrections", "Older homes often need grounding, bonding, or circuit fixes to pass inspection."),
      ("Permits & labor", "An electrical permit, utility coordination, and licensed-electrician rates drive much of the total."),
    ],
    "faqs": [
      ("How much does an electrical panel upgrade cost in {city}?",
       "Upgrading to a 200-amp panel in {city} typically costs {range}. A simple same-amperage replacement is lower; adding a new service mast and meter runs higher."),
      ("What are the signs I need a panel upgrade?",
       "Frequently tripped breakers, a fuse box, flickering lights, a panel under 100 amps, or plans for an EV charger, heat pump, or addition all point to an upgrade."),
      ("How long does a panel upgrade take?",
       "Most panel upgrades are a 4–8 hour job, plus a short utility disconnect and an inspection. Service-entrance work can extend it."),
      ("Do I need a permit to replace an electrical panel?",
       "Yes — panel work requires an electrical permit and inspection almost everywhere, and should only be done by a licensed electrician."),
    ],
  },
  "solar-panel-installation": {
    "noun": "solar panel installation", "a": "a solar panel installation",
    "kw": "solar panel installation cost",
    "lo": 16000, "hi": 26000, "basis": "for a typical 7 kW system, before incentives",
    "intro": "A residential solar system is priced mainly by size in kilowatts, plus panel and inverter quality and whether you add battery storage. Federal and local incentives can cut the net cost substantially.",
    "table_title": "Cost by system size (before incentives)",
    "table": [
      ("Small (5 kW)", 12000, 20000),
      ("Average (7 kW)", 16000, 26000),
      ("Large (10 kW)", 22000, 36000),
    ],
    "factors": [
      ("System size (kW)", "Bigger systems cost more up front but offset more of your electric bill — sizing to your usage matters."),
      ("Equipment quality", "Premium panels and inverters (and microinverters) cost more but produce more and last longer."),
      ("Roof type & complexity", "Steep, multi-plane, tile, or shaded roofs raise the install labor."),
      ("Battery storage", "Adding a home battery for backup or time-of-use savings adds several thousand dollars."),
      ("Incentives", "The federal tax credit and any state or utility rebates reduce the net cost well below the sticker price."),
    ],
    "faqs": [
      ("How much does solar panel installation cost in {city}?",
       "A typical 7 kW residential solar system in {city} runs about {range} before incentives. The federal tax credit and any local rebates lower the net cost from there."),
      ("Is home solar worth it?",
       "Solar pays back best where electricity is expensive and sun exposure is good; payback periods commonly land in the 6–12 year range, after which the power is essentially free."),
      ("How long does a solar installation take?",
       "The rooftop install is usually 1–3 days, but permitting and utility interconnection can stretch the full timeline to several weeks."),
      ("Does solar qualify for a tax credit?",
       "Residential solar has qualified for a federal tax credit on the system cost, often alongside state or utility incentives. Confirm current rules with a tax professional."),
    ],
  },
  "fence-installation": {
    "noun": "fence installation", "a": "a fence installation",
    "kw": "fence installation cost",
    "lo": 3000, "hi": 7500, "basis": "for about 150 linear feet",
    "intro": "Fencing is priced by linear foot and material, then by height, gates, and terrain. A standard residential yard runs roughly 150 linear feet.",
    "table_title": "Cost by material (about 150 linear feet)",
    "table": [
      ("Chain link", 2000, 4500),
      ("Wood privacy", 3000, 7500),
      ("Aluminum / ornamental", 4000, 9000),
      ("Vinyl", 4500, 10000),
    ],
    "factors": [
      ("Length", "Total linear footage is the main driver; bigger yards cost proportionally more."),
      ("Material", "Chain link is cheapest; wood, aluminum, and vinyl cost more for privacy and looks."),
      ("Height", "Taller privacy fences use more material and labor than a short boundary fence."),
      ("Gates", "Each walk or drive gate adds hardware and labor to the base run."),
      ("Terrain & posts", "Sloped, rocky, or root-filled ground makes post-setting slower and pricier."),
    ],
    "faqs": [
      ("How much does fence installation cost in {city}?",
       "Installing about 150 linear feet of fence in {city} runs about {range}, depending on the material and height. Chain link is the budget end; vinyl and ornamental sit higher."),
      ("What is the cheapest fence to install?",
       "Chain link is the most affordable durable option, followed by basic wood. Vinyl costs more up front but needs little maintenance."),
      ("How long does it take to install a fence?",
       "A typical residential fence is a 1–3 day job depending on length, material, and how hard the posts are to set."),
      ("Do I need a permit to build a fence?",
       "Many cities require a permit above a certain height and have setback and HOA rules. Check locally and confirm property lines before you build."),
    ],
  },
  "garage-door-replacement": {
    "noun": "garage door replacement", "a": "a garage door replacement",
    "kw": "garage door replacement cost",
    "lo": 1000, "hi": 3500, "basis": "for a standard door installed",
    "intro": "Replacing a garage door is a quick, high-ROI project. Cost depends on whether it is a single or double door, the material and insulation, and whether you add a new opener.",
    "table_title": "Cost by door type (installed)",
    "table": [
      ("Single steel door", 800, 2000),
      ("Double steel door", 1300, 3500),
      ("Insulated / premium", 2000, 5000),
      ("Custom wood / carriage", 3000, 8000),
    ],
    "factors": [
      ("Size", "A double door costs more than a single in both material and labor."),
      ("Material & insulation", "Insulated steel and premium finishes cost more than a basic single-layer door."),
      ("Windows & style", "Decorative glass, carriage-house styling, and custom colors raise the price."),
      ("Opener & hardware", "Adding or upgrading the opener, springs, and tracks adds to the install."),
      ("Labor", "Removal of the old door and local installer rates set the rest of the total."),
    ],
    "faqs": [
      ("How much does garage door replacement cost in {city}?",
       "A standard garage door replacement in {city} typically runs {range} installed. Double, insulated, and custom doors cost more than a basic single steel door."),
      ("Is an insulated garage door worth it?",
       "Insulated doors are worth it for attached garages, heated/cooled spaces, or rooms above the garage — they cut energy loss and dampen noise."),
      ("How long does it take to install a garage door?",
       "A standard replacement is usually a 3–5 hour job, including removing the old door and adjusting the springs and tracks."),
      ("How long do garage doors last?",
       "A quality garage door lasts about 15–30 years; springs and openers may need service sooner. Loud operation, sagging, and rising repair costs are signs to replace."),
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
  "los-angeles": {"name": "Los Angeles, CA", "idx": 1.25,
    "note": "Los Angeles combines high labor costs, strict California permitting and energy codes, and seismic requirements. The mild coastal-to-inland climate is easy on equipment, but demand and the cost of living keep nearly every home project above the national average."},
  "austin": {"name": "Austin, TX", "idx": 1.05,
    "note": "Austin's fast growth has pushed contractor demand and labor rates above the Texas norm, though still below coastal California. Hot, humid summers make efficient HVAC and quality roofing priorities, and Texas permitting is generally lighter than California's."},
  "dallas": {"name": "Dallas, TX", "idx": 1.00,
    "note": "Dallas sits near the national average on labor with a deep, competitive contractor market. Hot summers, occasional severe hailstorms, and expansive clay soils make roofing, HVAC, and foundation work especially common here."},
  "houston": {"name": "Houston, TX", "idx": 0.98,
    "note": "Houston's large contractor pool keeps labor at or just below the national average. Intense heat, humidity, and hurricane and flood exposure drive demand for resilient roofing, strong HVAC, and water-resistant materials."},
  "denver": {"name": "Denver, CO", "idx": 1.08,
    "note": "Denver's high-altitude climate brings big temperature swings, heavy snow loads, and intense sun that ages roofs faster. Labor runs above the national average, and Colorado permitting and energy codes add to project costs."},
  "atlanta": {"name": "Atlanta, GA", "idx": 0.97,
    "note": "Atlanta offers below-average labor costs and a deep contractor market. Hot, humid summers and frequent storms make HVAC efficiency and roofing durability the priorities for most homeowners here."},
  "chicago": {"name": "Chicago, IL", "idx": 1.10,
    "note": "Chicago's harsh winters, freeze-thaw cycles, and union labor push project costs above the national average. Heating systems, snow-rated roofing, and weatherproofing matter more here than in milder climates, and city permitting can be slow."},
  "miami": {"name": "Miami, FL", "idx": 1.06,
    "note": "Miami's hurricane exposure means strict building codes — impact windows and wind-rated roofing add cost. Heat, humidity, and salt air are hard on equipment, and labor runs above the national average."},
  "seattle": {"name": "Seattle, WA", "idx": 1.18,
    "note": "Seattle's wet climate makes roofing, siding, and drainage especially important, and its strong economy keeps labor well above the national average. Washington permitting and energy codes add to the cost of most home projects."},
  "las-vegas": {"name": "Las Vegas, NV", "idx": 1.00,
    "note": "Las Vegas sits near the national average on labor. Extreme desert heat makes air conditioning the most critical and hardest-working system in the home, often requiring larger units and sun-resistant roofing built for the climate."},
  "charlotte": {"name": "Charlotte, NC", "idx": 0.95,
    "note": "Charlotte is one of the more affordable major metros for home projects, with below-average labor costs and a growing contractor market. Hot, humid summers and occasional storms drive most HVAC and roofing demand here."},
}

FEATURED = ["sacramento","san-jose","fresno","san-diego","phoenix","los-angeles",
            "austin","dallas","houston","denver","atlanta","chicago","miami","seattle","las-vegas","charlotte"]

# ---------------------------------------------------------------- CALIFORNIA REGIONS (for bulk city pages)
REGIONS = {
 "bay-area": {"idx":1.35, "note":"The San Francisco Bay Area has some of the highest contractor labor rates in the country, along with strict California permitting, energy codes, and seismic requirements. The mild climate is easy on equipment, but demand and the cost of living keep nearly every home project well above the national average."},
 "la-socal-coast": {"idx":1.22, "note":"Coastal Southern California pairs a mild, equipment-friendly climate with a high cost of living, strict California permitting and energy codes, and seismic requirements. Salt air near the coast can accelerate corrosion on rooftop HVAC and metal roofing, and labor runs above the national average."},
 "inland-empire": {"idx":1.05, "note":"California's Inland Empire and high desert see hot, dry summers that make air conditioning and sun-resistant roofing priorities. Labor runs a little above the national average — below the coast — and projects still fall under California's permitting and energy rules."},
 "central-valley": {"idx":0.95, "note":"California's Central Valley has lower labor costs than the coastal metros, but extreme summer heat makes hard-working air conditioning essential. It is one of the more affordable parts of California for home projects while still under the state's permit and energy codes."},
 "sacramento-region": {"idx":1.05, "note":"The greater Sacramento region has hot, dry summers that push HVAC and roofing toward higher-efficiency options under California's Title 24 energy code. Labor runs a bit above the national average, with city and county permitting adding time and cost."},
 "central-coast": {"idx":1.12, "note":"California's Central Coast enjoys a mild marine climate that is gentle on equipment, but limited contractor supply and a high cost of living keep project prices above the national average, on top of California permitting."},
 "north-state": {"idx":1.02, "note":"Northern California and the Sierra foothills see colder winters, snow loads at elevation, and intense summer sun and wildfire exposure that drive demand for durable roofing and efficient heating. Labor sits near or just above the national average under California's permit rules."},
}

# (slug, "Name, CA", region) — incorporated California cities. Featured CA cities above are skipped automatically.
CA_CITIES = [
 # Bay Area
 ("san-francisco","San Francisco, CA","bay-area"),("oakland","Oakland, CA","bay-area"),("fremont","Fremont, CA","bay-area"),
 ("sunnyvale","Sunnyvale, CA","bay-area"),("santa-clara","Santa Clara, CA","bay-area"),("hayward","Hayward, CA","bay-area"),
 ("concord","Concord, CA","bay-area"),("berkeley","Berkeley, CA","bay-area"),("daly-city","Daly City, CA","bay-area"),
 ("san-mateo","San Mateo, CA","bay-area"),("redwood-city","Redwood City, CA","bay-area"),("mountain-view","Mountain View, CA","bay-area"),
 ("palo-alto","Palo Alto, CA","bay-area"),("vallejo","Vallejo, CA","bay-area"),("fairfield","Fairfield, CA","bay-area"),
 ("richmond","Richmond, CA","bay-area"),("antioch","Antioch, CA","bay-area"),("walnut-creek","Walnut Creek, CA","bay-area"),
 ("pleasanton","Pleasanton, CA","bay-area"),("livermore","Livermore, CA","bay-area"),("san-rafael","San Rafael, CA","bay-area"),
 ("napa","Napa, CA","bay-area"),("cupertino","Cupertino, CA","bay-area"),("milpitas","Milpitas, CA","bay-area"),
 ("union-city","Union City, CA","bay-area"),("san-leandro","San Leandro, CA","bay-area"),("pittsburg","Pittsburg, CA","bay-area"),
 ("vacaville","Vacaville, CA","bay-area"),("newark","Newark, CA","bay-area"),("brentwood","Brentwood, CA","bay-area"),
 ("dublin","Dublin, CA","bay-area"),("san-ramon","San Ramon, CA","bay-area"),("santa-rosa","Santa Rosa, CA","bay-area"),
 ("petaluma","Petaluma, CA","bay-area"),("novato","Novato, CA","bay-area"),("mountain-house","Mountain House, CA","bay-area"),
 # LA / SoCal coast
 ("long-beach","Long Beach, CA","la-socal-coast"),("santa-ana","Santa Ana, CA","la-socal-coast"),("anaheim","Anaheim, CA","la-socal-coast"),
 ("irvine","Irvine, CA","la-socal-coast"),("huntington-beach","Huntington Beach, CA","la-socal-coast"),("glendale","Glendale, CA","la-socal-coast"),
 ("santa-clarita","Santa Clarita, CA","la-socal-coast"),("oceanside","Oceanside, CA","la-socal-coast"),("garden-grove","Garden Grove, CA","la-socal-coast"),
 ("torrance","Torrance, CA","la-socal-coast"),("pasadena","Pasadena, CA","la-socal-coast"),("orange","Orange, CA","la-socal-coast"),
 ("fullerton","Fullerton, CA","la-socal-coast"),("thousand-oaks","Thousand Oaks, CA","la-socal-coast"),("simi-valley","Simi Valley, CA","la-socal-coast"),
 ("carlsbad","Carlsbad, CA","la-socal-coast"),("costa-mesa","Costa Mesa, CA","la-socal-coast"),("ventura","Ventura, CA","la-socal-coast"),
 ("santa-monica","Santa Monica, CA","la-socal-coast"),("newport-beach","Newport Beach, CA","la-socal-coast"),("chula-vista","Chula Vista, CA","la-socal-coast"),
 ("escondido","Escondido, CA","la-socal-coast"),("el-cajon","El Cajon, CA","la-socal-coast"),("vista","Vista, CA","la-socal-coast"),
 ("san-marcos","San Marcos, CA","la-socal-coast"),("encinitas","Encinitas, CA","la-socal-coast"),("burbank","Burbank, CA","la-socal-coast"),
 ("inglewood","Inglewood, CA","la-socal-coast"),("downey","Downey, CA","la-socal-coast"),("west-covina","West Covina, CA","la-socal-coast"),
 ("norwalk","Norwalk, CA","la-socal-coast"),("el-monte","El Monte, CA","la-socal-coast"),("carson","Carson, CA","la-socal-coast"),
 ("compton","Compton, CA","la-socal-coast"),("mission-viejo","Mission Viejo, CA","la-socal-coast"),("whittier","Whittier, CA","la-socal-coast"),
 # Inland Empire / desert
 ("riverside","Riverside, CA","inland-empire"),("san-bernardino","San Bernardino, CA","inland-empire"),("fontana","Fontana, CA","inland-empire"),
 ("moreno-valley","Moreno Valley, CA","inland-empire"),("rancho-cucamonga","Rancho Cucamonga, CA","inland-empire"),("ontario","Ontario, CA","inland-empire"),
 ("corona","Corona, CA","inland-empire"),("victorville","Victorville, CA","inland-empire"),("murrieta","Murrieta, CA","inland-empire"),
 ("temecula","Temecula, CA","inland-empire"),("rialto","Rialto, CA","inland-empire"),("hesperia","Hesperia, CA","inland-empire"),
 ("chino","Chino, CA","inland-empire"),("indio","Indio, CA","inland-empire"),("redlands","Redlands, CA","inland-empire"),
 ("chino-hills","Chino Hills, CA","inland-empire"),("upland","Upland, CA","inland-empire"),("apple-valley","Apple Valley, CA","inland-empire"),
 ("palm-desert","Palm Desert, CA","inland-empire"),("palm-springs","Palm Springs, CA","inland-empire"),("hemet","Hemet, CA","inland-empire"),
 ("menifee","Menifee, CA","inland-empire"),("jurupa-valley","Jurupa Valley, CA","inland-empire"),("lake-elsinore","Lake Elsinore, CA","inland-empire"),
 # Central Valley
 ("bakersfield","Bakersfield, CA","central-valley"),("stockton","Stockton, CA","central-valley"),("modesto","Modesto, CA","central-valley"),
 ("visalia","Visalia, CA","central-valley"),("clovis","Clovis, CA","central-valley"),("merced","Merced, CA","central-valley"),
 ("turlock","Turlock, CA","central-valley"),("tracy","Tracy, CA","central-valley"),("manteca","Manteca, CA","central-valley"),
 ("madera","Madera, CA","central-valley"),("hanford","Hanford, CA","central-valley"),("tulare","Tulare, CA","central-valley"),
 ("porterville","Porterville, CA","central-valley"),("lodi","Lodi, CA","central-valley"),("ceres","Ceres, CA","central-valley"),
 # Sacramento region
 ("elk-grove","Elk Grove, CA","sacramento-region"),("roseville","Roseville, CA","sacramento-region"),("folsom","Folsom, CA","sacramento-region"),
 ("citrus-heights","Citrus Heights, CA","sacramento-region"),("rancho-cordova","Rancho Cordova, CA","sacramento-region"),("davis","Davis, CA","sacramento-region"),
 ("woodland","Woodland, CA","sacramento-region"),("rocklin","Rocklin, CA","sacramento-region"),("lincoln","Lincoln, CA","sacramento-region"),
 ("yuba-city","Yuba City, CA","sacramento-region"),("el-dorado-hills","El Dorado Hills, CA","sacramento-region"),
 # Central Coast
 ("santa-barbara","Santa Barbara, CA","central-coast"),("san-luis-obispo","San Luis Obispo, CA","central-coast"),("salinas","Salinas, CA","central-coast"),
 ("santa-maria","Santa Maria, CA","central-coast"),("monterey","Monterey, CA","central-coast"),("santa-cruz","Santa Cruz, CA","central-coast"),
 ("paso-robles","Paso Robles, CA","central-coast"),("watsonville","Watsonville, CA","central-coast"),("lompoc","Lompoc, CA","central-coast"),
 # North state / Sierra
 ("redding","Redding, CA","north-state"),("chico","Chico, CA","north-state"),("eureka","Eureka, CA","north-state"),
 ("ukiah","Ukiah, CA","north-state"),("truckee","Truckee, CA","north-state"),("grass-valley","Grass Valley, CA","north-state"),
 ("south-lake-tahoe","South Lake Tahoe, CA","north-state"),("auburn","Auburn, CA","north-state"),("red-bluff","Red Bluff, CA","north-state"),
]
for _slug, _name, _region in CA_CITIES:
    if _slug not in CITIES:
        CITIES[_slug] = {"name": _name, "idx": REGIONS[_region]["idx"], "note": REGIONS[_region]["note"]}

# ---------------------------------------------------------------- TEMPLATE
def page_html(tslug, t, cslug, c):
    idx = c["idx"]; cn = c["name"]; city_short = cn.split(",")[0]
    headline_range = rng(t["lo"], t["hi"], idx)
    slug = f"how-much-does-{tslug}-cost-in-{cslug}"
    url = f"{DOMAIN}/{slug}"
    lg = leadgen_url(tslug, c.get("zip", ""))
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
    _link_cities = [fc for fc in FEATURED if fc != cslug][:12]
    other_cities = ", ".join(
        f'<a href="/how-much-does-{tslug}-cost-in-{fc}" class="text-emerald-700 underline">{CITIES[fc]["name"].split(",")[0]}</a>'
        for fc in _link_cities )
    other_trades = "".join(
        f'<li><a href="/how-much-does-{ot}-cost-in-{cslug}" class="text-emerald-700 underline">{TRADES[ot]["noun"].title()} in {city_short}</a></li>'
        for ot in TRADES if ot != tslug)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
{GSC_META}
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
    <a href="{lg}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-emerald-600 text-white font-semibold px-5 py-2.5 rounded-lg hover:bg-emerald-700">Compare local quotes →</a>
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

  <div class="bg-slate-900 text-white rounded-2xl p-8 mt-10">
    <div class="text-emerald-400 text-sm font-semibold uppercase tracking-wider mb-2">Ready to start?</div>
    <h3 class="text-2xl font-bold mb-3">Get matched with vetted {html.escape(city_short)} {t['noun']} pros and compare free quotes.</h3>
    <a href="{lg}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-white text-slate-900 font-semibold px-5 py-2.5 rounded-lg hover:bg-slate-100">Compare local quotes →</a>
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
            for cslug in FEATURED)
        links += f'<div class="px-3 py-2 text-slate-500 text-sm">+ {len(CITIES)-len(FEATURED)} more cities</div>'
        cards += (f'<div class="border border-slate-200 rounded-2xl p-6">'
                  f'<h2 class="text-2xl font-bold mb-1">{t["noun"].title()} cost</h2>'
                  f'<p class="text-slate-600 mb-3">{YEAR} price ranges by city.</p>'
                  f'<div class="grid sm:grid-cols-2 gap-1">{links}</div></div>')
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
{GSC_META}
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
    # Google Search Console HTML-file verification (must stay live permanently)
    with open(os.path.join(OUT, GSC_VERIFY), "w") as f:
        f.write(f"google-site-verification: {GSC_VERIFY}\n")
    print(f"generated {len(pages)} city-trade pages + index + sitemap + robots into {OUT}")
    print("trades:", list(TRADES), "| cities:", list(CITIES))

if __name__ == "__main__":
    main()
