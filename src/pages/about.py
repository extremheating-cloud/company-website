import os
from layout import components as T
from data import business as D
from pages.company_shared import PHOTOS, UPDATED, UPDATED_ISO, shell, section, prose_section, slot_img

ABOUT = {
    "breadcrumb": [("Home", "/"), ("About Us", "")],
    "h1": "About {X} Heating, Air, Plumbing",
    "h1Highlight": "Extreme",
    "answer": ("We're a locally owned heating, cooling and plumbing company, working the Dayton "
               f"and Cincinnati metros out of four Ohio shops since {D.FOUNDED}. We hold Ohio "
               f"licenses in both trades, and we've done more than "
               f"{D.JOBS_COMPLETED_LONG.rstrip('+')} jobs."),
    "intro": "Locally owned. Extremely committed.",
    # The rating is a Birdeye aggregate across platforms; never label it "on Google".
    "heroChips": ["Family Owned &amp; Operated", f"{D.YEARS_LOCAL} Years Local",
                  f"{D.GOOGLE_RATING} from {D.REVIEW_COUNT} reviews",
                  f"{D.LICENSE_HVAC} &middot; {D.LICENSE_PLUMBING}"],
    "heroPhoto": {"src": PHOTOS["companyGroup"], "pos": "50% 42%",
                  "alt": f"The {D.COMPANY} team in front of a company service van"},
    "storyPhoto": {"src": PHOTOS["skyline"],
                   "alt": f"An {D.COMPANY} service van with the Dayton skyline behind it"},
    "story": {
        "h2": "How long have you been doing this?",
        # TODO: opening years for the Troy and Waynesville offices.
        "p1": f"We started in {D.FOUNDED} the way most good service companies do: one van, one toolbox, and a promise to show up when we said we would. Mason opened in {D.MASON_OPENED}. Today it's four Ohio shops and a full crew of licensed HVAC and plumbing techs covering the same two metros.",
        "p2": "The work got bigger. The way it's priced didn't. You get a flat quote and you approve it before we open anything up, and a real person still answers the phone, day or night.",
    },
    "values": [
        {"t": "Honest pricing, upfront",
         "d": "Flat quotes you approve before we start. No surprise line items, ever."},
        {"t": "Your home, respected",
         "d": "Shoe covers, drop cloths, and a workspace left cleaner than we found it."},
        {"t": "Fast when it matters",
         "d": "90% of calls handled same-day, with a 24/7 line for real emergencies."},
        {"t": "Built on referrals",
         "d": "Most new customers come from old ones. We earn that, one visit at a time."},
    ],
    "stats": [
        {"n": D.YEARS_LOCAL, "cap": "years serving Ohio homes"},
        {"n": f'<span class="st">★</span> {D.GOOGLE_RATING}',
         "cap": f"average across {D.REVIEW_COUNT} {D.REVIEW_SOURCE}"},
        {"n": D.SAME_DAY, "cap": "of calls handled same-day"},
        {"n": "24/7", "cap": "emergency service line"},
    ],
    # Indoor-shot crews run first so the backdrop changes once; within a crew, title rank then last name.
    "team": [
        ("Leadership", [
            ("Douglas Washburn", "Founder &amp; Owner", "douglas-washburn"),
            ("Ryan Basinger", "Owner", "ryan-basinger"),
        ]),
        ("In the office", [
            ("Cyndi Reeves", "Financial Controller", "cyndi-reeves"),
            ("Aaron Matthew", "Operations Coordinator", "aaron-matthew"),
            ("Samantha Desaro", "Office Coordinator", "samantha-desaro"),
            ("David Engelbrink", "Inventory Coordinator", "david-engelbrink"),
            ("Aleasha King", "Customer Service Rep", "aleasha-king"),
        ]),
        ("Comfort Advisors", [
            ("Joe Richardson", "Comfort Advisor", "joe-richardson"),
            ("Shaun Vamos", "Comfort Advisor", "shaun-vamos"),
        ]),
        ("HVAC Service", [
            ("Ric White", "HVAC Service Manager", "ric-white"),
            ("Josh Adkins", "HVAC Technician", "josh-adkins"),
            ("Cody Evans", "HVAC Technician", "cody-evans"),
            ("Garry Key", "HVAC Technician", "garry-key"),
            ("Austin Robinson", "HVAC Technician", "austin-robinson"),
            ("Tristan Robinson", "HVAC Technician", "tristan-robinson"),
            ("Lee Sellon", "HVAC Technician", "lee-sellon"),
            ("Emmanuel Tshiala", "HVAC Technician", "emmanuel-tshiala"),
            ("Corey Witt", "HVAC Technician", "corey-witt"),
        ]),
        # Titles must fit a 135px tile on a 320px phone, hence "Install" not "Installation".
        ("HVAC Installation", [
            ("Anthony Griffin", "HVAC Install Lead", "anthony-griffin"),
            ("Tyler Hardy", "HVAC Install Lead", "tyler-hardy"),
            ("Brandon Orona", "HVAC Install Lead", "brandon-orona"),
            ("Robbie Collier", "HVAC Install Helper", "robbie-collier"),
            ("Chase Conway", "HVAC Install Helper", "chase-conway"),
            ("Jayvon Kilgore", "HVAC Install Helper", "jayvon-kilgore"),
            ("Logan Washburn", "HVAC Install Helper", "logan-washburn"),
        ]),
        ("Plumbing", [
            ("Andre Roeder", "Master Plumber", "andre-roeder"),
            ("Jason Romine", "Plumber", "jason-romine"),
            ("Chris Weekley", "Plumber", "chris-weekley"),
            ("Jim Nix", "Plumbing Dispatcher", "jim-nix"),
        ]),
        ("Duct Cleaning", [
            ("Matt Carson", "Duct Cleaning Lead", "matt-carson"),
            ("Jason Scales", "Duct Cleaning Helper", "jason-scales"),
        ]),
    ],
    "areas": [
        {"t": "Dayton metro",
         "d": "Dayton, Kettering, Beavercreek, Centerville, Springboro, Huber Heights and the surrounding Miami Valley.",
         "lm": "our Dayton service area →", "href": "/locations/dayton"},
        {"t": "Cincinnati metro",
         "d": "Cincinnati, Mason, West Chester, Fairfield, Middletown, Lebanon and communities across the metro.",
         "lm": "our Cincinnati service area →", "href": "/locations/cincinnati"},
    ],
    "table": {
        "eyebrow": "AT A GLANCE",
        "h2": "Who am I actually hiring?",
        "id": "at-a-glance",
        "takeaway": f"We've served the Dayton and Cincinnati metros since {D.FOUNDED}, under "
                    "Ohio HVAC license #37179.",
        "caption": "Company details at a glance",
        "columns": ["What you're asking", "The answer"],
        "rows": [
            ["Founded", f"{D.FOUNDED}, locally owned ever since"],
            ["Trades", "Heating, cooling, indoor air quality, residential plumbing"],
            ["Service area", "Dayton and Cincinnati metros, nine Ohio counties"],
            ["Offices", " · ".join(o["locality"] for o in D.OFFICES)],
            ["Ohio licenses", f'HVAC {D.LICENSE_HVAC} &middot; Plumbing {D.LICENSE_PLUMBING}'],
            ["Legal entities", f"{D.ENTITY_HVAC} (HVAC) · {D.ENTITY_PLUMBING} (plumbing)"],
            ["Jobs completed", D.JOBS_COMPLETED_LONG],
            ["Customer reviews", f"{D.GOOGLE_RATING}-star average across {D.REVIEW_COUNT} reviews"],
            ["Emergency service", "24/7, every day of the year"],
            ["Same-day service", f"{D.SAME_DAY} same-day service"],
            ["Membership", f'X-Plan, {D.XPLAN["annual"]} per year or {D.XPLAN["monthly"]} per month per system'],
        ],
    },
    "faqEyebrow": "ABOUT THE COMPANY",
    "faqH2": "What else do people ask?",
    # TODO: add a commercial-work FAQ once the client confirms whether it is in scope.
    "faq": [
        {"q": "When did you start?",
         "a": f"{D.FOUNDED}, and we've been locally owned ever since. The Mason office opened "
              f"in {D.MASON_OPENED}."},
        {"q": "Are you a franchise?",
         "a": "No. Locally owned, run out of four Ohio offices, and not part of a national "
              "chain."},
        {"q": "What are your Ohio license numbers?",
         "a": "Ohio HVAC #37179 and Ohio plumbing #13557. Both are on our estimates, invoices "
              'and trucks, as Ohio requires, and the <a href="/terms">license numbers and '
              'program terms</a> are on the terms page.'},
        {"q": "Do you do both HVAC and plumbing?",
         "a": 'Yes. Heating, cooling, indoor air quality and residential plumbing. One phone '
              'number and one <a href="/maintenance">X-Plan membership</a> cover both trades.'},
        {"q": "How many jobs have you done?",
         "a": f"More than {D.JOBS_COMPLETED_LONG.rstrip('+')} across the two metros since "
              f"{D.FOUNDED}."},
        {"q": "How do I get in touch?",
         "a": f'<a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> reaches all four offices and is '
              'the line answered at any hour. Local numbers for each shop, plus '
              '<a href="/contact">addresses and directions</a>, are on the contact page, and '
              '<a href="/referral">Extreme Rewards</a> pays you for sending someone new.'},
    ],
}

def about_hero(d):
    return f'''<div class="xsp-hero">
  {T.hero_mark()}
  <div class="xsp-hero-grid xco-hero-grid-400">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
      {T.answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      {T.chips(d["heroChips"])}
    </div>
    {slot_img("xco-heroslot", d.get("heroPhoto"), "DROP A TEAM PHOTO HERE")}
  </div>
</div>'''

def about_page(d, root_class):
    story = f'''<div>
  <div class="xco-story">
    <div>
      <div class="xsp-eyebrow">OUR STORY</div>
      <h2 class="xsp-h2">{d["story"]["h2"]}</h2>
      <p>{d["story"]["p1"]}</p>
      <p>{d["story"]["p2"]}</p>
    </div>
    {slot_img("xco-slot", d.get("storyPhoto"), "DROP A FOUNDERS / FIRST-VAN PHOTO",
              style="height:280px")}
  </div>
</div>'''
    licensed = prose_section(
        "LICENSED IN OHIO", "Are you licensed and insured?",
        ["Yes, on both counts: Ohio HVAC license #37179 and Ohio plumbing license #13557. Every "
         "tech is licensed and insured, and drug-tested and background-checked before they set "
         "foot in your house.",
         f'Heating and cooling runs through {D.ENTITY_HVAC}, plumbing through '
         f'{D.ENTITY_PLUMBING}. Both sets of '
         '<a href="/terms">license numbers and program terms</a> are on the terms page.'],
        sid="licensed")
    # TODO: mention the tech name and photo sent before arrival, if the client confirms it happens.
    who = prose_section(
        "AT YOUR DOOR", "Who will come to my house?",
        ["A licensed, insured technician in a marked company van. Shoe covers and drop cloths "
         "go down before anything starts, and we leave the space cleaner than we found it."],
        sid="who")
    values = "".join(
        f'''<div class="xco-ccard"><span class="xsp-glyph"><i></i><i></i></span>
  <div class="t">{v["t"]}</div><div class="d">{v["d"]}</div></div>''' for v in d["values"])
    values = section("WHAT WE STAND FOR", "How do you price a job?",
                     f'<div class="xco-vals">{values}</div>', sid="pricing",
                     lead=["Flat price, quoted before we start, and you approve it before "
                           "anything gets opened up. Estimates on replacements and new installs "
                           "are free, X-Plan members take 15% off repairs, and "
                           '<a href="/financing-options">financing covers the bigger '
                           "jobs</a>."])
    stats = "".join(
        f'<div><div class="n">{s["n"]}</div><div class="cap">{s["cap"]}</div></div>' for s in d["stats"])
    stats = f'''<div class="xco-stats">
  <img class="mark" src="{T.X_MARK}" alt=""{T.dim_attrs(T.X_MARK)} loading="lazy" decoding="async" style="position:absolute;right:-70px;bottom:-60px;width:300px;opacity:.06;transform:rotate(-8deg);filter:brightness(0) invert(1)">
  <div class="grid">{stats}</div>
</div>'''
    def crew(title, members, lead=False):
        cards = "".join(
            f'''<figure class="xco-mem"><img src="{PHOTOS["team"][slug]}" alt="{name}, {role.replace("&amp;", "and")} at {D.COMPANY}"{T.dim_attrs(PHOTOS["team"][slug])} loading="lazy" decoding="async">
    <figcaption><span class="nm">{name}</span><span class="rl">{role}</span></figcaption></figure>'''
            for name, role, slug in members)
        return f'''<div class="xco-crew">
  <div class="xco-crew-hd"><h3>{title}</h3><span class="n">{len(members)}</span></div>
  <div class="xco-team{" xco-team-lead" if lead else ""}">{cards}</div>
</div>'''
    team = section(
        "THE TEAM", "Who works here?",
        "".join(crew(t, m, lead=(t == "Leadership")) for t, m in d["team"]),
        sid="team",
        lead=[f"All {sum(len(m) for _, m in d['team'])} of us, across four Ohio shops. "
              "Every technician is licensed, insured, drug-tested and background-checked "
              "before they set foot in your house."])
    areas = "".join(
        f'''<a class="xsp-card" href="{a["href"]}">
  <span class="txt"><span class="t">{a["t"]}</span><br><span class="d">{a["d"]}</span></span>
  <span class="lm">{a["lm"]}</span><span class="mrow">→</span>
</a>''' for a in d["areas"])
    areas = section("WHERE WE WORK", "Do you come out to my town?",
                    f'<div class="xco-2col">{areas}</div>', sid="service-area",
                    lead=["Probably. We work across nine Ohio counties between the two metros: "
                          "Montgomery, Greene, Miami, Warren, Butler, Clark, Hamilton, Preble "
                          "and Darke."])
    # The address table stays on /contact only; repeating it here reads as duplicate content.
    offices = prose_section(
        "OUR OFFICES", "Where are your offices?",
        ['Four of them, all in Ohio: '
         + ", ".join(o["locality"] for o in D.OFFICES[:-1]) + f' and {D.OFFICES[-1]["locality"]}. '
         f'They all route to the same number, '
         f'<a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>, and the '
         '<a href="/contact">addresses and directions</a> are on the contact page.'],
        sid="offices")
    reviews = prose_section(
        "WHAT CUSTOMERS SAY", "What do customers say?",
        [f"{D.GOOGLE_RATING} stars across {D.REVIEW_COUNT} {D.REVIEW_SOURCE} from homeowners "
         "around Dayton and Cincinnati. That number is a Birdeye aggregate, so it pulls from "
         "every platform people leave reviews on rather than from a single site."],
        sid="reviews")
    body = f'''{about_hero(d)}
<div class="xco-body">
  {story}
  {licensed}
  {who}
  {values}
  {stats}
  {team}
  {offices}
  {areas}
  {reviews}
  {T.table_section(d["table"])}
  {T.faq(d["faq"], d["faqEyebrow"], h2=d["faqH2"])}
  {T.updated_line(UPDATED, UPDATED_ISO)}
</div>'''
    return shell(root_class, body)

def pages(root):
    return [(os.path.join(root, "pages", "company", "about.html"), about_page, ABOUT, "xsp-about")]
