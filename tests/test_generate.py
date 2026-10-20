"""Regression tests for the HomeCostCheck generator.  Run:  python3 -m unittest discover -s tests

Pages are rendered in memory (no 2,000-file write), so the suite runs in about a second.
"""
import json, os, re, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import generate as g  # noqa: E402

CSS = os.path.join(ROOT, "web", "styles.css")


def cost_page(trade, city):
    return g.page_html(trade, g.TRADES[trade], city, g.CITIES[city])


def ld_blocks(html_text):
    return [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_text)]


def visible_text(html_text):
    return re.sub(r"<[^>]+>", " ", html_text)


class SolarCreditAccuracy(unittest.TestCase):
    """Section 25D (30% homeowner solar credit) ended for systems installed after 2025-12-31.
    The pages told 2026 readers the credit would cut their net cost."""

    def test_no_page_promises_the_expired_credit(self):
        page = cost_page("solar-panel-installation", "fresno")
        text = visible_text(page) + json.dumps(ld_blocks(page))
        self.assertNotIn("before incentives", text)
        self.assertNotIn("federal tax credit and any", text)
        self.assertNotIn("lower the net cost from there", text)
        self.assertIn("ended", text)

    def test_faq_schema_matches_visible_faq(self):
        page = cost_page("solar-panel-installation", "fresno")
        faq = [b for b in ld_blocks(page) if b["@type"] == "FAQPage"][0]
        for q in faq["mainEntity"]:
            self.assertIn(q["acceptedAnswer"]["text"], g.html.unescape(page))


class HeadlineMatchesTable(unittest.TestCase):
    """The headline range must equal the table row its basis names (kitchen said 'mid-range'
    $15k-$45k while its own Mid-range row said $25k-$45k; HVAC 'full system' $7k-$14k vs $8k-$16k)."""

    def test_anchor_rows(self):
        anchored = [k for k, t in g.TRADES.items() if "anchor" in t]
        self.assertGreaterEqual(len(anchored), 6)
        for k in anchored:
            t = g.TRADES[k]
            _label, lo, hi = t["table"][t["anchor"]]
            self.assertEqual((t["lo"], t["hi"]), (lo, hi), k)

    def test_mid_range_label_only_when_true(self):
        for k, t in g.TRADES.items():
            if t["basis"].startswith("for a mid-range"):
                self.assertIn("anchor", t, f"{k} claims mid-range without an anchored row")

    def test_headline_inside_table_span(self):
        for k, t in g.TRADES.items():
            if " per " in t["table_title"]:   # per-unit table (windows); headline is a whole-home count
                continue
            self.assertGreaterEqual(t["lo"], min(r[1] for r in t["table"]), k)
            self.assertLessEqual(t["hi"], max(r[2] for r in t["table"]), k)


class CompiledCss(unittest.TestCase):
    """cdn.tailwindcss.com is a dev-only runtime compiler (render-blocking JS, FOUC/CLS).
    Pages must load the precompiled /styles.css, and it must cover every class they use."""

    SAMPLES = staticmethod(lambda: [
        cost_page("roof-replacement", "fremont"),
        g.city_hub_html("fremont", g.CITIES["fremont"]),
        g.trade_hub_html("roof-replacement", g.TRADES["roof-replacement"]),
        g.cities_index_html(), g.about_html(), g.how_we_estimate_html(), g.index_html(),
    ])
    NOT_TAILWIND = {"prose-slate"}  # never styled, by the CDN either

    def test_no_cdn_script(self):
        for page in self.SAMPLES():
            self.assertNotIn("cdn.tailwindcss.com", page)
            self.assertIn('href="/styles.css?v=', page)

    def test_css_covers_every_class(self):
        self.assertTrue(os.path.exists(CSS), "run ./build_css.sh")
        css = open(CSS).read()
        classes = set()
        for page in self.SAMPLES():
            for attr in re.findall(r'class="([^"]+)"', page):
                classes.update(attr.split())
        missing = []
        for c in sorted(classes - self.NOT_TAILWIND):
            esc = re.sub(r"([:/.\[\]])", r"\\\1", c)
            if "." + esc not in css:
                missing.append(c)
        self.assertEqual(missing, [])


class InternalLinking(unittest.TestCase):
    def test_region_city_links_its_neighbours(self):
        page = cost_page("roof-replacement", "fremont")
        bay = [s for (s, _n, r) in g.CA_CITIES if r == "bay-area" and s != "fremont"]
        linked = [s for s in bay if f'href="/how-much-does-roof-replacement-cost-in-{s}"' in page]
        self.assertGreaterEqual(len(linked), 5)
        self.assertNotIn('href="/how-much-does-roof-replacement-cost-in-fremont"', page)

    def test_featured_metro_still_gets_full_list(self):
        self.assertEqual(len(g.nearby_cities("sacramento")), 12)
        self.assertNotIn("sacramento", g.nearby_cities("sacramento"))

    def test_every_city_has_an_inbound_link_from_a_sibling_page(self):
        linked = set()
        for c in g.CITIES:
            linked.update(g.nearby_cities(c))
        orphans = [c for c, v in g.CITIES.items() if "region" in v and c not in linked]
        self.assertEqual(orphans, [])


class ScaledContentGuard(unittest.TestCase):
    """Region-clone pages (same index + note as every sibling) must not be indexed."""

    def test_clone_pages_noindex_metros_indexable(self):
        self.assertIn(g.ROBOTS_NOINDEX, cost_page("roof-replacement", "fremont"))
        self.assertIn(g.ROBOTS_NOINDEX, g.city_hub_html("fremont", g.CITIES["fremont"]))
        self.assertNotIn(g.ROBOTS_NOINDEX, cost_page("roof-replacement", "sacramento"))
        self.assertNotIn(g.ROBOTS_NOINDEX, g.city_hub_html("denver", g.CITIES["denver"]))
        self.assertNotIn(g.ROBOTS_NOINDEX, g.trade_hub_html("roof-replacement", g.TRADES["roof-replacement"]))

    def test_every_indexable_city_is_unique(self):
        notes = [(v["idx"], v["note"]) for c, v in g.CITIES.items() if g.is_indexable(c)]
        self.assertEqual(len(notes), len(set(notes)))
        self.assertEqual(sum(g.is_indexable(c) for c in g.CITIES), len(g.FEATURED))

    def test_flag_restores_indexing(self):
        old = g.INDEX_REGION_CLONES
        try:
            g.INDEX_REGION_CLONES = True
            self.assertNotIn(g.ROBOTS_NOINDEX, cost_page("roof-replacement", "fremont"))
        finally:
            g.INDEX_REGION_CLONES = old


class Casing(unittest.TestCase):
    def test_hvac_never_rendered_as_hvac_titlecase(self):
        self.assertEqual(g.title_case("HVAC installation"), "HVAC Installation")
        self.assertEqual(g.title_case("roof replacement"), "Roof Replacement")
        for page in (cost_page("hvac-installation", "denver"), g.index_html()):
            self.assertNotIn("Hvac", page)


class MonetizationLinks(unittest.TestCase):
    def test_ctas_are_external_sponsored_and_disclosed(self):
        page = cost_page("hvac-installation", "dallas")
        ctas = re.findall(r'<a href="([^"]+)"([^>]*)data-cta="compare-quotes-(?:top|bottom)"', page)
        self.assertEqual(len(ctas), 2)
        for href, attrs in ctas:
            self.assertTrue(href.startswith("https://"), href)
            self.assertIn("sponsored", attrs)
        self.assertEqual(page.count(g.DISCLOSURE), 2)

    def test_affiliate_template_switch(self):
        old = g.LEADGEN_AFFILIATE
        try:
            g.LEADGEN_AFFILIATE = "https://partner.example/r?svc={trade}&tt={tt}&zip={zip}"
            self.assertEqual(g.leadgen_url("roof-replacement", "95814"),
                             "https://partner.example/r?svc=roof-replacement&amp;tt=roofing&amp;zip=95814")
        finally:
            g.LEADGEN_AFFILIATE = old

    def test_every_trade_has_a_lead_slug(self):
        self.assertEqual(set(g.TT_SLUG), set(g.TRADES))


class FreshnessSignals(unittest.TestCase):
    def test_article_and_sitemap_dates(self):
        page = cost_page("fence-installation", "austin")
        art = [b for b in ld_blocks(page) if b["@type"] == "Article"][0]
        self.assertEqual(art["dateModified"], g.UPDATED)
        self.assertEqual(art["datePublished"], g.PUBLISHED)
        sm = g.sitemap_xml(["a"], ["b"], ["c"])
        self.assertEqual(sm.count(f"<lastmod>{g.UPDATED}</lastmod>"), 4)
        self.assertTrue(sm.startswith('<?xml'))

    def test_meta_description_not_cut_mid_word(self):
        self.assertEqual(g.clip("alpha beta gamma", 12), "alpha beta…")
        self.assertEqual(g.clip("short", 50), "short")
        for k, t in g.TRADES.items():
            page = g.trade_hub_html(k, t)
            desc = re.search(r'<meta name="description" content="([^"]*)"', page).group(1)
            self.assertTrue(desc.endswith(("…", ".")), desc[-30:])


if __name__ == "__main__":
    unittest.main()
