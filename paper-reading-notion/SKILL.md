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
- Keep formulas and variables when they clarify interfaces.
- Use paper figures/tables/project-page images as anchors.
- Preserve a critical voice. Use a few `💡` / `‼️` / `🧪` callouts in `思考` when they make the page easier to scan, matching the user's existing PaperReading style. Do not use emoji page icons.
- Do not set a Notion page cover/background unless the user explicitly asks.
- Link related notes only when they are existing pages under `实验室工作 / PaperReading`; do not link notes found elsewhere in Notion.

## Create Mode Workflow

1. Read the input paper.
   - For local PDFs, extract text page by page.
   - If available, find project page/arXiv/GitHub and stable image assets, but do not assume every paper has a project page.
   - Prefer original paper/project figures over generic images.
   - If no stable figure URL exists, render/crop screenshots into local PNGs. The Notion connector cannot embed local paths.
   - Upload local images with Notion's File Upload API via `scripts/upload_notion_images.py`, then append them as Notion-hosted image blocks. This requires `NOTION_TOKEN` or `NOTION_API_KEY` with access to the target page or its parent. Use `--cleanup` for temporary screenshots after successful upload.
   - Use `scripts/prepare_notion_figures.py` to render/crop PNGs and generate a local manifest before upload.
   - Do not create hosted-image or Computer Use paste workarounds. If File Upload API is unavailable, keep the figure caption/link and mention that the image was not inserted.
2. Run the first-principles analysis internally using `references/first-principles-prompt.md`.
   - Do not paste the full prompt structure into Notion.
   - Map it into the light Notion template.
3. Build the Notion page:
   - Metadata block.
   - `现况与动机`: problem, prior routes, why old interfaces fail, related-work links.
   - `方法`: one-sentence mechanism, task/interface, key designs, key formulas.
   - `实验`: experiment questions, baseline descriptions, evaluation set/protocol, main results, important ablations, what the results do and do not prove.
   - `思考`: reusable ideas, doubts/limitations, and possible follow-up experiments, usually grouped in a few `💡` / `‼️` / `🧪` callouts.
4. Search the existing `PaperReading` page for 3-8 important related works and use normal Markdown links to Notion pages. Link only pages that are children of `实验室工作 / PaperReading`. Do **not** use `<page>` tags in generated content; they may be escaped incorrectly.
5. Create the page under `实验室工作 / PaperReading` without a page cover/background.
6. Backlink maintenance: after creating or updating a page, update only backlink/reference lines in the related existing PaperReading pages that should mention this page. Fetch each target page first, insert only the missing link in the closest related-work/reference sentence or a minimal related-work line, and leave every other character unchanged.
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
6. When maintaining backlinks, update only the link/reference text in existing PaperReading pages and leave everything else unchanged.

## References

- `references/first-principles-prompt.md`: the user's coarse-reading analysis prompt.
- `references/notion-style.md`: page style, formulas/tables/images, and related-work linking rules.
- `scripts/prepare_notion_figures.py`: render/crop local PNGs from paper PDFs.
- `scripts/upload_notion_images.py`: upload local images to Notion with the File Upload API and append image blocks.
