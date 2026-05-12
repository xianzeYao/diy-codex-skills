---
name: paper-reading-notion
description: Use when creating or updating the user's Notion PaperReading notes from a paper PDF, arXiv/project link, Zotero PDF path, or later reading discussion. Builds lightweight Notion pages under 实验室工作/PaperReading with figures, formulas, tables, related-work links, and the user's critical reading style.
metadata:
  short-description: Create/update Notion PaperReading notes from papers
---

# Paper Reading Notion

Create and maintain the user's Notion `实验室工作 / PaperReading` pages.

Use this skill for two modes:

- **Create mode**: user gives a PDF path, Zotero PDF path, arXiv link, project page, or paper title and asks to write/read it into Notion.
- **Update mode**: user gives an existing PaperReading page plus refined thoughts,精读 discussion, translated paragraphs, critiques, or experiments to merge into the page.

The goal is not to replace the user's精读. Codex should do the mechanical and structural work: extract paper material, build a good Notion draft, link existing notes, and later merge confirmed thoughts.

## Required Style

Top-level Notion structure should stay light:

```markdown
> 作者：
> 机构：
> 链接：
> 投稿：
> 时间：

# 现况与动机
# 方法
# 实验
# 思考
```

Only add lower-level subsections when useful. Do not turn the page into a rigid report with many mandatory headings.

Prefer the user's style:

- Explain mechanisms and problem structure, not only summaries.
- Keep enough descriptive evidence before critique. A good page should first make the paper's task, mechanism, experiment setup, and concrete numbers clear; then add critical judgment. Do not make the page mostly opinions.
- Keep formulas and variables when they clarify interfaces.
- Golden rule for images: every image must呼应 and help the surrounding正文. Insert a figure only when the nearby paragraph/table uses it to explain a bottleneck, mechanism, setup, result, or limitation. Do not insert images just to make the page look richer.
- Use paper figures/tables/project-page images as anchors in the section where they are discussed. Do not collect figures at the bottom as a generic `图表摘录` section unless it is a temporary staging area that will be cleaned up.
- Preserve a critical voice in `思考`, matching the user's better PaperReading pages: `💡` for reusable insight, `‼️` for real risks/fairness/limitation questions, and `🧪` for testable follow-up experiments. Each callout should contain a few concrete points, not generic praise/criticism. Do not use emoji page icons.
- Do not set a Notion page cover/background unless the user explicitly asks.
- Link related notes only when they are existing pages under `实验室工作 / PaperReading`; do not link notes found elsewhere in Notion.
- For experiments, always name the baselines, explain what each baseline represents, describe the evaluation setting/protocol, then interpret the main result and ablations. Avoid result tables without context.
- Keep method and experiment roles separate. `方法` explains what the paper does and why the design might work; result tables, timing/memory numbers, benchmark metrics, and deployment-cost evidence belong in `实验`, even when they discuss a method component.
- Image captions should be plain descriptive names. Do not prefix captions with `Figure`, `Fig.`, `Table`, `Table/Figure`, or numbering unless the number is needed to disambiguate a paper-specific reference.

## Create Mode Workflow

1. Read the input paper.
   - For local PDFs, extract text page by page.
   - If available, find project page/arXiv/GitHub and stable image assets, but do not assume every paper has a project page.
   - Prefer original paper/project figures over generic images.
   - If no stable figure URL exists, render/crop screenshots into local PNGs. The Notion connector cannot embed local paths.
   - Upload local images with Notion's File Upload API via `scripts/upload_notion_images.py`, targeting the relevant page/block so the image appears near the paragraph/table it explains. This requires `NOTION_TOKEN` or `NOTION_API_KEY` with access to the target page or block. Use `--cleanup` for temporary screenshots after successful upload.
   - Use `scripts/prepare_notion_figures.py` to render/crop PNGs and generate a local manifest before upload.
   - Do not create hosted-image or Computer Use paste workarounds. If File Upload API is unavailable, keep the figure caption/link and mention that the image was not inserted.
2. Run the first-principles analysis internally using `references/first-principles-prompt.md`.
   - Do not paste the full prompt structure into Notion.
   - Map it into the light Notion template.
3. Build the Notion page:
   - Metadata block.
   - `现况与动机`: problem, prior routes, why old interfaces fail, related-work links.
   - `方法`: one-sentence mechanism, task/interface, key designs, key formulas. Do not put benchmark tables, timing numbers, memory results, or result-style cost analysis here.
   - `实验`: experiment questions, baseline descriptions, evaluation set/protocol, main results, important ablations, and what the results do and do not prove. Include enough factual setup before critique.
   - `思考`: 2-3 compact Notion callouts in the Point What You Mean style, not plain quote blocks: reusable insight (`💡`), serious doubts/limitations (`‼️`), and testable follow-up experiments (`🧪`). Keep each point tied to a mechanism, evidence gap, or experiment design.
   - Place each figure in context: teaser/problem figures in `现况与动机`, architecture/pipeline figures in `方法`, benchmark/result/ablation figures in `实验`, and only leave a separate figure list if the user explicitly asks.
4. Search the existing `PaperReading` page for 3-8 important related works and use normal Markdown links to Notion pages. Link only pages that are children of `实验室工作 / PaperReading`. Do **not** use `<page>` tags in generated content; they may be escaped incorrectly.
5. Create the page under `实验室工作 / PaperReading` without a page cover/background.
6. Backlink maintenance: after creating or updating a page, inspect related existing PaperReading pages for natural mentions of the new paper/method. If a page already mentions the paper title, acronym, or method name, convert only that existing phrase into a normal Markdown link and keep the sentence text unchanged. Do not append generic tail lines by default. Append a minimal related-work sentence only when there is no natural mention and the backlink is genuinely useful. In the final response, report every backlink edit with page title, the sentence/snippet touched, and the phrase that was linked.
7. Final response should include the Notion page URL and a short note about any limitations, e.g. PDF figures could not be extracted or Notion File Upload API was unavailable.

## Update Mode Workflow

1. Fetch the existing Notion page first.
2. Identify where the new material belongs:
   - background/motivation
   - method
   - experiment
   - `💡`
   - `‼️`
   - `🧪`
3. Update only the relevant section when possible. Avoid rewriting the whole page unless the user asks for a cleanup/rewrite.
4. Preserve existing user-written thoughts. Merge and refine; do not delete unless asked.
5. If the user provides chatbox精读 discussion, treat it as higher-priority than the initial AI draft.
6. When maintaining backlinks, update only an existing mention into a link when possible. Do not add tail "related" lines unless there is no natural mention and the link is important enough to justify a new sentence. Report exactly which page and sentence changed.

## References

- `references/first-principles-prompt.md`: the user's coarse-reading analysis prompt.
- `references/notion-style.md`: page style, formulas/tables/images, and related-work linking rules.
- `scripts/prepare_notion_figures.py`: render/crop local PNGs from paper PDFs.
- `scripts/upload_notion_images.py`: upload local images to Notion with the File Upload API and append image blocks.
