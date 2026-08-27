# Upstream provenance

- **Repository**: <https://github.com/ant-research/4DAnyone>
- **Project page**: <https://4danyone.github.io/>
- **Paper**: <https://arxiv.org/abs/2608.20335>
- **License**: Apache-2.0 (the 4DAnyone code). SMPL-X is licensed separately by
  the Max Planck Institute and requires a registered account at
  <https://smpl-x.is.tue.mpg.de/>; its license governs downstream use of any
  output derived from it. GVHMR and BiRefNet carry their own licenses.

## What ships where

| Asset | Source | Gated? |
|---|---|---|
| 4DAnyone checkpoints | Hugging Face | No — auto-downloaded on first use |
| BiRefNet foreground model | Hugging Face | No |
| Example clips | Hugging Face | No |
| GVHMR | Git submodule `third_party/GVHMR` | No — but must be initialized explicitly |
| SMPL-X (`SMPLX_NEUTRAL.npz`) | smpl-x.is.tue.mpg.de | **Yes** — interactive credentialed download |

## Known limitations

Stated by the authors, worth repeating to users before they invest a run:

- Low-memory inference (<32 GB VRAM) is a TODO, not a supported mode.
- TensorRT and sparse-attention acceleration are a TODO.
- No open-source 4DGS reconstruction path ships with the repo. The public
  Nerfstudio guide reconstructs a static 3DGS from one timestamp; the paper's
  FreeTimeGS implementation is not released.
- The input contract (121+ frames, 9:16, ≥720p, one person, mild camera motion)
  is a hard constraint of the trained model, not a configurable preference.

## Citation

```bibtex
@article{jin2026fdanyone,
  title={4DAnyone: Create Anyone in 4D from a Casual Monocular Video},
  author={Jin, Yudong and Xie, Tao and Zhang, Qihang and Shen, Zehong and Xu, Zhen and Shen, Yujun and Bao, Hujun and Zhou, Xiaowei and Xu, Yinghao},
  journal={arXiv preprint arXiv:2608.20335},
  year={2026},
  url={https://arxiv.org/abs/2608.20335}
}
```

## Ethical note

This model generates photorealistic novel views of a real person from a single
video. Use it on footage you have the rights to and the subject's consent for.
Decline requests to synthesize new viewpoints of an identifiable person who has
not consented — that is the same category as any other likeness synthesis, and
"it's only a camera angle" does not change it.
