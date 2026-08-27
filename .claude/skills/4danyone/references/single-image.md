# Single image → static 3D (experimental)

## Why this works at all

4DAnyone's CLI freezes the input at 121 frames, which reads like a demand for
motion. It is not. Nothing in the pipeline requires the subject to *move*:

- `fdanyone/video.py` decodes by sampling source timestamps and explicitly
  reuses a frame when several targets land on it — duplicate frames are a
  supported decode path, not an error case.
- GVHMR fits a pose per frame. Given 121 identical frames it converges on one
  pose repeated 121 times.
- Generation is conditioned on the per-view skeleton renders, which are then
  also static.

So holding one frame for 121 timestamps degenerates the pipeline into
single-image novel-view synthesis: an orbit of a motionless person. Feed that to
`scripts/export_nerfstudio.py --frame_index 0` and you get a static 3DGS —
3D from one frame, using a 4D pipeline as the multi-view generator.

## What is actually known

Be straight with users about the epistemic status here:

- **Untested by the authors.** They train and benchmark on casual video and
  publish no numbers for a static input. There is no quality claim to make.
- **The generator is a video model.** Its temporal layers are being handed a
  constant signal — a regime outside its training distribution. It may be fine;
  it may produce degraded or subtly inconsistent views. Find out with a 6-view
  run before paying for 48.
- **Occlusion is unrecoverable.** With video, a turning subject reveals their
  own back over time. One frame reveals nothing. Everything the camera cannot
  see is invented by the generator's prior, and no rig geometry changes that.
- **Purpose-built alternatives exist.** If single-image 3D humans are the actual
  goal rather than a 4DAnyone experiment, methods designed for it (PIFuHD, ECON,
  SIFU, Human3Diffusion) start from the right assumptions. Recommend them when
  the user's goal is the reconstruction rather than this pipeline.

## The workflow

```bash
python scripts/still_to_clip.py photo.jpg subject.mp4 --check
```

Then the normal run, using the clip like any other input:

```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
python inference.py --video_path "subject.mp4" --views_per_layer 6

# once a 6-view run looks right, go for coverage
python inference.py --video_path "subject.mp4" \
    --views_per_layer 16 --layer_pitches '[-10,15,35]'

python scripts/export_nerfstudio.py \
    --result_dir data/fdanyone/subject --frame_index 0
```

## Framing the crop

`still_to_clip.py` takes the largest 9:16 window that fits, centred by default.
On a wide image that window is tall and narrow, which frequently captures
bystanders — and a second person in frame breaks tracking. Aim it:

```bash
python still_to_clip.py group.jpg out.mp4 --focus-x 760        # centre on a subject
python still_to_clip.py group.jpg out.mp4 --crop 640,372,260,462  # exact window
```

An explicit `--crop` narrower than the full height is often the only way to
isolate one person, and giving up full height to do so is the right trade.

The script warns when the crop is narrower than 1080px, because the upscale to
1080×1920 adds pixels rather than detail. A tight crop of a distant subject
produces a soft input and a soft reconstruction.

## Rig choice differs from the video case

Static input inverts the usual advice. With video, a moderate rig plus the
subject's own rotation covers the body over time. With one frame, coverage comes
only from the rig, so the 48-view three-pitch layout is the one worth paying for:

```bash
--views_per_layer 16 --layer_pitches '[-10,15,35]'
```

Still validate with 6 views first — a bad input wastes eight times as much
compute at 48.

## Encoding

The clip is written lossless (`-qp 0`). At CRF 16 decoded frames drift by up to
6/255 (62.6 dB PSNR) — invisible to a viewer, but real inter-frame change in a
clip whose entire premise is that nothing changes, handed to a motion-estimation
model. Lossless costs roughly 2× the file size for a few seconds of video, which
is nothing next to a confusing debugging session. Use `--crf` to override when
size genuinely matters.

## Seated and occluded subjects

A subject seated behind a table, cropped at the waist, or otherwise occluded
below the torso is a hard case: GVHMR fits a full SMPL-X body and has to
hallucinate the hidden half, then every generated view inherits that guess.
Upper-body shots are supported by the input contract, but expect the
reconstruction to be least trustworthy exactly where the source showed least.
