# DermInsight AI: Source Code (`src/`)

This directory contains the modular Python implementation for training, fine-tuning, threshold optimization, and evaluation of **DenseNet-201** for dermoscopic melanoma classification.

---

## Directory Structure

```
src/
├── README.md                              # This source documentation file
├── densenet201_baseline.py                # Standalone baseline training and evaluation script
├── EXP_01_BASELINE/
│   └── densenet201_baseline.py            # Baseline experiment pipeline (BCE with pos_weight=50.21, threshold=0.5)
└── EXP_02_WEIGHTED_BCE/
    ├── stage2b_weighted_bce.py            # Fine-tuning pipeline with learning rate scheduling & checkpoint saving
    ├── stage2b_final_evaluation.py        # Exhaustive validation threshold sweep & held-out test evaluation
    └── stage2b_visual_results.py          # Publication-grade plotting for ROC, PR, threshold sweeps, and confusion matrices
```

---

## Command-Line Usage

### 1. Training Baseline DenseNet-201 (`EXP_01_BASELINE`)

```bash
python src/EXP_01_BASELINE/densenet201_baseline.py \
    --data_dir data \
    --output_dir results/EXP_01_BASELINE \
    --batch_size 32 \
    --epochs 3 \
    --learning_rate 1e-4 \
    --pos_weight 50.2067 \
    --seed 42
```

### 2. Fine-Tuning with Weighted BCE (`EXP_02_WEIGHTED_BCE`)

```bash
python src/EXP_02_WEIGHTED_BCE/stage2b_weighted_bce.py \
    --data_dir data \
    --checkpoint_dir models/EXP_02_WEIGHTED_BCE \
    --output_dir results/EXP_02_WEIGHTED_BCE \
    --batch_size 64 \
    --epochs 6 \
    --learning_rate 1e-4 \
    --pos_weight 50.2067
```

### 3. Threshold Calibration & Evaluation

```bash
python src/EXP_02_WEIGHTED_BCE/stage2b_final_evaluation.py \
    --model_path models/EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt \
    --data_dir data \
    --output_dir results/EXP_02_WEIGHTED_BCE
```
