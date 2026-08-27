#!/usr/bin/env python3
"""Check a clip against the 4DAnyone input contract before spending a GPU run.

4DAnyone always emits exactly 121 frames at 704x1280 and is trained on portrait
footage of a single person. A clip that violates the contract fails partway
through inference with a VideoContractError, after preprocessing has already
run. This script does the cheap checks up front with ffprobe.

Two requirements cannot be checked mechanically -- that exactly one person is in
frame, full-body or upper-body, and that camera motion is mild. Those are
reported as reminders; look at the video.

Usage:
    python check_video.py clip.mp4
    python check_video.py clip.mp4 --start-time 3.5 --target-fps 25
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction

REQUIRED_FRAMES = 121
MIN_SHORT_SIDE = 720           # 720p floor; 1080p recommended
TARGET_ASPECT = Fraction(9, 16)
ASPECT_TOLERANCE = 0.02        # 9:16 == 0.5625; allow a couple of percent
FPS_CANDIDATES = (30, 25, 24)  # auto target_fps prefers an even divisor of these
# ffprobe happily reports a still image as a 25 fps video stream with no duration,
# so a bare "0 frames" failure would misdiagnose the most common mistake: pointing
# this at a photo instead of a clip.
STILL_IMAGE_CODECS = {"png", "mjpeg", "bmp", "gif", "tiff", "webp", "jpeg2000"}


GREEN, YELLOW, RED, DIM, RESET = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[0m"


def probe(path: str) -> dict:
    if shutil.which("ffprobe") is None:
        sys.exit("error: ffprobe not found. Install ffmpeg to run this check.")
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_streams", "-show_format",
        "-of", "json", path,
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as exc:
        sys.exit(f"error: ffprobe could not read {path}\n{exc.stderr.strip()}")
    data = json.loads(out)
    if not data.get("streams"):
        sys.exit(f"error: no video stream in {path}")
    return data


def frame_count(stream: dict, fmt: dict, fps: float) -> tuple[int, bool]:
    """Return (frames, exact). Falls back to duration x fps when unindexed."""
    for key in ("nb_frames", "nb_read_frames"):
        value = stream.get(key)
        if value and str(value).isdigit() and int(value) > 0:
            return int(value), True
    duration = stream.get("duration") or fmt.get("duration")
    if duration:
        return int(float(duration) * fps), False
    return 0, False


def auto_target_fps(source_fps: float) -> float:
    """Mirror the pipeline's `target_fps="auto"` rule.

    auto keeps the input clock unless it divides evenly to 24, 25, or 30 FPS.
    This is an approximation of upstream behaviour, used only to estimate how
    much source footage a run consumes -- it does not change what inference does.
    """
    rounded = round(source_fps)
    if abs(source_fps - rounded) < 1e-6:
        for candidate in FPS_CANDIDATES:
            if rounded % candidate == 0:
                return float(candidate)
    return source_fps


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a clip for 4DAnyone.")
    ap.add_argument("video")
    ap.add_argument("--start-time", type=float, default=0.0,
                    help="Value you intend to pass as --start_time (seconds).")
    ap.add_argument("--target-fps", default="auto",
                    help="Value you intend to pass as --target_fps.")
    args = ap.parse_args()

    data = probe(args.video)
    stream, fmt = data["streams"][0], data.get("format", {})

    # A still image has no timeline to draw 121 frames from, and no amount of
    # cropping fixes that -- say so directly instead of reporting "0 frames".
    format_name = fmt.get("format_name", "")
    codec = stream.get("codec_name", "")
    has_timeline = bool(stream.get("nb_frames") or stream.get("duration") or fmt.get("duration"))
    if format_name.endswith("_pipe") or (codec in STILL_IMAGE_CODECS and not has_timeline):
        print(f"\n{args.video}")
        print(f"  {RED}FAIL{RESET}  Not a video          "
              f"{stream.get('width')}x{stream.get('height')} still image ({codec}).")
        print(f"\n{RED}Not ready:{RESET} 4DAnyone animates a person across time -- it needs a "
              f"video clip of at least {REQUIRED_FRAMES} frames, not a single frame.\n")
        return 1

    width, height = int(stream["width"]), int(stream["height"])
    # Respect rotation metadata: a phone clip is often stored landscape.
    rotation = 0
    for side in stream.get("side_data_list") or []:
        if "rotation" in side:
            rotation = abs(int(side["rotation"])) % 180
    if rotation == 90:
        width, height = height, width

    source_fps = 0.0
    for key in ("avg_frame_rate", "r_frame_rate"):
        try:
            # ffprobe writes "0/0" for streams it could not time; Fraction raises on it.
            source_fps = float(Fraction(stream.get(key) or "0/1"))
        except ZeroDivisionError:
            source_fps = 0.0
        if source_fps > 0:
            break
    if source_fps <= 0:
        sys.exit("error: could not determine frame rate")

    total_frames, exact = frame_count(stream, fmt, source_fps)
    available = max(0, total_frames - int(args.start_time * source_fps))

    target_fps = auto_target_fps(source_fps) if args.target_fps == "auto" else float(args.target_fps)
    needed_source_frames = int(REQUIRED_FRAMES / target_fps * source_fps + 0.5)

    aspect = width / height
    failures: list[str] = []

    def line(ok: bool, label: str, detail: str, hard: bool = True) -> None:
        mark, color = ("PASS", GREEN) if ok else (("FAIL", RED) if hard else ("WARN", YELLOW))
        print(f"  {color}{mark}{RESET}  {label:<22} {detail}")
        if not ok and hard:
            failures.append(label)

    print(f"\n{args.video}")
    print(f"{DIM}  {width}x{height} @ {source_fps:.3f} fps, "
          f"{total_frames} frames{'' if exact else ' (estimated)'}{RESET}\n")

    line(min(width, height) >= MIN_SHORT_SIDE,
         "Resolution",
         f"{width}x{height} (need short side >= {MIN_SHORT_SIDE}; 1080 recommended)")

    portrait_ok = abs(aspect - float(TARGET_ASPECT)) <= ASPECT_TOLERANCE
    line(portrait_ok, "Aspect ratio",
         f"{aspect:.4f} (need 9:16 = {float(TARGET_ASPECT):.4f})"
         + ("" if portrait_ok else " -- crop to portrait before running"))

    line(available >= needed_source_frames,
         "Usable frames",
         f"{available} available from t={args.start_time}s; "
         f"need ~{needed_source_frames} to fill {REQUIRED_FRAMES} frames at {target_fps:g} fps")

    if not exact:
        print(f"  {DIM}note{RESET}  frame count was estimated from duration; "
              f"trust it only if the margin is comfortable")

    line(False, "Single subject",
         "cannot be checked automatically -- confirm one person, full-body or upper-body",
         hard=False)
    line(False, "Camera motion",
         "cannot be checked automatically -- confirm only mild motion; "
         "GVHMR must attribute motion to the person, not the camera",
         hard=False)

    if failures:
        print(f"\n{RED}Not ready:{RESET} {', '.join(failures)}. "
              f"Fix these before running inference -- the pipeline rejects the clip "
              f"only after preprocessing has already run.\n")
        return 1
    print(f"\n{GREEN}Contract satisfied.{RESET} Start with a 6-view run to confirm quality "
          f"before committing to a large rig.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
