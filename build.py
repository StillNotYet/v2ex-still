"""Build the pasteable CSS; keep it below V2EX's 8K limit."""
from pathlib import Path
import re

root = Path(__file__).parent
source = (root / "v2ex-still.css").read_text()
css = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
css = re.sub(r"\s+", " ", css)
# Do not strip whitespace before ':'; it can be a descendant combinator.
css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
css = re.sub(r":\s+", ":", css).replace(";}", "}").strip()
for index, name in enumerate(sorted(set(re.findall(r"--s-[a-z]+", css)))):
    css = css.replace(name, "--s" + chr(97 + index))
assert len(css.encode()) < 8000, "CSS exceeds the pasteable size limit"
(root / "v2ex-still.min.css").write_text(css + "\n")
print(f"Built {len(css.encode())} bytes")
