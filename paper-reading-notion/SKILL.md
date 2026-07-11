---
name: "paper-reading-notion"
description: "Use when the user is reading a paper from PDF/arXiv/Zotero/project/title, creating or updating a Notion PaperReading note, doing paragraph-level 精读, backfilling reading thoughts, or testing paper understanding."
metadata:
  short-description: "Create/update Notion PaperReading notes from papers"
---

# Paper Reading Notion

Create and maintain the user's Notion `实验室工作 / PaperReading` pages, while also supporting the full interactive reading loop in chat. New paper pages should be figure/table-rich by default: use the paper's own screenshots, figures, tables, or project-page assets to explain the argument visually, while keeping the user's existing light template unchanged.

Use this skill for four modes:

- **Coarse-read mode**: user gives a PDF path, Zotero PDF path, arXiv link, project page, or paper title and asks to read/analyze it. Output the first-principles coarse analysis in chat first when requested, then create/update the Notion page.
- **Interactive精读 mode**: user pastes paper paragraphs in the same thread. Translate paragraph by paragraph and add brief analysis after each paragraph.
- **Update/backfill mode**: user gives refined thoughts,精读 discussion, translated paragraphs, critiques, or experiments and asks to merge them into an existing PaperReading page.
- **Test mode**: user asks to be tested on the paper. Generate understanding questions and later assess the user's answers.

The goal is not to replace the user's精读. Codex should keep the reading context, do the mechanical and structural work, build a good Notion draft, and preserve the user's own judgments as they emerge during discussion.

## Agent Workflow for Paper Pages

When creating a new PaperReading page or substantially rewriting an existing one, use five passes. **Each pass must be run as an independent subagent whenever subagent tooling is available.** The main thread may coordinate, crop, upload, and integrate, but it must not silently replace an independent pass with its own self-check. If a required subagent cannot be spawned because tools are unavailable, blocked, or at thread limits, state that explicitly before proceeding and report it in the final response.

Required independent subagents:

1. **Reading/Writing Agent**: read the paper, run the first-principles analysis, decide the page framing, and draft the Notion content in the required template.
2. **Debate Agent**: attack the Reading/Writing Agent's draft before Notion writing. Treat the `方法` section as a core attack target, not a formality. Check whether the method explanation reconstructs the actual data flow, modules, training/inference differences, losses, equations, and design rationale from the paper; flag vague architecture summaries, missing formulas, missing variables, unclear implementation assumptions, unsupported reconstructed formulas, and schema fields incorrectly written as math. Also check whether the motivation follows from related work and the introduction, whether experiment interpretation overclaims, and whether the user's possible research angle is preserved. The Reading/Writing Agent must revise after this critique.
3. **Figure/Table Inspection Agent**: inspect the selected PDF first, then project page/arXiv HTML for useful figures, screenshots, tables, qualitative examples, architecture diagrams, result tables, and ablation tables. Select assets that actively support nearby text; for each selected asset, record its PDF path or URL, page number, crop/screenshot source, why it matters, target section, proposed caption, and anchor sentence. Reject decorative or redundant assets, but do not skip setup, ablation, scaling, benchmark, or real-world tables, including early tables such as Table 1/2 when they carry the paper's core evidence.
4. **Screenshot QA Agent**: inspect every cropped/screenshot PNG before upload and reject weak crops. Verify the crop is from the original PDF or official page rendering, includes the full table/figure and caption when useful, has safe margins on all four sides, preserves the header/top rule, last row/bottom rule, left labels, rightmost columns, legends, footnotes/table notes, metric definitions, and caption text, is readable at Notion width, and is placed near text that discusses it. Prefer a slightly wider crop with surrounding whitespace over any crop that risks clipping content. Do not crop so tightly that the asset loses the author's caption, task/baseline names, explanatory context, or the paper's own analysis around the figure/table. If important content is within roughly 20 px of an edge, or if a table/figure edge is uncertain, recrop with larger margins and inspect again. Bad crops must be redone; do not upload a first crop blindly. Multiple Screenshot QA rounds are acceptable and expected when crops fail; only QA-passed assets may enter the final upload manifest.
5. **Review/Format Agent**: fetch or inspect the final draft/page, verify the template, section order, evidence labels, image/table placement, captions, formulas, tables, author limitations, local PDF path, and critical `思考` callouts. The review agent must identify concrete fixes rather than approving vaguely.

The Reading/Writing Agent owns the final integrated page, but it must revise against the Debate Agent, incorporate the Figure/Table Inspection Agent's useful selections, address Screenshot QA fixes, and resolve the Review/Format Agent's blocking issues before finalizing. The final response must list which five subagents ran. Do not claim the full workflow ran if any pass was performed only by the main thread.

## Quality Bar From User Feedback

When multiple papers need to be written or rewritten, process them **one paper at a time**. Do not bulk-generate shallow pages from a shared template and then upload all pages at once. For each paper, complete the full five-pass agent workflow, inspect the final page, and only then move to the next paper. If the user asks to batch many papers, batching is only for queue management; the actual read/write/review loop remains per-paper.

For screenshots, the target is the user's restored ERVLA-style page quality: complete figure/table crops that remain readable and meaningful in Notion. Do not interpret Screenshot QA as "crop as tightly as possible." A good crop usually includes the full figure or table, caption, important legend/table footnotes, table title, top/bottom rules, and enough surrounding paper context to understand what the asset is showing. Avoid slicing a paper figure/table into tiny fragments unless the paper itself has independent subfigures/tables and the nearby text discusses them separately.

If a crop looks visually clean but loses context, caption, baseline names, task names, metric definitions, table notes, or the author's own analysis, reject it. Prefer a slightly larger, ERVLA-style crop over a short crop that forces the Notion text to reconstruct missing context. The Review/Format Agent must specifically check for "too-short crops" and compare representative crops against this standard.

The default crop unit is the original paper figure/table plus its caption. Include surrounding author prose only when it is intentionally needed and the crop starts and ends at paragraph boundaries. Reject crops with half sentences, neighboring figure/table edges, page numbers, unrelated footnotes, residual column text, clipped captions, or clipped aggregate/table rules. Long appendix prompt pages are optional: include them only when central and readable, split only at natural headings/logical boundaries, and otherwise summarize the prompt schema in text instead of uploading unreadable prompt screenshots.

## Chat Reading Workflow

When the user starts a paper with this skill, keep the paper context active in the thread.

### First pass: coarse read

1. Read the paper and run `references/first-principles-prompt.md`.
2. If the user asks for output, produce a chat analysis following `references/first-principles-prompt.md` directly, including its section structure and evidence labels:
   - `Paper Compass`
   - `Task`
   - `Motivation / Challenge`
   - `Insight`
   - `Novelty`
   - `Potential Flaw & Future Direction`
   - `Judge / Debate`
   - `Revised Takeaway`
   - optional `Realization` only when useful or requested
3. Mark key claims as `【论文内容】`, `【我的推断】`, or `【不足以判断】`.
4. Enforce the order strictly: when the user asks for coarse-read output in chat, finish the chat analysis first, then create/update Notion. Do not create/update Notion first and defer the coarse-read report to the final response.
5. After the chat analysis, create or update the Notion page using the light Notion structure below. Do not paste the full coarse-read report into Notion unless the user explicitly asks.
6. When writing Notion, include a very short Paper Compass near the top as a callout or compact paragraph. It should help the user know what to watch for, not add a heavy new section.
7. When writing Notion, use `Judge / Debate` and `Revised Takeaway` to decide the final framing. The page should not simply reproduce the author's narrative; it should reflect which claims are well-supported, weakened, or still uncertain.

### Interactive精读

When the user pastes original paper paragraphs after the first pass:

1. Translate paragraph by paragraph.
2. After each paragraph, add 1-2 short explanations:
   - `【本文角度】` what role this paragraph plays in the paper's logic.
   - `【结合前文分析】` which part it maps to: Task / Challenge / Insight / Novelty / Potential flaw / Experiment.
3. If a paragraph is transition, experiment organization, or contains no important new information, say so directly and do not over-interpret.
4. Keep the user's paper-level context in mind; update earlier coarse judgments when精读 contradicts them.

### Backfill during精读

When the user says "写进 Notion", "回填", "更新这部分", or similar:

1. Fetch the existing Notion page.
2. Update only the closest relevant section.
3. Preserve the user's wording when it carries their judgment or口语化 style. Lightly clean grammar, but do not turn their voice into generic academic prose.
4. If the user's精读 contradicts the coarse draft, treat the精读 as higher priority and revise the draft.
5. Report what section changed. If any backlink is changed, report the page title, sentence/snippet, and linked phrase.

### Test

When the user asks "测试我":

1. Ask 5-8 questions.
2. Start with overall understanding, then details, then transfer/generalization.
3. Cover motivation, insight, novelty, experiment evidence, and flaw/future direction.
4. For each question, state what ability it tests.
5. After the user answers, judge whether they really understood and point out inaccurate or shallow parts.

## Required Style

Top-level Notion structure should stay light:

```markdown
> 作者：
> 机构：
> 链接：
> 投稿 / 时间：

# 现况与动机
# 方法
# 实验
# 思考
```

Only add lower-level subsections when useful. Do not turn the page into a rigid report with many mandatory headings.

Prefer the user's style:

- Explain mechanisms and problem structure, not only summaries.
- Keep enough descriptive evidence before critique. A good page should first make the paper's task, mechanism, experiment setup, and concrete numbers clear; then add critical judgment. Do not make the page mostly opinions.
- Keep formulas and variables when they clarify interfaces. Formulas must be readable in the final Notion page: use native Notion equation blocks for display equations and native Notion inline equation rich-text objects for inline variables. Do not write inline formulas as plain text, Markdown `$...$`, backticked pseudo-LaTeX, or escaped strings. Split long paper formulas into short display equations plus variable definitions. In ordinary paragraphs and bullets, inline variables such as `H_{vlm}`, `K^{vlm}_{\ell}`, `a_{score}`, or `p_{cot}` should be inserted as Notion inline equations when the API/tooling supports them; use prose only when an inline equation is unnecessary. Do not leave long malformed inline LaTeX, escaped Markdown, pseudo-formulas inside ordinary paragraphs, or single-line equations that overflow the Notion page. If the paper does not provide an explicit formula/loss but a compact formula clarifies the interface, label it clearly as `按论文描述重构，不是论文原式`; do not invent unspecified coordinate conventions, losses, or variables. Keep schema fields, prompt fields, and text labels such as `TASK`, `PLAN`, `MOVE`, `GRIPPER`, or `VISIBLE_OBJECTS` as plain field names, not inline equations.
- Author and institution metadata must preserve affiliation markers. If the paper uses superscripts, write authors with superscript numbers and list numbered institutions so the reader can map each author to an institution.
- Author footnote markers and symbol explanations such as `†Project Leader` or `⋆Corresponding Author` belong on the author line, not the venue/time line.
- Keep paper metadata compact at the top in one quote block. Put authors, institutions, links, and venue/time together in that single quote block; use line breaks inside the quote when needed, but do not split them into separate quote blocks and do not use a callout unless the user asks. Do not put the local PDF path in the Notion metadata unless the user asks; always include the resolved local PDF path in the chat final response so the user can check the source file.
- Venue/status extraction must not rely only on the PDF title page or arXiv abstract page. For arXiv papers, actively check project pages, OpenReview, conference/proceedings pages, author pages, Zotero metadata, and any existing user note when available. If the PDF/arXiv says only preprint but another credible source or the user's source note indicates acceptance, write the accepted venue first and keep arXiv submission/revision dates as version history, e.g. `投稿 / 状态：CoRL；arXiv v1 submitted ...；v3 revised ...`. If venue evidence conflicts, state the conflict instead of silently downgrading to `arXiv preprint`.
- Golden rule for images and tables: every asset must呼应 and help the surrounding正文. Insert a figure/table only when the nearby paragraph uses it to explain a bottleneck, mechanism, setup, result, ablation, or limitation. Do not insert assets just to make the page look richer.
- Use paper figures/tables/project-page images as anchors in the section where they are discussed. Do not collect figures or tables at the bottom as a generic `图表摘录` section unless it is a temporary staging area that will be cleaned up.
- Preserve a critical voice in `思考`, matching the user's template page: exactly three actual Notion callout blocks with gray background. Use `💡` for reusable insight, `❓` for questions/risks/limitations, and `🔬` for testable follow-up experiments. Each callout must contain numbered points inside the block (`1.`, `2.`, `3.` as needed), not unstructured prose. Do not use plain quote blocks or emoji page icons.
- Do not set a Notion page cover/background unless the user explicitly asks.
- Link related notes only when they are existing pages under `实验室工作 / PaperReading`; do not link notes found elsewhere in Notion.
- For experiments, always name the baselines, explain what each baseline represents, describe the evaluation setting/protocol, then interpret the main result and ablations. Avoid result tables without context.
- When an experiment mentions baseline methods, ablation variants, datasets, action representations, or evaluation settings that have not been clearly explained earlier, briefly explain them in the experiment section before interpreting numbers. Do not assume names like `FAST`, `No Choice`, `Knowledge Insulation`, `No Knowledge Truncation`, `π0.5`, or paper-specific variant names are self-explanatory.
- Keep method and experiment roles separate. `方法` explains what the paper does and why the design might work; result tables, timing/memory numbers, benchmark metrics, and deployment-cost evidence belong in `实验`, even when they discuss a method component.
- Image captions should be plain descriptive names. Do not prefix captions with `Figure`, `Fig.`, `Table`, `Table/Figure`, or numbering unless the number is needed to disambiguate a paper-specific reference.
- `TLDR` should be short and decisive: 1-3 compact paragraphs, no long report, no full experiment dump.
- `现况与动机` must use the paper introduction and related work to explain why prior work is insufficient. Name the relevant previous approaches when useful, state their assumptions or bottlenecks, and then derive the paper's motivation from those gaps.
- `方法` should be explained by unfolding the main method/architecture figure whenever available. Follow the figure's blocks, arrows, and numbered components in order, and use the surrounding text plus equations to explain what each block consumes, produces, supervises, and passes to the next block. Cover the important data flow, modules, losses/objectives, formulas, variable meanings, inference/training differences, and design rationale. Reconstruct the method from the paper's equations when equations exist; do not omit or paraphrase away formulas that define the model, loss, cache conditioning, action generation, or selection mechanism. Put each important equation in its own readable block and immediately explain every non-obvious variable in prose. Mark unclear parts as `【不足以判断】` instead of smoothing them over.
- `实验` must cover each important experiment, including result-table screenshots and key figures. For every experiment: explain the question, setting, baselines, metric, main result, author's interpretation, and your own analysis of what is and is not proven. Prefer screenshots/crops of paper tables over recreated Notion tables.
- Experiment subsection titles must be scientific questions or experiment names, not asset labels. Do not title sections as `Table 1`, `Figure 5`, `Table 14 / Figure 6`, etc. Mention paper table/figure numbers only inside the paragraph or caption when needed.
- Each experiment subsection should be detailed enough to stand alone: state the question being tested, evaluation setting/protocol, compared variants and what each variant means, metrics, main numbers, author interpretation, your analysis, and what the result does and does not prove. Do not collapse multiple ablations, scaling trends, and benchmarks into one short result dump.
- `思考` must consider limitations the authors state themselves, then add the user's/agent's own critique or follow-up only after separating it from the author-stated limitation.

## Create Mode Workflow

Use create mode by default when the user says "写 Notion", "新建", "创建页面", or asks to write a new paper note from a paper source. If an existing page with the same title is found, do not update it automatically unless the user explicitly asks to update/merge/overwrite it, or unless the request is clearly a backfill/refinement of that existing page. When both a duplicate and a create request are present, create a new page and mention the duplicate in the final response.

1. Resolve and read the input paper.
   - If the user gives a title, arXiv/project URL, or paper acronym and does not give a PDF path, first search local Zotero storage (`~/Zotero/storage/**`) for likely matching PDF filenames or metadata before downloading or relying on HTML. Prefer the Zotero PDF when it is complete and readable.
   - Validate the selected PDF before using it: check file size, page count, and that `startxref` / `%%EOF` exist or that `pdfinfo`/rendering succeeds. If a work-directory copy is broken but a Zotero PDF exists, switch to the Zotero PDF and report that source path.
   - For local PDFs, extract text page by page.
   - If available, find project page/arXiv/GitHub and stable image assets, but do not assume every paper has a project page.
   - Prefer original paper/project figures and table screenshots over generic images. A new PaperReading page should normally include relevant figures and result/ablation table screenshots unless the paper has no accessible visual assets or the Notion/API path is blocked.
   - Table image priority is strict: first crop the original PDF page/table; second screenshot the paper's official HTML/project-page rendering; third use an existing project-page table image; last resort recreate the table from extracted values. If the last resort is used, explicitly mark it as a recreated table image, not an original screenshot.
   - Do not stop at headline benchmark tables. Inspect the full paper and appendix table list, then include every table that is important to the argument: field ablations, data scaling, component ablations, benchmark comparisons, real-world results, and task-suite tables when the surrounding text depends on them.
   - If no stable figure URL exists, render/crop screenshots into local PNGs. The Notion connector cannot embed local paths.
   - Upload local images with Notion's File Upload API via `scripts/upload_notion_images.py`, targeting the relevant page/block so the image appears near the paragraph/table it explains. This requires `NOTION_TOKEN` or `NOTION_API_KEY` with access to the target page or block. Use `--after-block-id` when the target anchor block ID is known, or `--after-text` to locate the first matching paragraph/heading and insert after it. Use `--cleanup` for temporary screenshots after successful upload.
   - Use `scripts/prepare_notion_figures.py` to render/crop PNGs and generate a local manifest before upload.
   - Do not create hosted-image or Computer Use paste workarounds. If File Upload API is unavailable, keep the figure caption/link and mention that the image was not inserted.
2. Run the Reading/Writing Agent internally using `references/first-principles-prompt.md`.
   - Do not paste the full prompt structure into Notion.
   - Map it into the light Notion template.
   - Keep `TLDR` concise; put detailed evidence in `实验`, not in TLDR.
3. Run the Debate Agent against the Reading/Writing Agent draft.
   - Force the debate to produce specific rewrite requests, not generic criticism.
   - The Reading/Writing Agent must revise the page plan after the debate, especially when motivation, method details, or experiment claims are weak.
4. Run the Figure/Table Inspection Agent before final page creation/update.
   - Inspect paper figures/tables and project-page images, not only the text.
   - Choose the minimum useful set that makes the page图文并茂 and table-aware, usually including the main method figure plus the important result/ablation/scaling/benchmark/real-world table screenshots unless unavailable.
   - For each selected asset, specify: source PDF path or URL, PDF page number when applicable, target section, nearby anchor text, caption, and the claim/mechanism/evidence it supports.
   - Do not select assets whose only purpose is decoration, visual richness, or generic overview when the text does not use them.
5. Run Screenshot QA before upload. Open or inspect generated PNGs at the actual files that will be uploaded. Redo crops that miss captions, truncate rows/columns, have labels or rules too close to an edge, include too much unrelated text, are unreadable, or are from a recreated table when a PDF crop was available. When in doubt, widen the crop and include whitespace/caption rather than risking missing content. After upload, fetch/inspect the page structure and verify every image block is present near the intended anchor.
6. Build the Notion page:
   - Metadata block.
   - `TLDR`: 1-3 compact paragraphs with the thesis, strongest evidence, and bottom-line judgment.
   - `现况与动机`: problem, prior routes, related-work shortcomings, why old interfaces fail, and why this paper's question follows naturally.
   - `方法`: task/interface, data flow, architecture/main figure explanation, key designs, losses/objectives, training/inference differences, and key formulas with variable explanations. Use the main method figure as the spine: explain each labeled module/arrow in figure order before abstracting. Before finalizing this section, run the Debate Agent's method attack: ask what is still too high-level, which figure block or arrow is unexplained, which equation is missing, which variable is undefined, which design choice is asserted but not explained, what formula is reconstructed rather than original, whether schema fields are being mistaken for math variables, and what training/inference mismatch remains unclear. Do not omit formulas when the paper uses them to define the model, loss, or inference path. Do not put benchmark tables, timing numbers, memory results, or result-style cost analysis here.
   - `实验`: experiment-question titles, baseline descriptions, evaluation set/protocol, screenshots of main result tables/figures, main results, important ablations, author's interpretation, your analysis, and what the results do and do not prove. Include enough factual setup before critique. If a method, baseline, variant, dataset, or action representation appears only in the experiment table and has not been explained clearly, explain it locally before discussing its score. Do not use table/figure labels as subsection headings. Do not recreate result tables as Notion tables unless screenshots are unavailable and the limitation is reported.
   - `思考`: exactly three compact Notion callouts in the template style, not plain quote blocks: reusable insight (`💡`), questions/risks/limitations (`❓`), and testable follow-up experiments (`🔬`). Use gray background. Inside each callout, write numbered points (`1.`, `2.`, `3.` as needed). Include author-stated limitations first when available, then add Debate/Revised Takeaway critique for claims that should be weakened, alternative explanations, and follow-up checks. Keep each point tied to a mechanism, evidence gap, or experiment design.
   - Place each figure/table in context: teaser/problem figures in `现况与动机`, architecture/pipeline figures in `方法`, benchmark/result/ablation figures and tables in `实验`, and only leave a separate figure/table list if the user explicitly asks. For local PDF crops, insert through `scripts/upload_notion_images.py --after-text "<nearby sentence>"` or `--after-block-id <anchor-block-id>`; do not append all uploaded assets to the page root.
7. Search the existing `PaperReading` page for 3-8 important related works and use normal Markdown links to Notion pages. Link only pages that are children of `实验室工作 / PaperReading`. Do **not** use `<page>` tags in generated content; they may be escaped incorrectly.
8. Create the page under `实验室工作 / PaperReading` without a page cover/background.
9. Backlink maintenance: after creating or updating a page, inspect related existing PaperReading pages for natural mentions of the new paper/method. If a page already mentions the paper title, acronym, or method name, convert only that existing phrase into a normal Markdown link and keep the sentence text unchanged. Do not append generic tail lines by default. Append a minimal related-work sentence only when there is no natural mention and the backlink is genuinely useful. In the final response, report every backlink edit with page title, the sentence/snippet touched, and the phrase that was linked.
10. Run the Review/Format Agent and the post-write self-check below. Do not claim the Notion page is complete until both pass or until unresolved failures are explicitly reported.
11. Final response should include the Notion page URL, the resolved local PDF path, which agent passes ran, and a short note about any limitations, e.g. PDF figures/tables could not be extracted or Notion File Upload API was unavailable.

## Update Mode Workflow

Use update mode only when the user asks to update, merge, overwrite, backfill, 回填, 写进已有页面, or provides 精读/refined thoughts that clearly belong to an existing PaperReading page.

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
7. Run the post-write self-check below. Do not claim the Notion page is complete until it passes or until unresolved failures are explicitly reported.

## Post-Write Self-Check

After every Notion create/update, fetch the page and inspect the actual rendered block structure before finalizing.

Required checks:

1. **Structure**: top-level sections are light and ordered (`现况与动机`, `方法`, `实验`, `思考`); no accidental duplicate captions, duplicate paragraphs, or leftover staging sections.
2. **Formulas**: formulas are readable as Notion equations or equation rich text when possible, with one major equation per block and variable explanations nearby. Reconstructed formulas are explicitly labeled as reconstructed from the paper description, not original paper equations. Schema/prompt fields remain plain field names, not malformed math. If the connector cannot create equation blocks, use labeled code blocks; avoid malformed inline LaTeX and report the limitation.
3. **TLDR**: short and decisive; detailed method and experiment evidence lives in later sections.
4. **Motivation**: `现况与动机` uses introduction/related work to name prior approaches and their insufficiencies before introducing this paper's motivation.
5. **Method**: `方法` explains the main architecture/figure and does not hide unclear details; uncertain claims are marked `【不足以判断】`.
6. **Images and tables**: a new full PaperReading page includes relevant paper/project visuals and important result/ablation table screenshots by default, unless inaccessible or explicitly unnecessary. No temporary signed URLs, broken media, local filesystem paths, or recreated Notion result tables may appear in the page unless screenshots were impossible and the limitation is reported. Uploaded Notion file URLs may appear as signed URLs in fetched output, but they must be actual Notion file/image blocks, not pasted markdown links.
7. **Image/table placement**: every figure/table must be near the paragraph that discusses it and must have a plain descriptive caption. Do not leave a pile of assets at the end unless it is explicitly marked as a temporary staging area and reported as not final.
8. **Experiments**: each important experiment includes the question, setting, baselines/variants with local explanations, metrics, result asset, author's analysis, and the agent's own analysis of what is and is not proven.
9. **Tables**: every table must carry comparison or evidence that is used by the surrounding text. Remove or rewrite decorative/result-dump tables.
10. **PDF source**: final chat response includes the exact local PDF path used. The Notion page itself should keep metadata compact and omit the local PDF path unless the user requested otherwise.
11. **Screenshot QA**: cropped PNGs were visually checked after generation and the final page was checked after upload; no important table rows/columns/captions are clipped; crops have visible safety margins; Table 1/2-style setup evidence is not omitted when it is central to the argument. The final page uses only QA-passed assets from the final manifest; stale local screenshots or rejected crops are not uploaded or referenced. If long prompt screenshots were skipped because they were unreadable or fragmentary, the prompt schema is summarized in text and the limitation is reported.
12. **Thoughts**: `思考` must not be a plain opinion dump. It should contain exactly three actual Notion callout blocks with gray background, matching the template icons: `💡`, `❓`, and `🔬`. Each block should contain numbered points and tie to a mechanism, author-stated limitation, evidence gap, limitation, or concrete follow-up experiment.
13. **Debate revision**: the final page reflects the Debate Agent's strongest valid objections; unresolved objections are reported rather than hidden.

If any check fails, fix the page and fetch it again. If a tool/API limitation prevents a full fix, state the exact failed check and the reason in the final response.

## References

- `references/first-principles-prompt.md`: the user's coarse-reading analysis prompt.
- `references/notion-style.md`: page style, formulas/tables/images, and related-work linking rules.
- `scripts/prepare_notion_figures.py`: render/crop local PNGs from paper PDFs.
- `scripts/upload_notion_images.py`: upload local images to Notion with the File Upload API and insert image blocks after a target block/text anchor.
