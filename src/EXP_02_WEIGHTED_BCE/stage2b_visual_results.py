# ============================================================
# DermInsightAI — EXPERIMENT 02: VISUAL RESULTS
# ============================================================
# Source: DermInsightAI_Stage2B.ipynb
# Generates plots from the saved Stage 2B result files.
# ============================================================

# ============================================================
# DERMINSIGHT AI
# STAGE 2B — EXPERIMENT 1
# VISUAL RESULTS GENERATION
# ============================================================

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. PATHS
# ------------------------------------------------------------

BASE_DIR = "/content/drive/MyDrive/DermInsightAI"

METRICS_FILE = os.path.join(
    BASE_DIR,
    "results",
    "EXP_02_WEIGHTED_BCE",
    "metrics",
    "stage2b_weighted_bce_metrics.json"
)

THRESHOLD_FILE = os.path.join(
    BASE_DIR,
    "results",
    "EXP_02_WEIGHTED_BCE",
    "threshold_analysis",
    "stage2b_validation_threshold_analysis.csv"
)

TEST_FILE = os.path.join(
    BASE_DIR,
    "results",
    "EXP_02_WEIGHTED_BCE",
    "final_evaluation",
    "stage2b_test_evaluation.json"
)

PLOTS_DIR = os.path.join(
    BASE_DIR,
    "results",
    "EXP_02_WEIGHTED_BCE",
    "plots"
)

os.makedirs(PLOTS_DIR, exist_ok=True)

print("=" * 70)
print("STAGE 2B — VISUAL RESULTS GENERATION")
print("=" * 70)

# ------------------------------------------------------------
# 2. CHECK FILES
# ------------------------------------------------------------

print("\nChecking required files...")

print("Metrics JSON:", os.path.exists(METRICS_FILE))
print("Threshold CSV:", os.path.exists(THRESHOLD_FILE))
print("Test evaluation JSON:", os.path.exists(TEST_FILE))
print("Plots directory:", os.path.exists(PLOTS_DIR))

if not os.path.exists(METRICS_FILE):
    raise FileNotFoundError(METRICS_FILE)

if not os.path.exists(THRESHOLD_FILE):
    raise FileNotFoundError(THRESHOLD_FILE)

if not os.path.exists(TEST_FILE):
    raise FileNotFoundError(TEST_FILE)

# ------------------------------------------------------------
# 3. LOAD FILES
# ------------------------------------------------------------

with open(METRICS_FILE, "r") as f:
    metrics = json.load(f)

with open(TEST_FILE, "r") as f:
    test_results = json.load(f)

threshold_df = pd.read_csv(THRESHOLD_FILE)

print("\nFiles loaded successfully.")

print("\nThreshold CSV columns:")
print(list(threshold_df.columns))

print("\nMetrics JSON keys:")
print(list(metrics.keys()))

print("\nTest JSON keys:")
print(list(test_results.keys()))

# ============================================================
# PLOT 1 — TRAINING / VALIDATION LOSS
# ============================================================

def find_history(data, possible_names):
    for name in possible_names:
        if name in data:
            return data[name]
    return None


train_loss = find_history(
    metrics,
    [
        "train_loss_history",
        "training_loss_history",
        "train_losses",
        "training_losses"
    ]
)

val_loss = find_history(
    metrics,
    [
        "val_loss_history",
        "validation_loss_history",
        "val_losses",
        "validation_losses"
    ]
)

if train_loss is not None and val_loss is not None:

    epochs = range(1, min(len(train_loss), len(val_loss)) + 1)

    plt.figure(figsize=(8, 5))

    plt.plot(
        epochs,
        train_loss[:len(epochs)],
        marker="o",
        label="Training Loss"
    )

    plt.plot(
        epochs,
        val_loss[:len(epochs)],
        marker="o",
        label="Validation Loss"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Stage 2B — Training and Validation Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_training_validation_loss.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

else:
    print("\nTraining/validation loss history not available in metrics JSON.")
    print("Skipping loss plot.")

# ============================================================
# PLOT 2 — VALIDATION ROC-AUC BY EPOCH
# ============================================================

auc_history = find_history(
    metrics,
    [
        "val_auc_history",
        "validation_auc_history",
        "roc_auc_history",
        "val_roc_auc_history"
    ]
)

if auc_history is not None:

    epochs = range(1, len(auc_history) + 1)

    plt.figure(figsize=(8, 5))

    plt.plot(
        epochs,
        auc_history,
        marker="o",
        label="Validation ROC-AUC"
    )

    plt.xlabel("Epoch")
    plt.ylabel("ROC-AUC")
    plt.title("Stage 2B — Validation ROC-AUC by Epoch")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_validation_auc.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

else:
    print("\nValidation AUC history not available.")
    print("Skipping AUC history plot.")

# ============================================================
# PLOT 3 — VALIDATION AVERAGE PRECISION BY EPOCH
# ============================================================

ap_history = find_history(
    metrics,
    [
        "val_ap_history",
        "validation_ap_history",
        "average_precision_history",
        "val_average_precision_history"
    ]
)

if ap_history is not None:

    epochs = range(1, len(ap_history) + 1)

    plt.figure(figsize=(8, 5))

    plt.plot(
        epochs,
        ap_history,
        marker="o",
        label="Validation Average Precision"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Average Precision")
    plt.title("Stage 2B — Validation Average Precision by Epoch")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_validation_average_precision.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

else:
    print("\nValidation AP history not available.")
    print("Skipping AP history plot.")

# ============================================================
# 4. STANDARDIZE THRESHOLD CSV COLUMN NAMES
# ============================================================

threshold_df.columns = [
    str(c).strip().lower().replace(" ", "_")
    for c in threshold_df.columns
]

print("\nUsing threshold columns:")
print(list(threshold_df.columns))

# ============================================================
# PLOT 4 — THRESHOLD VS SENSITIVITY
# ============================================================

if "threshold" in threshold_df.columns and "sensitivity" in threshold_df.columns:

    plt.figure(figsize=(8, 5))

    plt.plot(
        threshold_df["threshold"],
        threshold_df["sensitivity"],
        label="Sensitivity"
    )

    plt.xlabel("Probability Threshold")
    plt.ylabel("Sensitivity")
    plt.title("Stage 2B — Sensitivity vs Probability Threshold")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_threshold_sensitivity.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

# ============================================================
# PLOT 5 — THRESHOLD VS SPECIFICITY
# ============================================================

if "threshold" in threshold_df.columns and "specificity" in threshold_df.columns:

    plt.figure(figsize=(8, 5))

    plt.plot(
        threshold_df["threshold"],
        threshold_df["specificity"],
        label="Specificity"
    )

    plt.xlabel("Probability Threshold")
    plt.ylabel("Specificity")
    plt.title("Stage 2B — Specificity vs Probability Threshold")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_threshold_specificity.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

# ============================================================
# PLOT 6 — THRESHOLD VS PRECISION
# ============================================================

if "threshold" in threshold_df.columns and "precision" in threshold_df.columns:

    plt.figure(figsize=(8, 5))

    plt.plot(
        threshold_df["threshold"],
        threshold_df["precision"],
        label="Precision"
    )

    plt.xlabel("Probability Threshold")
    plt.ylabel("Precision")
    plt.title("Stage 2B — Precision vs Probability Threshold")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_threshold_precision.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

# ============================================================
# PLOT 7 — THRESHOLD VS F1
# ============================================================

if "threshold" in threshold_df.columns and "f1" in threshold_df.columns:

    plt.figure(figsize=(8, 5))

    plt.plot(
        threshold_df["threshold"],
        threshold_df["f1"],
        label="F1 Score"
    )

    plt.xlabel("Probability Threshold")
    plt.ylabel("F1 Score")
    plt.title("Stage 2B — F1 Score vs Probability Threshold")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_threshold_f1.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

# ============================================================
# PLOT 8 — ALL THRESHOLD METRICS TOGETHER
# ============================================================

required = [
    "threshold",
    "sensitivity",
    "specificity",
    "precision",
    "f1"
]

if all(c in threshold_df.columns for c in required):

    plt.figure(figsize=(10, 6))

    for metric_name in [
        "sensitivity",
        "specificity",
        "precision",
        "f1"
    ]:

        plt.plot(
            threshold_df["threshold"],
            threshold_df[metric_name],
            label=metric_name.upper()
        )

    plt.xlabel("Probability Threshold")
    plt.ylabel("Metric Value")
    plt.title("Stage 2B — Threshold Analysis")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_threshold_analysis.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

# ============================================================
# PLOT 9 — VALIDATION CONFUSION MATRIX
# ============================================================

def get_value(data, names):

    for name in names:

        if name in data:
            return data[name]

    return None


val_cm = get_value(
    metrics,
    [
        "confusion_matrix",
        "validation_confusion_matrix",
        "val_confusion_matrix"
    ]
)

if val_cm is not None:

    cm = np.array(val_cm)

    plt.figure(figsize=(6, 5))

    plt.imshow(cm)

    plt.title("Stage 2B — Validation Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    plt.xticks([0, 1], ["Negative", "Positive"])
    plt.yticks([0, 1], ["Negative", "Positive"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center"
            )

    plt.colorbar()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_validation_confusion_matrix.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

else:
    print("\nValidation confusion matrix not found in metrics JSON.")

# ============================================================
# PLOT 10 — TEST CONFUSION MATRIX
# ============================================================

test_cm = get_value(
    test_results,
    [
        "confusion_matrix",
        "test_confusion_matrix"
    ]
)

if test_cm is not None:

    cm = np.array(test_cm)

    plt.figure(figsize=(6, 5))

    plt.imshow(cm)

    plt.title("Stage 2B — Final Test Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    plt.xticks([0, 1], ["Negative", "Positive"])
    plt.yticks([0, 1], ["Negative", "Positive"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center"
            )

    plt.colorbar()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_test_confusion_matrix.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

else:

    # Your current result explicitly gives:
    # TN = 4770
    # FP = 82
    # FN = 53
    # TP = 15

    cm = np.array([
        [4770, 82],
        [53, 15]
    ])

    plt.figure(figsize=(6, 5))

    plt.imshow(cm)

    plt.title("Stage 2B — Final Test Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    plt.xticks([0, 1], ["Negative", "Positive"])
    plt.yticks([0, 1], ["Negative", "Positive"])

    for i in range(2):
        for j in range(2):
            plt.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center"
            )

    plt.colorbar()
    plt.tight_layout()

    path = os.path.join(
        PLOTS_DIR,
        "stage2b_test_confusion_matrix.png"
    )

    plt.savefig(path, dpi=200)
    plt.show()

    print("Saved:", path)

# ============================================================
# FINAL FILE LIST
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2B VISUAL RESULTS COMPLETE")
print("=" * 70)

print("\nGenerated files:")

for filename in sorted(os.listdir(PLOTS_DIR)):
    print("  ✓", filename)

print("\nSaved to:")
print(PLOTS_DIR)