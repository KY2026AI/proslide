---
name: proslide-export
description: |
  ProSlide export sub-skill. Used when the main skill `proslide` needs to export HTML preview to PPTX.
  Trigger condition: user has confirmed the HTML preview and requested PPTX file generation.
---

# ProSlide Export

HTML → HD Screenshot → PPTX. Technical specifications, no workarounds allowed.

## Export Process

1. Playwright opens the local HTML file
2. Wait for fonts and CSS to fully render (`wait_for_timeout(1000)`)
3. Locate `.slide` element and take element-level screenshot
4. Create a blank 16:9 PPT and insert the screenshot to fill the entire page
5. Save `.pptx`

## Screenshot Mandatory Parameters

```python
screenshot_config = {
    "device_scale_factor": 2,      # Force 2x, never lower
    "target_selector": ".slide",   # Force element screenshot, never body
    "full_page": False,            # Force False
    "type": "png",                 # Force PNG
    "scale": "device",
}
```

## Correct Code Template

```python
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Inches

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(1000)
    slide = page.query_selector(".slide")
    screenshot_path = "slide.png"
    slide.screenshot(path=screenshot_path, type="png", scale="device")
    browser.close()

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]
s = prs.slides.add_slide(blank_layout)
s.shapes.add_picture(screenshot_path, Inches(0), Inches(0), width=Inches(13.333))
prs.save(output_path)
```

## Prohibited Items

- ❌ `page.screenshot()` for full-page capture
- ❌ `device_scale_factor < 2`
- ❌ Screenshot before CSS is fully loaded
- ❌ Keeping `.page-footer` causing page numbers to appear in screenshot
