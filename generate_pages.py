#!/usr/bin/env python3
"""Programmatic SEO page generator for aitoolpick.co.uk"""
import os, json, re
from datetime import date

SITE = "/Users/openclaw/Documents/hermes/aitoolpick-site"
TODAY = date.today().isoformat()
DOMAIN = "https://aitoolpick.co.uk"

TOOLS = {
    "jasper-ai": {"name": "Jasper AI", "cat": "Writing", "price": "From £19/mo", "score": 3.7, "aff": "https://jasper.ai"},
    "copyai": {"name": "Copy.ai", "cat": "Writing", "price": "From £36/mo", "score": 3.5, "aff": "https://copy.ai"},
    "koala-writer": {"name": "Koala Writer", "cat": "Writing", "price": "From £9/mo", "score": 3.8, "aff": "https://koala.sh"},
    "neuronwriter": {"name": "NeuronWriter", "cat": "SEO", "price": "From £19/mo", "score": 4.0, "aff": "https://neuronwriter.com"},
    "surfer-seo": {"name": "Surfer SEO", "cat": "SEO", "price": "From £79/mo", "score": 3.9, "aff": "https://surferseo.com"},
    "fathom-ai": {"name": "Fathom AI", "cat": "Meetings", "price": "Free", "score": 4.2, "aff": "https://fathom.video"},
    "airies": {"name": "Airies AI", "cat": "Writing", "price": "Free tier available", "score": 3.4, "aff": "https://airies.ai"},
    "freeagent": {"name": "FreeAgent", "cat": "Accounting", "price": "From £14.50/mo", "score": 4.1, "aff": "https://freeagent.com"},
    "mindbody": {"name": "Mindbody", "cat": "Scheduling", "price": "From £99/mo", "score": 3.3, "aff": "https://mindbodyonline.com"},
}

INDUSTRIES = {
    "hairdressers": {"name": "Hairdressers & Salons", "pain": ["booking management", "social media content", "client reminders", "review collection"], "tools": ["mindbody", "jasper-ai", "fathom-ai"]},
    "plumbers": {"name": "Plumbers & Tradespeople", "pain": ["quote generation", "job scheduling", "invoice chasing", "customer follow-up"], "tools": ["jasper-ai", "copyai", "freeagent"]},
    "estate-agents": {"name": "Estate Agents", "pain": ["property descriptions", "market reports", "client matching", "viewing scheduling"], "tools": ["jasper-ai", "neuronwriter", "surfer-seo"]},
    "restaurants": {"name": "Restaurants & Cafes", "pain": ["menu descriptions", "social media posts", "review management", "staff scheduling"], "tools": ["jasper-ai", "copyai", "mindbody"]},
    "accountants": {"name": "Accountants", "pain": ["client communications", "report writing", "data extraction", "compliance updates"], "tools": ["freeagent", "jasper-ai", "fathom-ai"]},
    "solicitors": {"name": "Solicitors & Law Firms", "pain": ["document drafting", "client intake", "case research", "billing"], "tools": ["jasper-ai", "copyai", "freeagent"]},
    "fitness-instructors": {"name": "Fitness Instructors & Gyms", "pain": ["class scheduling", "member communications", "social content", "payment collection"], "tools": ["mindbody", "jasper-ai", "copyai"]},
    "dentists": {"name": "Dentists & Dental Practices", "pain": ["appointment reminders", "patient communications", "treatment descriptions", "review requests"], "tools": ["mindbody", "jasper-ai", "fathom-ai"]},
}

UK_CITIES = [
    ("london", "London", "9M"), ("manchester", "Manchester", "2.8M"), ("birmingham", "Birmingham", "2.6M"),
    ("leeds", "Leeds", "1.9M"), ("glasgow", "Glasgow", "1.7M"), ("sheffield", "Sheffield", "1.6M"),
    ("bristol", "Bristol", "1.1M"), ("edinburgh", "Edinburgh", "950K"), ("liverpool", "Liverpool", "900K"),
    ("newcastle", "Newcastle", "850K"), ("nottingham", "Nottingham", "790K"), ("cardiff", "Cardiff", "720K"),
    ("southampton", "Southampton", "580K"), ("swansea", "Swansea", "480K"), ("oxford", "Oxford", "400K"),
    ("cambridge", "Cambridge", "350K"), ("brighton", "Brighton", "340K"), ("york", "York", "320K"),
    ("bath", "Bath", "300K"), ("reading", "Reading", "290K"),
]

NAV = """<nav>
  <div class="nav-inner">
    <a href="https://aitoolpick.co.uk" class="logo">AI Tool Pick<span>.</span></a>
    <a href="https://aitoolpick.co.uk/blog.html" class="nav-back">← Back to Reviews</a>
  </div>
</nav>
<div class="disclosure">This site contains affiliate links. We may earn a commission at no extra cost to you if you buy through our links. <a href="https://aitoolpick.co.uk/affiliate-disclosure.html">Learn more</a></div>"""

FOOTER = """<footer>
  <p><a href="https://aitoolpick.co.uk">AI Tool Pick</a> | <a href="https://aitoolpick.co.uk/blog.html">All Reviews</a> | <a href="https://aitoolpick.co.uk/affiliate-disclosure.html">Affiliate Disclosure</a></p>
  <p style="margin-top:8px">&copy; 2026 AI Tool Pick. All rights reserved.</p>
</footer>"""

CSS = open(os.path.join(SITE, "jasper-ai-review-uk-2026.html")).read().split("<style>")[1].split("</style>")[0]

NEWSLETTER_HTML = """
<section class="newsletter-section" id="newsletter">
  <div class="newsletter-inner">
    <div class="newsletter-label">Stay informed</div>
    <div class="newsletter-title">Weekly AI tool picks for UK businesses</div>
    <div class="newsletter-desc">One email a week. The best new AI tools, honest reviews, and money-saving tips - curated for UK small businesses.</div>
    <form class="newsletter-form" id="newsletter-form" method="POST" action="https://3cc19776.sibforms.com/serve/MUIFAOofIPWDC7p6ZNYA_lBDbGD7TXnmtRi6_C60iaM1Rq8RUYlQVOcm4IaKwQvoMYP4HPqTBS3XtCcKmUsVbjSjgtXbfWDuMKJydKD8v8U124pilWNiidY07SFTq4kT6HHD4-f2YmSBHnNWoLN2HmSTOPQiSDrfWBajIwUNN9KqvoQIGq5N6YFV3C1q1NwWIGb1DSRzsjTqNwOYvg==" target="hidden_iframe" onsubmit="newsletterSubmit(event)">
      <input type="email" name="EMAIL" class="newsletter-input" placeholder="your@email.co.uk" required>
      <button type="submit" class="newsletter-btn">Subscribe</button>
      <input type="text" name="email_address_check" value="" style="display:none;">
      <input type="hidden" name="locale" value="en">
    </form>
    <div class="newsletter-note" id="newsletter-note">No spam. Unsubscribe any time.</div>
    <iframe name="hidden_iframe" id="hidden_iframe" style="display:none;"></iframe>
  </div>
</section>
"""

NEWSLETTER_STYLES = """
.newsletter-section{background:var(--ink);color:var(--paper);padding:clamp(48px,8vw,96px) clamp(16px,4vw,48px);text-align:center}
.newsletter-inner{max-width:600px;margin:0 auto}
.newsletter-label{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:16px}
.newsletter-title{font-family:'Playfair Display',serif;font-size:clamp(24px,4vw,36px);font-weight:700;margin-bottom:16px}
.newsletter-desc{font-size:16px;color:rgba(250,250,247,.7);margin-bottom:32px;font-weight:300;line-height:1.6}
.newsletter-form{display:flex;gap:12px;max-width:460px;margin:0 auto 16px}
.newsletter-input{flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:12px 16px;color:var(--paper);font-family:inherit;font-size:14px;transition:all .2s}
.newsletter-input:focus{outline:none;border-color:var(--accent);background:rgba(255,255,255,.08)}
.newsletter-btn{background:var(--accent);color:var(--paper);border:none;border-radius:8px;padding:0 24px;font-weight:600;font-size:14px;cursor:pointer;transition:all .2s;white-space:nowrap}
.newsletter-btn:hover{background:#b83f08;transform:translateY(-1px)}
.newsletter-note{font-size:12px;color:rgba(250,250,247,.4)}
@media (max-width:480px){.newsletter-form{flex-direction:column}.newsletter-btn{padding:12px}}
"""

NEWSLETTER_JS = """
function newsletterSubmit(e){
  document.getElementById('newsletter-form').style.opacity='0.5';
  document.getElementById('newsletter-form').style.pointerEvents='none';
  setTimeout(function(){
    document.getElementById('newsletter-form').style.display='none';
    var note=document.getElementById('newsletter-note');
    note.textContent='Thanks! Check your inbox to confirm.';
    note.style.color='var(--accent)';
    note.style.fontSize='16px';
    note.style.fontWeight='600';
  }, 500);
}
"""

def faq_schema(questions):
    items = []
    for q, a in questions:
        items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}, indent=2)

def breadcrumb_schema(items):
    crumbs = [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(items)]
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}, indent=2)

def wrap_page(title, desc, canonical, schemas, body, eyebrow="Guide"):
    schema_blocks = "\n".join(f'<script type="application/ld+json">\n{s}\n</script>' for s in schemas)
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta name="google-adsense-account" content="ca-pub-8571190031949919">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8571190031949919" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | AI Tool Pick</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/favicon-v4.png">
<link rel="apple-touch-icon" href="/favicon-v4.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="AI Tool Pick">
<meta property="article:published_time" content="{TODAY}">
<meta property="article:modified_time" content="{TODAY}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
{schema_blocks}
<style>{CSS}
{NEWSLETTER_STYLES}
</style>
</head>
<body>
{NAV}
<main class="article-layout">
  <article class="article-main">
    <div class="article-eyebrow">{eyebrow}</div>
    {body}
  </article>
</main>
{NEWSLETTER_HTML}
{FOOTER}
<script>{NEWSLETTER_JS}</script>
</body>
</html>'''

def tool_link(slug):
    t = TOOLS[slug]
    return f'''<div class="affiliate-box">
      <h4>Try {t["name"]} Today</h4>
      <p>Start with {t["name"]} for your UK business.</p>
      <a href="{t["aff"]}" class="cta-button" target="_blank" rel="noopener nofollow">Get {t["name"]}</a>
    </div>'''

def gen_comparison(slug1, slug2):
    t1, t2 = TOOLS[slug1], TOOLS[slug2]
    fname = f"{slug1}-vs-{slug2}-uk-2026.html"
    title = f"{t1['name']} vs {t2['name']} 2026: Which Is Better for UK Small Businesses?"
    desc = f"Compare {t1['name']} and {t2['name']} for UK businesses. Pricing in GBP, features, pros and cons, and our verdict."
    canonical = f"{DOMAIN}/{fname}"
    schemas = [
        json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"author":{"@type":"Organization","name":"AI Tool Pick"},"publisher":{"@type":"Organization","name":"AI Tool Pick","url":DOMAIN},"datePublished":TODAY,"dateModified":TODAY,"url":canonical}),
        breadcrumb_schema([("Home", DOMAIN), ("Blog", f"{DOMAIN}/blog.html"), (f"{t1['name']} vs {t2['name']}", canonical)]),
        faq_schema([
            (f"Which is better, {t1['name']} or {t2['name']}?", f"{t1['name']} scores {t1['score']}/5 and {t2['name']} scores {t2['score']}/5 in our tests. {t1['name']} costs {t1['price']} while {t2['name']} costs {t2['price']}. For most UK small businesses, the higher-rated option offers better overall value."),
            (f"Can I use both {t1['name']} and {t2['name']} together?", f"Yes, many UK businesses use {t1['name']} and {t2['name']} together as they serve complementary purposes."),
            (f"Is there a free trial for {t1['name']} or {t2['name']}?", f"Both tools offer free trials or free tiers. Check their websites for current availability."),
        ])
    ]
    body = f'''<h1>{t1["name"]} vs {t2["name"]} 2026: Head-to-Head Comparison</h1>
    <div class="article-meta">
      <span class="meta-tag">{t1["cat"]}</span>
      <span>{TODAY}</span>
      <span>AI Tool Pick Team</span>
    </div>
    <p class="article-intro">Choosing between {t1["name"]} and {t2["name"]}? We tested both for UK small businesses. Here is how they compare on price, features, and value for money in 2026.</p>
    <div class="key-box"><h3>Quick Comparison</h3><ul>
      <li><strong>{t1["name"]}:</strong> {t1["price"]} — {t1["cat"]} — Score: {t1["score"]}/5</li>
      <li><strong>{t2["name"]}:</strong> {t2["price"]} — {t2["cat"]} — Score: {t2["score"]}/5</li>
    </ul></div>
    <h2>Pricing Comparison</h2>
    <table class="price-table"><thead><tr><th></th><th>{t1["name"]}</th><th>{t2["name"]}</th></tr></thead>
    <tbody>
      <tr><td>Starting Price</td><td class="price-gbp">{t1["price"]}</td><td class="price-gbp">{t2["price"]}</td></tr>
      <tr><td>Category</td><td>{t1["cat"]}</td><td>{t2["cat"]}</td></tr>
      <tr><td>Our Score</td><td>{t1["score"]}/5</td><td>{t2["score"]}/5</td></tr>
    </tbody></table>
    {tool_link(slug1)}
    {tool_link(slug2)}'''
    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, t1["cat"]))
    return fname

def gen_worth_it(slug):
    t = TOOLS[slug]
    fname = f"is-{slug}-worth-it-uk-2026.html"
    title = f"Is {t['name']} Worth It in 2026? UK Small Business Guide"
    desc = f"Is {t['name']} worth the cost for UK businesses? We break down {t['price']} pricing, time saved, and who should buy it."
    canonical = f"{DOMAIN}/{fname}"
    schemas = [
        json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"author":{"@type":"Organization","name":"AI Tool Pick"},"publisher":{"@type":"Organization","name":"AI Tool Pick","url":DOMAIN},"datePublished":TODAY,"dateModified":TODAY,"url":canonical}),
        breadcrumb_schema([("Home", DOMAIN), ("Blog", f"{DOMAIN}/blog.html"), (f"Is {t['name']} Worth It?", canonical)]),
        faq_schema([
            (f"How much does {t['name']} cost?", f"{t['name']} costs {t['price']} for UK businesses."),
            (f"Is {t['name']} good for small teams?", f"Yes, {t['name']} is designed to help small teams automate manual tasks efficiently."),
        ])
    ]
    body = f'''<h1>Is {t["name"]} Worth the Cost in 2026?</h1>
    <div class="article-meta">
      <span class="meta-tag">{t["cat"]}</span>
      <span>{TODAY}</span>
      <span>AI Tool Pick Team</span>
    </div>
    <p class="article-intro">{t["name"]} is one of the most talked-about tools in the {t["cat"].lower()} space. But for UK small businesses with tight budgets, is it actually worth the {t["price"]} starting price? We break it down.</p>
    {tool_link(slug)}'''
    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, t["cat"]))
    return fname

def gen_industry(slug):
    ind = INDUSTRIES[slug]
    fname = f"best-ai-tools-for-{slug}-uk-2026.html"
    title = f"Best AI Tools for {ind['name']} in the UK (2026)"
    desc = f"Discover the best AI software for {ind['name']} in the UK. Automate {ind['pain'][0]} and {ind['pain'][1]} to save hours every week."
    canonical = f"{DOMAIN}/{fname}"
    schemas = [
        json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"author":{"@type":"Organization","name":"AI Tool Pick"},"publisher":{"@type":"Organization","name":"AI Tool Pick","url":DOMAIN},"datePublished":TODAY,"dateModified":TODAY,"url":canonical}),
        breadcrumb_schema([("Home", DOMAIN), ("Blog", f"{DOMAIN}/blog.html"), (f"AI for {ind['name']}", canonical)]),
    ]
    tool_list_html = "\n".join(f"<li><strong>{TOOLS[ts]['name']}:</strong> Best for {TOOLS[ts]['cat']}</li>" for ts in ind["tools"])
    body = f'''<h1>Top AI Tools for {ind["name"]}</h1>
    <div class="article-meta">
      <span class="meta-tag">Industry Guide</span>
      <span>{TODAY}</span>
    </div>
    <p class="article-intro">If you're running a {ind["name"].lower()} business in the UK, you're likely spending too much time on {ind["pain"][0]} and {ind["pain"][1]}. AI can automate these tasks in minutes.</p>
    <ul>{tool_list_html}</ul>'''
    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, "Industry"))
    return fname

def gen_city(slug, name, pop):
    fname = f"ai-tools-for-small-businesses-{slug}-uk-2026.html"
    title = f"AI Tools for Small Businesses in {name} (2026 Guide)"
    desc = f"Boost your {name}-based small business with the best AI tools. Local guide for {name}'s {pop} entrepreneurs."
    canonical = f"{DOMAIN}/{fname}"
    schemas = [
        json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"author":{"@type":"Organization","name":"AI Tool Pick"},"publisher":{"@type":"Organization","name":"AI Tool Pick","url":DOMAIN},"datePublished":TODAY,"dateModified":TODAY,"url":canonical}),
        breadcrumb_schema([("Home", DOMAIN), ("Blog", f"{DOMAIN}/blog.html"), (f"AI in {name}", canonical)]),
    ]
    body = f'''<h1>How {name} Small Businesses are Using AI in 2026</h1>
    <div class="article-meta">
      <span class="meta-tag">Local Guide</span>
      <span>{TODAY}</span>
    </div>
    <p class="article-intro">{name} is home to a thriving community of {pop} entrepreneurs. In 2026, the most successful local firms are using AI to stay competitive and save time.</p>'''
    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, "City Guide"))
    return fname

def main():
    print("Generating pages...")
    for s1 in TOOLS:
        for s2 in TOOLS:
            if s1 != s2: gen_comparison(s1, s2)
        gen_worth_it(s1)
    for ind in INDUSTRIES: gen_industry(ind)
    for slug, name, pop in UK_CITIES: gen_city(slug, name, pop)
    
    # Generate Sitemap
    html_files = [f for f in os.listdir(SITE) if f.endswith(".html")]
    excluded = ["privacy-policy.html", "affiliate-disclosure.html", "index-old.html", "2026-03-16-article.html", "article.html", "test-article.html"]
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write(f'  <url><loc>{DOMAIN}/</loc><lastmod>{TODAY}</lastmod></url>\n')
        f.write(f'  <url><loc>{DOMAIN}/blog.html</loc><lastmod>{TODAY}</lastmod></url>\n')
        for h in sorted(html_files):
            if h not in excluded and not h.startswith("index"):
                f.write(f'  <url><loc>{DOMAIN}/{h}</loc><lastmod>{TODAY}</lastmod></url>\n')
        f.write('</urlset>')
    print(f"Sitemap regenerated: {len(html_files)} URLs")

if __name__ == "__main__":
    main()
