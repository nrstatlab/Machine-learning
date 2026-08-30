#!/usr/bin/env python3
"""Structural checks for index.html.

Catches the classes of defect that have actually bitten this file before:
unescaped `<` or `&` inside code panes, broken in-page anchors, code-tab
buttons pointing at panes that do not exist, Prism language classes missing
from the <pre>, Python panes that no longer parse, and headline counts in
the footer drifting away from the real number of cards.

Exit code 0 = clean, 1 = at least one failure.
"""
import ast
import html
import re
import sys
from pathlib import Path

DOC = Path(__file__).resolve().parent.parent / "index.html"
failures: list[str] = []
notes: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    if ok:
        notes.append(f"  ok    {label}")
    else:
        failures.append(f"  FAIL  {label}{': ' + detail if detail else ''}")


src = DOC.read_text(encoding="utf-8")

# ── code panes ────────────────────────────────────────────────────────────
panes = re.findall(
    r'<div class="code-pane[^"]*" id="([^"]+)">\s*'
    r'<pre class="language-(\w+)"><code class="language-(\w+)">(.*?)</code></pre>',
    src, re.S)
check(len(panes) == 46, "46 code panes found", f"found {len(panes)}")
check(all(a == b for _, a, b, _ in panes), "language class on both <pre> and <code>")

unescaped = [pid for pid, _, _, body in panes if re.search(r"<(?!/?(?:code|pre)\b)", body)]
check(not unescaped, "no raw '<' inside code panes", ", ".join(unescaped))

bare_amp = [pid for pid, _, _, body in panes
            if re.search(r"&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)", body)]
check(not bare_amp, "no bare '&' inside code panes", ", ".join(bare_amp))

bad_py = []
for pid, lang, _, body in panes:
    if lang != "python":
        continue
    try:
        ast.parse(html.unescape(body))
    except SyntaxError as exc:
        bad_py.append(f"{pid} (line {exc.lineno})")
check(not bad_py, "every Python pane parses", ", ".join(bad_py))

# ── navigation integrity ──────────────────────────────────────────────────
ids = set(re.findall(r'\bid="([^"]+)"', src))
anchors = re.findall(r'href="#([^"]+)"', src)
broken = sorted({a for a in anchors if a not in ids})
check(not broken, f"all {len(anchors)} in-page anchors resolve", ", ".join(broken))

tabs = re.findall(r"switchTab\(this,\s*'([^']+)'\)", src)
missing_tabs = sorted({t for t in tabs if t not in ids})
check(not missing_tabs, f"all {len(tabs)} code-tab targets resolve", ", ".join(missing_tabs))

scrolls = re.findall(r"scrollToUnit\('([^']+)'\)", src)
missing_units = sorted({t for t in scrolls if t not in ids})
check(not missing_units, "all unit jump targets resolve", ", ".join(missing_units))
check("function scrollTo(" not in src,
      "no global scrollTo shadowing window.scrollTo")

# ── card inventory vs. what the page claims ───────────────────────────────
cards = re.findall(r'<div class="algo-card" id="([^"]+)"', src)
examples = src.count('class="example-card')
keypoints = src.count('class="key-points"')
check(len(cards) == 23, "23 algorithm cards", f"found {len(cards)}")
check(examples == len(cards) * 3, "3 examples per card", f"found {examples}")
check(keypoints == len(cards), "assumptions/failure-modes row on every card",
      f"found {keypoints}")

footer = re.search(r"4 Units · (\d+) Algorithms · (\d+) Real-World Examples", src)
if footer:
    check(int(footer.group(1)) == len(cards) and int(footer.group(2)) == examples,
          "footer counts match the document",
          f"footer says {footer.group(1)}/{footer.group(2)}, "
          f"document has {len(cards)}/{examples}")
else:
    check(False, "footer count line present")

# ── currency shielded from MathJax ────────────────────────────────────────
body = re.sub(r"<pre.*?</pre>|<style.*?</style>|<script.*?</script>", "", src, flags=re.S)
leaky = []
for m in re.finditer(r"<(td|th)((?:(?!>).)*)>((?:(?!</\1>).)*)</\1>", body, re.S):
    attrs, text = m.group(2), m.group(3)
    stripped = re.sub(r"\$\$.*?\$\$", "", text, flags=re.S)
    stripped = re.sub(r"\$[^$\n]{1,200}\$", "", stripped)
    if "$" in stripped and "tex2jax_ignore" not in attrs:
        leaky.append(m.group(0)[:60])
check(not leaky, "currency cells shielded with tex2jax_ignore", "; ".join(leaky))

# ── report ────────────────────────────────────────────────────────────────
print("\n".join(notes))
if failures:
    print("\n".join(failures))
    print(f"\n{len(failures)} check(s) failed.")
    sys.exit(1)
print(f"\nAll {len(notes)} checks passed.")
