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
- Preserve critical voice in `💡`, `‼️`, and `🧪` callouts.
- Link related existing PaperReading notes when relevant.

## Create Mode Workflow

1. Read the input paper.
   - For local PDFs, extract text page by page.
   - If available, find project page/arXiv/GitHub and public image assets.
   - Prefer original paper/project figures over generic images.
2. Run the first-principles analysis internally using `references/first-principles-prompt.md`.
   - Do not paste the full prompt structure into Notion.
   - Map it into the light Notion template.
3. Build the Notion page:
   - Metadata block.
   - `现况与动机`: problem, prior routes, why old interfaces fail, related-work links.
   - `方法`: one-sentence mechanism, task/interface, key designs, key formulas.
   - `实验`: experiment questions, main results, important ablations, what the results do and do not prove.
   - `思考`: `💡` reusable ideas, `‼️` doubts/limitations, `🧪` possible follow-up experiments.
4. Search the existing `PaperReading` page for 3-8 important related works and use normal Markdown links to Notion pages. Do **not** use `<page>` tags in generated content; they may be escaped incorrectly.
5. Create the page under `实验室工作 / PaperReading`.
6. Final response should include the Notion page URL and a short note about any limitations, e.g. PDF figures could not be extracted and project-page images were used.

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

## References

- `references/first-principles-prompt.md`: the user's coarse-reading analysis prompt.
- `references/notion-style.md`: page style, formulas/tables/images, and related-work linking rules.
