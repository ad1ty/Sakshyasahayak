import urllib.request, re, json, os

BASE = 'https://raw.githubusercontent.com/ad1ty/Sakshyasahayak/main/'
FILES = ['index.html','about.html','trademark.html','copyright.html','patent.html','corporate.html','contact.html','sitemap.xml','vercel.json']
raw = {}
for f in FILES:
    with urllib.request.urlopen(BASE + f) as r:
        raw[f] = r.read().decode('utf-8')

LABELS = ['Home','About','Trademark','Copyright','Patent','Corporate','FAQ','Contact']
HREFS  = ['index.html','about.html','trademark.html','copyright.html','patent.html','corporate.html','faq.html','contact.html']

def nav_items(active):
    out = []
    for href, label in zip(HREFS, LABELS):
        ac = ' aria-current="page"' if href == active else ''
        out.append(f'    <li><a href="{href}"{ac}>{label}</a></li>')
    return '\n'.join(out)

def patch_nav(html, active):
    desktop = f'<ul class="nav-links" role="list">\n{nav_items(active)}\n  </ul>'
    mobile  = f'<ul class="nav-mobile-menu" id="mobile-nav" role="list" aria-label="Mobile navigation">\n{nav_items(active)}\n  </ul>'
    footer  = f'<ul class="footer-nav-list" role="list">\n{nav_items(active)}\n  </ul>'
    html = re.sub(r'<ul class="nav-links"[^>]*>.*?</ul>', desktop, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<ul class="nav-mobile-menu"[^>]*>.*?</ul>', mobile, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<ul class="footer-nav-list"[^>]*>.*?</ul>', footer, html, count=1, flags=re.DOTALL)
    return html

def patch_logo(html, label):
    return re.sub(r'(<a class="nav-logo"[^>]*aria-label=")[^"]*(")', rf'\g<1>{label}\g<2>', html)

def patch_meta(html, title, desc, canonical):
    html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, flags=re.DOTALL)
    if re.search(r'<meta name="description"', html):
        html = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{desc}">', html)
    else:
        html = html.replace('</title>', f'</title>\n  <meta name="description" content="{desc}">', 1)
    if re.search(r'<link rel="canonical"', html):
        html = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}">', html)
    else:
        html = html.replace('</title>', f'</title>\n  <link rel="canonical" href="{canonical}">', 1)
    return html

def schema(name, url, desc):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "LegalService",
      "name": "Sakshya Sahayak",
      "alternateName": "साक्ष्य सहायक",
      "url": "https://sakshyasahayak.in/",
      "telephone": "+91-9958088691",
      "email": "contact@sakshyasahayak.in",
      "areaServed": "India",
      "priceRange": "₹4,500 - ₹9,000 per trademark class",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Extension 2C, Street No.8, Nangloi",
        "addressLocality": "Delhi",
        "postalCode": "110041",
        "addressCountry": "IN"
      }},
      "employee": {{
        "@type": "Person",
        "name": "Aditya Chauhan",
        "jobTitle": "Advocate",
        "memberOf": {{"@type": "Organization", "name": "Bar Council of Delhi"}}
      }}
    }},
    {{
      "@type": "WebPage",
      "name": "{name}",
      "url": "{url}",
      "description": "{desc}",
      "isPartOf": {{"@type": "WebSite", "name": "Sakshya Sahayak", "url": "https://sakshyasahayak.in/"}}
    }}
  ]
}}
</script>'''

def patch_schema(html, name, url, desc):
    new = schema(name, url, desc)
    if re.search(r'<script type="application/ld\+json">', html):
        return re.sub(r'<script type="application/ld\+json">.*?</script>', new, html, count=1, flags=re.DOTALL)
    return html.replace('</head>', new + '\n</head>', 1)

META = {
  'trademark.html': ('Trademark Registration Lawyer Delhi | Trademark Objection Reply | Sakshya Sahayak',
    'Trademark registration in Delhi from ₹4,500/class. Trademark search, Form TM-A filing, examination reply, opposition & renewal. Aditya Chauhan, Advocate, Bar Council of Delhi.',
    'https://sakshyasahayak.in/trademark.html',
    'Trademark Registration & IP Services — Sakshya Sahayak','https://sakshyasahayak.in/trademark.html',
    'Information on trademark registration, search and clearance, examination reply, opposition proceedings and renewal under the Trade Marks Act 1999.',
    'Sakshya Sahayak — Delhi Trademark Lawyer — Home'),
  'copyright.html': ('Copyright Registration India | Copyright Licensing Agreements Delhi | Sakshya Sahayak',
    'Copyright registration with the Copyright Office, New Delhi under the Copyright Act 1957. Licensing agreements for creators, publishers & software developers. Aditya Chauhan, Advocate.',
    'https://sakshyasahayak.in/copyright.html',
    'Copyright Registration & Licensing — Sakshya Sahayak','https://sakshyasahayak.in/copyright.html',
    'Information on copyright registration under the Copyright Act 1957 and copyright licensing agreements for content creators and businesses.',
    'Sakshya Sahayak — Delhi Copyright Lawyer — Home'),
  'patent.html': ('Patent Filing India | Provisional Patent Application Delhi | Sakshya Sahayak',
    'Provisional patent application filing under the Patents Act 1970. Secures 12-month priority window before complete specification. Design registration also available. Aditya Chauhan, Advocate.',
    'https://sakshyasahayak.in/patent.html',
    'Patent Filing India — Sakshya Sahayak','https://sakshyasahayak.in/patent.html',
    'Information on provisional patent application filing under the Patents Act 1970 and design registration under the Designs Act 2000.',
    'Sakshya Sahayak — Delhi Patent Filing Lawyer — Home'),
  'corporate.html': ('Company Incorporation Delhi | DPIIT Startup Recognition | Contract Drafting | Sakshya Sahayak',
    'Company incorporation via SPICe+, Startup India DPIIT recognition, NDA & founders agreement drafting, MCA compliance. Corporate services for startups. Aditya Chauhan, Advocate, Delhi.',
    'https://sakshyasahayak.in/corporate.html',
    'Corporate & Startup Legal Services — Sakshya Sahayak','https://sakshyasahayak.in/corporate.html',
    'Information on company incorporation, DPIIT startup recognition, contract drafting, MCA compliance and legal opinions.',
    'Sakshya Sahayak — Delhi Corporate Law Firm — Home'),
  'about.html': ('About Sakshya Sahayak | Aditya Chauhan Advocate Delhi | IP Law Firm',
    'Sakshya Sahayak is a New Delhi IP law firm by Aditya Chauhan, Advocate (Bar Council of Delhi, D/11905/2022), specialising in trademarks, copyright, patent filing & corporate compliance.',
    'https://sakshyasahayak.in/about.html',
    'About Sakshya Sahayak — Delhi IP Law Firm','https://sakshyasahayak.in/about.html',
    'About Sakshya Sahayak, a New Delhi IP law firm by Aditya Chauhan, Advocate, specialising in trademarks, copyright, patent filing and corporate compliance.',
    'Sakshya Sahayak — Delhi Trademark and IP Law Firm — Home'),
  'contact.html': ('Contact Sakshya Sahayak | Delhi Trademark Lawyer | Professional Enquiries',
    'Contact details for Sakshya Sahayak, Delhi IP law firm. Aditya Chauhan, Advocate — email contact@sakshyasahayak.in or call +91 9958088691. Disclosed per BCI Rule 36.',
    'https://sakshyasahayak.in/contact.html',
    'Contact Sakshya Sahayak — Delhi IP Law Firm','https://sakshyasahayak.in/contact.html',
    'Contact details for Sakshya Sahayak, Delhi IP law firm. Professional enquiries only.',
    'Sakshya Sahayak — Delhi Trademark and IP Law Firm — Home'),
}

HERO_CTA = '''<!-- Hero CTA — disclosed pursuant to BCI Rule 36 -->
<div class="hero-cta reveal" style="margin-top: 2.5rem; display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; align-items: center;">
  <a href="contact.html" style="display:inline-block; padding: 0.75rem 2rem; background: #6B2D3E; color: #FAF6F0; font-family: inherit; font-size: 0.9rem; letter-spacing: 0.08em; text-transform: uppercase; text-decoration: none; border: 1.5px solid #6B2D3E; transition: background 0.2s, color 0.2s;" onmouseover="this.style.background=\'transparent\';this.style.color=\'#6B2D3E\';" onmouseout="this.style.background=\'#6B2D3E\';this.style.color=\'#FAF6F0\';">Professional Enquiries</a>
  <a href="faq.html" style="display:inline-block; padding: 0.75rem 2rem; background: transparent; color: #6B2D3E; font-family: inherit; font-size: 0.9rem; letter-spacing: 0.08em; text-transform: uppercase; text-decoration: none; border: 1.5px solid #C9A84C; transition: background 0.2s, color 0.2s;" onmouseover="this.style.background=\'#C9A84C\';this.style.color=\'#FAF6F0\';" onmouseout="this.style.background=\'transparent\';this.style.color=\'#6B2D3E\';">IP Law FAQ →</a>
</div>'''

PRACTICE_CTA = '''<!-- Practice areas footer CTA -->
<div class="reveal" style="text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(107,45,62,0.12);">
  <p style="font-family: \'Cormorant Garamond\', serif; font-size: 1rem; color: var(--color-text-muted); margin-bottom: 1.25rem; letter-spacing: 0.03em;">For procedural information on any of the above, refer to the contact details below.</p>
  <a href="contact.html" style="display:inline-block; padding: 0.75rem 2rem; background: #6B2D3E; color: #FAF6F0; font-family: inherit; font-size: 0.9rem; letter-spacing: 0.08em; text-transform: uppercase; text-decoration: none; border: 1.5px solid #6B2D3E; transition: background 0.2s, color 0.2s;" onmouseover="this.style.background=\'transparent\';this.style.color=\'#6B2D3E\';" onmouseout="this.style.background=\'#6B2D3E\';this.style.color=\'#FAF6F0\';">Professional Enquiries</a>
</div>'''

results = {}

for fname, html in raw.items():
    if fname == 'sitemap.xml':
        if 'faq.html' not in html:
            html = html.replace('</urlset>', '  <url>\n    <loc>https://sakshyasahayak.in/faq.html</loc>\n    <lastmod>2026-03-26</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
        html = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', '<lastmod>2026-03-26</lastmod>', html)
        results[fname] = html
        continue
    if fname == 'vercel.json':
        vj = json.loads(html)
        new_h = [{"source":"/assets/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=31536000, immutable"}]},{"source":"/(.*).css","headers":[{"key":"Cache-Control","value":"public, max-age=86400"}]}]
        ex = {h['source'] for h in vj.get('headers',[])}
        for h in new_h:
            if h['source'] not in ex:
                vj.setdefault('headers',[]).append(h)
        results[fname] = json.dumps(vj, indent=2, ensure_ascii=False)
        continue
    html = patch_nav(html, fname)
    if fname == 'index.html':
        html = patch_logo(html, 'Sakshya Sahayak — Delhi Trademark and IP Law Firm — Home')
        if 'hero-cta' not in html:
            html = re.sub(r'(</div>\s*)(<!--\s*\*|<section|<hr)', r'</div>\n\n' + HERO_CTA + r'\n\n\2', html, count=1, flags=re.DOTALL)
        if 'Practice areas footer CTA' not in html:
            html = re.sub(r'(</div>\s*</section>)', PRACTICE_CTA + r'\n\1', html, count=1, flags=re.DOTALL)
    if fname in META:
        t,d,c,sn,su,sd,la = META[fname]
        html = patch_meta(html, t, d, c)
        html = patch_schema(html, sn, su, sd)
        html = patch_logo(html, la)
    results[fname] = html

for fname, content in results.items():
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✓ written {fname}')

print('\nAll files patched successfully!')
