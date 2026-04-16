---
name: proslide-review
description: |
  ProSlide content review sub-skill. Used when the main skill `proslide` needs content diagnosis.
  Trigger conditions: user materials need content review, gap identification, typo checking.
---

# ProSlide Review

Content diagnosis framework. Output can be directly presented to the user.

## I. Review Main Process (Five-Layer Review Model)

Execute sequentially:
1. **Audience identification**: Identify reporting target, level, and focus areas
2. **Purpose identification**: Identify the PPT's purpose, usage scenario, and expected outcome
3. **Type identification**: Determine PPT type and call the corresponding special diagnosis framework
4. **Confirm identification results**: Present audience, purpose, and type identification conclusions to the user, **ask whether they are correct or need correction**. Without user confirmation, do not proceed to the next step.
5. **Content diagnosis**: Review material completeness, logic, audience fit, and expression structure
6. **Optimization suggestions output**: Output supplement, adjustment, reorganization, and correction suggestions by priority

## II. Special Diagnosis Frameworks

### 2.1 General Diagnosis Dimensions

Applicable to all PPT types:
- **Content completeness**: Does it have the necessary information to support this type of PPT?
- **Logical coherence**: Do the contents form a complete argument chain?
- **Audience fit**: Does it address the core concerns of the audience?
- **Expression structure fit**: Is it suitable for PPT presentation? Is there information overload, repetition, or hierarchy confusion?

### 2.2 Type-Specific Diagnosis

| Type | Special Diagnosis Framework |
|------|----------------------------|
| Achievement Report | Goal-Achievement-Comparison-Value |
| Problem Solving | Phenomenon-Impact-Root Cause-Evidence |
| Work Plan | Goal-Path-Tasks-Guarantee |
| Training / Sharing | Method-Case-Replicability |
| Job Performance / Competition | Performance-Ability-Match-Planning |
| Project Launch / Proposal | Background-Goal-Scope-Plan-Resources-Risks |
| Project Progress / Retrospective | Progress-Milestones-Risks-Resources |
| Special Report | Topic Focus-Analysis-Conclusion-Suggestion |
| Party Building | Position-Implementation-Mechanism-Effectiveness |

## III. Problem Solving Special Diagnosis: Four-Layer Diagnosis

Enabled only when type is identified as problem solving, rectification, or special governance.

| Layer | Checkpoints |
|-------|-------------|
| Phenomenon | Is the object, scope, time, and degree clear? Avoid vague descriptions |
| Impact | Is the business impact, risk consequence, or management consequence explained? |
| Root Cause | Are 5Why/Fishbone/5M1E used? Are surface causes distinguished from deep causes? |
| Evidence | Are there data, cases, comparisons, sources, etc. to support it? |

## III-2. Project Launch / Proposal Special Diagnosis: Six-Layer Diagnosis

Enabled only when type is identified as project launch / proposal.

| Layer | Checkpoints |
|-------|-------------|
| Background | Is the project source, business driver, policy requirement, or market opportunity explained? |
| Goal | Are goals clear, quantifiable, and strategically aligned? |
| Scope | Are project boundaries clear — what's included and excluded? |
| Plan | Are milestones, key nodes, and deliverables clear? |
| Resources | Are personnel, budget, technology, and external support in place or have acquisition paths? |
| Risks | Are major risks identified and preliminary response plans formed? |

## III-3. Project Progress / Retrospective Special Diagnosis: Four-Layer Diagnosis

Enabled only when type is identified as project progress / retrospective.

| Layer | Checkpoints |
|-------|-------------|
| Progress | Current completion rate, comparison with plan, completed key deliverables |
| Milestones | Milestone achievement status, next phase clear goals and time nodes |
| Risks | Currently identified risks, occurred problems and handling status |
| Resources | Resource usage and next-step resource needs |

## IV. Gap Identification Rules

### 4.1 Fact Gaps
- Only opinions, no data
- Only conclusions, no cases
- Only descriptions, no scope, time, object boundaries, or statistical口径
- Only results, no comparison baseline

### 4.2 Logic Gaps
- No causal chain between phenomenon and cause
- No correspondence between cause and measure
- No verification relationship between measure and result
- Conclusion exceeds material support scope

### 4.3 Audience Gaps
- Does not respond to audience core concerns
- Content focus inconsistent with reporting purpose
- Expression style does not match audience level or scenario
- Information granularity mismatched with audience cognition level

## V. Text Validation Rules

- Only check obvious typos, obvious improper word usage, and obvious punctuation errors
- Output format: `original word -> suggested correction`
- Be cautious with proper nouns, organization names, and policy terms
- Mark uncertain items as "suspected"
- Do not force corrections. Respect original text when user confirms it is correct.

## VI. Output Format (Phased)

### Phase 1: Identification Result Confirmation (Must output first)

After completing audience identification, purpose identification, and type identification, **first output the following to the user and request confirmation**:

> **Identified report profile:**
> - **Audience**: xxx
> - **Purpose**: xxx
> - **Type**: xxx (corresponding special framework: xxx)
>
> Is the above identification correct? If there are deviations, please let me know before I proceed to the next diagnosis step.

**Only after user confirmation (or correction) can proceed to Phase 2.**

### Phase 2: Complete Diagnosis Output

After user confirms identification results, output:
1. **Content diagnosis**: completeness, logic, and fit issues
2. **Gap identification**: fact gaps, logic gaps, audience gaps, text issues
3. **Optimization suggestions**: graded output by "must supplement / suggest supplement / structure optimization / text correction"
4. **Necessary follow-up questions**: When information is insufficient for high-confidence suggestions, list minimum necessary questions
