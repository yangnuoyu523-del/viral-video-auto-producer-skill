#!/usr/bin/env python3
"""Validate the local environment for viral-video-auto-producer."""

import json
import os
import shutil
import sys
from pathlib import Path


def exists(path):
    return bool(path) and Path(path).exists()


def main():
    home = Path.home()
    jy_root = os.getenv("JY_SKILL_ROOT") or str(home / ".codex/skills/jianying-editor")
    checks = {
        "python": sys.version.split()[0],
        "jianying_editor_skill": exists(Path(jy_root) / "scripts/jy_wrapper.py"),
        "JY_SKILL_ROOT": jy_root,
        "video_analyzer_skill": exists(home / ".codex/skills/video-analyzer-skill/SKILL.md"),
        "Spider_XHS_skill": exists(home / ".codex/skills/Spider_XHS/SKILL.md"),
        "de_ai_writing_skill": exists(home / ".codex/skills/de-ai-writing/SKILL.md"),
        "prompt_master_skill": exists(home / ".codex/skills/prompt-master/SKILL.md")
        or exists(home / ".codex/skills/prompt-master-nidhinjs/SKILL.md"),
        "jianying_drafts_root": exists(home / "Movies/JianyingPro/User Data/Projects/com.lveditor.draft"),
        "git": bool(shutil.which("git")),
        "env_has_ARK_API_KEY": bool(os.getenv("ARK_API_KEY")),
        "env_has_DOUBAO_API_KEY": bool(os.getenv("DOUBAO_API_KEY")),
        "env_has_DOUBAO_TEXT_MODEL": bool(os.getenv("DOUBAO_TEXT_MODEL")),
        "env_has_DOUBAO_VIDEO_MODEL": bool(os.getenv("DOUBAO_VIDEO_MODEL")),
    }

    try:
        import imageio_ffmpeg

        checks["imageio_ffmpeg"] = True
        checks["ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        checks["imageio_ffmpeg"] = False
        checks["ffmpeg_error"] = str(exc)

    try:
        import pymediainfo  # noqa: F401

        checks["pymediainfo"] = True
    except Exception as exc:
        checks["pymediainfo"] = False
        checks["pymediainfo_error"] = str(exc)

    required_ok = (
        checks["jianying_editor_skill"]
        and checks["imageio_ffmpeg"]
        and checks["jianying_drafts_root"]
    )
    result = {"ok": required_ok, "checks": checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if required_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
