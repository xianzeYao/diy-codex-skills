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

Optionally add a very short `Paper Compass` callout near the top, after metadata and before `现况与动机`. It should be 4-5 lines at most:

```markdown
<callout icon="🧭" color="gray_bg">
这篇的重点不是 ___，而是 ___。
它反对的旧假设是：___。
核心 claim：如果 ___，那么 ___，因为 ___。
最关键证据是：___。
我应该带走的是：___。
</callout>
```

Keep it lightweight. Do not create a large standalone section unless the user asks. If精读 later changes the main interpretation, update this compass.

## Mapping From Analysis To Notion

- Paper Compass → short top callout or first compact paragraph.
- Task → `方法`, usually under `Task` or folded into one-sentence mechanism.
- Motivation / Challenge → `现况与动机`.
- Insight + Novelty → `方法`, as concise mechanism explanation.
- Potential Flaw → `思考`, usually in a `‼️` callout.
- Judge / Debate → `思考`, especially `‼️` callouts for weakened claims, alternative explanations, unfair baselines, missing ablations, or claims that need精读 confirmation.
- Revised Takeaway → final framing across `现况与动机`, `方法`, `实验`, and especially `思考`; do not write the Notion page by simply following the author's narrative if the debate lowered confidence.
- Future Direction / Realization → `思考`, usually in a `🧪` callout.
- User's reusable idea → `思考`, usually in a `💡` callout.
- Use callout emoji sparingly in `思考` when it improves scanability. Do not use emoji page icons.
- Match the stronger existing Point What You Mean style for `思考`: a few compact callouts, each with concrete numbered points. `💡` should capture reusable conceptual insights, `‼️` should name real risks/limitations/fairness issues, and `🧪` should propose experiments that can actually test a claim. Avoid vague "值得关注" comments.
- Do not set Notion page covers/backgrounds unless the user explicitly asks.
- Balance factual reconstruction and critique. The page should contain enough concrete paper content—task/interface, mechanism, dataset, baselines, metrics, ablations, and numbers—before giving judgments. If the content reads mostly like opinions, add more paper-grounded description first.
- Keep method and experiment roles separate. Method sections should explain interfaces, information flow, training/inference procedure, and design tradeoffs. Result-like material—benchmark tables, timing/memory measurements, success rates, ablation numbers, or deployment cost evidence—belongs in `实验`, even if it evaluates one method component.

## Formulas

Use native Notion inline equation rich-text objects for short variables and expressions whenever the API/tooling supports them. Do not leave Markdown `$...$`, backticked pseudo-LaTeX, or escaped LaTeX as plain paragraph text in an API-created page.

Short inline examples:

```markdown
标准 VLA 是 [inline equation: \hat{a}_t = \pi_\theta(l_t, I_t)]。
```

Use display-style formulas only when multi-line or central to the method. Do not isolate every short equation as its own paragraph.

If a formula is reconstructed because the paper describes an interface but does not print an official equation, label it as `按论文描述重构，不是论文原式`. Do not invent unspecified coordinate conventions, losses, or variable semantics. Keep prompt/schema fields such as `TASK`, `PLAN`, `MOVE`, `GRIPPER`, and `VISIBLE_OBJECTS` as plain field names, not math.

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

Do not put experiment-style tables or measured results in `现况与动机` or `方法`. If a section mixes design and measurement, split it: keep the design explanation in `方法`, and move the measurement/cost evidence to an experiment subsection such as `推理成本`, `效率`, or `Ablation`.

## Images

Prefer:

1. Project page images that Notion can embed reliably.
2. Paper/arXiv figures if extractable.
3. Figure captions and links if images cannot be embedded.

Not every paper has a project page. For papers without stable image URLs, screenshots/crops are useful, but the insertion route matters. Do not insert local filesystem image paths such as `/tmp/foo.png` into Notion through the connector; the connector strips them and leaves broken image blocks.

Fallback workflow for missing figure URLs:

1. Render/crop figures from the PDF with `scripts/prepare_notion_figures.py`.
2. Upload the generated PNGs with `scripts/upload_notion_images.py --page-id <page-id> --after-text "<nearby sentence or heading>" <image.png> --caption "..." --cleanup`, or use `--after-block-id <block-id>` when the anchor block is already known. This uses Notion's File Upload API, stores the binary in Notion-managed storage, inserts the image near the relevant text, and removes temporary local screenshots after success.
3. Do not create hosted-image or Computer Use paste workarounds. If File Upload API is unavailable or the integration lacks page access, keep a caption/link instead of inserting a broken image.

Golden rule: images must呼应 and help the surrounding正文. Do not insert images for decoration, completeness, or page richness. Each image should make a nearby explanation easier to understand, inspect, or question.

Do not use decorative or unrelated images. Every image should anchor a method, data, or experiment point.

Crop quality standard:

1. Default to the original paper figure/table plus its caption.
2. Include surrounding prose only when the prose is intentionally discussed and the crop starts/ends at paragraph boundaries.
3. Reject half-sentence fragments, clipped captions, missing top/bottom rules, cut-off rows/columns, neighboring asset edges, page numbers, unrelated footnotes, or residual column text.
4. Run Screenshot QA before upload; failed crops must be redone and excluded from the final upload manifest.
5. Long appendix prompt pages are optional. Include them only if they remain readable in Notion and can be split at natural headings/logical boundaries; otherwise summarize the prompt schema in text.

Captions should be plain descriptive names. Avoid mechanical prefixes such as `Figure 1.`, `Fig.`, `Table`, or `Table/Figure`; Notion already renders the block as an image/table. Use `TraceVLA overview: original image + trace image + language instruction -> action tokens`, not `Figure 1. TraceVLA overview...`.

Place images where they are used, not in a bottom dump:

- Teaser/problem figures belong in `现况与动机`, immediately after the paragraph that states the bottleneck.
- Architecture, pipeline, data-construction, or loss diagrams belong in `方法`, close to the mechanism they explain.
- Benchmark screenshots, task grids, result plots, and ablation figures belong in `实验`, next to the setting/result interpretation.
- A separate `图表摘录` section is only acceptable as temporary staging while uploading/cropping; the final Notion page should usually remove it and distribute the images into context.

If using Notion File Upload API for local screenshots, insert after a real paragraph/heading/table anchor with `--after-text` or `--after-block-id`. Appending to the page root is only acceptable as temporary staging and must be cleaned before final self-check.

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

For backlinks from existing PaperReading pages, first look for an existing mention of the new paper, acronym, method name, or route. If the mention is already present, link that phrase only and leave the rest of the sentence unchanged:

```markdown
TraceVLA 这类 visual trace 方法...
```

becomes:

```markdown
[TraceVLA](https://www.notion.so/...) 这类 visual trace 方法...
```

Do not append generic tail lines such as `相关：TraceVLA...` by default. Add a new related-work sentence only when no natural mention exists and the backlink is worth adding as content, not just as navigation.

## Update Rules

When updating existing pages:

- Fetch first.
- Preserve user-written notes and callouts.
- Merge into the closest section.
- Do not delete critical comments unless asked.
- Treat user's interactive精读 conclusions as more authoritative than the initial Codex coarse draft.
- When adding backlinks to related existing PaperReading pages, fetch the target page first and edit only the smallest link/reference text needed. Prefer turning an existing mention into a link. Do not rewrite, reformat, append generic tail links, or otherwise clean up those existing pages.
- When backlinks are changed, report them in the conversation: page title, exact sentence/snippet, and the phrase that became a link. If no natural mention existed and no backlink was added, say that explicitly.
