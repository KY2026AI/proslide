---
name: proslide-export
description: |
  ProSlide 导出子skill。当主skill `proslide` 需要将HTML预览导出为PPTX时使用。
  触发条件：用户已确认HTML预览，要求生成PPTX文件。
---

# ProSlide Export

HTML → 高清截图 → PPTX。技术规范，禁止变通。

## 导出流程

1. Playwright 打开本地 HTML 文件
2. 等待字体和 CSS 完全渲染（`wait_for_timeout(1000)`）
3. 定位 `.slide` 元素，元素级截图
4. 创建 16:9 空白 PPT，插入截图铺满整页
5. 保存 `.pptx`

## 截图强制参数

```python
screenshot_config = {
    "device_scale_factor": 2,      # 强制2倍，禁止降低
    "target_selector": ".slide",   # 强制元素截图，禁止body
    "full_page": False,            # 强制False
    "type": "png",                 # 强制PNG
    "scale": "device",
}
```

## 正确代码模板

```python
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Inches

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 1280, "height": 720},
        device_scale_factor=2,  # 强制2倍，禁止降低
    )
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

## 禁止事项

- ❌ `page.screenshot()` 直接截整页
- ❌ `device_scale_factor < 2`
- ❌ CSS 未加载完成前截图
- ❌ 保留 `.page-footer` 导致页码出现在截图中
