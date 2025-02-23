import os
import shutil
from pathlib import Path
import re

DOCS_SOURCE = Path("docs")
DOCS_TARGET = Path("website/docs")
JEKYLL_HEADER = """---    
layout: docs    
title: {title}    
---    
"""

def replace_md_with_html(content):
    # Regular expression to find markdown links
    return re.sub(r"(\]\()(.*?)(\.md)(\))", r"\1\2.html\4", content)

def process_md_files(src, dest):
    for item in os.listdir(src):
        src_path = src / item
        dest_path = dest / item

        if src_path.is_dir():
            dest_path.mkdir(exist_ok=True)
            process_md_files(src_path, dest_path)
        elif src_path.suffix == ".md":
            with open(src_path, "r") as f:
                content = f.read()

                # Replace .md references with .html
            content = replace_md_with_html(content)

            title = item[:-3].replace("_", " ").title()
            new_content = JEKYLL_HEADER.format(title=title) + content

            with open(dest_path, "w") as f:
                f.write(new_content)

if __name__ == "__main__":
    if DOCS_TARGET.exists():
        shutil.rmtree(DOCS_TARGET)
    DOCS_TARGET.mkdir()

    process_md_files(DOCS_SOURCE, DOCS_TARGET)
    print(f"Processed {len(list(DOCS_TARGET.glob('**/*.md')))} documentation files")