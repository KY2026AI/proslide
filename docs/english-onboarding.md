# ProSlide English onboarding

This file is a map of the workflow already written in `skills/proslide/SKILL.md`. Follow that file, including every hard stop. This map does not replace it, does not translate every reference, and does not change the Chinese confirmation text.

This package is a skill pack: several `SKILL.md` files, and no root `SKILL.md`. Current Agensi packaging docs (checked 2026-11-24) say a pack is two or more `SKILL.md` files anywhere in the ZIP, and a root `SKILL.md` is not required. This is not an Agensi certification. The pack was not uploaded and was not run inside an Agensi agent.

The public files in this repository are the only source for this candidate. Do not assume they match any newer skill installed outside the repository.

## What you get

ProSlide is a staged presentation workflow:

1. Confirm the report type, language, page count, whether a diagnosis is needed, and whether extra content may be added.
2. Read the source notes only after those answers exist.
3. Plan pages and write an HTML preview at 1280×720.
4. Check the preview before showing it.
5. Stop. Ask whether the HTML needs changes, and whether speaker notes are needed.
6. Export a PPTX only after the HTML is accepted and the speaker-notes choice is settled.

The editable source is the HTML. A later PPTX is a screenshot file: each exported page is a raster image of a `.slide` element placed on a blank 16:9 slide. Titles, body text, and charts in that PPTX are not natively editable. Change the HTML and export again.

## How to start in English

Ask for a presentation, slide deck, slides, PowerPoint, PPTX, HTML preview, or speaker notes. The main skill description lists those English triggers next to the original Chinese triggers. You can answer later questions in English.

The agent may still ask with the Chinese sentences required by `skills/proslide/SKILL.md`. Those sentences were left as written. Answer the decision they ask for. "No changes" and "no speaker notes" are enough when they match what you want. Do not expect this candidate to have rewritten the workflow into English.

Saying "just do it", "you decide", or "skip the preview" does not skip a gate.

## Five answers the workflow requires

| Gate | What to say | Notes in this repository |
|---|---|---|
| Report type | One of A–H below | Do not leave this implied. |
| Language | Chinese, English, or both | Bilingual pages need both languages in the body, not only in titles. |
| Page count | A number you accept | The skill may suggest a number. Wait for an explicit yes. |
| Diagnosis | Yes or no | Yes runs `proslide-review` in two confirmation stages before HTML. |
| Extension | Yes or no | Yes runs `proslide-extend`. Added material stays marked as suggestion until you accept it. Facts are not invented. |

| Code | Type |
|---|---|
| A | Results report |
| B | Problem solving |
| C | Work plan |
| D | Training or sharing |
| E | Role review or internal application |
| F | Project kickoff |
| G | Progress review or retrospective |
| H | Party-building report, as defined in the Chinese workflow |

Type H is part of the existing workflow and uses the red theme already specified there. This candidate does not remove it.

## Hard stops

Stop and wait, even if several preferences were given at once:

- After the five gates: reading notes is allowed. Writing HTML, taking screenshots, and exporting PPTX are not.
- Diagnosis, if requested: first confirm the audience, purpose, and type. Then confirm the full diagnosis. Only then may HTML be written.
- Extension, if requested: confirm which suggestions to keep before they enter the HTML.
- HTML preview: deliver the file and wait. Do not screenshot or export yet.
- Speaker notes: ask before export. If notes are wanted, confirm their language and the speaking time, then use `proslide-speaker-notes`. Do not assume the notes use the slide language.
- Export: only after the HTML needs no further change and the notes choice is settled. Use `proslide-export`.

## Files the agent actually reads

From `skills/proslide/`, as that skill already instructs:

- `references/layout-rules.md` before HTML
- `references/layout-pattern-library.md` when the layout choice needs it
- `references/preview-qa.md` after the preview is drafted
- `references/failure-recovery.md` only if screenshot or export fails

Other skills in the pack, loaded when that stage is reached:

- `proslide-review` for diagnosis
- `proslide-extend` for accepted extension of thin notes
- `proslide-chart` before a bar, line, pie, stacked, scatter, or radar chart is written
- `proslide-speaker-notes` for a spoken script
- `proslide-export` for PPTX

Those skill bodies are Chinese. Use them as the instructions. This English file only tells you the order.

## HTML preview

Pages are `.slide` elements at 1280×720 on a white background. The content box is top 100px, left 45px, right 45px, bottom 28px. Each page has a title, a top rule, a logo area, and a conclusion bar. Training pages (type D) may use a guiding sentence instead of a hard conclusion. The default colors in `references/layout-rules.md` are unchanged: `#001E50`, `#00B0F0`, and `#C00000`. This onboarding does not restyle that workflow.

Put the caller's own logo in the working folder as `logo.png`, `logo.jpg`, `logo.jpeg`, `logo.svg`, or `logo.webp` if they want one. Do not download a brand mark. If no logo is there, ask before inventing one. The generic sample in this package uses a wordmark that says EXAMPLE because it is example data, not a brand.

## Export behavior in this repository

`skills/proslide-export/scripts/export_html_to_pptx.py` and `src/export.py` are the same standalone script. Agensi runs a packaged script from a temporary copy, so this script does not read other files in the pack. Install its libraries in the buyer environment. They are listed in `requirements.txt` and are not bundled:

```bash
pip install playwright python-pptx
playwright install chromium
python export_html_to_pptx.py --input preview.html --output deck.pptx
```

What the script in this repository actually does:

- Opens the HTML in Chromium with a 1280×720 viewport and `device_scale_factor` 2.
- Waits 1000ms. It does not wait on `document.fonts.ready`.
- Finds the first `.slide` with `query_selector`, then takes a PNG of that element.
- Builds one 16:9 slide (13.333 by 7.5 inches) from `slide_layouts[6]` and inserts the PNG at the origin with width 13.333 inches. Height is not passed. The python-pptx release required here documents that omitting one dimension preserves aspect ratio, and on its default template layout 6 is named Blank. This candidate did not write a PPTX of the sample.
- Deletes the temporary PNG.

So a multi-page HTML file is not fully exported by this script. `references/failure-recovery.md` asks for every `.slide`, both width and height, and a higher scale. That file is the recovery checklist. It describes stricter checks than the script performs. The inline sample in `skills/proslide-export/SKILL.md` matches the script: one element screenshot, scale 2, width set, height omitted.

The PPTX page is a screenshot. It is not natively editable text or charts. Keep the HTML.

No Agensi paid tool, API key, or hosted model is required for this package. The export still needs a local Python environment that can launch Chromium. Whether an Agensi buyer session allows that launch was not tested.

## Generic example

`examples/generic-english-preview/` is a product preview fixture, not a deck to ship as client work.

- `PROMPT.md` is the demonstration input.
- `preview.html` is a hand-authored two-page illustration for that input.
- `example-mark.svg` is a sample wordmark that reads EXAMPLE. It is not a brand logo.

Demonstration input:

Make an English presentation preview for a community library board update. Use only this example data, and label it as example data: fictional Northline Community Library; in the last quarter the Saturday workshop series ran 12 sessions; 186 attendees signed in; the holds queue for new titles moved from 14 days to 9 days. I want a short progress review, English, 2 pages, no deep diagnosis, and no content beyond these notes. Stop at the HTML preview. Do not export a PPTX until I approve the preview.

The organization, Northline Community Library, and the figures (12 sessions, 186 sign-ins, a holds queue from 14 days to 9 days) are example data. They are not measured results. Do not export a PPTX of this fixture until the owner has approved a real HTML preview. The packaging command does not create a PPTX.

## What this candidate leaves unresolved

- Name uniqueness on Agensi was not checked.
- The official category list was not copied. The owner picks categories on the submit form.
- No live Agensi agent was asked to follow an English or Chinese prompt. English coverage here is a static check of trigger phrases and eval fixtures.
- Buyer font availability, `file://` access, and Playwright install rights were not tested in an Agensi session.
- Website upload is the intended channel (50 MB, 1,000 files). The separate in-agent upload channel is smaller (100 files, 5 MB, text only) and is not the target of this ZIP.

## Package command

From the repository root:

```bash
python3 scripts/package_agensi_candidate.py
```

That writes a local ZIP, a manifest, and a validation report. It does not publish a release, open a listing, or upload the ZIP.
