#!/usr/bin/env python3
"""
Normalize the favicon <link> block across every .html file in the site root.

Idempotent: re-running it (or running it after adding new pages) rewrites the
block in place rather than stacking duplicates. Run from the directory that
holds index.html.

    python3 fix-favicons.py
"""

import pathlib
import re
import sys

ANCHOR = re.compile(r'^[ \t]*<meta name="theme-color"[^>]*>[ \t]*$', re.M)

# Any pre-existing icon/manifest declaration, so the script can replace instead
# of append.
OLD_LINK = re.compile(
    r'^[ \t]*<link[^>]*rel="(?:icon|shortcut icon|apple-touch-icon'
    r'|apple-touch-icon-precomposed|manifest|mask-icon)"[^>]*>[ \t]*\n',
    re.M | re.I,
)

BLOCK = """<link rel="icon" href="favicon.ico" sizes="32x32" />
<link rel="icon" href="favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="apple-touch-icon.png" />
<link rel="manifest" href="manifest.webmanifest" />"""


def patch(path: pathlib.Path) -> str:
    src = path.read_text(encoding="utf-8")
    body = OLD_LINK.sub("", src)

    m = ANCHOR.search(body)
    if not m:
        return "SKIPPED (no theme-color anchor)"

    out = body[: m.end()] + "\n" + BLOCK + body[m.end() :]
    if out == src:
        return "unchanged"
    path.write_text(out, encoding="utf-8")
    return "patched"


def main() -> int:
    root = pathlib.Path(".")
    pages = sorted(root.glob("*.html"))
    if not pages:
        print("No .html files here. Run this from the directory with index.html.")
        return 1
    for p in pages:
        print(f"{p.name:<30} {patch(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
