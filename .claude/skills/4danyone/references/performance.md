# Inference performance

Upstream measurements for the 6-view full-orbit example, median of three runs:

```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
python inference.py \
    --video_path "data/source/pexels/2785536-uhd_2160_3840_25fps.mp4" \
    --views_per_layer 6
```

## Denoising

| GPU | SDPA (min) | FlashAttention-3 (min) | SageAttention (min) | Peak CUDA allocated (GiB) | GPU memory (GiB) |
| --- | ---: | ---: | ---: | ---: | ---: |
| H200 | 9.17 | 7.84 | 7.86 | 43.34 | 140.40 |
| H20-3E | 20.59 | 16.62 | 13.91 | 43.34 | 140.40 |
| RTX 5880 Ada | 20.85 | — | 18.01 | 43.32 | 47.99 |
| RTX A6000 | 22.93 | — | 22.75 | 43.32 | 47.99 |

`—` means the backend is unavailable on that GPU. Peak allocation was identical
across backends on each GPU, which is why attention backends buy speed but not
headroom: **they do not make this fit on a smaller card.**

## Preprocessing

| GPU | GVHMR (min) | Skeleton extraction (min) |
| --- | ---: | ---: |
| H200 | 0.94 | 0.57 |
| H20-3E | 0.97 | 0.55 |
| RTX 5880 Ada | 0.94 | 1.00 |
| RTX A6000 | 1.70 | 1.06 |

GVHMR output is cached per clip, so this cost is paid once per input, not once
per rig.

## Scaling

Denoising time scales with total view count. A 24-view run is roughly four times
a 6-view run on the same hardware; 48 views over three pitch rings, roughly
eight times. Budget accordingly before starting a large rig, and validate the
clip with a 6-view run first.

## Optional attention backends

Either is optional and auto-detected at runtime:

- [FlashAttention-3](https://github.com/Dao-AILab/flash-attention/tree/main/hopper) — Hopper only (H100/H200/H20).
- [SageAttention](https://github.com/thu-ml/SageAttention) — broader GPU support; the official `sageattn` entry point dispatches an architecture-specific kernel per GPU.

On Ada/Ampere workstation cards SageAttention is the only one of the two that
applies, and the gain is modest (~10–15%). On H20-3E it is substantial (~30%).
