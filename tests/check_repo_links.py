#!/usr/bin/env python3
"""Checks that relative links and images in all Markdown files exist. Run from the repo root."""
import re, pathlib, sys
root = pathlib.Path(".")
bad = 0
for md in root.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    for m in re.finditer(r'!?\[[^\]]*\]\(([^)\s]+)\)|<img[^>]+src="([^"]+)"', text):
        t = (m.group(1) or m.group(2)).split("#")[0]
        if not t or t.startswith(("http", "mailto:")): continue
        if not (md.parent / t).exists():
            print(f"BROKEN: {md} -> {t}"); bad += 1
for md in root.rglob("*.md"):
    if "images/animations/" not in md.read_text(encoding="utf-8"):
        print(f"NO ANIMATION: {md}"); bad += 1
print("All relative links OK and every Markdown file has an animation" if not bad else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
