# ProSlide Integration Guide

This document explains how to integrate ProSlide into different AI platforms and bot frameworks.

---

## 1. Claude Code / Claude Desktop

### Installation
1. Locate your Claude skills directory:
   - macOS: `~/.claude/skills/`
   - Windows: `%APPDATA%\Claude\skills\`
   - Linux: `~/.config/claude/skills/`

2. Copy each skill folder:
   ```bash
   cp -r skills/proslide ~/.claude/skills/
   cp -r skills/proslide-review ~/.claude/skills/
   cp -r skills/proslide-export ~/.claude/skills/
   cp -r skills/proslide-extend ~/.claude/skills/
   cp -r skills/proslide-chart ~/.claude/skills/
   ```

3. Ensure the export environment has Playwright installed:
   ```bash
   pip install playwright python-pptx
   playwright install chromium
   ```

### Usage
When a user mentions "PPT", "slides", "presentation", "汇报", "幻灯片", etc., Claude will automatically load `proslide` and follow the 10-step workflow.

Sub-skills are invoked via the Skill tool:
- `proslide-review` → content diagnosis
- `proslide-extend` → content extension
- `proslide-export` → PPTX generation
- `proslide-chart` → chart guidelines

---

## 2. OpenClaw / Custom Agent Frameworks

### Prompt Injection Pattern
Inject the skill markdown directly into the system prompt:

```python
SYSTEM_PROMPT = """
You are an AI assistant with the following skills available:

{proslide_skill_md}
{proslide_review_skill_md}
{proslide_export_skill_md}
{proslide_extend_skill_md}
{proslide_chart_skill_md}

When the user mentions PPT/slides/presentation, you MUST follow the ProSlide 10-step workflow.
Call sub-skills by name in your reasoning and route to the appropriate handler.
"""
```

### Tool Mapping
Map each sub-skill to a function:

```python
tools = {
    "proslide": lambda: orchestrate_workflow(),
    "proslide-review": lambda content: review_content(content),
    "proslide-extend": lambda content: extend_content(content),
    "proslide-export": lambda html_path: run_export_script(html_path),
    "proslide-chart": lambda spec: chart_guidelines(spec),
}
```

### Export Handler
Use the provided script or call it programmatically:

```python
from src.export import export_html_to_pptx

output = export_html_to_pptx("preview.html", "output.pptx")
```

---

## 3. Feishu (Lark) Bots

### Architecture

```
User Message
    ↓
Intent Parser (detects PPT keywords)
    ↓
ProSlide Agent (loads skills/proslide/SKILL.md as prompt)
    ↓
Conversation turns: confirm type → language → pages → diagnosis → extension
    ↓
HTML Generator (renders 1280×720 preview)
    ↓
User Preview Card (send HTML file or screenshot)
    ↓
Export Service (Playwright worker generates PPTX)
    ↓
User receives PPTX file
```

### Implementation Tips

**Intent Detection**
Trigger on keywords: PPT, 幻灯片, 汇报, presentation, 生成页面, 帮我做PPT, etc.

**Conversation State Machine**
Store the current step (1–10) in session state. Each user reply advances the state.

**HTML Preview Delivery**
- Generate the HTML on your server
- Take a screenshot with Playwright
- Send the image as a message card
- Provide "Confirm" / "Adjust" buttons

**PPTX Export**
Run `src/export.py` in a serverless function or container:

```bash
python src/export.py -i /tmp/preview.html -o /tmp/output.pptx
```

Then upload `/tmp/output.pptx` to the chat via the Feishu Drive API.

### Message Card Suggestion
Use a Feishu interactive card to show the preview and action buttons:

```json
{
  "config": { "wide_screen_mode": true },
  "elements": [
    {
      "tag": "img",
      "img_key": "preview_image_key",
      "alt": { "tag": "plain_text", "content": "Slide Preview" }
    },
    {
      "tag": "action",
      "actions": [
        { "tag": "button", "text": { "tag": "plain_text", "content": "确认生成PPTX" }, "type": "primary", "value": {"action": "export"} },
        { "tag": "button", "text": { "tag": "plain_text", "content": "调整内容" }, "type": "default", "value": {"action": "revise"} }
      ]
    }
  ]
}
```

---

## 4. Generic REST API / SaaS Integration

If you are building a presentation generation API:

### Endpoint Design

```http
POST /api/v1/presentations
Content-Type: application/json

{
  "title": "Q1 Safety Report",
  "type": "B",
  "language": "zh",
  "pages": 2,
  "content": { ... },
  "options": {
    "deep_diagnosis": false,
    "content_extension": false
  }
}
```

### Response

```json
{
  "id": "pres_123",
  "status": "preview_ready",
  "preview_url": "https://cdn.example.com/pres_123/preview.html",
  "preview_image": "https://cdn.example.com/pres_123/preview.png",
  "actions": {
    "confirm": "https://api.example.com/v1/presentations/pres_123/export",
    "revise": "https://api.example.com/v1/presentations/pres_123/revise"
  }
}
```

### Export Endpoint

```http
POST /api/v1/presentations/pres_123/export
```

Returns the generated `.pptx` file or a download URL.

---

## 5. Customizing for Your Organization

### Brand Colors
Edit the color specifications in `skills/proslide/SKILL.md`:
- Primary `#001E50` → your brand primary
- Accent `#00B0F0` → your brand accent
- Warning `#C00000` → your brand warning/red

### Logo Handling
The skill looks for `logo.png`, `logo.jpg`, `logo.jpeg`, `logo.svg`, or `logo.webp` in the working directory. You can:
1. Pre-place a default logo in your execution environment
2. Accept logo uploads from users
3. Skip the logo if none is provided

### Report Types
The A–H report type framework can be extended by adding new types to `skills/proslide/SKILL.md` and `skills/proslide-review/SKILL.md`.

---

## Need Help?

Open an issue with your platform details and we can expand this guide.
