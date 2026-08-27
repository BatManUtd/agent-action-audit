# `inference.py` argument reference

Everything is exposed through [Fire](https://github.com/google/python-fire), so
every parameter below is a `--flag value` on the command line. List values are
passed as quoted JSON-ish literals: `--layer_pitches '[-10,15,35]'`,
`--gpu_ids '[0,1]'`.

Run `python inference.py --help` in the checkout for the authoritative list.

## Input

| Flag | Default | Notes |
|---|---|---|
| `video_path` | *(required)* | Input clip. Must contain at least 121 usable frames from `start_time` onward. |
| `start_time` | `0.0` | Clip start on the input timeline, in seconds. The cheapest way to skip a shaky or empty opening. |
| `target_fps` | `"auto"` | `auto` keeps the input clock unless it divides evenly to 24, 25, or 30 FPS. A positive number requests an explicit FPS. |

## Camera rig

Total views = `views_per_layer × len(layer_pitches)`.

| Flag | Default | Constraint |
|---|---|---|
| `views_per_layer` | `24` | Evenly spaced yaw positions per pitch ring. Must be divisible by 4 or 6. |
| `layer_pitches` | `[15]` | One pitch per ring, in degrees. Each value must be within −15…45. Positive places the camera above the subject. |
| `start_yaw` | `0` | Yaw of the first view, in degrees. `0` faces the person. |
| `yaw_span` | `360` | Angular range per ring, 1…360 degrees. The end angle is excluded, so a full ring never duplicates a view. |

### Rig recipes

```bash
# 6-view full orbit — smoke test
--views_per_layer 6

# 24-view full orbit — dense orbit shot, usable for 4DGS
--views_per_layer 24

# 48 views over three pitch rings — best coverage for reconstruction
--views_per_layer 16 --layer_pitches '[-10,15,35]'

# 8-view frontal arc — front hemisphere only
--views_per_layer 8 --start_yaw -90 --yaw_span 180
```

## Generation behaviour

These control the two-stage generation strategy. The defaults are what the
authors benchmark; change them only with a reason, and record the change in
whatever you report back.

| Flag | Default | Notes |
|---|---|---|
| `views_per_group` | `"auto"` | Maximum target views denoised together. `auto` picks 6 when possible, otherwise 4. A manual value must be 4 or 6 **and** divide `views_per_layer`. |
| `enable_rcp` | `True` | Generate sparse proposal views first when producing more than six targets, then condition the dense pass on them. Proposal count follows `views_per_group`. Disabling it is faster but degrades cross-view consistency. |
| `enable_tcr` | `True` | Cyclically shift view groups between denoising steps, which reduces seams between groups. |
| `seed` | `42` | Shared by proposal and target generation. Change it to resample a run you did not like; keep it fixed when comparing rigs. |

## Paths

| Flag | Default | Notes |
|---|---|---|
| `data_dir` | `"data"` | Root for reusable GVHMR motion results and final outputs. |
| `model_dir` | `"models"` | Model root; missing public checkpoints download here on first use. |
| `checkpoint_path` | `None` | Override the 4DAnyone checkpoint with a local file. |
| `mhr70_regressor_path` | `None` | Override the SMPL-X → MHR70 regressor. |
| `gvhmr_root` | `"third_party/GVHMR"` | Path to the GVHMR checkout. Must contain `hmr4d/__init__.py`, i.e. the submodule was initialized. |

## Compute

| Flag | Default | Notes |
|---|---|---|
| `gpu_ids` | `None` | GPU IDs for parallel denoising. `None` means **all visible GPUs** — pass an explicit list on a shared machine. |

`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` is set in the upstream
benchmark commands and is worth keeping; it reduces allocator fragmentation
during the long denoising loop.

## Return value

`inference()` returns a dict describing the run, and the same information is
persisted to `metadata.json` in the output directory. Prefer reading
`metadata.json` when reporting results — it survives the process.
