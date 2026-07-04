import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
out = sys.argv[2]
width = sys.argv[3] if len(sys.argv) > 3 else None
height = sys.argv[4] if len(sys.argv) > 4 else None

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:29229")
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle")
    page.emulate_media(media="print")
    kw = dict(path=out, print_background=True,
              margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    if width and height:
        kw["width"] = width
        kw["height"] = height
    else:
        kw["prefer_css_page_size"] = True
    page.pdf(**kw)
    page.close()
    print("PDF written:", out)
