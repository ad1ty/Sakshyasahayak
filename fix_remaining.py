# Step 1: Update sitemap.xml with 4 blog URL blocks
# Step 2: Add Articles nav link to all 8 HTML files

TODAY = '2026-03-26'
BASE_URL = 'https://sakshyasahayak.in'

# Safe read/write
def rf(p):
    with open(p, 'r', encoding='utf-8') as f: return f.read()
def wf(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# === STEP 1: SITEMAP ===
SITEMAP_ADDITIONS = '''  <!-- Blog listing page -->
  <url>
    <loc>https://sakshyasahayak.in/blog.html</loc>
    <lastmod>2026-03-26</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <!-- Blog article: Trademark Registration -->
  <url>
    <loc>https://sakshyasahayak.in/blog-trademark-registration-india.html</loc>
    <lastmod>2026-03-26</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>

  <!-- Blog article: Copyright Registration -->
  <url>
    <loc>https://sakshyasahayak.in/blog-copyright-registration-india.html</loc>
    <lastmod>2026-03-26</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>

  <!-- Blog article: Provisional Patent -->
  <url>
    <loc>https://sakshyasahayak.in/blog-provisional-patent-india.html</loc>
    <lastmod>2026-03-26</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>

'''

sitemap = rf('sitemap.xml')
if 'blog.html' in sitemap:
    print('Sitemap already has blog entries, skipping')
else:
    sitemap_new = sitemap.replace('</urlset>', SITEMAP_ADDITIONS + '</urlset>')
    wf('sitemap.xml', sitemap_new)
    print('Sitemap updated with 4 blog URL blocks')

# === STEP 2: ADD ARTICLES NAV TO ALL HTML FILES ===
FIND = '<li><a href="faq.html">FAQ</a></li>'
REPLACE = '<li><a href="faq.html">FAQ</a></li>\n    <li><a href="blog.html">Articles</a></li>'

# Pages to update (not blog pages themselves)
pages = [
    'index.html', 'trademark.html', 'copyright.html', 'patent.html',
    'corporate.html', 'about.html', 'contact.html', 'faq.html'
]

for page in pages:
    try:
        content = rf(page)
        if '<a href="blog.html">Articles</a>' in content:
            print(f'{page}: Articles nav already present, skipping')
            continue
        count = content.count(FIND)
        if count == 0:
            print(f'WARNING: {page}: FAQ nav item not found!')
            continue
        new_content = content.replace(FIND, REPLACE)
        wf(page, new_content)
        print(f'{page}: Added Articles nav ({count} occurrence(s) replaced)')
    except FileNotFoundError:
        print(f'WARNING: {page} not found!')

print('\n=== ALL DONE ===')
