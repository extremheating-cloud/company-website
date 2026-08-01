import * as React from "react"
import {
    COLORS,
    FONT_STACK,
    ensureMontserrat,
} from "https://framer.com/m/Theme-cgWgED.js@B2PNlINgwl1DTpD88aOo"

const GOOGLE_RATING = "4.9"

/* Curated Google reviews — updated 2026-07-23 (20 real reviews).
 * To refresh monthly: replace entries below (quote + name, city optional). */
const REVIEWS: { quote: string; name: string; city?: string }[] = [
    {
        quote: "Had a last-minute emergency before a holiday weekend and gave them a call and they were out within an hour to take a look at our air-conditioning unit.",
        name: "Desiree Hardin",
    },
    {
        quote: "Our technician, Tristan, was knowledgeable, explained things well, pleasant and friendly, even answering kids questions, and work diligently to complete the job.",
        name: "Brad & Jean Bisson",
    },
    {
        quote: "Both Garry and Tristan showed up on time and were courteous and friendly. Took the time to listen and detail everything they were doing.",
        name: "Josh Smith",
    },
    {
        quote: "Austin confirmed his arrival time once he was enroute. He quickly assessed the situation after hearing what was going on and went to work.",
        name: "James Campion",
    },
    {
        quote: "Services provided have been excellent and above expectations. Technicians very professional in helping solve issues.",
        name: "Woodrow Gibson",
    },
    {
        quote: "Called company who installed could not get here any sooner than 7days. Called Extreme they were here next day. Thanks Cody Evans job well done!",
        name: "Nick",
    },
    {
        quote: "Garry was very professional. He was prompt. Everything was explained clearly. Several options were presented. He was patient and very polite.",
        name: "Rodney Rohrer",
    },
    {
        quote: "Lee was professional, friendly, and did a great job going over all details related to our heating and AC unit. Couldn't be happier.",
        name: "Geoff Borasz",
    },
    {
        quote: "Josh was polite, he was knowledgeable and on time… This business has always provided the best service!",
        name: "Shannon Velasco",
    },
    {
        quote: "Cody did a thorough job checking our AC… He said he still checked it all out. It has worked fine ever since.",
        name: "Gwendolyn Ralston",
    },
    {
        quote: "Cody Evans showed up today for a chemical cleaning on the outside unit and some minor services inside. Professional, personable, and efficient with his work.",
        name: "Kenneth Douglas",
    },
    {
        quote: "Did a great job went over everything with us. Was a fast repair. Our grandson's graduation party is here this Saturday so we are glad to have the AC back running.",
        name: "Kip Smith",
    },
    {
        quote: "Very professional people to deal with… definitely recommend Extreme Heating & Air for first check & fast, high tech solutions & great crew. Thanks!",
        name: "Ferda G.",
    },
    {
        quote: "Our AC wasn't working well after the heatwave. Extreme had a technician out within 12 hours… he was great, got it fixed and didn't try to upsell me at all.",
        name: "Suzie Wegh",
    },
    {
        quote: "Awesome and professional. Will trust Extreme with all my HVAC needs from now on. Happy customer! Cody was great!",
        name: "Craig Johnson",
    },
    {
        quote: "Furnace cleaning on HVAC system that was installed a few years ago by Extreme was just accomplished again by Cory Witt, Extreme technician and he did an outstanding job.",
        name: "Jerry Siders",
    },
    {
        quote: "Tristan was incredible. He was quickly able to diagnose the issue… and provided me with a lot of useful information that will help me in the future.",
        name: "Tyrus Wesson",
    },
    {
        quote: "The tech was top notch!",
        name: "David Overla",
    },
    {
        quote: "I had Tristan and he did a wonderful job explaining and checking everything to help diagnose what the issue was. Would do business with them again.",
        name: "Michael Stringfield",
    },
    {
        quote: "Lee at Extreme is very professional. He has a warm, friendly presence and attitude that is contagious. One of the best technicians I have met over the past 15 years.",
        name: "Chad Baver",
    },
]

const VIDEO_EMBED =
    "https://www.youtube.com/embed/lUjB1pt9yBw?autoplay=1&rel=0&modestbranding=1"
const VIDEO_THUMB =
    "https://cdn.jsdelivr.net/gh/extremheating-cloud/extreme-assets@main/images/descriptive/van.png"

const FAQS = [
    {
        q: "Are your technicians licensed and insured?",
        a: "Yes. Our HVAC technicians are fully licensed and insured, and receive ongoing training to deliver safe, high-quality service in every home.",
    },
    {
        q: "Do you offer free estimates?",
        a: "Yes — we provide free estimates for system replacements, new installations, and major repair projects.",
    },
    {
        q: "Do you offer financing options?",
        a: "We partner with trusted lenders to offer convenient monthly payment options on qualifying equipment and repair work.",
    },
    {
        q: "Which areas do you serve?",
        a: "Extreme Heating, Air, Plumbing serves homeowners across Dayton, Cincinnati, Troy, Tipp City, and surrounding Miami Valley communities.",
    },
]

const STATS: [string, string][] = [
    ["20+", "Years of service"],
    ["25k+", "Jobs completed"],
    ["24/7", "Emergency service"],
    ["90%", "Same-day service"],
]

function AboutFaqReviews() {
    const [playVideo, setPlayVideo] = React.useState(false)
    const [openIndex, setOpenIndex] = React.useState<number | null>(0)

    React.useEffect(ensureMontserrat, [])

    const trackRef = React.useRef<HTMLDivElement | null>(null)
    const [dot, setDot] = React.useState(0)
    const [dotCount, setDotCount] = React.useState(1)

    React.useEffect(() => {
        const track = trackRef.current
        if (!track) return
        const measure = () =>
            setDotCount(Math.max(1, Math.round(track.scrollWidth / track.clientWidth)))
        const onScroll = () =>
            setDot(Math.round(track.scrollLeft / track.clientWidth))
        measure()
        window.addEventListener("resize", measure)
        track.addEventListener("scroll", onScroll, { passive: true })
        return () => {
            window.removeEventListener("resize", measure)
            track.removeEventListener("scroll", onScroll)
        }
    }, [])

    const page = (dir: number) => {
        const track = trackRef.current
        if (!track) return
        track.scrollBy({ left: dir * track.clientWidth, behavior: "smooth" })
    }

    return (
        <div className="xa-root">
            <style>{CSS}</style>

            <section className="xa-about">
                <div className="xa-wrap xa-about-grid">
                    <div className="xa-photo-wrap">
                        <div className="xa-photo-accent" aria-hidden />
                        {!playVideo ? (
                            <button
                                type="button"
                                className="xa-photo"
                                onClick={() => setPlayVideo(true)}
                                aria-label="Play company video"
                            >
                                <img src={VIDEO_THUMB} alt="The Extreme Team" />
                                <span className="play" aria-hidden>
                                    <svg
                                        width="30"
                                        height="30"
                                        fill="#fff"
                                        viewBox="0 0 24 24"
                                    >
                                        <path d="M8 5v14l11-7z" />
                                    </svg>
                                </span>
                            </button>
                        ) : (
                            <div className="xa-photo video">
                                <iframe
                                    src={VIDEO_EMBED}
                                    title="Extreme Heating, Air, Plumbing Video"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
                                    allowFullScreen
                                />
                            </div>
                        )}
                    </div>

                    <div>
                        <div className="xa-eyebrow purple">ABOUT EXTREME</div>
                        <h2 className="xa-h2">
                            Comfort &amp; efficiency you can trust.
                        </h2>
                        <p className="xa-body">
                            For over two decades, the Extreme Team has helped
                            homeowners across Dayton, Cincinnati, and the Miami
                            Valley stay comfortable in every season. From
                            emergency repairs to full system replacements,
                            we're known for honest recommendations, precise
                            workmanship, and friendly, no-pressure service.
                        </p>
                        <div className="xa-stats">
                            {STATS.map(([n, l]) => (
                                <div key={l} className="xa-stat">
                                    <div className="n">{n}</div>
                                    <div className="l">{l}</div>
                                </div>
                            ))}
                        </div>
                        <a href="/about" className="xa-outline-btn">
                            About Us&nbsp;&nbsp;→
                        </a>
                    </div>
                </div>
            </section>

            <section className="xa-faq">
                <div className="xa-wrap">
                    <div className="xa-center-head">
                        <div className="xa-eyebrow green">FAQ</div>
                        <h2 className="xa-h2">Your questions, answered.</h2>
                        <p className="xa-body">
                            Answers to the most common questions our customers
                            ask. If you don't see what you're looking for, our
                            team is always happy to help.
                        </p>
                    </div>
                    <div className="xa-acc">
                        {FAQS.map((item, i) => {
                            const open = openIndex === i
                            return (
                                <div
                                    key={i}
                                    className={
                                        "xa-acc-row" + (open ? " open" : "")
                                    }
                                >
                                    <button
                                        type="button"
                                        className="xa-acc-btn"
                                        aria-expanded={open}
                                        onClick={() =>
                                            setOpenIndex(open ? null : i)
                                        }
                                    >
                                        <span>{item.q}</span>
                                        <span
                                            className="xa-acc-toggle"
                                            aria-hidden
                                        >
                                            {open ? "−" : "+"}
                                        </span>
                                    </button>
                                    {open && (
                                        <p className="xa-acc-a">{item.a}</p>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </div>
            </section>

            <section className="xa-reviews">
                <div className="xa-wrap">
                    <div className="xa-center-head">
                        <div className="xa-eyebrow green">
                            CUSTOMER REVIEWS
                        </div>
                        <h2 className="xa-h2">
                            See what homeowners say about the Extreme Team.
                        </h2>
                        <p className="xa-body">
                            Real feedback from families across Dayton,
                            Cincinnati, and the Miami Valley — pulled directly
                            from our Google Reviews.
                        </p>
                        <div className="xa-rating-chip">
                            <span className="stars">★★★★★</span>
                            {GOOGLE_RATING} on Google
                        </div>
                    </div>
                    <div className="xa-carousel">
                        <button
                            type="button"
                            className="xa-arr prev"
                            aria-label="Previous reviews"
                            onClick={() => page(-1)}
                        >
                            ‹
                        </button>
                        <div className="xa-track" ref={trackRef}>
                            {REVIEWS.map((r, i) => (
                                <figure key={i} className="xa-review">
                                    <div className="stars" aria-label="5 stars">
                                        ★★★★★
                                    </div>
                                    <blockquote>"{r.quote}"</blockquote>
                                    <figcaption>
                                        <span className="who">
                                            {r.name}
                                            {r.city ? ` · ${r.city}` : ""}
                                        </span>
                                        <span className="via">
                                            via Google Reviews
                                        </span>
                                    </figcaption>
                                </figure>
                            ))}
                        </div>
                        <button
                            type="button"
                            className="xa-arr next"
                            aria-label="More reviews"
                            onClick={() => page(1)}
                        >
                            ›
                        </button>
                        {dotCount > 1 && (
                            <div className="xa-dots" aria-hidden>
                                {Array.from({ length: dotCount }, (_, i) => (
                                    <span
                                        key={i}
                                        className={
                                            "d" + (i === dot ? " on" : "")
                                        }
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </section>
        </div>
    )
}


const CSS = `
.xa-root, .xa-root *{ box-sizing:border-box; font-family:${FONT_STACK} }
.xa-wrap{ max-width:1280px; margin:0 auto; padding:0 40px }

.xa-eyebrow{ font-size:11.5px; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px }
.xa-eyebrow.green{ color:${COLORS.greenDark} }
.xa-eyebrow.purple{ color:${COLORS.purple} }
.xa-h2{
  font-style:italic; font-weight:900; font-size:33px; letter-spacing:-.5px; line-height:1.15;
  color:${COLORS.ink}; margin:0 0 12px;
}
.xa-body{ font-size:15px; line-height:1.6; font-weight:500; color:${COLORS.body}; margin:0 }

.xa-about{ background:#fff; padding:60px 0 64px }
.xa-about-grid{ display:grid; grid-template-columns:.95fr 1.05fr; gap:48px; align-items:center }
.xa-photo-wrap{ position:relative }
.xa-photo-accent{
  position:absolute; top:-16px; left:-16px; width:120px; height:120px;
  background:${COLORS.green}; border-radius:16px; z-index:0;
}
.xa-photo{
  position:relative; z-index:1; display:block; width:100%; height:380px; border:none; padding:0;
  border-radius:20px; overflow:hidden; cursor:pointer; background:${COLORS.softBg};
}
.xa-photo img{ width:100%; height:100%; object-fit:cover; display:block }
.xa-photo .play{
  position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:72px; height:72px; border-radius:999px; background:rgba(15,23,42,.55);
  display:grid; place-items:center; backdrop-filter:blur(4px); transition:background .15s ease;
}
.xa-photo:hover .play{ background:${COLORS.purple} }
.xa-photo.video iframe{ width:100%; height:100%; border:0; display:block }
.xa-photo:focus-visible{ outline:2px solid ${COLORS.purple}; outline-offset:3px }
.xa-body + .xa-stats{ margin-top:22px }
.xa-stats{ display:grid; grid-template-columns:1fr 1fr; gap:16px 24px; margin:22px 0 24px }
.xa-stat .n{ font-style:italic; font-weight:900; font-size:26px; color:${COLORS.purple} }
.xa-stat .l{ font-size:12px; font-weight:700; letter-spacing:.5px; text-transform:uppercase; color:${COLORS.muted}; margin-top:2px }
.xa-outline-btn{
  display:inline-flex; align-items:center; justify-content:center; min-height:44px;
  border:2px solid ${COLORS.purple}; color:${COLORS.purple}; font-weight:800; font-size:14.5px;
  border-radius:12px; padding:11px 24px; text-decoration:none;
  transition:background .15s ease, color .15s ease;
}
.xa-outline-btn:hover{ background:${COLORS.purple}; color:#fff }
.xa-outline-btn:focus-visible{ outline:2px solid ${COLORS.purple}; outline-offset:3px }

.xa-faq{ background:${COLORS.softBg}; padding:56px 0 60px }
.xa-center-head{ max-width:640px; margin:0 auto 28px; text-align:center }
.xa-acc{ max-width:760px; margin:0 auto; display:grid; gap:12px }
.xa-acc-row{ background:#fff; border-radius:14px; overflow:hidden; transition:box-shadow .18s ease }
.xa-acc-row:hover{ box-shadow:0 12px 30px rgba(84,39,112,.12) }
.xa-acc-btn{
  width:100%; display:flex; align-items:center; justify-content:space-between; gap:16px;
  padding:17px 20px; min-height:44px; border:none; background:none; cursor:pointer; text-align:left;
  font:700 15px ${FONT_STACK}; color:${COLORS.ink};
}
.xa-acc-btn:focus-visible{ outline:2px solid ${COLORS.purple}; outline-offset:-2px; border-radius:14px }
.xa-acc-toggle{
  width:30px; height:30px; flex:none; border-radius:999px; display:grid; place-items:center;
  background:${COLORS.purpleTint}; color:${COLORS.purple}; font-size:17px; font-weight:700;
  transition:background .15s ease, color .15s ease;
}
.xa-acc-row.open .xa-acc-toggle{ background:${COLORS.purple}; color:#fff }
.xa-acc-a{
  font-size:14px; line-height:1.65; font-weight:500; color:${COLORS.body};
  margin:0; padding:0 20px 18px; max-width:640px;
}

.xa-reviews{ background:#fff; padding:56px 0 64px }
.xa-rating-chip{
  display:inline-flex; align-items:center; gap:8px; margin-top:16px;
  border:1px solid ${COLORS.border}; border-radius:999px; padding:9px 16px;
  font-size:13px; font-weight:800; color:${COLORS.ink};
}
.xa-rating-chip .stars{ color:${COLORS.stars}; letter-spacing:1px }
/* custom reviews carousel (2a §9 cards; mobile per 2b) */
.xa-carousel{ position:relative; margin-top:12px }
.xa-track{
  display:flex; gap:16px; overflow-x:auto; scroll-snap-type:x mandatory;
  scrollbar-width:none; -webkit-overflow-scrolling:touch;
}
.xa-track::-webkit-scrollbar{ display:none }
.xa-review{
  flex:0 0 calc((100% - 48px) / 4); min-height:216px; scroll-snap-align:start; margin:0;
  border:1px solid ${COLORS.border}; border-radius:16px; padding:20px;
  background:#fff; display:flex; flex-direction:column; gap:10px;
}
.xa-review .stars{ color:${COLORS.stars}; letter-spacing:2px; font-size:13px }
.xa-review blockquote{ margin:0; font-size:14px; line-height:1.6; font-weight:500; color:${COLORS.body} }
.xa-review figcaption{ margin-top:auto; display:flex; flex-direction:column; gap:2px }
.xa-review .who{ font-weight:800; font-size:13px; color:${COLORS.ink} }
.xa-review .via{ font-size:11.5px; font-weight:500; color:${COLORS.muted} }
.xa-arr{
  position:absolute; top:50%; transform:translateY(-50%); z-index:2;
  width:36px; height:36px; border-radius:999px; border:1px solid ${COLORS.border};
  background:#fff; color:${COLORS.purple}; font-size:20px; line-height:1; cursor:pointer;
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 4px 12px rgba(15,23,42,.10); transition:background .15s ease;
}
.xa-arr:hover{ background:${COLORS.purpleTint} }
.xa-arr.prev{ left:-14px }
.xa-arr.next{ right:-14px }
.xa-dots{ display:flex; justify-content:center; gap:6px; margin-top:16px }
.xa-dots .d{ width:6px; height:6px; border-radius:999px; background:#D8D5DE; transition:all .2s ease }
.xa-dots .d.on{ width:18px; background:${COLORS.green} }

@media (max-width: 899px){
  .xa-wrap{ padding:0 20px }
  .xa-h2{ font-size:24px }
  .xa-about{ padding:44px 0 46px }
  .xa-about-grid{ grid-template-columns:1fr; gap:28px }
  .xa-photo{ height:200px }
  .xa-photo-accent{ width:84px; height:84px; top:-10px; left:-10px }
  .xa-outline-btn{ width:100%; min-height:48px }
  .xa-faq{ padding:40px 0 44px }
  .xa-reviews{ padding:40px 0 48px }
  .xa-review{ flex:0 0 100% }
  .xa-arr{ display:none }
}
`

export default AboutFaqReviews
