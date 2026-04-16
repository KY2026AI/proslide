---
name: proslide-extend
description: |
  ProSlide content extension sub-skill. Used when the main skill `proslide` confirms user needs content extension.
  Trigger condition: user materials are too sparse to support a complete page structure, need logical deduction based on existing information to supplement content.
---

# ProSlide Extend

Logical deduction-based content extension from existing materials. Fabricating facts is strictly prohibited.

## Trigger Condition

User selects "need content extension" and materials are clearly insufficient to support the target page count's complete structure.

## Supplementable Dimensions

Selectively supplement one or more from the following dimensions based on material gaps and report type:

- **Background**: Business environment, policy drivers, historical evolution
- **Problem / Pain Point**: Phenomenon description, impact scope, severity
- **Goal**: Quantified indicators, time nodes, coverage scope
- **Solution Path**: Overall strategy, phase division, core ideas
- **Key Actions**: Specific measures, responsibility division, resource input
- **Expected Results**: Quantifiable effects, comparison baseline
- **Risks and Constraints**: Potential risks, response plans, resource limitations
- **Conclusions and Suggestions**: Core judgments, next actions, decision recommendations

## Core Rules

1. **Logical deduction**: All supplemented content must be reasonably inferred from original materials and cannot deviate from the topic
2. **Non-factual expression**: Must be presented in the form of "suggestions / inferences / extendable directions", clearly distinguished from user's original materials
3. **No fabrication**: Strictly prohibited from making up specific data, names, departments, times, cases, and other factual information
4. **User confirmation**: After outputting extended content, must ask whether user adopts it. Without confirmation, it cannot be directly used for generation.

## Output Format

1. **Original material summary**: Briefly summarize information already provided by user
2. **Missing dimension judgment**: Point out which dimensions have gaps
3. **Extension content suggestions**: Graded output by "suggested supplement / extendable direction / inference"
4. **User confirmation**: Ask whether user adopts these extended content
