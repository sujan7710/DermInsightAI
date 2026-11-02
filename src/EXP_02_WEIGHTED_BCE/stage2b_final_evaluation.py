# ============================================================
# DermInsightAI — EXPERIMENT 02: FINAL TEST EVALUATION
# ============================================================
# Source: DermInsightAI_Stage2B.ipynb
# Extracted from the executed final-evaluation cell.
# ============================================================

# ============================================================
# DERMINSIGHT AI — STAGE 2B FINAL TEST EVALUATION
# ============================================================

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from torchvision.models import DenseNet201_Weights

from PIL import Image

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)

# ============================================================
# 1. PATHS
# ============================================================

PROJECT_DIR = Path("/content/drive/MyDrive/DermInsightAI")

TRAIN_CSV = PROJECT_DIR / "data/processed/train.csv"
VAL_CSV   = PROJECT_DIR / "data/processed/val.csv"
TEST_CSV  = PROJECT_DIR / "data/processed/test.csv"

IMAGE_DIR = Path("/content/isic2020/train-image/image")

MODEL_PATH = PROJECT_DIR / "models/densenet201_stage2b_weighted_bce.pt"

RESULTS_DIR = PROJECT_DIR / "results/EXP_02_WEIGHTED_BCE/final_evaluation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON = RESULTS_DIR / "stage2b_test_evaluation.json"

# ============================================================
# 2. DEVICE
# ============================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 70)
print("STAGE 2B — FINAL TEST EVALUATION")
print("=" * 70)

print("Device:", DEVICE)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print(
        "VRAM:",
        round(
            torch.cuda.get_device_properties(0).total_memory / (1024**3),
            2
        ),
        "GB"
    )

# ============================================================
# 3. CHECK FILES
# ============================================================

print("\nChecking required files...")

required = {
    "Train CSV": TRAIN_CSV,
    "Validation CSV": VAL_CSV,
    "Test CSV": TEST_CSV,
    "Image directory": IMAGE_DIR,
    "Stage 2B checkpoint": MODEL_PATH,
}

for name, path in required.items():
    print(f"{name}: {path.exists()}")

if not VAL_CSV.exists():
    raise FileNotFoundError(f"Validation CSV not found: {VAL_CSV}")

if not TEST_CSV.exists():
    raise FileNotFoundError(f"Test CSV not found: {TEST_CSV}")

if not IMAGE_DIR.exists():
    raise FileNotFoundError(f"Image directory not found: {IMAGE_DIR}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Stage 2B checkpoint not found: {MODEL_PATH}")

# ============================================================
# 4. LOAD CSVs
# ============================================================

val_df = pd.read_csv(VAL_CSV)
test_df = pd.read_csv(TEST_CSV)

print("\nValidation rows:", len(val_df))
print("Validation positives:", int(val_df["target"].sum()))
print("Validation negatives:", int((val_df["target"] == 0).sum()))

print("\nTest rows:", len(test_df))
print("Test positives:", int(test_df["target"].sum()))
print("Test negatives:", int((test_df["target"] == 0).sum()))

# ============================================================
# 5. TRANSFORM
# ============================================================

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ============================================================
# 6. DATASET
# ============================================================

class ISICDataset(Dataset):

    def __init__(self, dataframe, image_dir, transform=None):
        self.df = dataframe.reset_index(drop=True)
        self.image_dir = Path(image_dir)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        row = self.df.iloc[idx]

        image_name = str(row["image_name"])

        # CSV contains names like ISIC_1234567
        # Actual files are .jpg
        if not image_name.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            image_name = image_name + ".jpg"

        image_path = self.image_dir / image_name

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = Image.open(image_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        label = float(row["target"])

        return image, torch.tensor(label, dtype=torch.float32)

# ============================================================
# 7. DATA LOADERS
# ============================================================

val_dataset = ISICDataset(
    val_df,
    IMAGE_DIR,
    transform=test_transform
)

test_dataset = ISICDataset(
    test_df,
    IMAGE_DIR,
    transform=test_transform
)

val_loader = DataLoader(
    val_dataset,
    batch_size=64,
    shuffle=False,
    num_workers=0,
    pin_memory=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=64,
    shuffle=False,
    num_workers=0,
    pin_memory=False
)

print("\nValidation batches:", len(val_loader))
print("Test batches:", len(test_loader))

# ============================================================
# 8. MODEL
# ============================================================

class DenseNet201Baseline(nn.Module):

    def __init__(self):
        super().__init__()

        self.backbone = models.densenet201(
            weights=None
        )

        in_features = self.backbone.classifier.in_features

        self.backbone.classifier = nn.Identity()

        self.head = nn.Linear(
            in_features,
            1
        )

    def forward(self, x):

        features = self.backbone(x)

        return self.head(features)

# ============================================================
# 9. LOAD CHECKPOINT
# ============================================================

print("\nLoading Stage 2B checkpoint...")

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=False
)

print("Checkpoint type:", type(checkpoint))

if isinstance(checkpoint, dict):
    print("Checkpoint keys:", list(checkpoint.keys()))

state_dict = checkpoint["state_dict"]

model = DenseNet201Baseline()

model.load_state_dict(state_dict)

model = model.to(DEVICE)
model.eval()

print("Stage 2B model loaded successfully.")

if isinstance(checkpoint, dict):
    if "epoch" in checkpoint:
        print("Best checkpoint epoch:", checkpoint["epoch"])

    if "auc" in checkpoint:
        print("Stored validation AUC:", checkpoint["auc"])

# ============================================================
# 10. PREDICTION FUNCTION
# ============================================================

def collect_predictions(model, loader):

    all_probs = []
    all_labels = []

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(
                DEVICE,
                non_blocking=True
            )

            logits = model(images).squeeze(1)

            probs = torch.sigmoid(logits)

            all_probs.extend(
                probs.cpu().numpy().tolist()
            )

            all_labels.extend(
                labels.numpy().tolist()
            )

    return (
        np.asarray(all_labels).astype(int),
        np.asarray(all_probs)
    )

# ============================================================
# 11. VALIDATION PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("STEP 1 — VALIDATION THRESHOLD SELECTION")
print("=" * 70)

val_labels, val_probs = collect_predictions(
    model,
    val_loader
)

print("Validation predictions:", len(val_probs))
print("Validation labels:", len(val_labels))

val_auc = roc_auc_score(
    val_labels,
    val_probs
)

val_ap = average_precision_score(
    val_labels,
    val_probs
)

print(f"Validation ROC-AUC: {val_auc:.4f}")
print(f"Validation PR-AUC:  {val_ap:.4f}")

# ============================================================
# 12. SELECT THRESHOLD USING VALIDATION ONLY
# ============================================================

thresholds = np.arange(
    0.01,
    1.00,
    0.01
)

best_threshold = 0.5
best_f1 = -1

threshold_results = []

for threshold in thresholds:

    preds = (
        val_probs >= threshold
    ).astype(int)

    precision = precision_score(
        val_labels,
        preds,
        zero_division=0
    )

    sensitivity = recall_score(
        val_labels,
        preds,
        zero_division=0
    )

    specificity = (
        ((val_labels == 0) & (preds == 0)).sum()
        / max((val_labels == 0).sum(), 1)
    )

    f1 = f1_score(
        val_labels,
        preds,
        zero_division=0
    )

    threshold_results.append({
        "threshold": float(threshold),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "precision": float(precision),
        "f1": float(f1)
    })

    if f1 > best_f1:

        best_f1 = f1
        best_threshold = float(threshold)

best_val_preds = (
    val_probs >= best_threshold
).astype(int)

best_val_cm = confusion_matrix(
    val_labels,
    best_val_preds,
    labels=[0, 1]
)

tn, fp, fn, tp = best_val_cm.ravel()

best_val_sensitivity = tp / max(tp + fn, 1)
best_val_specificity = tn / max(tn + fp, 1)
best_val_precision = tp / max(tp + fp, 1)
best_val_accuracy = (tp + tn) / max(
    tp + tn + fp + fn,
    1
)

print("\nBest validation threshold:", best_threshold)

print("Validation metrics at selected threshold:")
print(f"Sensitivity: {best_val_sensitivity:.4f}")
print(f"Specificity: {best_val_specificity:.4f}")
print(f"Precision:   {best_val_precision:.4f}")
print(f"F1:          {best_f1:.4f}")
print(f"Accuracy:    {best_val_accuracy:.4f}")

print("\nValidation confusion matrix:")
print(best_val_cm)

# ============================================================
# 13. FINAL TEST PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 — FINAL TEST EVALUATION")
print("=" * 70)

print(
    "IMPORTANT: Test set is being evaluated with the "
    "validation-selected threshold:",
    best_threshold
)

test_labels, test_probs = collect_predictions(
    model,
    test_loader
)

print("\nTest predictions:", len(test_probs))
print("Test labels:", len(test_labels))

# ============================================================
# 14. TEST ROC-AUC / PR-AUC
# ============================================================

test_auc = roc_auc_score(
    test_labels,
    test_probs
)

test_ap = average_precision_score(
    test_labels,
    test_probs
)

# ============================================================
# 15. TEST CLASSIFICATION METRICS
# ============================================================

test_preds = (
    test_probs >= best_threshold
).astype(int)

test_cm = confusion_matrix(
    test_labels,
    test_preds,
    labels=[0, 1]
)

tn, fp, fn, tp = test_cm.ravel()

test_sensitivity = tp / max(tp + fn, 1)
test_specificity = tn / max(tn + fp, 1)

test_precision = precision_score(
    test_labels,
    test_preds,
    zero_division=0
)

test_f1 = f1_score(
    test_labels,
    test_preds,
    zero_division=0
)

test_accuracy = accuracy_score(
    test_labels,
    test_preds
)

# ============================================================
# 16. PRINT FINAL RESULTS
# ============================================================

print("\n" + "=" * 70)
print("FINAL STAGE 2B TEST RESULTS")
print("=" * 70)

print(f"Test ROC-AUC:   {test_auc:.4f}")
print(f"Test PR-AUC:    {test_ap:.4f}")
print(f"Threshold:      {best_threshold:.2f}")
print(f"Sensitivity:    {test_sensitivity:.4f}")
print(f"Specificity:    {test_specificity:.4f}")
print(f"Precision:      {test_precision:.4f}")
print(f"F1-score:       {test_f1:.4f}")
print(f"Accuracy:       {test_accuracy:.4f}")

print("\nTest confusion matrix:")
print(test_cm)

print("\nTN:", tn)
print("FP:", fp)
print("FN:", fn)
print("TP:", tp)

# ============================================================
# 17. SAVE RESULTS
# ============================================================

results = {
    "experiment": "stage2b_weighted_bce",

    "checkpoint": str(MODEL_PATH),

    "best_epoch": (
        int(checkpoint["epoch"])
        if isinstance(checkpoint, dict)
        and "epoch" in checkpoint
        else None
    ),

    "validation": {
        "roc_auc": float(val_auc),
        "pr_auc": float(val_ap),
        "selected_threshold": float(best_threshold),
        "sensitivity": float(best_val_sensitivity),
        "specificity": float(best_val_specificity),
        "precision": float(best_val_precision),
        "f1": float(best_f1),
        "accuracy": float(best_val_accuracy),
        "tn": int(best_val_cm[0, 0]),
        "fp": int(best_val_cm[0, 1]),
        "fn": int(best_val_cm[1, 0]),
        "tp": int(best_val_cm[1, 1])
    },

    "test": {
        "roc_auc": float(test_auc),
        "pr_auc": float(test_ap),
        "threshold": float(best_threshold),
        "sensitivity": float(test_sensitivity),
        "specificity": float(test_specificity),
        "precision": float(test_precision),
        "f1": float(test_f1),
        "accuracy": float(test_accuracy),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp)
    },

    "test_samples": int(len(test_labels)),
    "test_positive": int(test_labels.sum()),
    "test_negative": int((test_labels == 0).sum())
}

with open(
    OUTPUT_JSON,
    "w"
) as f:
    json.dump(
        results,
        f,
        indent=2
    )

print("\nResults saved to:")
print(OUTPUT_JSON)

print("\n" + "=" * 70)
print("TEST EVALUATION COMPLETE")
print("=" * 70)