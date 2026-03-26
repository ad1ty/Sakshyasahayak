import re

def rf(p): return open(p, 'r', encoding='utf-8').read()
def wf(p, c): open(p, 'w', encoding='utf-8').write(c)

print('=== CRITICAL WEBSITE BUGFIXES ===')
print('Fixing 4 broken pages + logo + malformed tags\n')

# === CRITICAL FIX #1: Restore CSS Links on 4 Broken Pages ===
print('🔴 CRITICAL FIX #1: Restoring CSS link tags...')

# Correct CSS link block to add
CSS_LINKS = '''  <link rel="stylesheet" href="base.css">
  <link rel="stylesheet" href="style.css">'''

broken_pages = ['trademark.html', 'copyright.html', 'patent.html', 'corporate.html']

for page in broken_pages:
    try:
        html = rf(page)
        
        # Check if CSS links already exist
        if 'rel="stylesheet"' in html and 'base.css' in html:
            print(f'  - {page}: CSS links already present')
            continue
        
        # Find the position to insert CSS links (after meta tags, before </head>)
        # Look for the last <link> tag (likely favicons) or <meta> tag before </head>
        if '<link rel="icon"' in html:
            # Insert after the last favicon link
            html = re.sub(
                r'(<link rel="icon"[^>]*>)(?!\s*<link rel="icon")',
                r'\1\n' + CSS_LINKS,
                html
            )
        elif '</head>' in html:
            # Insert just before </head>
            html = html.replace('</head>', CSS_LINKS + '\n  </head>')
        
        wf(page, html)
        print(f'  ✅ {page}: Added CSS link tags')
    except FileNotFoundError:
        print(f'  ⚠️ {page}: File not found')

# === CRITICAL FIX #2: Fix Logo Paths to Absolute ===
print('\n🔴 CRITICAL FIX #2: Fixing logo image paths...')

all_pages = [
    'index.html', 'about.html', 'trademark.html', 'copyright.html',
    'patent.html', 'corporate.html', 'contact.html', 'faq.html',
    'blog.html', 'blog-trademark-registration-india.html',
    'blog-copyright-registration-india.html',
    'blog-provisional-patent-india.html'
]

for page in all_pages:
    try:
        html = rf(page)
        
        # Check current logo path
        if 'src="logo.png"' in html:
            html = html.replace('src="logo.png"', 'src="/logo.png"')
            wf(page, html)
            print(f'  ✅ {page}: Fixed logo path to absolute')
        elif 'src="/logo.png"' in html:
            print(f'  - {page}: Logo path already absolute')
        else:
            print(f'  - {page}: No logo.png reference found')
    except FileNotFoundError:
        print(f'  ⚠️ {page}: File not found')

# === CRITICAL FIX #3: Fix Malformed Anchor Tags ===
print('\n🔴 CRITICAL FIX #3: Fixing malformed anchor tags...')

for page in ['patent.html', 'corporate.html']:
    try:
        html = rf(page)
        
        # Fix malformed canonical URL (likely the culprit)
        # Pattern: href="https://sakshyasahayak.in/patent.html> (missing closing quote)
        html = re.sub(
            r'href="(https://sakshyasahayak\.in/[^"]+\.html)>',
            r'href="\1">',
            html
        )
        
        # Also fix any other malformed href attributes
        html = re.sub(
            r'href="([^"]*)(https://sakshyasahayak\.in/[^"]+\.html)">',
            r'href="\2">',
            html
        )
        
        wf(page, html)
        print(f'  ✅ {page}: Fixed malformed anchor/link tags')
    except FileNotFoundError:
        print(f'  ⚠️ {page}: File not found')

# === FIX #4: Remove Raw > Symbols from Trademark Process Steps ===
print('\n🟠 FIX #4: Fixing trademark process step markers...')

try:
    html = rf('trademark.html')
    
    # Replace raw > symbols used as step markers
    # Pattern: > 1, > 2, > 3, etc.
    html = re.sub(r'>\s*(\d+)(?=\s*<)', r'<span class="step-number">\1</span>', html)
    
    # Alternative: if steps are structured differently
    html = re.sub(r'(>\s*)(\d+)(\s*</)', r'\1<span class="step-number">\2</span>\3', html)
    
    wf('trademark.html', html)
    print('  ✅ trademark.html: Cleaned up process step markers')
except FileNotFoundError:
    print('  ⚠️ trademark.html: File not found')

# === FIX #5: Add CTA Buttons to Copyright, Patent, Corporate Pages ===
print('\n🟠 FIX #5: Adding CTA buttons to inner pages...')

CTA_BUTTON = '''\n  <!-- Professional Enquiry CTA -->\n  <div class="cta-section" style="text-align:center;padding:2rem 0;background:#FAF6F0;margin:2rem 0;border-radius:8px;">\n    <h3 style="margin-bottom:1rem;color:#1a1a2e;">Need Expert Assistance?</h3>\n    <a href="contact.html" style="display:inline-block;padding:0.75rem 2rem;background:#6B2D3E;color:#FAF6F0;text-decoration:none;border-radius:4px;font-weight:600;transition:background 0.2s;" onmouseover="this.style.background='#8B3D4E';" onmouseout="this.style.background='#6B2D3E';">Send a Professional Enquiry</a>\n  </div>'''

for page in ['copyright.html', 'patent.html', 'corporate.html']:
    try:
        html = rf(page)
        
        # Check if CTA already exists
        if 'Professional Enquiry' in html or 'cta-section' in html:
            print(f'  - {page}: CTA already present')
            continue
        
        # Insert CTA before </main> or before the footer
        if '</main>' in html:
            html = html.replace('</main>', CTA_BUTTON + '\n  </main>')
        elif '<footer' in html:
            html = re.sub(r'(<footer[^>]*>)', CTA_BUTTON + r'\n\n  \1', html)
        
        wf(page, html)
        print(f'  ✅ {page}: Added CTA button')
    except FileNotFoundError:
        print(f'  ⚠️ {page}: File not found')

print('\n=== ALL CRITICAL FIXES APPLIED ===')
print('\nNext: git add . && git commit && git push')
