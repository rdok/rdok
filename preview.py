import subprocess
import sys
import webbrowser
from pathlib import Path

subprocess.run([sys.executable, "scripts/fetch_stats.py"], check=True)

readme = Path("README.md").read_text(encoding="utf-8")

Path("preview.html").write_text(
    f"""<!DOCTYPE html>
<html>
<body style="max-width:896px; margin:auto; padding:20px;">
{readme}
</body>
</html>""",
    encoding="utf-8",
)

webbrowser.open(Path("preview.html").resolve().as_uri())
