#!/usr/bin/env python3
"""Expand a single image into a conforming still clip for 4DAnyone.

4DAnyone's CLI freezes the input at 121 frames, but nothing in the pipeline
requires the subject to *move*: the decoder already reuses frames when
timestamps repeat (fdanyone/video.py), GVHMR recovers a pose per frame, and the
generator is conditioned on the resulting skeleton renders. Hold one frame for
121 timestamps and the run degenerates into single-image novel-view synthesis --
an orbit of a motionless person, which `scripts/export_nerfstudio.py` then turns
into a static 3DGS.

This is off-label. The authors train and benchmark on motion, and publish no
numbers for a static input. Treat the output as an experiment, not a supported
mode, and read references/single-image.md before relying on it.

Usage:
    python still_to_clip.py photo.jpg out.mp4
    python still_to_clip.py group.png out.mp4 --focus-x 760 --check
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

TARGET_W, TARGET_H = 1080, 1920
PORTRAIT = Fraction(9, 16)
REQUIRED_FRAMES = 121
DEFAULT_FRAMES = 150       # margin over the 121-frame contract
DEFAULT_FPS = 30

YELLOW, RED, GREEN, DIM, RESET = "\033[33m", "\033[31m", "\033[32m", "\033[2m", "\033[0m"


def portrait_crop(width: int, height: int, focus_x: float | None,
                  focus_y: float | None) -> tuple[int, int, int, int]:
    """Largest 9:16 window inside the image, centred on the focus point."""
    if Fraction(width, height) > PORTRAIT:
        # Wider than 9:16 -- full height, narrow the width.
        crop_h = height
        crop_w = int(height * PORTRAIT)
    else:
        # Taller than 9:16 -- full width, shorten the height.
        crop_w = width
        crop_h = int(width / PORTRAIT)

    cx = width / 2 if focus_x is None else focus_x
    cy = height / 2 if focus_y is None else focus_y
    x = int(round(cx - crop_w / 2))
    y = int(round(cy - crop_h / 2))
    # Keep the window inside the image.
    x = max(0, min(x, width - crop_w))
    y = max(0, min(y, height - crop_h))
    # libx264 needs even dimensions.
    return x, y, crop_w - (crop_w % 2), crop_h - (crop_h % 2)


def main() -> int:
    ap = argparse.ArgumentParser(description="Turn one image into a 4DAnyone-conforming still clip.")
    ap.add_argument("image")
    ap.add_argument("output", nargs="?", default=None,
                    help="Output .mp4 (default: <image stem>_still.mp4 beside the image).")
    ap.add_argument("--focus-x", type=float, default=None,
                    help="Horizontal centre of the crop, in source pixels. Aim this at your subject "
                         "when the image contains more than one person.")
    ap.add_argument("--focus-y", type=float, default=None, help="Vertical centre of the crop.")
    ap.add_argument("--crop", default=None, metavar="X,Y,W,H",
                    help="Explicit crop window, overriding the automatic 9:16 window.")
    ap.add_argument("--frames", type=int, default=DEFAULT_FRAMES,
                    help=f"Frames to emit (default {DEFAULT_FRAMES}; the contract needs {REQUIRED_FRAMES}).")
    ap.add_argument("--fps", type=int, default=DEFAULT_FPS, help=f"Output frame rate (default {DEFAULT_FPS}).")
    ap.add_argument("--crf", type=int, default=None,
                    help="Encode lossy at this CRF instead of lossless. Lossless is the default "
                         "because inter-frame compression noise would otherwise be the only thing "
                         "moving in the clip, and GVHMR reads motion for a living.")
    ap.add_argument("--check", action="store_true", help="Run check_video.py on the result.")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            sys.exit(f"error: {tool} not found. Install ffmpeg.")

    src = Path(args.image)
    if not src.is_file():
        sys.exit(f"error: no such file: {src}")
    out = Path(args.output) if args.output else src.with_name(f"{src.stem}_still.mp4")

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(src)],
        capture_output=True, text=True)
    if probe.returncode != 0 or "x" not in probe.stdout:
        sys.exit(f"error: could not read image dimensions from {src}\n{probe.stderr.strip()}")
    width, height = (int(v) for v in probe.stdout.strip().split("x")[:2])

    if args.crop:
        try:
            x, y, crop_w, crop_h = (int(v) for v in args.crop.split(","))
        except ValueError:
            sys.exit("error: --crop expects X,Y,W,H in pixels")
    else:
        x, y, crop_w, crop_h = portrait_crop(width, height, args.focus_x, args.focus_y)

    if args.frames < REQUIRED_FRAMES:
        print(f"{RED}error{RESET}  --frames {args.frames} is below the {REQUIRED_FRAMES}-frame contract.")
        return 1

    print(f"\n{src}  {DIM}{width}x{height}{RESET}")
    print(f"  crop      {crop_w}x{crop_h} at ({x},{y})"
          f"{'  [explicit]' if args.crop else '  [auto 9:16]'}")
    print(f"  output    {TARGET_W}x{TARGET_H}, {args.frames} frames @ {args.fps} fps "
          f"({args.frames / args.fps:.1f}s), "
          f"{'lossless' if args.crf is None else f'CRF {args.crf}'}")

    if crop_w < TARGET_W:
        print(f"  {YELLOW}note{RESET}      crop is {crop_w}px wide, upscaling to {TARGET_W}px. "
              f"Upscaling adds pixels, not detail -- a tighter source hurts output quality.")

    # Lossless keeps every decoded frame bit-identical. At CRF 16 the frames drift
    # by up to 6/255 (62.6 dB) -- invisible, but it is real inter-frame change in a
    # clip whose entire premise is that nothing changes.
    encode = ["-qp", "0"] if args.crf is None else ["-crf", str(args.crf)]
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-loop", "1", "-i", str(src),
        "-frames:v", str(args.frames), "-r", str(args.fps),
        "-vf", f"crop={crop_w}:{crop_h}:{x}:{y},scale={TARGET_W}:{TARGET_H}:flags=lanczos",
        "-pix_fmt", "yuv420p", "-c:v", "libx264", *encode, str(out),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"error: ffmpeg failed\n{result.stderr.strip()}")

    print(f"\n{GREEN}Wrote{RESET} {out}  {DIM}({out.stat().st_size / 1e6:.1f} MB){RESET}")

    if args.check:
        checker = Path(__file__).with_name("check_video.py")
        print()
        subprocess.run([sys.executable, str(checker), str(out)])

    print(f"""
Next, in the 4DAnyone checkout:

    PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \\
    python inference.py --video_path "{out}" --views_per_layer 16 --layer_pitches '[-10,15,35]'

    python scripts/export_nerfstudio.py \\
        --result_dir data/fdanyone/{out.stem} --frame_index 0

Every output frame is identical by construction, so frame_index 0 loses nothing.
The 48-view rig is the one worth paying for here -- coverage, not duration, is
what a static reconstruction has to work with.
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
