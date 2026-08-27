---
name: 4danyone
description: Turn a casual monocular video of one person into synchronized multi-view videos (and optionally a 3DGS reconstruction) using ant-research/4DAnyone. Use this whenever the user wants free-viewpoint, orbit, novel-view, multi-camera, 4D, 4DGS, or Gaussian-splatting output from a single-camera clip of a person — including phrasings like "make an orbit shot from this phone video", "generate other camera angles of this person", "turn this clip into a 3D/4D capture", "render this person from a different angle", or any mention of 4DAnyone, GVHMR motion recovery, or SMPL-X-driven novel view synthesis. Also use it when setting up, installing, or troubleshooting the 4DAnyone environment, choosing a camera rig, validating an input clip, or exporting to Nerfstudio Splatfacto.
---

# 4DAnyone: monocular video → multi-view video

4DAnyone (ant-research, Apache-2.0) recovers a person's 3D motion from one
casual video and generates synchronized videos from an arbitrary rig of virtual
cameras. Those views are the raw material for 3DGS/4DGS reconstruction.

Pipeline in one line: **input clip → GVHMR motion recovery → SMPL-X skeleton
render per target view → diffusion generation of each target view.**

The whole thing is a single `inference.py` invocation. Most of the work in
practice is (a) getting the environment and the gated SMPL-X asset in place and
(b) making sure the input clip satisfies a fairly strict contract. Do those two
in order and the run usually just works.

## Before anything else: is this machine capable?

Check this first and say so plainly — it saves the user a 30-minute install
that ends in an OOM.

- **GPU memory: ~48 GB minimum.** Peak live tensor allocation is ~43.3 GiB
  regardless of GPU. Low-memory (<32 GB) inference is an open upstream TODO,
  not a flag you can pass. A 24 GB consumer card will not run this.
- **CUDA GPU required.** There is no CPU or MPS path.
- **Runtime**: roughly 10–25 minutes for a 6-view run on one datacenter GPU,
  plus ~2 min preprocessing. More views cost proportionally more.
- **Disk**: tens of GB for checkpoints, SMPL-X, and per-view video output.

```bash
nvidia-smi --query-gpu=name,memory.total --format=csv
```

If the user is on a laptop, a Mac, or a small GPU, tell them up front that this
needs a rented A6000/L40S/H100-class machine, and offer to prepare the exact
commands to run there rather than pretending it will work locally.

## Step 1 — Install

Use the bundled installer; it performs the upstream steps in order and is
idempotent, so it is safe to re-run after a partial failure.

```bash
bash .claude/skills/4danyone/scripts/setup.sh ~/4DAnyone
```

It clones the repo, initializes the GVHMR submodule, creates the `4danyone`
conda env on Python 3.11, installs `requirements.txt`, and pre-fetches the
public checkpoints and example clip.

**SMPL-X is the step that blocks people.** It is licensed separately and is not
on Hugging Face — the installer prompts for the credentials of an account
registered at <https://smpl-x.is.tue.mpg.de/>. That prompt needs a real
terminal. If you are running non-interactively (CI, a background agent, a
detached shell), the download cannot complete: stop and ask the user to run

```bash
conda activate 4danyone && cd ~/4DAnyone && python scripts/download_smplx.py
```

themselves in a terminal, rather than burning a run that will fail later with an
`AssetError`. Never ask the user to paste those credentials into the chat.

## Step 2 — Validate the input clip

The input contract is strict and the failure mode is a `VideoContractError`
several minutes into a run. Check first:

```bash
python .claude/skills/4danyone/scripts/check_video.py path/to/clip.mp4
```

It reports, and flags violations of:

| Requirement | Why it matters |
|---|---|
| ≥ 720p (1080p preferred) | Generation quality degrades badly below this |
| 9:16 portrait | The model is trained on portrait framing; other ratios get cropped or rejected |
| ≥ 121 usable frames | Every run produces exactly 121 output frames; short clips cannot fill them |
| One person, full-body or upper-body | Multiple subjects break tracking and motion recovery |
| Only mild camera motion | GVHMR must attribute motion to the person, not the camera |

The last two are judgment calls the script cannot make — look at the video (or
ask) rather than assuming. If the clip is close but not conforming, prefer
fixing it with a pre-pass (crop to 9:16, trim to a still-camera section, upscale
to 1080p) over pushing a marginal clip through a 20-minute run.

`--start_time` selects where the 121-frame window begins, which is the cheapest
way to skip a shaky opening.

## Starting from a single image

A still photo can go through this pipeline. The 121-frame contract constrains the
*decoder*, not the model: `fdanyone/video.py` already reuses frames when
timestamps repeat, so holding one frame for 121 timestamps degenerates the run
into single-image novel-view synthesis — an orbit of a motionless person, which
the Nerfstudio export then turns into a static 3DGS.

```bash
python .claude/skills/4danyone/scripts/still_to_clip.py photo.jpg subject.mp4 --check
```

Then run inference on `subject.mp4` exactly like any other input.

Two things to tell the user before they spend a GPU hour on it. The authors
neither test nor benchmark static input, so there is no quality claim to make —
a 6-view run is the only way to find out. And one frame reveals nothing about
the subject's back: with video the person turns and shows you, whereas here
everything unseen is invented by the generator's prior. If reconstruction is the
real goal rather than this pipeline specifically, purpose-built single-image
methods (PIFuHD, ECON, SIFU, Human3Diffusion) start from better assumptions.

Rig advice inverts here — see `references/single-image.md` for why coverage
matters more when the subject never moves, plus crop framing and encoding notes.

## Step 3 — Choose a camera rig

The rig is defined by how many yaw positions per ring (`views_per_layer`), which
pitch rings exist (`layer_pitches`), and what slice of the circle is covered
(`start_yaw`, `yaw_span`). Total views = `views_per_layer × len(layer_pitches)`.

Pick by intent:

| Intent | Command tail | Views |
|---|---|---|
| First test / smoke test | `--views_per_layer 6` | 6 |
| Orbit shot, dense 360° | `--views_per_layer 24` | 24 |
| 4DGS/3DGS reconstruction | `--views_per_layer 16 --layer_pitches '[-10,15,35]'` | 48 |
| Front-facing only (talking head, product demo) | `--views_per_layer 8 --start_yaw -90 --yaw_span 180` | 8 |

Constraints that will reject a run immediately: `views_per_layer` must be
divisible by 4 or 6; each pitch must be within −15…45 degrees; `yaw_span` is
1…360. Yaw 0 faces the subject; positive pitch places cameras above them.

Default to the 6-view run for anything exploratory. It is the difference between
finding a bad input in 12 minutes and finding it in an hour.

## Step 4 — Run

```bash
conda activate 4danyone
cd ~/4DAnyone
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
python inference.py \
    --video_path "data/source/my_clip.mp4" \
    --views_per_layer 6
```

`gpu_ids` splits denoising across GPUs and defaults to every visible device, so
on a shared machine pass it explicitly (`--gpu_ids '[0]'`) instead of quietly
occupying all of them.

The full argument list, including the RCP/TCR generation-quality switches and
the fps/seed controls, is in `references/cli.md` — read it when the user wants
anything beyond the four rigs above.

## Step 5 — Outputs and what to hand back

Results land under `data/fdanyone/<clip>/`, where `<clip>` is the input filename
without extension:

- `videos/dense/00.mp4 … <N-1>.mp4` — the generated target views. **This is the
  deliverable**; index order matches `cameras.json`.
- `cameras.json` — intrinsics and poses per view, needed by any downstream
  reconstruction.
- `skeletons/`, `videos/sparse/` — pose conditioning and intermediate proposal
  views. Useful for diagnosing a bad run, not for delivery.
- `metadata.json` — settings, timings, model versions. Quote from this when
  reporting what actually ran.
- `data/gvhmr/results/<clip>/` — cached motion recovery, reused automatically if
  you re-run the same clip with a different rig. Re-running rigs is therefore
  much cheaper than the first run; mention that when a user is unsure which rig
  they want.

All outputs are 121 frames at 704×1280, no audio.

For 3DGS reconstruction from a synchronized frame (Nerfstudio Splatfacto,
including the perceptual-loss variant and the viewer), see
`references/outputs.md`.

## When a run fails

Upstream raises typed errors; map them to the actual cause instead of retrying
blindly:

- `VideoContractError` → the clip cannot yield 121 frames. Re-check with
  `check_video.py`, adjust `--start_time`, or get a longer clip.
- `AssetError` → a checkpoint or SMPL-X is missing/invalid, or GVHMR was never
  initialized. Re-run `setup.sh`; if it names SMPL-X, that is the interactive
  download from Step 1.
- `ConfigurationError` → the rig violates a constraint (divisibility, pitch
  range, yaw span). Fix the arguments; do not work around it.
- CUDA OOM → this is a hardware ceiling, not a tuning problem. The only real
  levers are a bigger GPU or waiting for upstream low-memory support. Say that
  rather than suggesting placebo flags.

If generation is slow on a capable GPU, `references/performance.md` has measured
runtimes per GPU and the optional FlashAttention-3 / SageAttention backends,
which are auto-detected when installed.

## Reference files

Read these on demand rather than up front:

- `references/cli.md` — every `inference.py` argument, with defaults and valid ranges.
- `references/single-image.md` — the static-input mode: what is known, what is guesswork, crop framing, rig choice.
- `references/outputs.md` — output layout in detail, plus the Nerfstudio/3DGS workflow.
- `references/performance.md` — measured runtimes, peak VRAM, attention backends.
- `references/upstream.md` — provenance, license, citation, known limitations.
