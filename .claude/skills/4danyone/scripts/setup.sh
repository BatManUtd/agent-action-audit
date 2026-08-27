#!/usr/bin/env bash
# Install ant-research/4DAnyone into a target directory.
#
# Idempotent: safe to re-run after a partial failure. Each step is skipped if it
# has already succeeded, so a failed pip install or an interrupted download can
# be resumed by simply running this again.
#
# Usage: bash setup.sh [install_dir]        (default: ~/4DAnyone)

set -euo pipefail

INSTALL_DIR="${1:-$HOME/4DAnyone}"
REPO_URL="https://github.com/ant-research/4DAnyone.git"
ENV_NAME="4danyone"

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
die() { printf '\n\033[31merror: %s\033[0m\n' "$*" >&2; exit 1; }

command -v git >/dev/null   || die "git is not installed."
command -v conda >/dev/null || die "conda is not on PATH. Install Miniconda/Miniforge first."

say "Checking GPU"
if command -v nvidia-smi >/dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
    echo "4DAnyone peaks at ~43.3 GiB of CUDA allocation; ~48 GB of VRAM is the practical floor."
else
    echo "warning: nvidia-smi not found. 4DAnyone requires a CUDA GPU; there is no CPU path."
fi

say "Cloning into $INSTALL_DIR"
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Already cloned; leaving the working tree untouched."
else
    git clone "$REPO_URL" "$INSTALL_DIR"
fi
cd "$INSTALL_DIR"

say "Initializing the GVHMR submodule"
# inference.py fails with an AssetError unless third_party/GVHMR/hmr4d exists.
git submodule update --init third_party/GVHMR

say "Creating the '$ENV_NAME' conda environment (Python 3.11)"
if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    echo "Environment already exists; reusing it."
else
    conda create -n "$ENV_NAME" python=3.11 -y
fi

# `conda activate` needs the shell hook when running from a non-interactive script.
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

say "Installing requirements"
pip install -r requirements.txt

say "Pre-fetching public model weights and the example clip"
python scripts/download_model.py
python scripts/download_example.py

say "Installing SMPL-X (separately licensed)"
# SMPL-X is not on Hugging Face. The downloader prompts for the credentials of
# an account registered at https://smpl-x.is.tue.mpg.de/, so it needs a real TTY.
if [ -t 0 ]; then
    python scripts/download_smplx.py
else
    cat <<MSG
Skipped: this shell is not interactive and the SMPL-X download prompts for
credentials from https://smpl-x.is.tue.mpg.de/.

Finish it yourself in a terminal before running inference:

    conda activate 4danyone
    cd "$INSTALL_DIR"
    python scripts/download_smplx.py

Without it, inference fails with an AssetError.
MSG
fi

say "Done"
cat <<MSG
Installed at: $INSTALL_DIR

Smoke test (~12 min on an A6000-class GPU):

    conda activate $ENV_NAME
    cd "$INSTALL_DIR"
    PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \\
    python inference.py \\
        --video_path "data/source/pexels/2785536-uhd_2160_3840_25fps.mp4" \\
        --views_per_layer 6

Output lands in data/fdanyone/<clip>/videos/dense/.
MSG
