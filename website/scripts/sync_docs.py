#!/usr/bin/env python3  
import os
import shutil
from pathlib import Path
import re
import posixpath

DOCS_SOURCE = Path("docs")
DOCS_TARGET = Path("website/docs")
JEKYLL_HEADER = """---      
layout: docs      
title: {title}      
---      
"""

# This function takes the content of a markdown file and the file’s current  
# relative directory (relative to the docs root) and replaces internal markdown links  
# (links ending with .md) with links that use the relative_url filter and an absolute docs path.  
# External links (those starting with http:// or https://) are left unchanged.  
def replace_md_with_html(content, current_rel_dir):
    # Pattern: Match links that are NOT external and end with .md.  
    # Group members:  
    #   Group(1) - the literal "]("  
    #   Group(2) - the link URL without the .md extension  
    #   Group(3) - the closing ")"  
    pattern = re.compile(r'(\]\()((?!https?://)[^)\s]+?)\.md(\))', flags=re.IGNORECASE)

    def repl(match):
        link = match.group(2).strip()
        # If the link is relative (does not start with a slash), join it with the current relative directory.  
        if not link.startswith("/"):
            # Create an absolute path relative to the docs root.  
            abs_path = posixpath.normpath(posixpath.join("/docs", current_rel_dir, link))
        else:
            # If already absolute, just normalize the path.  
            abs_path = posixpath.normpath(link)
            # Add the .html extension, as it will be converted in the site.
        abs_path += ".html"
        # Return a new markdown link using Jekyll’s relative_url filter.  
        return f'{match.group(1)}{{{{ "{abs_path}" | relative_url }}}}{match.group(3)}'

    return pattern.sub(repl, content)

# Processes markdown files recursively.  
# "rel_dir" is a string representing the current directory relative to DOCS_SOURCE using POSIX-style paths.  
def process_md_files(src: Path, dest: Path, rel_dir=""):
    for item in os.listdir(src):
        src_path = src / item
        dest_path = dest / item

        if src_path.is_dir():
            # Compute new relative directory for files in subdirectories.  
            new_rel_dir = posixpath.join(rel_dir, item) if rel_dir else item
            dest_path.mkdir(exist_ok=True)
            process_md_files(src_path, dest_path, new_rel_dir)
        elif src_path.suffix.lower() == ".md":
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

                # Replace markdown links with converted links.
            content = replace_md_with_html(content, rel_dir)

            # Use the filename (without ".md") as the title.  
            title = item[:-3].replace("_", " ").title()
            new_content = JEKYLL_HEADER.format(title=title) + content

            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(new_content)

if __name__ == "__main__":
    if DOCS_TARGET.exists():
        shutil.rmtree(DOCS_TARGET)
    DOCS_TARGET.mkdir(parents=True, exist_ok=True)

    process_md_files(DOCS_SOURCE, DOCS_TARGET)
    num_files = len(list(DOCS_TARGET.glob("**/*.md")))
    print(f"Processed {num_files} documentation files")  