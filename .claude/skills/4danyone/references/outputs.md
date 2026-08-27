# Outputs and 3DGS reconstruction

## Layout

With the default `--data_dir data`:

```text
data/
├── gvhmr/results/<clip>/
│   ├── motion.json
│   └── motion.safetensors
└── fdanyone/<clip>/
    ├── metadata.json
    ├── cameras.json
    ├── skeletons/00.mp4 ... <N-1>.mp4
    └── videos/
        ├── sparse/*.mp4                # RCP proposal views, when used
        └── dense/00.mp4 ... <N-1>.mp4  # final target views
```

`<clip>` is the input filename without its extension; `N` is the number of
target views.

| Path | What it is |
|---|---|
| `videos/dense/` | The generated target views — the actual deliverable. |
| `videos/sparse/` | Intermediate proposal views for larger rigs. Diagnostic only. |
| `skeletons/` | Pose-conditioning renders aligned with the target views. Useful for spotting motion-recovery failures: if the skeleton is wrong here, no amount of resampling will fix the output. |
| `cameras.json` | Intrinsics and poses for every target view, indexed to match `dense/`. |
| `metadata.json` | Input, generation settings, model versions, timings, and per-worker metrics for multi-GPU runs. |
| `gvhmr/results/` | Cached motion recovery. Reused automatically when the same clip is re-run with a different rig, which makes rig experiments much cheaper than the first run. |

Every output video is 121 frames at 704×1280, at the selected output FPS, with
no audio.

## Nerfstudio / 3DGS reconstruction

This reconstructs a **static** 3DGS from one synchronized timestamp. It does not
reproduce the 4DGS results in the paper — the FreeTimeGS implementation used
there is not public. Say so when a user asks for "the 4D result"; promising 4DGS
from this path would be wrong.

### Install

Follow the [Nerfstudio installation guide](https://docs.nerf.studio/quickstart/installation.html)
in a **separate** environment, then:

```bash
pip install huggingface-hub safetensors
```

### Export a frame

Run the exporter inside the 4DAnyone environment:

```bash
conda activate 4danyone
python scripts/export_nerfstudio.py \
    --result_dir data/fdanyone/<clip> \
    --frame_index 0
```

Produces:

```text
data/nerfstudio/<clip>/frame_000/
├── transforms.json
├── sparse_pcd.ply                 # visual-hull initialization
├── images/00.png ... <N-1>.png
└── masks/00.png ... <N-1>.png
```

### Train

Standard Splatfacto:

```bash
ns-train splatfacto \
    --data data/nerfstudio/<clip>/frame_000 \
    --pipeline.model.background-color random
```

Splatfacto with perceptual loss (better detail; enable `bfloat16` if the GPU
supports it):

```bash
python scripts/train_nerfstudio.py splatfacto-perceptual \
    --data data/nerfstudio/<clip>/frame_000 \
    --pipeline.model.background-color random \
    --pipeline.model.perceptual-loss-weight 0.4 \
    --pipeline.model.perceptual-compute-dtype bfloat16
```

### View

Use the wrapper so the custom method is registered before Nerfstudio loads the
saved config:

```bash
python scripts/view_nerfstudio.py \
    --load-config outputs/<clip>/splatfacto-perceptual/<timestamp>/config.yml \
    --viewer.websocket-port 7007
```

For a remote box, forward the port:

```bash
ssh -N -L 7007:127.0.0.1:7007 <server>
```

Reconstruction quality tracks view coverage — the 48-view three-pitch rig is the
one worth using here. A 6-view orbit will reconstruct poorly and that is
expected, not a bug to chase.
