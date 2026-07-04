import sys
from playwright.sync_api import sync_playwright

url = "file:///home/ubuntu/aipark-submission/site/index.html"
out = sys.argv[1] if len(sys.argv) > 1 else "/home/ubuntu/aipark-submission/ZILAL_AL_SAFA_proposal.pdf"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:29229")
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle")
    page.emulate_media(media="screen")
    page.pdf(path=out, format="A4", print_background=True,
             margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    page.close()
    print("PDF written:", out)
