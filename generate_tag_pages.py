#!/usr/bin/env python3
"""Generate tag pages with posts for Math Digest"""

import os
import re
from pathlib import Path

POSTS_DIR = Path("/root/.openclaw/workspace/nothing/posts")
TAGS_DIR = Path("/root/.openclaw/workspace/nothing/tags")

def extract_tags_from_post(filepath):
    """Extract tags from a post HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for tags in the content
        # Pattern: class="tag">tag-name</a> or similar
        tags = []
        
        # Try different patterns
        patterns = [
            r'<span[^>]*class=["\']tag["\'][^>]*>([^<]+)</span>',
            r'class=["\']tag["\'][^>]*>([^<]+)</a>',
            r'<a[^>]*class=["\']tag["\'][^>]*>([^<]+)</a>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                tag = match.strip().lower().replace(' ', '-')
                if tag and tag not in tags:
                    tags.append(tag)
        
        return tags
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def extract_post_info(filepath):
    """Extract post title and date from HTML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else filepath.stem
        
        # Extract date from filename or content
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
        date = date_match.group(1) if date_match else ""
        
        # Extract summary - look for first paragraph after post-date
        summary = ""
        summary_match = re.search(r'class=["\']post-date["\'][^>]*>[^<]+</p>\s*<p>([^<]+)', content)
        if summary_match:
            summary = summary_match.group(1)[:200] + "..." if len(summary_match.group(1)) > 200 else summary_match.group(1)
        
        return {
            'filename': filepath.name,
            'title': title.replace('Math Digest — ', ''),
            'date': date,
            'summary': summary
        }
    except Exception as e:
        print(f"Error extracting info from {filepath}: {e}")
        return {
            'filename': filepath.name,
            'title': filepath.stem,
            'date': '',
            'summary': ''
        }

def generate_tag_page(tag, posts):
    """Generate HTML for a tag page."""
    posts_html = ""
    for post in sorted(posts, key=lambda x: x['filename'], reverse=True):
        posts_html += f'''
        <div class="post-card">
            <h3><a href="../posts/{post['filename']}">📐 {post['title']}</a></h3>
            <p class="post-date">{post['date']}</p>
            <p>{post['summary']}</p>
        </div>
'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Math Digest — Posts tagged with {tag}">
    <meta name="theme-color" content="#2c3e50">
    <title>Math Digest — Tag: {tag}</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header class="site-header">
        <h1>📐 Math Digest</h1>
        <p class="site-description">A curated collection of mathematical insights</p>
    </header>

    <nav>
        <ul>
            <li><a href="../index.html">Home</a></li>
            <li><a href="../posts/index.html">All Posts</a></li>
            <li><a href="./index.html">Tags</a></li>
            <li><a href="https://github.com/slop-machine-542/nothing">GitHub</a></li>
        </ul>
    </nav>

    <main>
        <h1>🏷️ Tag: {tag}</h1>
        <p>Posts tagged with "{tag}"</p>
        
        {posts_html if posts_html else '<p><em>No posts found with this tag.</em></p>'}
        
        <p style="margin-top: 2rem;">
            <a href="./index.html" class="tag">← Back to all tags</a>
        </p>
    </main>

    <footer>
        <p><strong>Math Digest</strong> — Powered by curiosity and mathematics</p>
        <p>
            <a href="https://github.com/slop-machine-542/nothing">View on GitHub</a> |
            <a href="../index.html">Home</a> |
            <a href="../posts/index.html">All Posts</a>
        </p>
    </footer>
</body>
</html>
'''
    return html

def main():
    # Build mapping of tags to posts
    tag_posts = {}
    
    for post_file in POSTS_DIR.glob("*.html"):
        if post_file.name == "index.html":
            continue
        
        tags = extract_tags_from_post(post_file)
        post_info = extract_post_info(post_file)
        
        print(f"Processing {post_file.name}: tags = {tags}")
        
        for tag in tags:
            if tag not in tag_posts:
                tag_posts[tag] = []
            tag_posts[tag].append(post_info)
    
    # Generate tag pages
    for tag, posts in tag_posts.items():
        tag_file = TAGS_DIR / f"{tag}.html"
        html = generate_tag_page(tag, posts)
        
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated: {tag_file} ({len(posts)} posts)")
    
    print(f"\nGenerated {len(tag_posts)} tag pages")

if __name__ == "__main__":
    main()
