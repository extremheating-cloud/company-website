"""Build the self-hosted site into site/.

Run after build.py:   python3 build.py && python3 build_site.py
Or just:              python3 build_site.py     (it runs build.py first)

Takes every Framer embed in pages/, wraps it in a full HTML document with the header,
footer, meta and schema, and writes it to site/<route>/index.html so paths map to URLs
on any static host. pages/ is left alone — the embeds stay valid until cutover.
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PAGES = os.path.join(ROOT, "pages")
SITE = os.path.join(ROOT, "site")

import shell, homepage, site_data as D  # noqa: E402

# Routes that differ from their file path. hvac/ and company/ are build-time grouping,
# not URL structure — the live site serves those pages at the root.
def route_for(rel):
    url = "/" + rel.replace(os.sep, "/")
    # /locations/<city>/overview.html serves at /locations/<city>, but the plumbing
    # families genuinely live at /plumbing/<family>/overview — that is the live URL and
    # what every internal link points to. Only collapse the locations case.
    if url.endswith("/overview.html") and url.startswith("/locations/"):
        url = url[: -len("/overview.html")]
    elif url.endswith(".html"):
        url = url[: -len(".html")]
    url = url.replace("/hvac/", "/").replace("/company/", "/")
    # /locations/<city> keeps its folder; /plumbing/... keeps its prefix
    return url or "/"

def out_path(url):
    if url == "/":
        return os.path.join(SITE, "index.html")
    return os.path.join(SITE, url.strip("/"), "index.html")

def main():
    # regenerate the embeds first so site/ can never be built from stale input
    subprocess.run([sys.executable, os.path.join(HERE, "build.py")], check=True,
                   stdout=subprocess.DEVNULL)
    shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(SITE, exist_ok=True)

    written = []

    # --- homepage: authored directly, not an embed ---
    p = out_path("/")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(shell.document(homepage.META, homepage.homepage()))
    written.append("/")

    # --- every generated page ---
    for root, _, files in os.walk(PAGES):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, name), PAGES)
            html = open(os.path.join(root, name), encoding="utf-8").read()
            url = route_for(rel)
            meta = shell.meta_for(rel, html)
            meta["url"] = url
            meta["nav"] = "/" + url.split("/")[1] if url != "/" else ""
            body = shell._strip_embed(html)
            dest = out_path(url)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(shell.document(meta, body))
            written.append(url)

    # --- schedule wizard bundle ---
    # Built by `npm run build:schedule` and committed to assets/js/, because site/ is
    # generated and gitignored. Missing bundle is a warning, not a failure: the loader
    # in chrome.py falls back to /contact if the script 404s.
    src_js = os.path.join(ROOT, "assets", "js", "schedule.js")
    if os.path.exists(src_js):
        os.makedirs(os.path.join(SITE, "js"), exist_ok=True)
        shutil.copy2(src_js, os.path.join(SITE, "js", "schedule.js"))
    else:
        print("  ! assets/js/schedule.js missing — run: npm run build:schedule")

    # --- favicons ---
    # Served same-origin rather than from the CDN: the browser requests /favicon.ico
    # on every page load whether or not it is declared, and it was 404ing on all 307.
    for src_name, dest_name in (("logo-icon.ico", "favicon.ico"),
                                ("apple-touch-icon.png", "apple-touch-icon.png")):
        src = os.path.join(ROOT, "assets", "brand", src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(SITE, dest_name))
        else:
            print(f"  ! assets/brand/{src_name} missing")

    # --- redirects, for hosts that read a _redirects file (Cloudflare, Netlify) ---
    with open(os.path.join(SITE, "_redirects"), "w") as f:
        f.write("/refer  /referral  301\n")

    # --- sitemap ---
    urls = "".join(f"<url><loc>{D.SITE_URL}{u}</loc></url>" for u in sorted(set(written)))
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>'
                f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {D.SITE_URL}/sitemap.xml\n")

    print(f"site/ built — {len(written)} pages")
    return written

if __name__ == "__main__":
    main()
