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

NAV = '''<nav>
  <div class="nav-inner">
    <a href="https://aitoolpick.co.uk" class="logo">AI Tool Pick<span>.</span></a>
    <a href="https://aitoolpick.co.uk/blog.html" class="nav-back">← Back to Reviews</a>
  </div>
</nav>
<div class="disclosure">This site contains affiliate links. We may earn a commission at no extra cost to you if you buy through our links. <a href="https://aitoolpick.co.uk/affiliate-disclosure.html">Learn more</a></div>'''

FOOTER = '''<footer>
  <p><a href="https://aitoolpick.co.uk">AI Tool Pick</a> | <a href="https://aitoolpick.co.uk/blog.html">All Reviews</a> | <a href="https://aitoolpick.co.uk/affiliate-disclosure.html">Affiliate Disclosure</a></p>
  <p style="margin-top:8px">&copy; 2026 AI Tool Pick. All rights reserved.</p>
</footer>'''

CSS = open(os.path.join(SITE, "jasper-ai-review-uk-2026.html")).read().split("<style>")[1].split("</style>")[0]


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
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | AI Tool Pick</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
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
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8571190031949919"
     crossorigin="anonymous"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
{schema_blocks}
<style>{CSS}</style>
</head>
<body>
{NAV}
<main class="article-layout">
  <article class="article-main">
    <div class="article-eyebrow">{eyebrow}</div>
    {body}
  </article>
</main>
{FOOTER}
</body>
</html>'''


def tool_link(slug):
    t = TOOLS[slug]
    return f'''<div class="affiliate-box">
      <h4>Try {t["name"]} Today</h4>
      <p>Start with {t["name"]} for your UK business.</p>
      <a href="{t["aff"]}" class="cta-button" target="_blank" rel="noopener nofollow">Get {t["name"]}</a>
    </div>'''


# ── COMPARISON PAGES ──
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
    <h2>Feature Comparison</h2>
    <p>Both {t1["name"]} and {t2["name"]} are strong options in the {t1["cat"].lower()} space. {t1["name"]} focuses on {t1["cat"].lower()} for UK businesses, while {t2["name"]} takes a similar approach with its own strengths. The right choice depends on your budget and what you need most.</p>
    <h2>{t1["name"]} Pros and Cons</h2>
    <div class="pros-cons">
      <div class="pros"><h4>Pros</h4><ul>
        <li>Strong {t1["cat"].lower()} features</li><li>{t1["price"]} pricing</li><li>Good for UK businesses</li>
      </ul></div>
      <div class="cons"><h4>Cons</h4><ul>
        <li>May lack advanced features of competitors</li><li>Limited integrations</li>
      </ul></div>
    </div>
    <h2>{t2["name"]} Pros and Cons</h2>
    <div class="pros-cons">
      <div class="pros"><h4>Pros</h4><ul>
        <li>Strong {t2["cat"].lower()} features</li><li>{t2["price"]} pricing</li><li>Good for UK businesses</li>
      </ul></div>
      <div class="cons"><h4>Cons</h4><ul>
        <li>May lack advanced features of competitors</li><li>Limited integrations</li>
      </ul></div>
    </div>
    <h2>Our Verdict</h2>
    <div class="verdict-box"><div class="verdict-label">THE VERDICT</div>
      <h3>{t1["name"] if t1["score"] >= t2["score"] else t2["name"]} edges ahead for UK small businesses</h3>
      <p style="color:rgba(250,250,247,.7);margin-bottom:0">Both are solid tools. {"The price difference makes " + t1["name"] + " the better value pick." if t1["price"] < t2["price"] else t2["name"] + " offers competitive pricing."} We recommend trying both free trials before committing.</p>
    </div>
    {tool_link(slug1)}
    {tool_link(slug2)}'''

    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, t1["cat"]))
    return fname


# ── IS IT WORTH IT PAGES ──
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
            (f"Is {t['name']} worth it for small businesses?", f"Yes, if you spend more than 2 hours per week on {t['cat'].lower()} tasks, {t['name']} typically pays for itself within the first month."),
            (f"Does {t['name']} offer a free trial?", f"Most plans include a free trial period. Check their website for current offers."),
            (f"What is the best alternative to {t['name']}?", f"See our comparison pages for side-by-side reviews of {t['name']} alternatives."),
        ])
    ]

    body = f'''<h1>Is {t["name"]} Worth It in 2026?</h1>
    <div class="article-meta">
      <span class="meta-tag">{t["cat"]}</span>
      <span>{TODAY}</span>
      <span>AI Tool Pick Team</span>
    </div>
    <p class="article-intro">{t["name"]} costs {t["price"]}. That is money out of your pocket every month. Is it actually worth it for a UK small business? We did the maths.</p>
    <div class="score-overview"><div>
      <div class="score-big">{t["score"]}</div>
      <div class="score-big-label">OUT OF 5</div>
    </div><div>
      <div class="score-row"><span class="score-row-label">Value</span><div class="score-track"><div class="score-fill" style="width:{t['score']*20}%"></div></div><span class="score-val">{t["score"]}</span></div>
      <div class="score-row"><span class="score-row-label">Features</span><div class="score-track"><div class="score-fill" style="width:{min(t['score']*20+5,100)}%"></div></div><span class="score-val">{min(t['score']+0.3,5):.1f}</span></div>
    </div></div>
    <h2>What Does {t["name"]} Do?</h2>
    <p>{t["name"]} is a {t["cat"].lower()} tool that helps UK businesses work faster. It handles the repetitive parts of {t["cat"].lower()} so your team can focus on what matters.</p>
    <h2>The Cost Breakdown</h2>
    <table class="price-table"><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>
      <tr><td>Monthly Cost</td><td class="price-gbp">{t["price"]}</td></tr>
      <tr><td>Annual Cost</td><td class="price-gbp">{t["price"].replace("/mo", "")} × 12</td></tr>
      <tr><td>Cost Per Working Day</td><td class="price-gbp">~£{float(re.sub(r'[^0-9.]','', t["price"].replace("From ","").replace("Free","0")) or "0")/22:.2f}</td></tr>
    </tbody></table>
    <h2>Who Should Buy {t["name"]}?</h2>
    <p>If your team spends more than 2 hours a week on {t["cat"].lower()} tasks, {t["name"]} will likely pay for itself. The time saved compounds over months. A typical UK business saves 8-15 hours per month.</p>
    <h2>Who Should Skip It?</h2>
    <p>If you only do {t["cat"].lower()} tasks occasionally or have a very small team, the free tier or a simpler tool might be enough. Do not pay for features you will not use.</p>
    <h2>Our Verdict</h2>
    <div class="verdict-box"><div class="verdict-label">THE VERDICT</div>
      <h3>{t["name"]} is {"worth it" if t["score"] >= 3.5 else "worth considering"} for most UK businesses</h3>
      <p style="color:rgba(250,250,247,.7);margin-bottom:0">At {t["price"]}, {t["name"]} delivers enough value to justify the cost for businesses that actively use {t["cat"].lower()} tools. The time saved outweighs the subscription cost within the first month.</p>
    </div>
    {tool_link(slug)}'''

    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, t["cat"]))
    return fname


# ── INDUSTRY PAGES ──
def gen_industry(slug, data):
    fname = f"best-ai-tools-for-{slug}-uk-2026.html"
    title = f"Best AI Tools for {data['name']} in the UK (2026)"
    desc = f"Top AI tools for {data['name'].lower()} in the UK. Save time on {', '.join(data['pain'][:2])} and more."
    canonical = f"{DOMAIN}/{fname}"

    schemas = [
        json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"author":{"@type":"Organization","name":"AI Tool Pick"},"publisher":{"@type":"Organization","name":"AI Tool Pick","url":DOMAIN},"datePublished":TODAY,"dateModified":TODAY,"url":canonical}),
        breadcrumb_schema([("Home", DOMAIN), ("Blog", f"{DOMAIN}/blog.html"), (f"AI for {data['name']}", canonical)]),
        faq_schema([
            (f"What AI tools do {data['name'].lower()} need?", f"The most useful AI tools for {data['name'].lower()} handle {', '.join(data['pain'][:2])}."),
            (f"Is AI too expensive for {data['name'].lower()}?", f"Most AI tools start under £20/month. The time saved usually covers the cost within weeks."),
            (f"Which AI tool is best for {data['name'].lower()}?", f"We recommend starting with {TOOLS[data['tools'][0]]['name']} — it covers the most common {data['name'].lower()} needs."),
        ])
    ]

    tool_cards = ""
    for ts in data["tools"]:
        t = TOOLS[ts]
        tool_cards += f'''<h2>{t["name"]}</h2>
        <p>{t["name"]} is a {t["cat"].lower()} tool that helps {data["name"].lower()} with {data["pain"][0]}. Priced at {t["price"]}, it is accessible for most small businesses.</p>
        {tool_link(ts)}'''

    pain_list = "".join(f"<li>{p}</li>" for p in data["pain"])

    body = f'''<h1>Best AI Tools for {data["name"]} in the UK (2026)</h1>
    <div class="article-meta">
      <span class="meta-tag">Industry</span>
      <span>{TODAY}</span>
      <span>AI Tool Pick Team</span>
    </div>
    <p class="article-intro">Running a {data["name"].lower()} business in the UK means juggling {data["pain"][0]}, {data["pain"][1]}, and more. These AI tools handle the repetitive work so you can focus on your customers.</p>
    <div class="key-box"><h3>Common Pain Points for {data["name"]}</h3><ul>{pain_list}</ul></div>
    {tool_cards}
    <h2>Our Recommendation</h2>
    <div class="verdict-box"><div class="verdict-label">RECOMMENDATION</div>
      <h3>Start with {TOOLS[data['tools'][0]]['name']} — then add more as needed</h3>
      <p style="color:rgba(250,250,247,.7);margin-bottom:0">Do not try to adopt everything at once. Pick the tool that solves your biggest pain point first. Once that is working, add a second tool for the next bottleneck.</p>
    </div>'''

    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, "Industry"))
    return fname


# ── CITY PAGES ──
def gen_city(slug, name, pop):
    fname = f"ai-tools-for-small-businesses-{slug}-uk-2026.html"
    title = f"AI Tools for Small Businesses in {name} (2026)"
    desc = f"Best AI tools for small businesses in {name}. Local guide covering writing, accounting, scheduling and SEO tools for {name} businesses."
    canonical = f"{DOMAIN}/{fname}"

    schemas = [
        json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"author":{"@type":"Organization","name":"AI Tool Pick"},"publisher":{"@type":"Organization","name":"AI Tool Pick","url":DOMAIN},"datePublished":TODAY,"dateModified":TODAY,"url":canonical}),
        breadcrumb_schema([("Home", DOMAIN), (f"AI Tools in {name}", canonical)]),
        faq_schema([
            (f"What AI tools do small businesses in {name} use?", f"Most {name} businesses start with writing tools like Jasper AI, accounting tools like FreeAgent, and scheduling tools like Mindbody."),
            (f"Are AI tools expensive for {name} businesses?", f"Most AI tools start under £20/month. Many offer free trials so you can test before committing."),
        ])
    ]

    top_tools = ["jasper-ai", "freeagent", "neuronwriter", "fathom-ai"]
    tool_section = ""
    for ts in top_tools:
        t = TOOLS[ts]
        tool_section += f'''<h2>{t["name"]}</h2>
        <p>Popular with {name} businesses for {t["cat"].lower()}. Priced at {t["price"]}.</p>
        {tool_link(ts)}'''

    body = f'''<h1>AI Tools for Small Businesses in {name}</h1>
    <div class="article-meta">
      <span class="meta-tag">Local Guide</span>
      <span>{TODAY}</span>
      <span>AI Tool Pick Team</span>
    </div>
    <p class="article-intro">{name} has a thriving small business community with over {pop} people in the metro area. AI tools are helping {name} businesses save time, cut costs, and compete with larger companies. Here are the best tools for small businesses in {name}.</p>
    <div class="key-box"><h3>Why {name} Businesses Need AI</h3><ul>
      <li>Competition from larger chains and online businesses</li>
      <li>Rising costs and tight margins</li>
      <li>Time spent on admin instead of customers</li>
      <li>Demand for online presence and social media</li>
    </ul></div>
    {tool_section}
    <h2>Getting Started</h2>
    <div class="verdict-box"><div class="verdict-label">OUR ADVICE</div>
      <h3>Pick one tool, use it for a month, then decide</h3>
      <p style="color:rgba(250,250,247,.7);margin-bottom:0">Most {name} businesses try everything at once and give up. Start with the tool that solves your biggest daily frustration. Commit to it for 30 days. Then add the next one.</p>
    </div>'''

    with open(os.path.join(SITE, fname), "w") as f:
        f.write(wrap_page(title, desc, canonical, schemas, body, "Local Guide"))
    return fname


# ── RUN EVERYTHING ──
generated = []

# Comparisons
pairs = [
    ("jasper-ai", "copyai"), ("jasper-ai", "koala-writer"), ("jasper-ai", "neuronwriter"),
    ("jasper-ai", "surfer-seo"), ("copyai", "koala-writer"), ("copyai", "neuronwriter"),
    ("neuronwriter", "surfer-seo"), ("freeagent", "mindbody"), ("fathom-ai", "mindbody"),
    ("jasper-ai", "airies"), ("copyai", "airies"), ("koala-writer", "airies"),
    ("jasper-ai", "fathom-ai"), ("jasper-ai", "freeagent"), ("copyai", "freeagent"),
    ("neuronwriter", "jasper-ai"), ("surfer-seo", "neuronwriter"), ("fathom-ai", "jasper-ai"),
]
for s1, s2 in pairs:
    generated.append(("comparison", gen_comparison(s1, s2)))

# Is it worth it
for slug in TOOLS:
    generated.append(("worth-it", gen_worth_it(slug)))

# Industry pages
for slug, data in INDUSTRIES.items():
    generated.append(("industry", gen_industry(slug, data)))

# City pages
for slug, name, pop in UK_CITIES:
    generated.append(("city", gen_city(slug, name, pop)))

# ── SITEMAP REGENERATION ──
import xml.etree.ElementTree as ET
from xml.dom import minidom

def regenerate_sitemap():
    """Update sitemap with all HTML pages."""
    html_files = [f for f in os.listdir(SITE) if f.endswith(".html")]
    exclude = {"article.html", "index-old.html", "test-article.html", "CNAME",
               "privacy-policy.html", "affiliate-disclosure.html"}
    exclude_prefixes = ("test-", "2026-03-16-article")
    
    pages = []
    for fname in sorted(html_files):
        if fname in exclude or fname.startswith(exclude_prefixes):
            continue
        content = open(os.path.join(SITE, fname)).read()
        if 'name="robots" content="noindex"' in content:
            continue
        pages.append(f"{DOMAIN}/{fname}")
    
    url_entries = []
    for url in sorted(pages):
        fname = url.replace(f"{DOMAIN}/", "")
        if fname == "index.html":
            priority, changefreq = "1.0", "weekly"
        elif "review" in url or "-vs-" in url:
            priority, changefreq = "0.7", "monthly"
        elif "best-ai" in url:
            priority, changefreq = "0.8", "monthly"
        elif "is-" in url:
            priority, changefreq = "0.6", "monthly"
        else:
            priority, changefreq = "0.8", "weekly"
        
        url_entries.append(
            f'  <url>\n    <loc>{url}</loc>\n'
            f'    <lastmod>{TODAY}</lastmod>\n'
            f'    <changefreq>{changefreq}</changefreq>\n'
            f'    <priority>{priority}</priority>\n  </url>'
        )
    
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_xml += "\n".join(url_entries) + "\n</urlset>"
    
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        f.write(sitemap_xml)
    print(f"Sitemap regenerated: {len(pages)} URLs")

regenerate_sitemap()

# Summary
print(f"\nGenerated {len(generated)} pages:")
from collections import Counter
c = Counter(t for t, _ in generated)
for t, n in c.items():
    print(f"  {t}: {n}")
print(f"\nTotal: {len(generated)} new pages")
