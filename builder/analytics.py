"""Third-party tags, exactly as supplied by the client 2026-08-03.

Kept in one module rather than pasted into shell.py so the inventory is readable in
one place. Anything that talks to a third party from the browser belongs here, and
the privacy policy's service-provider list is written from this file.

WHAT LOADS, AND FROM WHOM

    Google Tag Manager      GTM-TG8GZWXC          googletagmanager.com
    Google Analytics 4      G-GCH0RVQ88Y          googletagmanager.com
    Google Ads              AW-974361798          googletagmanager.com
    Meta Pixel              1116748220634990      connect.facebook.net
    Broccoli widget         c5182eae-968f-...     cdn.broccoli.com
    Podium widget           47709907-f239-...     connect.podium.com
    ServiceTitan scheduler  tenant 770617940      go.servicetitan.com  (iframe, on demand)
    FollowUp Pro chat       (A2P opt-in path 2)   followup-pro-37ed6.web.app

BOOKING FLOW, decided 2026-08-03: the site keeps its own scheduling wizard. Every
.js-schedule button opens assets/js/schedule.js, exactly as before. The ServiceTitan
modal below is loaded but is NOT wired to any button on this site — it exists so the
Broccoli widget can trigger it by posting {type: "OPEN_ST_SCHEDULER"} or dispatching
the OPEN_ST_SCHEDULER event. That is deliberate. Do not "fix" the apparently dead
listener by pointing the Schedule buttons at it.

THREE THINGS WORTH KNOWING, recorded here because they are easy to forget later:

1. PERFORMANCE. This is not a neutral addition. The competitor audit on 2026-08-02
   scored Eco Plumbers 22/100 on performance against our 76, and the report attributes
   it specifically to "6.1 MB of third-party JS from broccoli.com and ServiceTitan" —
   the same two vendors as below. Their LCP is 7.75 to 9.70 s. Ours was 3.42 s before
   this. Measure after launch rather than assuming; the mitigations that do not cost
   any tracking are already applied here (async on everything that allows it, defer on
   Podium, ServiceTitan loaded only when someone opens it).

2. DOUBLE COUNTING. GTM can fire GA4 itself, and gtag.js for G-GCH0RVQ88Y loads
   directly below as well. If a GA4 tag also exists inside the GTM container, every
   pageview is counted twice. Nothing here can detect that; it has to be checked in
   the container. [NEEDS: confirm whether GTM-TG8GZWXC contains a GA4 configuration
   tag for G-GCH0RVQ88Y. If it does, one of the two should go.]

3. NUMBER SWAPPING. The last gtag config enables Google Ads dynamic number insertion
   for (844) 584-7399, so Google replaces that number on the page with a tracking
   one. It matches on the exact string, so the four local office numbers added on
   2026-08-03 are NOT swapped and will report as untracked. That may be what you
   want, since they are the numbers on the Google Business Profiles, but it is a
   decision rather than an accident.
"""

# Everything that has to be in <head>. Order is the client's, and it matters: the GTM
# snippet expects to run before anything pushes to dataLayer.
HEAD = """
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TG8GZWXC');</script>
<!-- End Google Tag Manager -->
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GCH0RVQ88Y"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-974361798"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GCH0RVQ88Y');
  gtag('config', 'AW-974361798');
</script>

<!-- GTAG For Phone Call Click -->
<script>
function gtag_report_conversion(url) {
  var callback = function () {
    if (typeof(url) != 'undefined') {
      window.location = url;
    }
  };
  gtag('event', 'conversion', {
      'send_to': 'AW-974361798/mAc6CKqtoa0bEMapztAD',
      'value': 1.0,
      'currency': 'USD',
      'event_callback': callback
  });
  return false;
}
</script>

<script>
  gtag('config', 'AW-974361798/mC9aCLvK9rkbEMapztAD', {
    'phone_conversion_number': '(844) 584-7399'
  });
</script>

<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1116748220634990');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1116748220634990&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
"""

# Everything that goes immediately after <body>. The GTM noscript iframe has to be
# first inside body per Google's own instruction.
BODY_START = """
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TG8GZWXC"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
<script
  id="broccoli-widget-embed"
  src="https://cdn.broccoli.com/c5182eae-968f-47b1-acb0-be2459d2e4c5.js"
></script>

<script defer src="https://connect.podium.com/widget.js#ORG_TOKEN=47709907-f239-4a8c-8ec9-3f273c4f629b" id="podium-widget" data-organization-api-token="47709907-f239-4a8c-8ec9-3f273c4f629b"></script>

<!-- FollowUp Pro chat widget. This is opt-in path 2 in the A2P 10DLC registration,
     so it has to be on EVERY page: the registration says "available on every page of
     https://www.extremeheating.com" and a homepage-only widget makes that false.
     It renders in a shadow root on <extreme-chat>, so site CSS cannot reach in and it
     cannot leak out. Nothing renders or hits the network until a visitor sends
     something, so a bounce costs nothing.
     Do not fork this script or self-host a modified build: the consent disclosure it
     shows is quoted character for character in the registration and stored verbatim
     as the TCPA record. Changes go through FollowUp Pro. -->
<script src="https://followup-pro-37ed6.web.app/chat-widget.js"
        data-endpoint="https://us-central1-followup-pro-37ed6.cloudfunctions.net"
        data-phone="+18445847399"
        data-phone-display="(844) 584-7399"
        defer></script>

<!-- Extreme skin for the chat widget.
     The widget ships a generic look that does not speak the rest of the site's
     language, and on a phone it is the only surface a visitor sees full screen.
     This restyles it. What it does NOT do is fork the script: the build above is
     the vendor's, byte for byte, from their CDN. No DOM is added, moved or
     relabeled, no text is edited, and the consent disclosure — quoted verbatim in
     the A2P registration and stored as the TCPA record — is untouched. This is one
     <style> element appended to the widget's open shadow root, so deleting this
     block reverts the widget to the vendor's own appearance and nothing else.
     If FollowUp Pro renames their internal classes, these rules stop matching and
     it reverts on its own. That is the intended failure mode.

     Two of the rules below are fixing the vendor's bugs rather than their taste,
     and both are worth reporting upstream:
       1. .fine (the consent paragraph) asks for 12px slate in their own stylesheet
          and never gets it, because .card p is one point more specific and wins at
          14px in full ink. That is why the disclosure renders as the largest block
          in the form. We apply their intent, a half step larger than they asked.
       2. Nothing in the fullscreen phone layout accounts for the safe area, so on
          a notched iPhone the header sits under the status bar and the footer under
          the home indicator. -->
<script>
(function () {
  var CSS = `
/* header ------------------------------------------------------------------
   The subtitle is 48 characters and .hdr-id gets 254px at a 390px width, so two
   lines was never avoidable. Two tidy lines read as deliberate; what read as
   broken was the status dot centering itself against a two-line block. */
.hdr{padding:13px 10px 13px 16px;gap:8px}
.hdr-title{font-size:15.5px;font-weight:800;letter-spacing:-.02em}
.hdr-sub{align-items:flex-start;font-size:11.5px;line-height:1.35;gap:7px}
.hdr-sub .dot{margin-top:4px;box-shadow:0 0 0 3px rgba(97,188,71,.22)}
.hdr-btn{width:40px;height:40px;border-radius:10px}
.wrap[data-fullscreen="true"] .hdr{padding-top:calc(13px + env(safe-area-inset-top))}

/* one surface, not two -----------------------------------------------------
   The gate form was a bordered, shadowed, gradient-topped card sitting on a
   background one shade off from it, which on a full-screen phone panel is a
   container drawn twice. The header already carries a green gradient rule 20px
   above the card's, so the card's is redundant as well as fussy. The cloud
   backdrop stays, because behind message bubbles that contrast does real work. */
.log{padding:14px 14px 8px}
.card{border:0;border-radius:16px;padding:16px 15px;box-shadow:0 2px 14px rgba(15,23,42,.08)}
.card::before{display:none}
.card h3{font-size:17px;font-weight:800;letter-spacing:-.02em;margin:0 0 6px}
.card p{font-size:14px;line-height:1.5;margin:0 0 14px}

/* fields in the site's shape: 12px radius, not 4. 16px type on the inputs is
   load-bearing and stays — anything smaller and iOS zooms the page on focus. */
.fld{margin:0 0 12px}
.fld label{font-size:12px;font-weight:700;letter-spacing:.01em;color:var(--exc-slate);margin:0 0 5px}
.fld input,.fld textarea,.composer textarea{border-radius:12px;border:1.5px solid var(--exc-border);padding:12px 13px}
.fld textarea{min-height:82px;line-height:1.5}

/* the disclosure. Secondary, never buried: #64748B on white is 4.76:1, which
   clears AA, and the links keep a real underline and full brand purple. */
.card p.fine{font-size:12.5px;line-height:1.55;color:var(--exc-slate);margin:0 0 14px}
.card p.fine a{color:var(--exc-purple);font-weight:700;text-decoration:underline;text-underline-offset:2px}

/* CTA in the site's weight and radius */
.card-actions{margin-top:2px}
.btn{font-size:15.5px;font-weight:800;letter-spacing:0;border-radius:12px;min-height:48px;
box-shadow:0 2px 12px rgba(95,41,128,.26)}

/* the bottom was three stacked full-width strips competing for one corner */
.lock{font-size:12.5px;font-weight:700;color:var(--exc-slate);padding:12px}
.lock svg{width:15px;height:15px;stroke:var(--exc-slate)}
.composer{padding:10px 12px}
.send{width:46px;height:46px}
.foot{font-size:11.5px;padding:0 14px 12px}
.foot a{font-weight:700}
.wrap[data-fullscreen="true"] .foot{padding-bottom:calc(12px + env(safe-area-inset-bottom))}

/* bubbles pick up the site's radius */
.bub{font-size:14.5px;border-radius:14px}
`;
  var ID = "exc-extreme-skin";
  function skin() {
    var host = document.querySelector("extreme-chat");
    if (!host || !host.shadowRoot) return false;
    if (host.shadowRoot.getElementById(ID)) return true;
    var s = document.createElement("style");
    s.id = ID;
    s.textContent = CSS;
    // Appended last so it wins on order wherever specificity ties. Where it does
    // not tie, the selectors above are written to out-specify, not to shout with
    // !important — that would also override the vendor's own state rules for
    // errors, disabled buttons and focus.
    host.shadowRoot.appendChild(s);
    return true;
  }
  if (skin()) return;
  // The widget script is deferred, so the element usually is not there yet.
  var mo = new MutationObserver(function () { if (skin()) mo.disconnect(); });
  mo.observe(document.documentElement, { childList: true, subtree: true });
  setTimeout(function () { mo.disconnect(); }, 20000);
})();
</script>

<script>
(function () {
  function openSTScheduler() {
    if (document.getElementById("st-modal")) return;

    const modal = document.createElement("div");
    modal.id = "st-modal";
    modal.style.position = "fixed";
    modal.style.top = "0";
    modal.style.left = "0";
    modal.style.width = "100%";
    modal.style.height = "100%";
    modal.style.background = "rgba(0,0,0,0.6)";
    modal.style.zIndex = "999999";
    modal.style.display = "flex";
    modal.style.alignItems = "center";
    modal.style.justifyContent = "center";

    const box = document.createElement("div");
    box.style.width = "90%";
    box.style.maxWidth = "1100px";
    box.style.height = "90%";
    box.style.background = "#fff";
    box.style.borderRadius = "16px";
    box.style.overflow = "hidden";
    box.style.position = "relative";

    const iframe = document.createElement("iframe");
    iframe.src = "https://go.servicetitan.com/webscheduler?tenantid=770617940";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";

    const close = document.createElement("div");
    close.innerHTML = "×";
    close.style.position = "absolute";
    close.style.top = "12px";
    close.style.right = "16px";
    close.style.fontSize = "28px";
    close.style.cursor = "pointer";
    close.style.zIndex = "10";

    close.onclick = () => modal.remove();
    modal.onclick = (e) => {
      if (e.target === modal) modal.remove();
    };

    box.appendChild(close);
    box.appendChild(iframe);
    modal.appendChild(box);
    document.body.appendChild(modal);
  }

  // Listen for iframe trigger
  window.addEventListener("message", function (event) {
    if (event.data && event.data.type === "OPEN_ST_SCHEDULER") {
      openSTScheduler();
    }
  });

  // Optional: allow triggering from same page too
  window.addEventListener("OPEN_ST_SCHEDULER", openSTScheduler);
})();
</script>
"""
