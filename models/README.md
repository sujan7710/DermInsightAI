# DermInsight AI: Trained Model Checkpoints

This directory houses the five verified deep transfer learning checkpoints based on **DenseNet-201** pre-trained on ImageNet-1K (`DenseNet201_Weights.IMAGENET1K_V1`).

---

## Checkpoint Registry

| Experiment Directory | Checkpoint Filename | File Size | Epochs Completed | Best Epoch | Best Val ROC-AUC | Imbalance Strategy |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| `EXP_01_BASELINE` | `densenet201_baseline_best.pt` | 70.30 MB | 3 | 3 | 0.8472 | Weighted BCE ($w_{pos}=50.21$) |
| `EXP_02_WEIGHTED_BCE` | `densenet201_stage2b_weighted_bce.pt` | 70.38 MB | 6 | 3 | 0.9188 | Weighted BCE + Threshold Opt ($\tau=0.86$) |
| `EXP_03_WEIGHTED_SAMPLER` | `densenet201_weighted_sampler_best.pt` | 70.36 MB | 5 | 2 | 0.9062 | PyTorch `WeightedRandomSampler` |
| `EXP_04_FOCAL_LOSS` | `densenet201_focal_loss_best.pt` | 70.35 MB | 5 | 5 | 0.9181 | Lin et al. Focal Loss ($\alpha=0.75, \gamma=2.0$) |
| `EXP_05_RANDOM_OVERSAMPLING` | `densenet201_random_oversampling_best.pt` | 208.96 MB | 5 | 2 | 0.9082 | Training-only Random Oversampling |

*Note on File Sizes:* Model checkpoints are tracked via **Git LFS** (`.gitattributes`). Ensure Git LFS is installed (`git lfs install && git lfs pull`) when cloning this repository.

---

## How to Load a Checkpoint in PyTorch

```python
import torch
from torchvision import models

# 1. Initialize DenseNet-201 backbone
model = models.densenet201(weights=None)
num_features = model.classifier.in_features
model.classifier = torch.nn.Linear(num_features, 1)

# 2. Load trained checkpoint weights
checkpoint_path = "models/EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt"
checkpoint = torch.load(checkpoint_path, map_location="cpu")

# Handle state_dict wrapper if present
if "model_state_dict" in checkpoint:
    model.load_state_dict(checkpoint["model_state_dict"])
elif "state_dict" in checkpoint:
    model.load_state_dict(checkpoint["state_dict"])
else:
    model.load_state_dict(checkpoint)

model.eval()
print(f"Successfully loaded checkpoint from {checkpoint_path}")
```
