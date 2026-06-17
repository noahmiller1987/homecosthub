# HomeCostHub — Plan B passive-portfolio MVP (pSEO)

Local-services cost pSEO. **Niche #1 from plan-b-passive-portfolio.md, founder-approved "do #1" 2026-06-16.**
NOTHING is registered or spent — this is a local build for review before a domain is chosen.

## What this is
`generate.py` turns a dataset (TRADES × CITIES) into static "How much does [trade] cost in [city]" pages
— the exact long-tail, high-commercial-intent query people Google before hiring a contractor.

- **MVP:** 4 trades × 5 metros = **20 pages** + index + sitemap + robots.
- Each page: city-adjusted price ranges, a material/type cost table, cost-factor list, a city-specific
  paragraph, 5 FAQs (FAQPage + Article schema), internal links to sibling pages, and 2 lead-gen CTA slots.
- ~750 words/page, genuinely differentiated by city index + local notes (not thin/duplicate).

## Scale (the whole point)
Add rows to `CITIES` / `TRADES` in `generate.py` and re-run → hundreds of pages from one template.
e.g. 8 trades × 25 cities = 200 pages, same effort.

## Monetization (applied AFTER pages index, ~weeks)
The two CTAs carry `data-affiliate="lead-gen-slot"` — wire to a home-services lead-gen affiliate
(Modernize / Networx / Angi Leads / HomeAdvisor) once traffic accrues, plus display (Ezoic/AdSense)
at their traffic thresholds. Honest ramp: 3–6 months to first meaningful checks.

## Deploy (when founder approves a domain)
1. Pick a brandable domain (~$10–12/yr) — **founder gate, nothing bought yet.**
2. Swap the `DOMAIN` constant in `generate.py`, re-run.
3. Push to a Vercel project (free `*.vercel.app` to start; same static/cleanUrls setup as ListingStage).
4. Submit sitemap to Google Search Console.

## Run
    python3 generate.py   # regenerates everything into web/
