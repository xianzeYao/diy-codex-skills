# Notion PaperReading Style Rules

## Page Shape

Use this light outer structure:

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

Do not add many mandatory headings. Add local headings only if they make the page easier to scan.

## Mapping From Analysis To Notion

- Task → `方法`, usually under `Task` or folded into one-sentence mechanism.
- Motivation / Challenge → `现况与动机`.
- Insight + Novelty → `方法`, as concise mechanism explanation.
- Potential Flaw → `思考`, usually in a `‼️` callout.
- Future Direction / Realization → `思考`, usually in a `🧪` callout.
- User's reusable idea → `思考`, usually in a `💡` callout.
- Use callout emoji sparingly in `思考` when it improves scanability. Do not use emoji page icons.
- Do not set Notion page covers/backgrounds unless the user explicitly asks.
- Balance factual reconstruction and critique. The page should contain enough concrete paper content—task/interface, mechanism, dataset, baselines, metrics, ablations, and numbers—before giving judgments. If the content reads mostly like opinions, add more paper-grounded description first.

## Formulas

Use inline formulas when they are short:

```markdown
标准 VLA 是 $`\hat{a}_t = \pi_\theta(l_t, I_t)`$。
```

Use display-style formulas only when multi-line or central to the method. Do not isolate every short equation as its own paragraph.

## Tables

For Notion tables, use explicit HTML tables or Notion-compatible tables without markdown separator rows. Avoid emitting markdown separator rows like:

```markdown
|---|---:|
```

Those may become bogus rows in Notion.

## Experiments

The experiment section should not be just a score table. Include:

1. Baselines and what each baseline represents.
2. Evaluation settings/protocols: datasets, tasks, number of configurations/rollouts, metrics, and whether the setup is simulation or real robot.
3. Main result table with concrete numbers.
4. Ablations tied back to the method's core claim.
5. A short interpretation of what the evidence proves and what it does not prove.

Prefer critical analysis after the factual setup. A useful pattern is: `baseline/setting -> result -> why it supports the mechanism -> limitation of the evidence`.

## Images

Prefer:

1. Project page images that Notion can embed reliably.
2. Paper/arXiv figures if extractable.
3. Figure captions and links if images cannot be embedded.

Not every paper has a project page. For papers without stable image URLs, screenshots/crops are useful, but the insertion route matters. Do not insert local filesystem image paths such as `/tmp/foo.png` into Notion through the connector; the connector strips them and leaves broken image blocks.

Fallback workflow for missing figure URLs:

1. Render/crop figures from the PDF with `scripts/prepare_notion_figures.py`.
2. Upload the generated PNGs with `scripts/upload_notion_images.py --page-id <page-id> <image.png> --caption "..." --cleanup`. This uses Notion's File Upload API, stores the binary in Notion-managed storage, appends an image block, and removes temporary local screenshots after success.
3. Do not create hosted-image or Computer Use paste workarounds. If File Upload API is unavailable or the integration lacks page access, keep a caption/link instead of inserting a broken image.

Do not use decorative or unrelated images. Every image should anchor a method, data, or experiment point.

## Related Work Linking

Search within `实验室工作 / PaperReading` for important related papers. Link only 3-8 high-value matches that are actual children of the PaperReading page. Do not link random Notion pages, external notes, or pages found outside PaperReading unless the user explicitly asks.

Use normal Markdown links:

```markdown
[MOKA](https://www.notion.so/...)
```

Do not use `<page>` tags in generated page content; the Notion connector may escape them into broken text.

Prefer links in context, not a separate dump:

```markdown
Visual prompting 路线里可以和 [MOKA](...)、[RoboPoint](...) 一起看。
```

## Update Rules

When updating existing pages:

- Fetch first.
- Preserve user-written notes and callouts.
- Merge into the closest section.
- Do not delete critical comments unless asked.
- Treat user's精读/chatbox conclusions as more authoritative than initial Codex draft.
- When adding backlinks to related existing PaperReading pages, fetch the target page first and edit only the smallest link/reference text needed. Do not rewrite, reformat, or otherwise clean up those existing pages.
