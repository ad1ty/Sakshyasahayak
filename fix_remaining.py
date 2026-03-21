#!/usr/bin/env python3
"""
Fix all remaining HTML inconsistencies in Sakshya Sahayak website
Run this from the repository root directory
"""

import re

def fix_file(filename, canonical_url, missing_footer_links=[]):
    print(f"Fixing {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Broken canonical tag (different patterns per file)
    canonical_patterns = [
        (r'  //sakshyasahayak\.in/[^"]+"\s*>\s*>\s*>', f'  >'),
        (r'  //sakshyasahayak\.in/[^"]+"\s*>&gt;&gt;', f'  >'),
        (r'  //sakshyasahayak\.in/[^"]+"\s*> >>', f'  >'),
        (r'  //sakshyasahayak\.in/[^"]+"\s*>', f'  >'),
    ]
    
    for pattern, replacement in canonical_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix 2: Missing > opening tags in nav (both desktop and mobile)
    content = re.sub(r'(\s+)><a href="([^"]+)">([^<]+)</a></li>', r'\1><a href="\2">\3</a></li>', content)
    
    # Fix 3: Add missing footer nav links
    if missing_footer_links:
        footer_nav_pattern = r'(<ul class="footer-nav-list">)(.*?)(</ul>)'
        match = re.search(footer_nav_pattern, content, re.DOTALL)
        if match:
            existing_nav = match.group(2)
            # Add missing links before Contact
            for link_html in missing_footer_links:
                if link_html not in existing_nav:
                    # Insert before Contact
                    existing_nav = existing_nav.replace(
                        '><a href="contact.html">Contact</a></li>',
                        f'{link_html}\n          ><a href="contact.html">Contact</a></li>'
                    )
            content = re.sub(footer_nav_pattern, rf'\1{existing_nav}\3', content, flags=re.DOTALL)
    
    # Fix 4: Standardize copyright text
    copyright_patterns = [
        (r'© 2026 Sakshya Sahayak(?:\s*\|[^<]*)?', 
         '© 2026 Sakshya Sahayak. All rights reserved. | Maintained in compliance with BCI Rule 36, Chapter II, Part VI.'),
    ]
    
    for pattern, replacement in copyright_patterns:
        content = re.sub(pattern, replacement, content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {filename} fixed!")

# Fix each remaining file
fix_file('copyright.html', 
         'https://sakshyasahayak.in/copyright.html',
         missing_footer_links=['><a href="corporate.html">Corporate</a></li>'])

fix_file('patent.html', 
         'https://sakshyasahayak.in/patent.html',
         missing_footer_links=[
             '><a href="copyright.html">Copyright</a></li>',
             '><a href="corporate.html">Corporate</a></li>'
         ])

fix_file('corporate.html', 
         'https://sakshyasahayak.in/corporate.html',
         missing_footer_links=[
             '><a href="copyright.html">Copyright</a></li>',
             '><a href="patent.html">Patent</a></li>'
         ])

fix_file('disclaimer.html', 
         'https://sakshyasahayak.in/disclaimer.html',
         missing_footer_links=[
             '><a href="copyright.html">Copyright</a></li>',
             '><a href="patent.html">Patent</a></li>',
             '><a href="corporate.html">Corporate</a></li>'
         ])

fix_file('contact.html', 
         'https://sakshyasahayak.in/contact.html',
         missing_footer_links=[
             '><a href="copyright.html">Copyright</a></li>',
             '><a href="patent.html">Patent</a></li>',
             '><a href="corporate.html">Corporate</a></li>'
         ])

# Fix sitemap.xml
print("Fixing sitemap.xml...")
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap_additions = '''  <url>
    oc>https://sakshyasahayak.in/about.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    oc>https://sakshyasahayak.in/trademark.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    oc>https://sakshyasahayak.in/copyright.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    oc>https://sakshyasahayak.in/patent.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    oc>https://sakshyasahayak.in/corporate.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    oc>https://sakshyasahayak.in/disclaimer.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    oc>https://sakshyasahayak.in/contact.html</loc>
    astmod>2026-03-22</lastmod>
    hangefreq>yearly</changefreq>
    <priority>0.8</priority>
  </url>
'''

if 'about.html' not in sitemap:
    sitemap = sitemap.replace('</urlset>', sitemap_additions + '</urlset>')
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print("✓ sitemap.xml fixed!")
else:
    print("✓ sitemap.xml already has new pages!")

print("\n✅ All fixes complete!")
print("\nNext steps:")
print("1. Review changes: git diff")
print("2. Commit: git add . && git commit -m 'Fix all HTML inconsistencies'")
print("3. Push: git push origin main")
