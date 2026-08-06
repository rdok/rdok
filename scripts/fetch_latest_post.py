import re
import urllib.request
import xml.etree.ElementTree as ElementTree
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path

FEED_URL = "https://stories.rdok.co.uk/rss.xml"
FEED_TIMEOUT_SECONDS = 30
START = "<!-- LATEST-POST:START -->"
END = "<!-- LATEST-POST:END -->"


def render_section(title, link, published):
    return (
        f'<p><a href="{escape(link)}"><strong>{escape(title, quote=False)}</strong></a>'
        f" · {format_date(published)}</p>"
    )


def format_date(published):
    parsed = parsedate_to_datetime(published)
    return f"{parsed.day} {parsed:%b %Y}"


def splice(readme, section):
    if START not in readme or END not in readme:
        raise ValueError(f"Markers {START} / {END} not found in README.md")

    pattern = f"{re.escape(START)}.*?{re.escape(END)}"
    updated, substitutions = re.subn(
        pattern, lambda _: f"{START}\n{section}\n{END}", readme, count=1, flags=re.DOTALL
    )
    if substitutions != 1:
        raise ValueError(f"Expected one {START}...{END} block, spliced {substitutions}")
    return updated


def latest_post(feed_xml):
    item = ElementTree.fromstring(feed_xml).find("./channel/item")
    if item is None:
        raise ValueError("The feed contains no items.")

    title = item.findtext("title", "").strip()
    link = item.findtext("link", "").strip()
    published = item.findtext("pubDate", "").strip()

    if not (title and link and published):
        raise ValueError(
            f"Incomplete feed item: title={title!r} link={link!r} pubDate={published!r}"
        )
    if not link.startswith(("http://", "https://")):
        raise ValueError(f"Refusing a link that is not http(s): {link!r}")

    return title, link, published


def main():
    print(f"Fetching {FEED_URL}...")
    with urllib.request.urlopen(FEED_URL, timeout=FEED_TIMEOUT_SECONDS) as response:
        title, link, published = latest_post(response.read())

    readme_path = Path("README.md")
    readme = readme_path.read_text(encoding="utf-8")
    updated = splice(readme, render_section(title, link, published))

    if updated == readme:
        print("No change.")
        return

    readme_path.write_text(updated, encoding="utf-8")
    print(f"Updated: {title}")


if __name__ == "__main__":
    main()
