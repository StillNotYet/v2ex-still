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
    css = css.replace(name, "--" + chr(65 + index))
output = css + "\n"
size = len(output.encode())
if size >= 8000:
    raise SystemExit(f"CSS exceeds the pasteable size limit ({size} bytes)")
for filename in ("v2ex-still.min.css", "v2ex-still.theme.min.css"):
    (root / filename).write_text(output)
print(f"Built {size} bytes")
