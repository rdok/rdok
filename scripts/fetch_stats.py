import urllib.request
import os

BASE = "https://github-readme-stats-rdok.vercel.app"
COMMON = "username=rdok&theme=gruvbox&hide_border=true"

CARDS = {
    "stats/github-stats.svg": (
        f"{BASE}/api?{COMMON}&show_icons=true&count_private=true"
        f"&hide=stars,issues"
        f"&show=prs_merged_percentage"
        f"&custom_title=GitHub+Stats"
    ),
    "stats/top-langs.svg": (
        f"{BASE}/api/top-langs?{COMMON}&layout=compact&langs_count=7&card_width=467"
    ),
}

os.makedirs("stats", exist_ok=True)

for path, url in CARDS.items():
    print(f"Fetching {path}...")
    urllib.request.urlretrieve(url, path)

print("Done.")
