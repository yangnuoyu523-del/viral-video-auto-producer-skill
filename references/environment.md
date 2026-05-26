# Environment And API Setup

## Required Local Environment

- macOS or Windows with Python 3.9+.
- JianYing/CapCut desktop installed if you want editable draft output.
- `jianying-editor` skill installed.
- `JY_SKILL_ROOT` points to the installed `jianying-editor` skill directory.
- `imageio-ffmpeg` Python package. The build script uses it to locate ffmpeg.
- Source videos must be public, local, or user-provided.

Install Python dependencies if needed:

```bash
python3 -m pip install --user imageio-ffmpeg pymediainfo
```

If using the existing `jianying-editor` skill:

```bash
export JY_SKILL_ROOT="$HOME/.codex/skills/jianying-editor"
```

## Recommended Skills

- `video-analyzer`: extract transcripts and visual structure from B站/YouTube/local videos.
- `Spider_XHS`: collect public Xiaohongshu notes/account data.
- `de-ai-writing`: remove stiff AI tone from Chinese copy.
- `prompt-master`: improve prompt quality for script/video/image tools.
- `jianying-editor`: create editable JianYing drafts.

## Optional APIs

The workflow can run manually without a model API, but API access improves automation.

### Text/Reasoning Model

Use any strong LLM for analysis, formula selection, and script generation. For Doubao/Volcengine Ark users, store keys in `.env`:

```bash
ARK_API_KEY=your_ark_or_doubao_key
DOUBAO_API_KEY=your_ark_or_doubao_key
DOUBAO_TEXT_MODEL=Doubao-Seed-2.0-pro
```

Model IDs and endpoint names can change. Confirm the exact model ID in your provider console.

### Video Generation Model

Only needed if generating new video footage, not for editing existing footage:

```bash
DOUBAO_VIDEO_MODEL=Doubao-Seedance-1.5-pro
```

Keep video generation separate from editable draft assembly. Generated videos should first be downloaded locally, then passed into the draft builder.

### Web Crawling

For public web/video pages, normal browser or command-line access is enough.
For Xiaohongshu, use public-access data only and respect platform terms.

## macOS JianYing Notes

Newer macOS JianYing drafts may use encrypted project files. The safest editable workflow is:

1. create a pyJianYingDraft-compatible draft,
2. put all media inside the draft folder,
3. patch `draft_info.json`, `template-2.tmp`, `draft_settings`, and `root_meta_info.json`,
4. let JianYing convert the draft into its native format when opened.

If JianYing still rejects the draft, deliver a rendered MP4 fallback and keep the editable config so the draft can be rebuilt.
