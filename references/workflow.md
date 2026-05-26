# End-To-End Production Workflow

## A. Benchmark Learning

1. Collect public benchmark videos/accounts from the user.
2. Use `video-analyzer` for full transcript and scene extraction.
3. Use `Spider_XHS` for public Xiaohongshu note/comment data when needed.
4. Rank benchmark videos by relevance, not just popularity.
5. Extract one formula per benchmark video.

Learning report fields:

- video title/link,
- topic,
- hook,
- transcript structure,
- scene rhythm,
- title/cover method,
- emotional curve,
- comment feedback,
- reusable formula,
- unsuitable use cases.

## B. Formula Selection

Before writing the final script, propose formula candidates and stop for confirmation.

Formula card format:

```markdown
### 公式 A：反差钩子 + 正经科普
- 适合素材：
- 开头 3 秒：
- 文案结构：
- 剪辑规律：
- 为什么可能爆：
- 风险：
```

Do not combine several formula cards unless the user explicitly asks for a hybrid.

## C. Script Generation

After confirmation, generate:

- title options,
- cover text,
- oral script,
- second-by-second timeline,
- scene/shot table,
- subtitles/text overlays,
- asset checklist,
- fact-check checklist.

For Chinese tech/product videos, prefer:

- short direct sentences,
- concrete nouns and visual actions,
- verified claims,
- one clear audience question at the end.

Avoid:

- stiff phrases like “赋能用户生态”,
- fake meme language that real reporters would not say,
- overexplaining the formula in the final copy,
- copying benchmark wording.

## D. Editing Production

Create a config JSON for `scripts/build_editable_jianying_draft.py`.

Minimum tracks:

- `VideoTrack`: cut source clips by timestamp.
- `VoiceOver`: narration audio.
- `BGM`: background music.
- `Subtitles`: oral-script subtitles.
- `SceneTags`: small labels for quick comprehension.
- `InfoCards`: concept/fact cards.
- `VerifyCards`: uncertainty markers.

For macOS JianYing reliability:

- source media must be transcoded before import,
- all media must live inside draft folder,
- no external `/Downloads` or temporary paths in final draft JSON,
- validate the draft after creation.

## E. Final Delivery

Report:

- draft path,
- config path,
- output script path,
- validation result,
- missing assets to replace,
- whether the project is editable or rendered fallback.

If the draft fails to open, troubleshoot in this order:

1. confirm all material paths exist,
2. confirm all material paths are inside the draft folder,
3. transcode H.264/AAC again,
4. remove animations/effects,
5. make a one-video safe-import draft,
6. provide rendered MP4 fallback only as last resort.
