---
name: proslide-chart
description: |
  ProSlide chart design sub-skill. Used when the main skill `proslide` involves ECharts chart generation or chart review.
  Trigger condition: the page needs to insert bar charts, line charts, pie charts, stacked charts, scatter plots, radar charts, and other data visualizations.
---

# ProSlide Chart

Chart design principles: reasonable, concise, non-misleading.

## I. Chart Selection Rules

Choose based on data structure and expression purpose:
- **Bar/Column Chart**: Category comparison, horizontal comparison
- **Line Chart**: Time trends, change processes
- **Pie Chart**: Composition proportions (few and clear categories)
- **Stacked Chart**: Total and component changes
- **Scatter Plot**: Correlation, distribution identification
- **Radar Chart**: Multi-dimensional indicator relative comparison

When type mismatch occurs, suggest a more suitable chart instead of forcing the drawing.

## II. Rationality Constraints

- Prohibit forcing indicators with different dimensions or vastly different magnitudes into the same axis
- No more than 3 colors in the same chart (excluding grayscale accents)
- Stacked charts only applicable to additive items; target values suggest dashed frames, reference lines, or independent series
- Axis truncation, dual-axis charts, and mixed percentage/absolute value usage must clearly label口径
- Too many pie slices → switch to bar chart

## III. Simplicity Constraints

- Grid lines: default to removed or extremely weakened
- Borders/shadows: no shadows on chart containers, border ≤ 1px
- Data labels: preferentially label key values, avoid full labeling causing occlusion
- When chart is too complex, prefer splitting into multiple charts

## IV. Default Color Scheme

```js
color: ['#001E50', '#00B0F0', '#C00000']
```

- Primary: core series or main conclusion
- Accent: comparison series
- Warning: anomalies, risks, key emphasis
- Grayscale: auxiliary information, background, secondary labels
- No 3D charts or strong gradients

## V. Page-Level Requirements

- Chart titles should directly express the conclusion
- Each chart should preferably carry only one core conclusion
- Charts serve the page narrative and should not become standalone exhibits
