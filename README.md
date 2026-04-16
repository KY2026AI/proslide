# ProSlide

🎯 **Intelligent Slide Generator** — HTML Preview → Screenshot → PPTX

A platform-agnostic skill system for generating presentation slides from structured content. No PPT templates required.

---

## ✨ What is ProSlide?

ProSlide is a **10-step workflow** that helps AI assistants and bots generate professional PowerPoint slides:

1. **Type confirmation** → What kind of presentation?
2. **Language confirmation** → Chinese, English, or bilingual?
3. **Page count confirmation** → How many slides?
4. **Deep diagnosis check** → Need content review?
5. **Content extension check** → Need logical expansion?
6. **Content diagnosis** (on demand) → Gap analysis
7. **Structure planning** → Allocate content across pages
8. **HTML preview generation** → Pixel-perfect 1280×720 preview
9. **User confirmation** → Review and iterate
10. **Export to PPTX** → Playwright screenshot → slide

---

## 🏗️ Project Structure

```
proslide-project/
├── README.md
├── skills/
│   ├── proslide/              # Main skill - workflow orchestration
│   ├── proslide-review/       # Content diagnosis & gap analysis
│   ├── proslide-extend/       # Logical content extension
│   ├── proslide-export/       # HTML → Screenshot → PPTX
│   └── proslide-chart/        # Chart design guidelines
├── src/
│   └── export.py              # Standalone export script
├── examples/
│   └── base-slide.html        # Base HTML template
└── docs/
    └── INTEGRATION.md         # Platform integration guides
```

---

## 🚀 Quick Start

### For Claude Code / Claude Desktop

1. Copy the `skills/` directories into your Claude skills folder
2. Reference the skill with `proslide` when users mention "PPT", "slides", or "presentation"
3. The main skill will guide the conversation through all 10 steps

### For OpenClaw / Custom Agents

1. Include the skill markdown files in your agent's system prompt or skill registry
2. Map `proslide-export` to a tool that runs `python src/export.py`
3. Follow the workflow constraints in `skills/proslide/SKILL.md`

### For Feishu (Lark) Bots

1. Parse user intent (PPT generation keywords)
2. Load `skills/proslide/SKILL.md` as the core agent prompt
3. Implement sub-skills as internal functions or API calls
4. Use `src/export.py` or an equivalent Playwright service for final PPTX generation

See [`docs/INTEGRATION.md`](docs/INTEGRATION.md) for detailed integration guides.

---

## 📐 Design System

### Slide Canvas
- **Resolution**: 1280 × 720 px (16:9)
- **Content area**: `top: 100px; left: 45px; right: 45px; bottom: 28px`
- **Top line**: `top: 85px; height: 3px`

### Color Palette
| Role | Hex | Usage |
|------|-----|-------|
| Primary | `#001E50` | Titles, headers, top line |
| Accent | `#00B0F0` | Highlights, data, labels |
| Warning/Party | `#C00000` | Risks, warnings, party-building themes |

### Typography Rules
- **Minimum body text**: 11px
- **Default body text**: 13px (audience-first)
- **Must enlarge** when content fills ≤ 85% of available height
- Bilingual layouts: **English below or to the right of Chinese**

### Key Layout Principles
- **Same level, same structure**: Parallel information points must use parallel visual forms
- **No decorative elements**: Every visual must serve content semantics
- **No passive whitespace**: Adjust structure before accepting large blank areas
- **Quote bar required**: Every page must start with a core insight summary

---

## 🛠️ Standalone Export Script

```bash
pip install playwright python-pptx
playwright install chromium

python src/export.py \
  --input examples/base-slide.html \
  --output output.pptx
```

The export script:
- Opens the HTML at 2× device scale factor
- Waits for fonts/CSS to render
- Takes an element screenshot of `.slide`
- Embeds it into a 16:9 blank PPTX

---

## 📋 Report Types (A–H)

| ID | Type | Framework |
|----|------|-----------|
| A | Achievement Report | Goal-Achievement-Comparison-Value |
| B | Problem Solving | Phenomenon-Impact-Root Cause-Evidence |
| C | Work Plan | Goal-Path-Tasks-Guarantee |
| D | Training / Sharing | Method-Case-Replicability |
| E | Job Performance / Competition | Performance-Ability-Match-Planning |
| F | Project Launch / Proposal | Background-Goal-Scope-Plan-Resources-Risks |
| G | Project Progress / Retrospective | Progress-Milestones-Risks-Resources |
| H | Party Building | Position-Implementation-Mechanism-Effectiveness |

---

## 🤝 Contributing

This skill system is being actively refined through real-world test cases. If you discover layout edge cases, visual bugs, or missing constraints, please:

1. Test with a real content example
2. Identify the specific rule that should have prevented the issue
3. Submit a PR updating the relevant `SKILL.md`

---

## 📄 License

MIT License — use freely in your own agents, bots, and workflows.
