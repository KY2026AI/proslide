---
name: proslide
description: |
  ProSlide - Intelligent Slide Generator (HTML Preview → Screenshot → PPTX).
  Trigger scenarios: when the user mentions "PPT", "slides", "presentation", "HTML preview", "generate page", etc.
  Core feature: no need for PPT templates, directly generate HTML preview, confirm with user, then export to PPTX.
---

# ProSlide

Intelligent slide generator. Workflow: HTML Preview → User Confirmation → Playwright Screenshot → PPTX content page.

## Core Workflow

1. Type confirmation → 2. Language confirmation → 3. Page count confirmation → 4. Deep diagnosis confirmation → 5. Content extension confirmation → 6. Content diagnosis (on demand) → 7. Structure planning → 8. HTML preview generation → 9. User confirmation → 10. Export to PPTX

**Must confirm in sequence: report type, language version, target page count, need deep diagnosis, need content extension. Skipping or using defaults is strictly prohibited.**

---

## Step 1: Report Type Confirmation

Ask user to choose (A-H):
- A. Achievement Report
- B. Problem Solving
- C. Work Plan
- D. Training / Sharing
- E. Job Performance / Competition
- F. Project Launch / Proposal
- G. Project Progress / Retrospective
- H. Party Building

## Step 2: Language Version (Mandatory)

**If not specified by user, never default to Chinese.** Must explicitly ask:
- 1. Chinese
- 2. English
- 3. Chinese + English

## Step 3: Target Page Count (Mandatory)

**Must explicitly confirm page count. Never default to 1 page.** Can give suggestions (e.g. "suggest 2 pages"), but wait for user confirmation.

## Step 4: Deep Diagnosis Confirmation (Mandatory)

Before collecting core content, **must explicitly ask whether deep diagnosis is needed**. Options:
- Needed
- Not needed

If user chooses "Needed", after reading materials **call sub-skill `proslide-review`** (Skill tool) to output diagnosis results, then ask whether to adjust materials based on results.

## Step 5: Content Extension Confirmation (Mandatory)

Before collecting core content, **must explicitly ask whether content extension is needed**. Options:
- Needed
- Not needed

If user chooses "Needed", after reading materials **call sub-skill `proslide-extend`** (Skill tool), supplement content based on original material logic in the form of "suggestions / inferences / extendable directions", then ask whether user adopts them.

## Step 6: Content Diagnosis (On Demand)

Only execute when user chooses "Needed" in Step 4. After reading materials, call sub-skill `proslide-review`, output diagnosis results to user, and ask whether to adjust materials.

## Step 7: Structure Planning

Allocate content according to page count. 1-page high-density matrix requires special attention to font size.

## Step 8: HTML Preview Generation

### Page Specs (Unchangeable)

```css
.slide { width: 1280px; height: 720px; background: #FFFFFF; }
.content-area {
  position: absolute;
  top: 100px; left: 45px; right: 45px; bottom: 28px;
  display: flex; flex-direction: column; gap: 10px;
}
```

### Fixed Elements (Required on every page)

- **Top line**: `position: absolute; top: 85px; left: 0; width: 100%; height: 3px; background: #001E50; z-index: 10;`
- **Top-right Logo**: `position: absolute; top: 15px; right: 30px; width: 180px; height: 55px; object-fit: contain; z-index: 10;`
  - Before generating HTML, check working directory for `logo.png`, `logo.jpg`, `logo.jpeg`, `logo.svg`, `logo.webp`
  - Use first matched file as logo source: `<img class="logo" src="matched-filename" alt="Logo">`
  - If no logo file exists, inform user they can place a logo image, or generate without logo first
- **Page Title**: `position: absolute; top: 22px; left: 60px; font-size: 30-34px; font-weight: bold; color: #001E50;`
- **Top quote bar (`.quote-bar`)**: Every page must include a summary sentence at the top of content area to capture the core message;禁止直接进入罗列 without summary

### Top Element Constraints

- `.quote-bar` **must** be the first flex child of `.content-area`, never use `position: absolute` to float it
- Quote text defaults to `text-align: left`
- **Page title must be completely above the top line**: The top line is at `top: 85px`, so the title area (including multi-line) bottom **must not exceed 82px**. If title is long, control `font-size` (minimum 22px) and `line-height` to ensure total height does not exceed `85px - 22px = 63px`. Never squeeze line space for wrapping.
- **Do not arbitrarily break user titles**: User-provided title text must be output as-is. Strictly prohibited from inserting `<br>` for line breaks unless user explicitly requests multi-line presentation.

### Font Size Constraints (Audience-Oriented)

- **Readability优先于最小化**: PPT is for meeting room / projection scenarios. Font size defaults should prioritize "audience in the back row can read clearly", not starting from minimum and adjusting up.
- Body text minimum **11px**, default starting **13px**; titles, data, labels scale proportionally from this baseline
- **Must enlarge when space is sufficient**: Before generating HTML, actively estimate content occupancy. If content height ≤ available height × 85%, must uniformly increase font size by 1–2px across all levels; if still not overflowing after enlarging → continue enlarging until approaching comfortable upper limit
- **Prohibited from being overly conservative within safety margins**: Never reserve >20% blank space without enlarging font size under the excuse of "preventing overflow". Audience reading convenience takes priority over absolute safe margins.
- High-density pages may reduce to 11px, but must consciously note "minimum font size adopted due to density constraints", and simultaneously enhance recognition through bold, color blocks, and icons.

### Image Constraints

1. **Fully displayed**: User-provided images must be fully displayed using `object-fit: contain`. Prohibited from using `cover` or fixed aspect ratios that cause distortion.
2. **Prohibited from overflowing containers**: If placed in colored blocks, cards, etc., images must be fully within container boundaries. Overflow is prohibited.
3. **Fallback protection**: Image outer containers must have `overflow: hidden`
4. **Height control**: Avoid using `justify-content: center` on image containers that may cause top/bottom overflow unless content height is strictly limited or container has fixed height.

### Chart Constraints

If charts are involved, **call sub-skill `proslide-chart`** (Skill tool).

### Information Expression Constraints

- **Structured first**: Reorganize information by logic, use modular, visual, and flow-based expression
- **Relationship visualization**: Use layout to express parallel, progressive, contrast, hierarchical, and cyclic relationships
- **Data chartization**: Prioritize charts for data presentation, avoid pure text stacking
- **Material relevance**: Prioritize visual elements strongly related to content (icons, charts, diagrams, infographics, tables, etc.)
- **Bilingual layout**: When Chinese and English appear together, English should be below or to the right of Chinese. English above Chinese is strictly prohibited.
- **No decorative materials**: Do not use meaningless decorative materials or visual elements that conflict with the theme style.

### Icon Constraints

- **Icon library**: Use Lucide-style linear icons (SVG)
- **Visual specs**: 2px stroke, rounded endpoints, clean and modern lines
- **Semantic first**: Icons must serve content semantics. Pure decorative icons are prohibited. Icon meaning must be consistent with text direction.
- **Color limit**: Icons use no more than 3 colors (excluding grayscale accents)
- **Spacing**: 8–12px between icon and text
- **Size limit**: Icon size must not exceed the visually dominant size of its text level
- **High-density handling**: In high-density layouts, prioritize structure over forced icons

### Layout and Whitespace Constraints

1. **Whitespace must serve expression**
   - Whitespace should emphasize main information, enhance hierarchy, and improve reading rhythm
   - If whitespace is excessive and cannot form visual balance, adjust structure rather than adding more whitespace
   - Prohibit "passive whitespace caused by insufficient content" from occupying the main body of the page

2. **Sparse content and heterogeneous card visual reinforcement rules**
   - When single-page content is insufficient or card content volumes vary greatly, prohibit filling space by forcing equal-height columns, stretching containers, or adding meaningless empty frames
   - Prioritize resolving passive whitespace through structural adjustments: asymmetric grids, flow heights, tighter spacing, left-right contrast, top-bottom layering
   - Use stronger title hierarchy, key numbers, icons, status labels, list emphasis marks, and other structured visual elements to fill content areas instead of blank space
   - All reinforcement means must serve content semantics. Pure decorative filling is prohibited.

### Color Specifications

- Primary (deep blue): `#001E50`
- Accent (bright blue): `#00B0F0`
- Red: `#C00000` (only for problem identification, risk warning, party-building themes)
- **Full-page red theme for party-building**: When report type is party-building, page titles, column titles, icons, data cards, key text, and other main visual elements **must uniformly use `#C00000`** as the theme color. Deep blue `#001E50` is prohibited.

## Step 9: User Confirmation

Inform file path and ask whether adjustments are needed. **Export is prohibited without confirmation.**

## Step 10: Export to PPTX

After user confirmation, **call sub-skill `proslide-export`** (Skill tool) to execute screenshot and PPTX insertion.

---

## Prohibited Behavior List

- ❌ Check PPT templates (cover.pptx, etc.) — this workflow does not require templates
- ❌ Default to Chinese when language is not confirmed
- ❌ Generate directly without confirming page count
- ❌ Use absolute positioning for quote bar causing overlap
- ❌ Overly compress font size when space is sufficient
- ❌ Export to PPTX directly without user confirmation
