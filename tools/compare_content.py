#!/usr/bin/env python3
"""Compare the visible body text of a built page against the captured live-site baseline.

  compare_content.py BASELINE_TXT BUILT_HTML [--skip-baseline-lines N]

Baseline text = audit/baseline/text/<slug>.txt (text of the live <main>, including
its side-navigation list, which is navigation rather than content: skip it with
--skip-baseline-lines). Built text = text inside <main>, excluding .sr-only
accessibility additions and <nav> elements. Whitespace and non-breaking spaces are
normalised; nothing else is (case, punctuation, typos and entities must match).
Exit status 0 = identical, 1 = differences (printed)."""
import difflib, re, sys
from html.parser import HTMLParser


class Extract(HTMLParser):
    BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "tr", "div", "section", "article", "header", "br", "ul", "ol", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip = []          # stack of tags being skipped
        self.out = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.in_main = True
        if not self.in_main:
            return
        cls = (a.get("class") or "").split()
        if self.skip or tag == "nav" or "sr-only" in cls or tag in ("script", "style"):
            self.skip.append(tag) if tag not in ("br", "img") else None
            return
        if tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if self.skip and tag == self.skip[-1]:
            self.skip.pop()
            return
        if self.in_main and not self.skip and tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.in_main and not self.skip:
            self.out.append(data)


def norm_lines(text):
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.split("\n")]
    return [l for l in lines if l]


def main():
    base_path, built_path = sys.argv[1], sys.argv[2]
    skip = 0
    if "--skip-baseline-lines" in sys.argv:
        skip = int(sys.argv[sys.argv.index("--skip-baseline-lines") + 1])
    base = norm_lines(open(base_path, encoding="utf-8").read())[skip:]
    ex = Extract()
    ex.feed(open(built_path, encoding="utf-8").read())
    built = norm_lines("".join(ex.out))
    # Compare as a flowing text so that block-structure changes (e.g. a heading and a
    # paragraph merged or split by markup) are judged on words, not line breaks.
    bw, tw = " ".join(base).split(" "), " ".join(built).split(" ")
    if bw == tw:
        print(f"IDENTICAL  {built_path}  ({len(bw)} words)")
        return 0
    print(f"DIFFERENT  {built_path}")
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, bw, tw, autojunk=False).get_opcodes():
        if op != "equal":
            print(f"  {op}: baseline[{' '.join(bw[i1:i2])!r}] -> built[{' '.join(tw[j1:j2])!r}]")
    return 1


if __name__ == "__main__":
    sys.exit(main())
