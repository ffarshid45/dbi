import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
out = sys.argv[2]
full = len(sys.argv) > 3 and sys.argv[3] == "full"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:29229")
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()
    page.set_viewport_size({"width": 1360, "height": 900})
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(700)
    page.screenshot(path=out, full_page=full)
    page.close()
    print("shot:", out)
