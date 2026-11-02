# ============================================================
# DermInsightAI — EXPERIMENT 02: WEIGHTED BCE
# ============================================================
# Source: DermInsightAI_Stage2B.ipynb
# This is the actual Stage 2B training pipeline extracted from
# the executed Colab notebook.
#
# The experiment methodology is preserved.
# Paths are organized for the final Drive project structure.
# ============================================================

# ============================================================
# DERMINSIGHT AI — STAGE 2B EXPERIMENT 1
# CORRECTED VERSION
#
# Uses:
#   CSVs       -> Google Drive
#   Images     -> Kaggle dataset currently in Colab
#   Model      -> existing baseline checkpoint
#
# Baseline checkpoint is NOT overwritten.
# ============================================================

import os
import json
import copy
import random
import numpy as np
import pandas as pd

from pathlib import Path
from PIL import Image

import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader

from torchvision import transforms
from torchvision import models

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score
)

# ============================================================
# 1. REPRODUCIBILITY
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_DIR = Path(
    "/content/drive/MyDrive/DermInsightAI"
)

# CSVs are on Drive
TRAIN_CSV = PROJECT_DIR / "data/processed/train.csv"
VAL_CSV = PROJECT_DIR / "data/processed/val.csv"

# IMPORTANT:
# Images are taken directly from the Kaggle dataset.
IMAGE_DIR = Path(
    "/content/isic2020/train-image/image"
)

# Existing baseline model
BASELINE_MODEL = (
    PROJECT_DIR /
    "models/densenet201_baseline_best.pt"
)

# New Stage 2B outputs
MODELS_DIR = PROJECT_DIR / "models"
RESULTS_DIR = PROJECT_DIR / "results/EXP_02_WEIGHTED_BCE/metrics"

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RESULTS_DIR = PROJECT_DIR / "results/EXP_02_WEIGHTED_BCE/metrics"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MODELS_DIR = PROJECT_DIR / "models/EXP_02_WEIGHTED_BCE"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

STAGE2B_MODEL = (
    MODELS_DIR /
    "densenet201_stage2b_weighted_bce.pt"
)

STAGE2B_METRICS = (
    RESULTS_DIR /
    "stage2b_weighted_bce_metrics.json"
)


# ============================================================
# 3. DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("STAGE 2B — EXPERIMENT 1")
print("=" * 70)

print("Device:", DEVICE)

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )

    print(
        "VRAM:",
        round(
            torch.cuda.get_device_properties(
                0
            ).total_memory / 1024**3,
            2
        ),
        "GB"
    )


# ============================================================
# 4. CHECK FILES
# ============================================================

print("\nChecking required files...")

print(
    "Train CSV:",
    TRAIN_CSV.exists()
)

print(
    "Validation CSV:",
    VAL_CSV.exists()
)

print(
    "Kaggle image directory:",
    IMAGE_DIR.exists()
)

print(
    "Baseline checkpoint:",
    BASELINE_MODEL.exists()
)

if not TRAIN_CSV.exists():
    raise FileNotFoundError(
        f"Train CSV missing: {TRAIN_CSV}"
    )

if not VAL_CSV.exists():
    raise FileNotFoundError(
        f"Validation CSV missing: {VAL_CSV}"
    )

if not IMAGE_DIR.exists():
    raise FileNotFoundError(
        f"Kaggle image directory missing: {IMAGE_DIR}"
    )

if not BASELINE_MODEL.exists():
    raise FileNotFoundError(
        f"Baseline checkpoint missing: {BASELINE_MODEL}"
    )


# ============================================================
# 5. LOAD CSVs
# ============================================================

train_df = pd.read_csv(TRAIN_CSV)
val_df = pd.read_csv(VAL_CSV)

print("\nTrain rows:", len(train_df))
print("Validation rows:", len(val_df))

print(
    "Train positives:",
    int(train_df["target"].sum())
)

print(
    "Train negatives:",
    int(
        (train_df["target"] == 0).sum()
    )
)

print(
    "Validation positives:",
    int(val_df["target"].sum())
)

print(
    "Validation negatives:",
    int(
        (val_df["target"] == 0).sum()
    )
)


# ============================================================
# 6. VERIFY TRAIN + VALIDATION IMAGES
# ============================================================

print("\nChecking image availability...")

def image_path_from_name(name):

    name = str(name)

    if not name.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):
        name += ".jpg"

    return IMAGE_DIR / name


train_missing = []

for name in train_df["image_name"]:

    path = image_path_from_name(name)

    if not path.exists():
        train_missing.append(str(name))

val_missing = []

for name in val_df["image_name"]:

    path = image_path_from_name(name)

    if not path.exists():
        val_missing.append(str(name))


print(
    "Train missing:",
    len(train_missing)
)

print(
    "Validation missing:",
    len(val_missing)
)

if train_missing:

    print(
        "First missing train images:",
        train_missing[:10]
    )

    raise FileNotFoundError(
        "Some training images are missing from Kaggle dataset."
    )

if val_missing:

    print(
        "First missing validation images:",
        val_missing[:10]
    )

    raise FileNotFoundError(
        "Some validation images are missing from Kaggle dataset."
    )

print(
    "All required train/validation images found."
)


# ============================================================
# 7. TRANSFORMS
# SAME AS BASELINE
# ============================================================

train_transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        15,
        interpolation=transforms.InterpolationMode.BILINEAR
    ),

    transforms.ColorJitter(
        brightness=0.1,
        contrast=0.1,
        saturation=0.1,
        hue=0.05
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


val_transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# 8. DATASET
# ============================================================

class ISICDataset(Dataset):

    def __init__(
        self,
        dataframe,
        image_dir,
        transform=None
    ):

        self.df = dataframe.reset_index(
            drop=True
        )

        self.image_dir = Path(
            image_dir
        )

        self.transform = transform


    def __len__(self):

        return len(self.df)


    def __getitem__(self, idx):

        row = self.df.iloc[idx]

        image_name = str(
            row["image_name"]
        )

        if not image_name.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            image_name += ".jpg"

        image_path = (
            self.image_dir /
            image_name
        )

        image = Image.open(
            image_path
        ).convert("RGB")

        if self.transform is not None:

            image = self.transform(
                image
            )

        label = torch.tensor(
            float(row["target"]),
            dtype=torch.float32
        )

        return image, label


# ============================================================
# 9. DATASETS + LOADERS
# ============================================================

train_dataset = ISICDataset(
    train_df,
    IMAGE_DIR,
    transform=train_transform
)

val_dataset = ISICDataset(
    val_df,
    IMAGE_DIR,
    transform=val_transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=0,
    pin_memory=False
)

val_loader = DataLoader(
    val_dataset,
    batch_size=64,
    shuffle=False,
    num_workers=0,
    pin_memory=False
)

print("\nTrain batches:", len(train_loader))
print("Validation batches:", len(val_loader))


# ============================================================
# 10. MODEL
#
# IMPORTANT:
# weights=None because the existing checkpoint already
# contains the trained DenseNet201 weights.
# ============================================================

class DenseNet201Baseline(nn.Module):

    def __init__(self):

        super().__init__()

        backbone = models.densenet201(
            weights=None
        )

        in_features = (
            backbone.classifier.in_features
        )

        backbone.classifier = nn.Identity()

        self.backbone = backbone

        self.head = nn.Linear(
            in_features,
            1
        )


    def forward(self, x):

        features = self.backbone(x)

        logits = self.head(
            features
        )

        return logits


model = DenseNet201Baseline()


# ============================================================
# 11. LOAD EXISTING BASELINE
# ============================================================

print(
    "\nLoading existing baseline checkpoint..."
)

checkpoint = torch.load(
    BASELINE_MODEL,
    map_location="cpu"
)

print(
    "Checkpoint keys:",
    list(checkpoint.keys())
)

state_dict = checkpoint[
    "state_dict"
]

model.load_state_dict(
    state_dict
)

model = model.to(DEVICE)

print(
    "Baseline checkpoint loaded successfully."
)

print(
    "Original best epoch:",
    checkpoint.get(
        "epoch",
        "unknown"
    )
)

print(
    "Original validation AUC:",
    checkpoint.get(
        "auc",
        "unknown"
    )
)


# ============================================================
# 12. CLASS WEIGHT
# SAME AS BASELINE
# ============================================================

positive_count = int(
    train_df["target"].sum()
)

negative_count = int(
    (train_df["target"] == 0).sum()
)

pos_weight_value = (
    negative_count /
    positive_count
)

pos_weight = torch.tensor(
    [pos_weight_value],
    dtype=torch.float32,
    device=DEVICE
)

print(
    "\nPositive class weight:",
    round(
        pos_weight_value,
        4
    )
)


# ============================================================
# 13. LOSS + OPTIMIZER
# ============================================================

criterion = nn.BCEWithLogitsLoss(
    pos_weight=pos_weight
)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-4,
    weight_decay=1e-4
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=1,
    min_lr=1e-6
)


# ============================================================
# 14. VALIDATION
# ============================================================

def evaluate(
    model,
    loader
):

    model.eval()

    total_loss = 0.0

    probabilities = []
    labels_all = []

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(
                DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                DEVICE,
                non_blocking=True
            )

            logits = model(
                images
            ).squeeze(1)

            loss = criterion(
                logits,
                labels
            )

            probs = torch.sigmoid(
                logits
            )

            total_loss += (
                loss.item() *
                images.size(0)
            )

            probabilities.extend(
                probs.cpu().numpy()
            )

            labels_all.extend(
                labels.cpu().numpy()
            )

    probabilities = np.asarray(
        probabilities
    )

    labels_all = np.asarray(
        labels_all
    )

    average_loss = (
        total_loss /
        len(loader.dataset)
    )

    auc = roc_auc_score(
        labels_all,
        probabilities
    )

    ap = average_precision_score(
        labels_all,
        probabilities
    )

    return (
        average_loss,
        auc,
        ap
    )


# ============================================================
# 15. TRAIN
# ============================================================

MAX_EPOCHS = 8

EARLY_STOPPING_PATIENCE = 3

best_auc = -1.0
best_epoch = 0

epochs_without_improvement = 0

best_state = None

history = []

print("\n")
print("=" * 70)
print("STARTING STAGE 2B TRAINING")
print("=" * 70)


for epoch in range(
    1,
    MAX_EPOCHS + 1
):

    model.train()

    running_loss = 0.0

    for batch_idx, (
        images,
        labels
    ) in enumerate(
        train_loader
    ):

        images = images.to(
            DEVICE,
            non_blocking=True
        )

        labels = labels.to(
            DEVICE,
            non_blocking=True
        )

        optimizer.zero_grad(
            set_to_none=True
        )

        logits = model(
            images
        ).squeeze(1)

        loss = criterion(
            logits,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item() *
            images.size(0)
        )

        if (
            (batch_idx + 1) %
            max(
                1,
                len(train_loader) // 10
            ) == 0
            or
            batch_idx ==
            len(train_loader) - 1
        ):

            print(
                f"Epoch {epoch}/{MAX_EPOCHS} "
                f"Batch {batch_idx + 1}/{len(train_loader)} "
                f"Loss={loss.item():.4f}",
                flush=True
            )


    train_loss = (
        running_loss /
        len(train_loader.dataset)
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    val_loss, val_auc, val_ap = evaluate(
        model,
        val_loader
    )


    current_lr = (
        optimizer.param_groups[0]["lr"]
    )


    scheduler.step(
        val_auc
    )


    history.append({

        "epoch": epoch,

        "train_loss": train_loss,

        "val_loss": val_loss,

        "val_auc": val_auc,

        "val_ap": val_ap,

        "learning_rate": current_lr
    })


    print("\n")
    print("-" * 70)

    print(
        f"Epoch {epoch}/{MAX_EPOCHS}"
    )

    print(
        f"Train loss: {train_loss:.4f}"
    )

    print(
        f"Validation loss: {val_loss:.4f}"
    )

    print(
        f"Validation ROC-AUC: {val_auc:.4f}"
    )

    print(
        f"Validation AP: {val_ap:.4f}"
    )

    print(
        f"Learning rate: {current_lr:.7f}"
    )


    # --------------------------------------------------------
    # BEST MODEL
    # --------------------------------------------------------

    if val_auc > best_auc:

        best_auc = val_auc

        best_epoch = epoch

        epochs_without_improvement = 0

        best_state = copy.deepcopy(
            model.state_dict()
        )

        torch.save(
            {
                "state_dict": best_state,
                "epoch": epoch,
                "auc": best_auc,
                "experiment":
                    "stage2b_weighted_bce"
            },
            STAGE2B_MODEL
        )

        print(
            f"NEW BEST MODEL SAVED — "
            f"AUC={best_auc:.4f}"
        )

    else:

        epochs_without_improvement += 1

        print(
            "No validation AUC improvement."
        )


    # --------------------------------------------------------
    # EARLY STOPPING
    # --------------------------------------------------------

    if (
        epochs_without_improvement
        >= EARLY_STOPPING_PATIENCE
    ):

        print(
            "\nEarly stopping triggered."
        )

        break


# ============================================================
# 16. SAVE METRICS
# ============================================================

baseline_auc = float(
    checkpoint.get(
        "auc",
        float("nan")
    )
)

metrics_output = {

    "experiment":
        "stage2b_weighted_bce",

    "baseline_validation_auc":
        baseline_auc,

    "best_validation_auc":
        float(best_auc),

    "best_epoch":
        int(best_epoch),

    "improvement":
        float(
            best_auc - baseline_auc
        ),

    "max_epochs":
        MAX_EPOCHS,

    "batch_size":
        64,

    "learning_rate":
        1e-4,

    "weight_decay":
        1e-4,

    "positive_class_weight":
        float(pos_weight_value),

    "history":
        history
}


with open(
    STAGE2B_METRICS,
    "w"
) as f:

    json.dump(
        metrics_output,
        f,
        indent=2
    )


# ============================================================
# 17. FINAL RESULT
# ============================================================

print("\n")
print("=" * 70)
print("STAGE 2B EXPERIMENT 1 COMPLETE")
print("=" * 70)

print(
    f"Baseline validation AUC: "
    f"{baseline_auc:.4f}"
)

print(
    f"Stage 2B best validation AUC: "
    f"{best_auc:.4f}"
)

print(
    f"Best epoch: "
    f"{best_epoch}"
)

print(
    f"Improvement: "
    f"{best_auc - baseline_auc:+.4f}"
)

print("\nModel saved to:")
print(STAGE2B_MODEL)

print("\nMetrics saved to:")
print(STAGE2B_METRICS)

print(
    "\nBaseline checkpoint was NOT modified."
)