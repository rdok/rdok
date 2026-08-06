import pytest

from fetch_latest_post import END, START, format_date, latest_post, render_section, splice


def test_reads_the_first_item_title():
    title, _, _ = latest_post(make_feed())
    assert title == "Trusting agent code"


def test_reads_the_first_item_link():
    _, link, _ = latest_post(make_feed())
    assert link == "https://example.com/posts/trusting-agent-code/"


def test_reads_the_first_item_publication_date():
    _, _, published = latest_post(make_feed())
    assert published == "Wed, 05 Aug 2026 12:00:00 GMT"


def test_rejects_a_feed_with_no_items():
    with pytest.raises(ValueError):
        latest_post(b"<rss><channel></channel></rss>")


def test_rejects_an_item_missing_its_title():
    with pytest.raises(ValueError):
        latest_post(make_feed(title=""))


def test_rejects_an_item_missing_its_link():
    with pytest.raises(ValueError):
        latest_post(make_feed(link=""))


def test_rejects_an_item_missing_its_date():
    with pytest.raises(ValueError):
        latest_post(make_feed(published=""))


def test_rejects_a_link_that_is_not_http():
    with pytest.raises(ValueError):
        latest_post(make_feed(link="javascript:alert(1)"))


def test_formats_the_date_without_a_leading_zero():
    assert format_date("Wed, 05 Aug 2026 12:00:00 GMT") == "5 Aug 2026"


def test_renders_the_title_as_a_link():
    assert '<a href="https://example.com/"><strong>A title</strong></a>' in render_section(
        "A title", "https://example.com/", DATE
    )


def test_renders_the_date_beside_the_title():
    assert "5 Aug 2026" in render_section("A title", "https://example.com/", DATE)


def test_escapes_markup_in_the_title():
    assert "&lt;script&gt;" in render_section("<script>", "https://example.com/", DATE)


def test_inserts_the_new_section():
    assert "fresh" in splice(make_readme("stale"), "fresh")


def test_replaces_whatever_sits_between_the_markers():
    assert "stale" not in splice(make_readme("stale"), "fresh")


def test_leaves_the_start_marker_in_place():
    assert START in splice(make_readme("stale"), "fresh")


def test_leaves_the_end_marker_in_place():
    assert END in splice(make_readme("stale"), "fresh")


def test_splicing_twice_changes_nothing_the_second_time():
    once = splice(make_readme("stale"), "fresh")
    assert splice(once, "fresh") == once


def test_keeps_content_outside_the_markers():
    assert "# Profile" in splice(make_readme("stale"), "fresh")


def test_rejects_a_readme_without_markers():
    with pytest.raises(ValueError):
        splice("# Profile\n", "fresh")


def test_rejects_markers_in_the_wrong_order():
    with pytest.raises(ValueError):
        splice(f"# Profile\n\n{END}\nbody\n{START}\n", "fresh")


DATE = "Wed, 05 Aug 2026 12:00:00 GMT"


def make_feed(
    title="Trusting agent code",
    link="https://example.com/posts/trusting-agent-code/",
    published=DATE,
):
    return f"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item>
    <title>{title}</title>
    <link>{link}</link>
    <pubDate>{published}</pubDate>
  </item>
  <item>
    <title>An older post</title>
    <link>https://example.com/posts/older/</link>
    <pubDate>Tue, 04 Aug 2026 12:00:00 GMT</pubDate>
  </item>
</channel></rss>""".encode()


def make_readme(body):
    return f"# Profile\n\n{START}\n{body}\n{END}\n"
