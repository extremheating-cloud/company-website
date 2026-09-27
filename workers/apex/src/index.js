const ORIGIN = "https://followup-pro-37ed6.web.app";
const CANONICAL = "https://www.extremeheating.com";
const APEX = "https://extremeheating.com";

// Onboarding's root-relative /assets/ and /img/ would collide with the marketing site's on www.
const PROXIED = ["/onboarding", "/assets/", "/img/"];

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.hostname !== "extremeheating.com") {
      return Response.redirect(APEX + url.pathname + url.search, 302);
    }

    if (!PROXIED.some((p) => url.pathname.startsWith(p))) {
      return Response.redirect(CANONICAL + url.pathname + url.search, 301);
    }

    const upstream = await fetch(ORIGIN + url.pathname + url.search, request);
    const res = new Response(upstream.body, upstream);
    if ((res.headers.get("content-type") || "").includes("text/html")) {
      res.headers.set("Cache-Control", "no-store");
    }
    return res;
  },
};
