#!/usr/bin/env python3
"""Build an editable JianYing draft from a JSON config.

The script creates a multi-track editable draft while keeping all media inside
the draft folder for better macOS JianYing compatibility.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_jianying_skill_root() -> Path:
    env_root = os.getenv("JY_SKILL_ROOT", "").strip()
    candidates = [
        Path(env_root).expanduser() if env_root else None,
        Path.home() / ".codex/skills/jianying-editor",
        Path.home() / ".codex/skills/jianying-editor-skill",
    ]
    for candidate in candidates:
        if candidate and (candidate / "scripts/jy_wrapper.py").exists():
            return candidate
    raise RuntimeError("Cannot find jianying-editor skill. Set JY_SKILL_ROOT.")


JY_SKILL_ROOT = resolve_jianying_skill_root()
sys.path.insert(0, str(JY_SKILL_ROOT / "scripts"))

from utils.env_setup import setup_env  # noqa: E402

setup_env()

import pyJianYingDraft as draft  # noqa: E402
from jy_wrapper import JyProject  # noqa: E402


def ffmpeg_exe() -> str:
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def seconds(value, default=None):
    if value is None:
        return default
    return float(value)


def transcode_video(src: Path, dst: Path, width: int = 1920, height: int = 1080) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            ffmpeg_exe(),
            "-y",
            "-i",
            str(src),
            "-vf",
            f"scale={width}:{height},setsar=1,fps=30,format=yuv420p",
            "-c:v",
            "libx264",
            "-profile:v",
            "high",
            "-level",
            "4.1",
            "-tag:v",
            "avc1",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            str(dst),
        ]
    )


def transcode_audio(src: Path, dst: Path, duration=None, loop=False) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg_exe(), "-y"]
    if loop:
        cmd += ["-stream_loop", "-1"]
    cmd += ["-i", str(src)]
    if duration:
        cmd += ["-t", str(duration)]
    cmd += [
        "-vn",
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(dst),
    ]
    run(cmd)


def text_style(draft_module, size, color, bold):
    return draft_module.TextStyle(
        size=float(size),
        bold=bool(bold),
        color=tuple(float(x) for x in color),
        auto_wrapping=True,
        max_line_width=0.84,
    )


def add_text(project, item):
    color = item.get("color", [1.0, 1.0, 1.0])
    project.add_text_simple(
        item["text"],
        start_time=f"{float(item['start'])}s",
        duration=f"{float(item['duration'])}s",
        track_name=item.get("track", "Subtitles"),
        style=text_style(draft, item.get("size", 5.2), color, item.get("bold", False)),
        border=draft.TextBorder(
            color=(0.0, 0.0, 0.0),
            alpha=0.92,
            width=float(item.get("border_width", 36.0)),
        ),
        clip_settings=draft.ClipSettings(transform_y=float(item.get("y", -0.72))),
    )


def add_video_loop(project, media_path: Path, slot: dict, default_scale: float) -> None:
    cursor = float(slot["start"])
    remaining = float(slot["duration"])
    ranges = slot.get("source_ranges") or [{"start": 0, "duration": remaining}]
    idx = 0
    scale = float(slot.get("scale", default_scale))
    volume = float(slot.get("volume", 0.0))
    track = slot.get("track", "VideoTrack")

    while remaining > 0.05:
        source = ranges[idx % len(ranges)]
        src_start = float(source.get("start", 0.0))
        src_duration = float(source.get("duration", remaining))
        dur = min(remaining, src_duration)
        seg = project.add_clip(
            str(media_path),
            source_start=f"{src_start}s",
            duration=f"{dur}s",
            target_start=f"{cursor}s",
            track_name=track,
        )
        if seg:
            seg.volume = volume
            seg.clip_settings = draft.ClipSettings(scale_x=scale, scale_y=scale)
        cursor += dur
        remaining -= dur
        idx += 1


def set_material_names(content_path: Path) -> None:
    data = json.loads(content_path.read_text(encoding="utf-8"))
    for group in ("videos", "audios"):
        for item in data.get("materials", {}).get(group, []):
            path = item.get("path")
            if path:
                item["name"] = Path(path).name
    for key in ("platform", "last_modified_platform"):
        if isinstance(data.get(key), dict):
            data[key]["os"] = "mac"
    content_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def patch_macos_index(project, draft_path: Path, duration_us: int) -> None:
    content_path = draft_path / "draft_content.json"
    if content_path.exists():
        set_material_names(content_path)
        shutil.copyfile(content_path, draft_path / "draft_info.json")
        shutil.copyfile(content_path, draft_path / "template-2.tmp")

    (draft_path / "draft_settings").write_text(
        "\n".join(
            [
                "[General]",
                "cloud_last_modify_platform=mac",
                f"draft_create_time={int(time.time())}",
                f"draft_last_edit_time={int(time.time())}",
                "real_edit_keys=1",
                f"real_edit_seconds={int(duration_us / 1_000_000)}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    root_meta = Path(project.root) / "root_meta_info.json"
    if not root_meta.exists():
        return
    try:
        data = json.loads(root_meta.read_text(encoding="utf-8"))
    except Exception:
        return

    now_us = int(time.time() * 1_000_000)
    stores = data.setdefault("all_draft_store", [])
    info_path = draft_path / "draft_info.json"
    content_size = int(content_path.stat().st_size) if content_path.exists() else 0
    entry = None
    for existing in stores:
        if existing.get("draft_name") == project.name or existing.get("draft_fold_path") == str(draft_path):
            entry = existing
            break
    if entry is None:
        entry = {
            "cloud_draft_cover": False,
            "cloud_draft_sync": False,
            "draft_cloud_last_action_download": False,
            "draft_cloud_purchase_info": "",
            "draft_cloud_template_id": "",
            "draft_cloud_tutorial_info": "",
            "draft_cloud_videocut_purchase_info": "",
            "draft_id": str(uuid.uuid4()).upper(),
            "draft_is_ai_shorts": False,
            "draft_is_cloud_temp_draft": False,
            "draft_is_invisible": False,
            "draft_is_web_article_video": False,
            "draft_type": "",
            "draft_web_article_video_enter_from": "",
            "tm_draft_cloud_completed": "",
            "tm_draft_cloud_entry_id": -1,
            "tm_draft_cloud_modified": 0,
            "tm_draft_cloud_parent_entry_id": -1,
            "tm_draft_cloud_space_id": -1,
            "tm_draft_cloud_user_id": -1,
            "tm_draft_create": now_us,
        }
        stores.append(entry)

    entry.update(
        {
            "draft_cover": str(draft_path / "draft_cover.jpg"),
            "draft_fold_path": str(draft_path),
            "draft_json_file": str(info_path),
            "draft_name": project.name,
            "draft_new_version": "164.0.0",
            "draft_root_path": str(project.root),
            "draft_timeline_materials_size": content_size,
            "streaming_edit_draft_ready": True,
            "tm_duration": duration_us,
            "tm_draft_modified": now_us,
            "tm_draft_removed": 0,
        }
    )
    root_meta.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")


def create_cover(video_path: Path, cover_path: Path) -> None:
    try:
        run(
            [
                ffmpeg_exe(),
                "-y",
                "-ss",
                "1",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-q:v",
                "3",
                str(cover_path),
            ]
        )
    except Exception:
        pass


def validate_draft(draft_path: Path) -> dict:
    content_path = draft_path / "draft_content.json"
    result = {
        "draft_path": str(draft_path),
        "draft_content_exists": content_path.exists(),
        "all_materials_inside_draft": True,
        "missing_materials": [],
        "tracks": [],
    }
    if not content_path.exists():
        return result
    data = json.loads(content_path.read_text(encoding="utf-8"))
    for track in data.get("tracks", []):
        result["tracks"].append(
            {
                "name": track.get("name"),
                "type": track.get("type"),
                "segments": len(track.get("segments", [])),
            }
        )
    for group in ("videos", "audios"):
        for item in data.get("materials", {}).get(group, []):
            path = item.get("path")
            if not path:
                continue
            if not Path(path).exists():
                result["missing_materials"].append(path)
            if not str(path).startswith(str(draft_path)):
                result["all_materials_inside_draft"] = False
    return result


def build(config_path: Path) -> dict:
    config = load_config(config_path)
    draft_name = config["draft_name"]
    duration = float(config.get("duration", 60))
    duration_us = int(duration * 1_000_000)
    width = int(config.get("width", 1080))
    height = int(config.get("height", 1920))

    project = JyProject(draft_name, width=width, height=height, overwrite=True)
    draft_path = Path(project.root) / project.name
    media_dir = draft_path / "materials"

    source_video = Path(config["source_video"]).expanduser()
    if not source_video.exists():
        raise FileNotFoundError(source_video)
    internal_video = media_dir / "video" / "source_safe.mp4"
    source_w = int(config.get("source_width", 1920))
    source_h = int(config.get("source_height", 1080))
    transcode_video(source_video, internal_video, source_w, source_h)

    for slot in config.get("visual_slots", []):
        add_video_loop(project, internal_video, slot, float(config.get("video_scale", 1.78)))

    for idx, audio in enumerate(config.get("audio_tracks", [])):
        src = Path(audio.get("path") or audio.get("source") or "").expanduser()
        if not src.exists():
            raise FileNotFoundError(src)
        safe_name = f"{audio.get('track', 'audio').lower()}_{idx}.m4a"
        internal_audio = media_dir / "audio" / safe_name
        transcode_audio(
            src,
            internal_audio,
            duration=seconds(audio.get("duration")),
            loop=bool(audio.get("loop", False)),
        )
        seg = project.add_audio_safe(
            str(internal_audio),
            start_time=f"{float(audio.get('start', 0.0))}s",
            duration=f"{float(audio.get('duration', duration))}s",
            track_name=audio.get("track", "AudioTrack"),
        )
        if seg:
            seg.volume = float(audio.get("volume", 1.0))

    for item in config.get("text_items", []):
        add_text(project, item)

    save_result = project.save()
    patch_macos_index(project, Path(save_result["draft_path"]), duration_us)
    create_cover(internal_video, Path(save_result["draft_path"]) / "draft_cover.jpg")

    validation = validate_draft(Path(save_result["draft_path"]))
    meta = {
        "draft_name": project.name,
        "draft_path": save_result["draft_path"],
        "config_path": str(config_path),
        "internal_video": str(internal_video),
        "duration_seconds": duration,
        "validation": validation,
    }
    output_meta = config.get("output_meta")
    if output_meta:
        output_path = Path(output_meta).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        meta["output_meta"] = str(output_path)
    return meta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to editable draft config JSON")
    args = parser.parse_args()
    meta = build(Path(args.config).expanduser())
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
