---
name: viral-video-auto-producer
description: End-to-end reusable workflow for learning from public viral short videos, extracting reusable爆款公式, waiting for formula/structure confirmation, generating original Chinese scripts from user materials, and producing editable JianYing/CapCut drafts with internalized media assets. Use for AI机器人情报站、科技产品视频、小红书/B站/YouTube爆款学习、自动选题、口播稿、分镜、剪辑工程交付。
---

# Viral Video Auto Producer

Use this skill when the user wants the full short-video production pipeline:

1. learn from public viral videos/accounts,
2. extract reusable formulas instead of copying expressions,
3. receive new materials/news/product links,
4. propose formula + copy structure + editing pattern for confirmation,
5. generate original script and timeline,
6. create an editable JianYing draft or fallback assets,
7. deliver project paths and validation notes.

## Core Rules

- One video = one main爆款公式. Do not mix multiple formulas into a四不像.
- Before generating the final script, pause for user confirmation of: selected formula, copy structure, and editing rhythm.
- Learn transferable structure, not exact wording. Avoid copying creator names, unique phrasing, or identifiable sequence details.
- For current news, product claims, model availability, prices, laws, and API details, verify with current sources.
- For Xiaohongshu collection, prefer `Spider_XHS` if installed. For video extraction, use `video-analyzer` when available.
- For wording, use `de-ai-writing` / `prompt-master` style guidance when installed: natural, human, not stiff, not meme-for-meme.
- For editable JianYing drafts on macOS, internalize media files into the draft folder before saving. Never rely on external media paths.

## Workflow

### 1. Learning Phase

Use benchmark videos/accounts supplied by the user.

Extract for each selected viral video:

- full transcript/caption text,
- opening 3-second hook,
- script structure,
- editing rhythm,
- scene/shot pattern,
- title/cover strategy,
- emotional curve,
- audience comments or visible feedback when available,
- reusable formula and when not to use it.

Output a compact learning report and a formula library.

### 2. Formula Confirmation

Before script writing, give 2-5 formula candidates:

- formula name,
- why it fits the supplied materials,
- copy structure,
- editing rhythm,
- first 3 seconds,
- risks and missing assets.

Stop and ask the user to confirm one formula. Do not decide silently.

### 3. Material Intake and Topic Selection

Parse user materials into:

- source facts,
- strongest visual hooks,
- human-interest angles,
- tech/product angle,
- missing assets,
- claims requiring verification.

Pick the most interesting topic first, not the broadest coverage. Do not force all materials into one video.

### 4. Script Generation

After formula confirmation, generate:

- 3-5 natural titles,
- cover text suggestions,
- oral script,
- second-by-second timeline,
- editable shot list,
- text overlays,
- BGM/SFX notes,
- asset gap list,
- fact-check list.

Keep narration human and concrete. Avoid fake excitement and awkward phrasing.

### 5. Editable Draft Production

When making a JianYing draft, use the bundled script:

```bash
python <skill_root>/scripts/build_editable_jianying_draft.py --config project_config.json
```

The config schema and examples are in `templates/editable_draft_config.example.json`.

Draft safety requirements:

- transcode video to H.264/AAC MP4,
- transcode audio to AAC M4A,
- place all media inside `<draft>/materials/`,
- use separate editable tracks for video, voiceover, BGM, subtitles, labels, and info cards,
- patch macOS draft index files,
- validate that all media paths exist and are inside the draft folder.

### 6. Delivery

Return:

- editable draft path,
- generated script path,
- config path,
- meta/validation path,
- remaining asset gaps,
- if draft cannot open, provide a rendered MP4 fallback but clearly mark it as non-editable.

## Environment Quick Check

Run:

```bash
python <skill_root>/scripts/validate_environment.py
```

Read `references/environment.md` for required tools, optional APIs, and `.env` examples.

Read `references/github-publish.md` when the user asks how to upload this skill to GitHub.
