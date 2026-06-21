# ProSlide

ProSlide 是一个面向演示文稿生产的 Codex skill，用于把用户提供的汇报素材逐步转成可预览、可确认、可导出的 PPTX。它的核心不是一次性生成成品，而是通过明确的阶段确认，把内容逻辑、HTML 设计稿、讲稿需求、导出模式和最终结果逐步收敛。

当用户提到 `PPT`、`幻灯片`、`汇报`、`presentation`、`HTML预览`、`生成页面`、`优化PPT`、`做成PPT` 等需求时，应优先使用本技能。

## Core Workflow

1. 确认报告类型
2. 确认语言版本
3. 确认目标页数
4. 确认是否需要深度诊断
5. 确认是否需要延伸内容
6. 按需进行内容诊断或延伸
7. 规划页面结构
8. 生成 HTML 预览
9. 执行四层防打回质检
10. 等待用户确认 HTML，并确认是否需要讲稿
11. 确认导出模式
12. 导出高清还原版、混合可编辑版或两版 PPTX

## Hard Stops

ProSlide 是多轮确认流程，以下节点必须停止并等待用户确认：

- 参数确认后：只允许读取素材、抽取文字、查看原稿结构，禁止生成 HTML 或 PPTX。
- 深度诊断第一阶段：先输出受众、目的、类型、专项框架识别画像，等待确认。
- 深度诊断第二阶段：输出完整诊断建议后，等待用户确认是否采纳。
- 延伸内容确认：只给出建议和可延展方向，等待用户确认采纳范围。
- HTML 预览确认：生成 HTML 后只交付预览，未经确认禁止截图或导出。
- 讲稿确认：导出前必须询问是否需要讲稿；需要时还要确认讲稿语言和汇报时长。
- 导出模式确认：只有 HTML 无需调整且讲稿需求已确认后，才允许让用户选择高清还原版、混合可编辑版或两版都要。
- 导出确认：只有用户明确选择导出模式后，才允许导出 PPTX。

## Report Types

参数确认阶段必须让用户明确报告类型：

| Code | Type |
|---|---|
| A | 成果汇报 |
| B | 问题解决 |
| C | 工作方案 |
| D | 培训分享 |
| E | 述职竞聘 |
| F | 项目启动立项 |
| G | 项目进度复盘 |
| H | 党建 |

## Quality Gate

HTML 预览交付前必须执行四层防打回质检：

- L1 页面硬伤检查：标题、顶部横线、logo、核心观点条、图片、字号、溢出、遮挡、重叠、低对比度等。
- L2 版式逻辑检查：内容关系与版式是否匹配，同级信息是否同构，阅读顺序是否自然。
- L3 汇报内容检查：结论、证据、归因、优先级、节奏、责任和指标是否能支撑汇报。
- L4 会议室终审：不了解背景的人看 10 秒，是否能知道本页表达什么、为什么重要、下一步是什么。

只有质检通过后，才可以把 HTML 预览交给用户确认。

## Layout Rules

生成 HTML 前必须读取 `skills/proslide/references/layout-rules.md`。关键约束包括：

- 页面固定为 `1280px x 720px`，白底。
- 内容区固定为 `top: 100px; left: 45px; right: 45px; bottom: 28px`。
- 每页必须包含页面标题、完整顶部横线、logo 区域、核心观点条或结论条。
- 禁止纯大段文字堆叠，必须按并列、对比、流程、数据、问题-方案等关系模块化表达。
- 图标必须是语义化 SVG 或图片，禁止用文字、数字、emoji 伪装图标。
- 明显留白必须通过语义信息图、版式重排或内容结构优化处理。
- 禁止无意义渐变，核心观点条优先使用纯色浅底。

## Directory Structure

```text
.
├── README.md
├── skills/
│   ├── proslide/
│   │   ├── SKILL.md
│   │   ├── evals/
│   │   │   └── evals.json
│   │   └── references/
│   │       ├── failure-recovery.md
│   │       ├── layout-rules.md
│   │       └── preview-qa.md
│   ├── proslide-chart/
│   ├── proslide-export/
│   ├── proslide-extend/
│   ├── proslide-review/
│   └── proslide-speaker-notes/
├── docs/
├── examples/
└── src/
```

## Related Skills

ProSlide 会按阶段调用或参考这些相关 skill：

- `proslide-review`：深度诊断，识别受众、目的、类型和专项框架。
- `proslide-extend`：素材不足或需要增强时，提供可采纳的延伸方向。
- `proslide-chart`：涉及图表或数据可视化时使用。
- `proslide-speaker-notes`：用户需要讲稿时使用。
- `proslide-export`：HTML 确认后按用户选择输出高清还原版、混合可编辑版或两版 PPTX。

## Export Modes

ProSlide 在最终导出前会让用户明确选择：

- **高清还原版**：将每页 HTML 以高清截图铺满 PPT，视觉还原度最高，适合正式展示；页面内容作为整页图片，不能逐项编辑。
- **混合可编辑版**：文字、表格、基础形状、色块、线条和进度条优先转换为 PowerPoint 原生可编辑元素；复杂图表、SVG 图标或特殊视觉效果使用独立矢量图或高清图片。适合后续修改，但可能存在轻微字体、间距或换行差异。
- **两版都要**：同时输出两种文件，分别服务展示交付和后续编辑。

混合可编辑版不会把整页截图包装成 SVG 来冒充可编辑内容。正文文字保留为文本对象，基础形状保持可单独选中和修改；只有难以可靠原生重建的复杂模块才会降级为独立 SVG 或高清 PNG。

## Install From GitHub

Codex 的 GitHub skill 安装脚本默认读取 `main` 分支。请按 `skills/<skill-name>` 路径安装主 skill 和需要的子 skill：

```bash
python scripts/install-skill-from-github.py \
  --repo KY2026AI/proslide \
  --path \
  skills/proslide \
  skills/proslide-review \
  skills/proslide-extend \
  skills/proslide-chart \
  skills/proslide-speaker-notes \
  skills/proslide-export
```

## Usage Notes

- 不要跳过参数确认，也不要替用户默认语言、页数、讲稿需求。
- 用户说“直接做”“你看着办”时，仍必须遵守强制中断点。
- HTML 预览确认前，不得导出 PPTX。
- 导出前必须确认高清还原版、混合可编辑版或两版都要。
- 高清还原版必须使用 `.slide` 元素级高清截图，不得用整页截图后裁切替代。
- 混合可编辑版必须保留文字与基础形状的原生编辑能力，禁止整页栅格化。
- 导出后必须重新渲染并检查页数、尺寸、内容完整性、清晰度和视觉溢出。

## Repository

GitHub: <https://github.com/KY2026AI/proslide>
