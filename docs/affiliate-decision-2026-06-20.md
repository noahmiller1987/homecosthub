# HomeCostCheck — lead-gen affiliate decision (2026-06-20)

All 1,873 pages now route "Compare local quotes" → Thumbtack deep links (functional, $0 payout).
Goal: swap to a **paid** home-services lead-gen affiliate. Below is the ranked pick + the exact founder step.

## The reality check
- Our 12 trades: roofing, HVAC, kitchen, water heater, bathroom, windows, painting, flooring,
  electrical panel, solar, fence, garage door. Lead-gen buyers pay most for **roofing, solar,
  windows, HVAC, bathroom** (high ticket) — we cover all of them.
- HomeCostCheck has ~0 traffic and **isn't indexed by Google yet**. Most networks want "traffic
  credentials," so approval is easier with *some* indexed traffic — but the best fit has **no stated
  traffic minimum**, so we apply now and have the payout link ready the moment traffic lands.

## Ranked recommendation
1. **Modernize — APPLY FIRST.** Direct program, explicitly welcomes home-improvement/design content
   sites, pays **per lead** for exactly our top trades (windows, roofing, HVAC, solar + others).
   No stated traffic minimum. They respond within 24h.
   → Apply: **https://modernize.com/contact?publisher** (or email their publisher team). Free to join.
   Ask for: a per-trade deep-link / tracking URL with a sub-id parameter we can template per page.
2. **Angi (absorbed HomeAdvisor) — BACKUP.** Via Impact Radius; pay-per-service-request. Broadest
   trade coverage, but Impact approval can be stricter on low-traffic sites. Apply if Modernize stalls.
3. **HomeAdvisor/Home Depot installation via CJ/Impact** — $1.50–$16 (HA) up to $20–$200 (HD install)
   per qualified lead, but content-site acceptance is "limited." Only if 1 & 2 fall through.

## What's already built so the switch is one line
`generate.py` has `LEADGEN_AFFILIATE` (currently "") + a `leadgen_url(tslug, zip)` resolver with a
`TT_SLUG` map. When Modernize gives the tracking template:
1. Set `LEADGEN_AFFILIATE = "https://...PARTNERID...?service={trade}&zip={zip}&subid={tt}"`
   (map their token names to our `{trade}`/`{zip}`/`{tt}` placeholders).
2. `python3 generate.py` → commit (as noahmiller1987@gmail.com) → `git push` → all 1,873 pages monetize.
3. Verify live: `curl -sL <a page> | grep -o 'href="[^"]*Compare'` resolves to the paid link.

## Parallel unlock (separate task): get indexed
Affiliate payout is worthless without traffic. Site is GSC-verified + sitemap submitted but not yet
indexed. Next: confirm sitemap accepted, request indexing on top pages, build a few inbound links.
