# ProSlide English listing copy

Draft for the owner to paste into the Agensi website form. Not submitted. Not uploaded. Not an Agensi certification.

Docs checked on 2026-11-24:

- https://www.agensi.io/docs/packaging
- https://www.agensi.io/docs/submit-on-the-website
- https://www.agensi.io/docs/creator-faq
- https://www.agensi.io/docs/what-you-can-sell

Those pages describe a skill pack as two or more `SKILL.md` files in one ZIP. A root `SKILL.md` is not required. Website upload allows 50 MB and 1,000 files. This candidate follows that pack shape. It does not use Agensi tools.

If the name ProSlide is already taken, a fallback under the 60-character name limit is `ProSlide HTML Preview to PPTX`. Uniqueness was not checked.

## Form fields

### Name

ProSlide

### Summary

ProSlide turns confirmed notes into a 16:9 HTML slide preview, then a PPTX of high-resolution screenshots of those slides. For updates, plans, and reviews. Each exported slide is a picture of the HTML, not natively editable text.

### Compatibility note

Needs Python 3, playwright, python-pptx, and Chromium in the buyer environment. No API key and no Agensi tools. The skill pack has no root SKILL.md. Export writes a screenshot slide, and the script captures the first `.slide` only. Workflow text is Chinese; an English guide is included. This is not an Agensi certification.

### Tags

presentation, slides, powerpoint, pptx, html-preview, speaker-notes

### Use cases

Status update, project review, work plan, training outline, HTML preview before any PPTX export

### Docs URL

https://github.com/KY2026AI/proslide

### Agensi tools

None. Do not attach image, video, voice, music, or live-data tools. This pack does not call them.

### Pricing

Unset. This candidate does not choose free or paid, and it does not change payout setup. A free listing does not need a payout method; a paid listing would. That choice is the owner's.

## Description

ProSlide helps a person turn source notes into a presentation through explicit confirmation, not a one-shot file drop.

Buyers who want a status update, a plan, a problem-solving review, a training talk, or a project retrospective can use it. English and Chinese requests are both in scope. The instructions the agent follows are the existing Chinese skills. `docs/english-onboarding.md` is the English map of that same workflow.

The pack contains six skills: the main workflow, content review, content extension, chart guidance, speaker notes, and screenshot export. The buyer's agent is expected to choose among them by each skill's name and description. Current Agensi docs say that is how a skill pack is routed, and that shared files outside the skill folders are delivered with a loaded skill.

What the buyer can expect when the workflow is followed:

- A stop for report type, language, page count, diagnosis, and extension before any HTML is written.
- An HTML preview at 1280×720, which remains the editable source.
- A four-layer self-check, defined in the Chinese skill, before that preview is handed over.
- A further stop for visual changes and for speaker notes.
- Only then, a PPTX.

The PPTX is made by photographing `.slide` elements. Each exported slide is a raster image on a blank 16:9 slide. Text and charts are not natively editable inside PowerPoint. Edit the HTML and export again.

Suitable users are people who will answer the confirmation questions and who can install Python libraries for the export step. It is a poor fit for unattended generation, for editing objects inside PowerPoint, or for buyers who need Agensi's paid media tools.

Report types in the existing workflow are results, problem solving, work plan, training, role review, project kickoff, progress review, and a Party-building type (H). Type H was not removed.

Default slide colors in the Chinese layout rules (`#001E50`, `#00B0F0`, `#C00000`) are unchanged. The generic sample uses a separate neutral palette and an EXAMPLE wordmark so the preview fixture is not dressed as a company brand.

## See it in action

Illustrative expected behavior for a reviewer. This is not a recorded agent transcript, not a timed run, and not a measured quality score. No model was executed to produce the sample. The HTML fixture in `examples/generic-english-preview/` was hand-authored to show the preview shape for the same fictional brief. Figures below are example data, not measured results.

Demonstration input:

Make an English presentation preview for a community library board update. Use only this example data, and label it as example data: fictional Northline Community Library; in the last quarter the Saturday workshop series ran 12 sessions; 186 attendees signed in; the holds queue for new titles moved from 14 days to 9 days. I want a short progress review, English, 2 pages, no deep diagnosis, and no content beyond these notes. Stop at the HTML preview. Do not export a PPTX until I approve the preview.

What the workflow in this repository calls for next:

The request matches the English triggers on the main skill (presentation, HTML preview, slides). Language, page count, diagnosis, and extension are already answered: English, 2 pages, no diagnosis, no extra content. Report type still needs an explicit confirmation. The notes point at a progress review (type G). The agent should ask for that confirmation rather than skip ahead, and it may use the Chinese prompt text required by the skill.

After the type is confirmed, the agent may read the notes, plan two 1280×720 pages, and write HTML. Each page should have a title, a top rule, a logo area, and a conclusion bar. It should not invent a cause, a budget, a staffing name, or another result. It should run the four-layer check described in the skill before the preview is shown, then ask whether the HTML needs changes and whether speaker notes are needed. It should not take the export screenshot and should not write a PPTX until those answers exist.

The hand-authored preview opens as two slides for fictional Northline Community Library. Slide one states the three example figures and lists what the notes do not contain. Slide two reads the same figures as one sequence and ends on an example staffing check with no owner and no budget. The sample mark says EXAMPLE. It is not a brand logo.

A later export, if the owner approves real HTML, follows `src/export.py`: Chromium captures the first `.slide` as a PNG at device scale 2 and places that picture on one blank 16:9 slide. The second slide is not exported by that script. The picture is not natively editable. This candidate does not include a finished PPTX of the sample.

## Limitations and FAQ

### Can the buyer edit the PPTX text or charts?

No. Each exported slide is a screenshot, so the text is not natively editable. The HTML file is the source to edit. Then export again.

### Does the script export every page?

No. In this repository `query_selector` returns the first `.slide` only, and the presentation receives one picture. `references/failure-recovery.md` describes a stricter multi-page check. The script does not implement that check. Width is set to 13.333 inches. Height is not passed; the required python-pptx release preserves aspect ratio in that case. Layout index 6 on its default template is the blank layout. No sample PPTX was written for this candidate.

### What must the buyer install?

Python 3, playwright, python-pptx, and Chromium. See `requirements.txt`. Nothing from that list is bundled. There is no API key. There are no Agensi tools.

### Will the agent speak English?

English triggers are in the skill descriptions, and this listing is English. The workflow body and several required prompts remain Chinese. This candidate does not claim an English reply from a live model. That was not tested.

### Is the sample a real library result?

No. Northline Community Library and its 12 sessions, 186 sign-ins, and 14-to-9-day queue are example data in a hand-authored fixture.

### Is this listing approved or certified?

No. This is not an Agensi certification. The ZIP has not been submitted. Review time, ranking, and name availability are outside this candidate.

### Which permissions should the owner expect a scanner to notice?

The export script reads a local HTML file, launches Chromium, writes a PPTX, and deletes a temporary PNG. It does not call a remote API. It does not ask for GitHub, Slack, Notion, or a model key. Whether the buyer session allows a browser process is unresolved.

## Screenshot note for the form

Use the rendered PNG of the generic HTML preview as a product screenshot if you want one. It shows the hand-authored example, not a recorded generation and not a PPTX. Agensi allows up to six screenshots on the website form. Images in the ZIP are not what the buyer agent reads; the HTML source is the text the agent can use.
