from browser.scraper import extract_text, extract_links, get_soup, _parse_ddg_lite, _parse_ddg_html, _parse_bing, _resolve_ddg_link


def test_extract_text_regression():
    """
    Regression test: the original code called `soup.text(seperator=...)`.
    `.text` is a BeautifulSoup *property* (a plain string), not a method,
    so calling it raised `TypeError: 'str' object is not callable`.
    This confirms extract_text uses `.get_text()` instead and works.
    """
    html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
    assert extract_text(html) == "Hello World"


def test_extract_links():
    html = '<a href="https://example.com">link</a>'
    assert extract_links(html) == ["https://example.com"]


def test_get_soup_parses():
    soup = get_soup("<p>test</p>")
    assert soup.find("p").text == "test"


def test_parse_ddg_lite():
    html = '<a class="result-link" href="https://example.com/a">Title A</a>'
    assert _parse_ddg_lite(html) == [{"title": "Title A", "link": "https://example.com/a"}]


def test_parse_ddg_html_unwraps_redirect_link():
    """
    Regression test: DuckDuckGo sometimes wraps result links in a
    //duckduckgo.com/l/?uddg=<encoded> redirect rather than a direct URL.
    """
    html = ('<a class="result__a" '
            'href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com%2Fjob&rut=x">Job</a>')
    assert _parse_ddg_html(html) == [{"title": "Job", "link": "https://example.com/job"}]


def test_parse_bing():
    html = '<li class="b_algo"><h2><a href="https://example.com/b">Title B</a></h2></li>'
    assert _parse_bing(html) == [{"title": "Title B", "link": "https://example.com/b"}]


def test_resolve_ddg_link_passthrough_for_direct_urls():
    assert _resolve_ddg_link("https://example.com/direct") == "https://example.com/direct"
