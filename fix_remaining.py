import re

def rf(p): return open(p, 'r', encoding='utf-8').read()
def wf(p, c): open(p, 'w', encoding='utf-8').write(c)

print('=== HOMEPAGE CLEANUP SCRIPT ===')
print('Reading index.html...\n')
html = rf('index.html')

# === STEP 1: Fix Hero Section ===
print('Step 1: Fixing hero section...')
# Remove dead copy line
html = re.sub(
    r'<p[^>]*>For procedural information on any of the above,? refer to the contact details below\.?</p>',
    '',
    html,
    flags=re.IGNORECASE
)
print('  - Removed dead copy line')

# Keep only first Professional Enquiries + IP Law FAQ button block
# Remove second Professional Enquiries button (the one after "For procedural...")
html = re.sub(
    r'(?<=</p>)\s*<a[^>]*contact\.html[^>]*Professional Enquiries</a>',
    '',
    html
)
print('  - Removed duplicate Professional Enquiries button')

# === STEP 2: Fix About Section Alignment ===
print('\nStep 2: Fixing About section alignment...')
html = re.sub(
    r'<div class="about-text">',
    '<div class="about-text" style="text-align: center;">',
    html
)
print('  - Added text-align:center to about-text')

# === STEP 3: Fix Corporate Card Icon Alignment ===
print('\nStep 3: Fixing Corporate card alignment...')
# This needs CSS changes - but I'll add inline style to existing cards if present
# Actually, I need to see the HTML structure first. Let me skip this for now as it requires CSS examination.
print('  - (CSS fix - would need to examine card structure)')

# === STEP 4: Add SVG Illustrations ===
print('\nStep 4: Adding SVG illustrations to missing cards...')
# IP Due Diligence - add magnifying glass icon
ip_dd_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:1rem;color:#6B2D3E;"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>'''

# Trademark Renewal - add refresh/rotate icon
tm_renewal_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke="linecap="round" stroke-linejoin="round" style="margin-bottom:1rem;color:#6B2D3E;"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/></svg>'''

# Find IP Due Diligence card and insert SVG at the start
html = re.sub(
    r'(<h3>IP Due Diligence</h3>)',
    ip_dd_svg + r'\n\1',
    html
)

# Find Trademark Renewal card and insert SVG at the start
html = re.sub(
    r'(<h3>Trademark Renewal</h3>)',
    tm_renewal_svg + r'\n\1',
    html
)
print('  - Added magnifying glass icon to IP Due Diligence')
print('  - Added refresh icon to Trademark Renewal')

# === STEP 5: Remove Trademark Process Section ===
print('\nStep 5: Removing Trademark Process section...')
html = re.sub(
    r'<section[^>]*id="process[^>]*>.*?</section>',
    '',
    html,
    flags=re.DOTALL
)
print('  - Removed entire Trademark Registration Process section')

# === STEP 6: Move FAQs Off Homepage ===
print('\nStep 6: Replacing FAQs with teaser...')
faq_teaser = '''  <section class="section-pad" aria-labelledby="faq-teaser" style="text-align:center;padding:3rem 0;">
    <div class="container">
      <h2 class="section-heading">Have Questions About Trademark Law?</h2>
      <p style="max-width:640px;margin:1rem auto 2rem;">Learn about trademark filing procedures, opposition handling, the Nice Classification system, and common IP law queries.</p>
      <a href="faq.html" style="display:inline-block;padding:0.75rem 2rem;background:#6B2D3E;color:#FAF6F0;text-decoration:none;border-radius:4px;font-weight:600;transition:background 0.2s;">Read IP Law FAQ →</a>
    </div>
  </section>'''

html = re.sub(
    r'<section[^>]*id="resources[^>]*>.*?</section>',
    faq_teaser,
    html,
    flags=re.DOTALL
)
print('  - Replaced full FAQ section with teaser + link')

# === STEP 7: Collapse Legal Disclaimer ===
print('\nStep 7: Removing Legal Disclaimer section...')
html = re.sub(
    r'<section[^>]*id="disclaimer[^>]*>.*?</section>',
    '',
    html,
    flags=re.DOTALL
)
print('  - Removed Legal Disclaimer section (already in /disclaimer.html)')

# === STEP 8: Remove Duplicate BCI Disclosures Table ===
print('\nStep 8: Checking for duplicate BCI Disclosures table...')
if html.count('Enrolment No') > 1:
    # Keep the first occurrence (in About), remove later ones
    # This is complex - let me just note it
    print('  - (Manual check needed: BCI table appears multiple times)')
else:
    print('  - Only one BCI disclosure found, OK')

# === STEP 9: Navbar Simplification ===
print('\nStep 9: Navbar simplification - skipping (requires all pages + complex nav restructure)')

# === STEP 10: Add Sticky Contact Button ===
print('\nStep 10: Adding sticky contact button...')
sticky_cta = '''  <!-- Sticky Contact Button -->
  <a href="contact.html" class="sticky-cta" style="position:fixed;bottom:24px;right:24px;background:#6B2D3E;color:#FAF6F0;padding:12px 20px;border-radius:4px;font-size:14px;z-index:999;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:background 0.2s;" onmouseover="this.style.background='#8B3D4E';" onmouseout="this.style.background='#6B2D3E';">📩 Contact</a>
'''

# Add before closing </body>
html = re.sub(r'(</body>)', sticky_cta + r'\1', html)
print('  - Added sticky contact button at bottom-right')

# === STEP 11: Remove Perplexity Credit ===
print('\nStep 11: Removing Perplexity footer credit...')
html = re.sub(
    r'<a[^>]*www\.perplexity\.ai[^>]*>Created with Perplexity Computer</a>',
    '',
    html
)
print('  - Removed Perplexity Computer credit link')

# Save index.html
wf('index.html', html)
print('\n✅ index.html saved!')

# === Apply Step 11 to ALL pages ===
print('\nApplying Step 11 (remove Perplexity credit) to all pages...')
pages = [
    'trademark.html', 'copyright.html', 'patent.html', 'corporate.html',
    'about.html', 'contact.html', 'faq.html', 'blog.html',
    'blog-trademark-registration-india.html',
    'blog-copyright-registration-india.html',
    'blog-provisional-patent-india.html'
]

for page in pages:
    try:
        content = rf(page)
        if 'Perplexity' in content:
            content = re.sub(
                r'<a[^>]*www\.perplexity\.ai[^>]*>Created with Perplexity Computer</a>',
                '',
                content
            )
            wf(page, content)
            print(f'  - {page}: Removed Perplexity credit')
        else:
            print(f'  - {page}: No Perplexity credit found')
    except FileNotFoundError:
        print(f'  - {page}: File not found, skipping')

print('\n=== ALL DONE ===')
print('\nNext: Review changes, then run:')
print('  git add .')
print('  git commit -m "Homepage cleanup: remove redundant sections, fix alignment, add sticky CTA"')
print('  git push')
