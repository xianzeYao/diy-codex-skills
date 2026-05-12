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
- Potential Flaw → `思考`, written as explicit doubts or limitations.
- Future Direction / Realization → `思考`, written as possible follow-up directions.
- User's reusable idea → `思考`, written as reusable insights.
- Do not use emoji headings, emoji callouts, or emoji page icons unless the user explicitly asks.

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

## Images

Prefer:

1. Project page images with stable public URLs.
2. Paper/arXiv figures if extractable.
3. Figure captions and links if images cannot be embedded.

Not every paper has a project page. For papers without stable public image URLs, screenshots/crops are useful only if they can be uploaded or hosted as Notion-visible assets. Do not insert local filesystem image paths such as `/tmp/foo.png` into Notion; the connector strips them and leaves broken image blocks.

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
