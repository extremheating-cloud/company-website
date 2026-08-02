"""Full HTML documents for the self-hosted site.

The Framer build wraps each page's content in a `srcdoc` iframe, so the page itself
has a title and meta description and then no headings at all — measured on the live
site, `/locations/dayton` renders zero `<h1>` and 41x more copy inside iframes than
outside. This module is what fixes that: same content, in the document, where a
crawler reads it.

Output goes to site/, leaving pages/ as the Framer embeds so both stay buildable
until cutover.
"""
import os
import re
import site_data as D
import chrome
import template as T

FONT = ("https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@"
        "0,400;0,500;0,600;0,700;0,800;0,900;1,800;1,900&display=swap")

BASE_CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:#0F172A;color-scheme:light;
font-family:"Montserrat",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial;
overflow-x:hidden}
img{max-width:100%}
main{display:block}
/* The header is sticky, so a hash link would otherwise land its target underneath
   it. The embed script measured this at jump time; standalone it is one rule. */
[id]{scroll-margin-top:96px}
:where(a,button,input,summary):focus-visible{outline:3px solid #61BC47;outline-offset:2px}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:#5F2980;padding:12px 18px;
font-weight:800;z-index:1000;border-radius:0 0 10px 0}
.skip:focus{left:0}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;
animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
"""

def _strip_embed(html):
    """The generated pages are Framer embeds: a <section class="xhac-svc"> carrying its
    own <style> and <script>. For the standalone site we keep all of it — the CSS and
    behaviour are the same — but the anchor script's cross-frame handling is dead
    weight without an iframe, so it is removed rather than left to no-op."""
    html = re.sub(r'\n?\s*<script>\s*\(\(\) => \{\s*const root = document\.currentScript'
                  r'.*?</script>', "", html, flags=re.S)
    return html.strip()

def _schema(page):
    """LocalBusiness + areaServed. No address on service-area pages — those are not
    storefronts, and marking them up as such would be a misrepresentation."""
    import json
    data = {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "name": "Extreme Heating, Air, Plumbing",
        "url": D.SITE_URL + page["url"],
        "telephone": D.PHONE_E164,
        "aggregateRating": {"@type": "AggregateRating",
                            "ratingValue": D.GOOGLE_RATING, "bestRating": "5"},
        "areaServed": [{"@type": "City", "name": n} for n in page.get("areaServed", [])
                       ] or [{"@type": "City", "name": "Dayton"},
                             {"@type": "City", "name": "Cincinnati"}],
    }
    if page.get("address"):
        a = page["address"]
        data["address"] = {"@type": "PostalAddress", "streetAddress": a["street"],
                           "addressLocality": a["locality"], "addressRegion": a["region"],
                           "postalCode": a["zip"], "addressCountry": "US"}
    return ('<script type="application/ld+json">' +
            json.dumps(data, separators=(",", ":")) + "</script>")

def document(page, body_html):
    """page: {url, title, description, h1?, areaServed?, address?, nav?}"""
    url = page["url"]
    canonical = D.SITE_URL + (url if url != "/" else "/")
    title = page["title"]
    desc = page["description"]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{D.COMPANY}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#5E2C7E">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT}">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<style>{BASE_CSS}{chrome.CSS}</style>
{_schema(page)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{chrome.header(page.get("nav", ""))}
<main id="main">
{body_html}
</main>
{chrome.footer()}
{chrome.JS}
</body>
</html>
'''

# ---------------------------------------------------------------- page metadata
# Titles follow the handoff pattern: "{Service} in {City}, OH | Extreme Heating, Air,
# Plumbing". Descriptions are written per page rather than templated, because a
# duplicated meta description is worth less than none.
def meta_for(rel_path, html):
    """Derive title/description/url from a generated embed. Falls back to the page's
    own H1 so nothing ships with a placeholder title."""
    url = "/" + rel_path.replace("\\", "/")
    url = url[:-len("/overview.html")] if url.endswith("/overview.html") else url[:-len(".html")]
    url = url.replace("/company/", "/").replace("/hvac/", "/")
    if url in ("/index", ""):
        url = "/"
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1txt = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
    intro = re.search(r'<p class="xsp-intro">(.*?)</p>', html, re.S)
    introtxt = re.sub(r"<[^>]+>", "", intro.group(1)).strip() if intro else ""
    introtxt = re.sub(r"\s+", " ", introtxt)[:155]
    return {
        "url": url,
        "title": f"{h1txt} | {D.COMPANY}" if h1txt else D.COMPANY,
        "description": introtxt or f"{D.COMPANY} — heating, cooling and plumbing across Dayton and Cincinnati.",
        "nav": "/" + url.split("/")[1] if url != "/" else "",
    }
