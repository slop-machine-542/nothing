#!/usr/bin/env python3
"""
Rewrite all HTML files in the nothing repository with a consistent MathJax 2.7.9 template.
"""

import os
import re
import glob

# The consistent HTML template with MathJax 2.7.9
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="theme-color" content="#2c3e50">
    <title>{title}</title>
    
    <!-- MathJax 2.7.9 Configuration -->
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({{
            tex2jax: {{
                inlineMath: [['\\\\(', '\\\\)']],
                displayMath: [['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            }},
            "HTML-CSS": {{
                availableFonts: ["TeX"],
                linebreaks: {{ automatic: true }}
            }},
            SVG: {{
                linebreaks: {{ automatic: true }}
            }}
        }});
    </script>
    <!-- MathJax 2.7.9 from cdnjs.cloudflare.com -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-AMS_HTML"></script>
    
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <nav>
        <ul>
            <li><a href="{home_link}">Home</a></li>
            <li><a href="{posts_link}">All Posts</a></li>
            <li><a href="{tags_link}">Tags</a></li>
            <li><a href="https://github.com/slop-machine-542/nothing">GitHub</a></li>
        </ul>
    </nav>

    <header class="site-header">
        <h1>{header_title}</h1>
        {header_subtitle}
    </header>

    <main>
{content}
    </main>

    <footer>
        <p><strong>Daily Math Digest</strong> — Powered by curiosity and mathematics.</p>
        <p>
            <a href="https://github.com/slop-machine-542/nothing">View on GitHub</a> | 
            <a href="{home_link}">Home</a> |
            <a href="{posts_link}">All Posts</a>
        </p>
    </footer>
</body>
</html>'''

def extract_content_from_html(filepath):
    """Extract the main content from an existing HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract content between <main> tags
    main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
    if main_match:
        return main_match.group(1).strip()
    
    # Try to extract content between <body> tags (excluding nav and footer)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
        # Remove nav
        body_content = re.sub(r'<nav[^>]*>.*?</nav>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        # Remove footer
        body_content = re.sub(r'<footer[^>]*>.*?</footer>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        # Remove header/site-header if present
        body_content = re.sub(r'<header[^>]*>.*?</header>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        return body_content.strip()
    
    return ""

def extract_title_from_html(filepath):
    """Extract the title from an existing HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try <title> tag
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    
    # Try h1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if h1_match:
        return re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
    
    return "Daily Math Digest"

def extract_description_from_html(filepath):
    """Extract the description from an existing HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try meta description
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if desc_match:
        return desc_match.group(1).strip()
    
    desc_match = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', content, re.IGNORECASE)
    if desc_match:
        return desc_match.group(1).strip()
    
    return "A curated collection of mathematical insights, theorems, and explorations"

def rewrite_index_html():
    """Rewrite the root index.html file."""
    filepath = '/root/.openclaw/workspace/nothing/index.html'
    
    content = extract_content_from_html(filepath)
    title = extract_title_from_html(filepath)
    description = extract_description_from_html(filepath)
    
    # For index.html, we need to preserve the posts array and script
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    # Extract the script section
    script_match = re.search(r'<script>.*?</script>', original, re.DOTALL | re.IGNORECASE)
    script_content = script_match.group(0) if script_match else ""
    
    # Combine content and script
    full_content = content + '\n\n' + script_content if script_content else content
    
    new_html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        css_path='css/style.css',
        home_link='index.html',
        posts_link='posts/index.html',
        tags_link='tags/index.html',
        header_title='📐 Daily Math Digest',
        header_subtitle='<p class="site-description">A curated collection of mathematical insights, theorems, and explorations. Discover beautiful mathematics from topology to number theory, updated regularly.</p>',
        content=full_content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Rewrote: {filepath}")

def rewrite_posts_index_html():
    """Rewrite the posts/index.html file."""
    filepath = '/root/.openclaw/workspace/nothing/posts/index.html'
    
    content = extract_content_from_html(filepath)
    title = extract_title_from_html(filepath)
    description = extract_description_from_html(filepath)
    
    # Extract script
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    script_match = re.search(r'<script>.*?</script>', original, re.DOTALL | re.IGNORECASE)
    script_content = script_match.group(0) if script_match else ""
    
    full_content = content + '\n\n' + script_content if script_content else content
    
    new_html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        css_path='../css/style.css',
        home_link='../index.html',
        posts_link='./index.html',
        tags_link='../tags/index.html',
        header_title='📐 Daily Math Digest',
        header_subtitle='<p class="site-description">All Posts Archive</p>',
        content=full_content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Rewrote: {filepath}")

def rewrite_tags_index_html():
    """Rewrite the tags/index.html file."""
    filepath = '/root/.openclaw/workspace/nothing/tags/index.html'
    
    content = extract_content_from_html(filepath)
    title = extract_title_from_html(filepath)
    description = extract_description_from_html(filepath)
    
    # Extract script
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    script_match = re.search(r'<script>.*?</script>', original, re.DOTALL | re.IGNORECASE)
    script_content = script_match.group(0) if script_match else ""
    
    full_content = content + '\n\n' + script_content if script_content else content
    
    new_html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        css_path='../css/style.css',
        home_link='../index.html',
        posts_link='../posts/index.html',
        tags_link='./index.html',
        header_title='📐 Daily Math Digest',
        header_subtitle='<p class="site-description">Browse Posts by Tag</p>',
        content=full_content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Rewrote: {filepath}")

def rewrite_post_file(filepath):
    """Rewrite an individual post HTML file."""
    content = extract_content_from_html(filepath)
    title = extract_title_from_html(filepath)
    description = extract_description_from_html(filepath)
    
    # Extract script if any
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    script_match = re.search(r'<script>.*?</script>', original, re.DOTALL | re.IGNORECASE)
    script_content = script_match.group(0) if script_match else ""
    
    full_content = content + '\n\n' + script_content if script_content else content
    
    # Extract date from filename if possible
    filename = os.path.basename(filepath)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        date_str = date_match.group(1)
        header_subtitle = f'<p class="date">{date_str}</p>'
    else:
        header_subtitle = ''
    
    new_html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        css_path='../css/style.css',
        home_link='../index.html',
        posts_link='./index.html',
        tags_link='../tags/index.html',
        header_title='📐 Daily Math Digest',
        header_subtitle=header_subtitle,
        content=full_content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Rewrote: {filepath}")

def main():
    base_dir = '/root/.openclaw/workspace/nothing'
    
    # Rewrite main index.html
    rewrite_index_html()
    
    # Rewrite posts/index.html
    rewrite_posts_index_html()
    
    # Rewrite tags/index.html
    rewrite_tags_index_html()
    
    # Rewrite all post files
    post_files = glob.glob(os.path.join(base_dir, 'posts', '*.html'))
    for filepath in post_files:
        if os.path.basename(filepath) == 'index.html':
            continue  # Already handled
        rewrite_post_file(filepath)
    
    print("\nAll HTML files have been rewritten with the consistent MathJax 2.7.9 template!")

if __name__ == '__main__':
    main()
