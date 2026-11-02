import argparse
import json
import math
import os
import random
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
from torchvision.transforms import InterpolationMode
from torchvision.models import DenseNet201_Weights


SEED = 42
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class DermImageDataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame, image_dir: Path, transform=None):
        self.df = dataframe.reset_index(drop=True)
        self.image_dir = Path(image_dir)
        self.transform = transform

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        row = self.df.iloc[idx]
        image_name = str(row["image_name"]).strip()
        image_path = self.image_dir / f"{image_name}.jpg"
        if not image_path.exists():
            raise FileNotFoundError(f"Missing image file: {image_path}")

        image = Image.open(image_path).convert("RGB")
        if self.transform is not None:
            image = self.transform(image)

        label = float(row["target"])
        return image, label, image_name


class DermInsightDenseNet201(nn.Module):
    def __init__(self):
        super().__init__()
        weights = DenseNet201_Weights.IMAGENET1K_V1
        backbone = models.densenet201(weights=weights)
        self.backbone = backbone
        in_features = backbone.classifier.in_features
        self.backbone.classifier = nn.Identity()
        self.head = nn.Linear(in_features, 1)

    def forward(self, x):
        features = self.backbone(x)
        logits = self.head(features)
        return logits.squeeze(1)


def build_transform(is_train: bool = False):
    if is_train:
        return transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(15, interpolation=InterpolationMode.BILINEAR),
                transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )
    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


def compute_class_weights(train_df: pd.DataFrame) -> torch.Tensor:
    pos_count = int(train_df["target"].sum())
    neg_count = int(len(train_df) - pos_count)
    if pos_count == 0 or neg_count == 0:
        raise ValueError("Each training split must contain both classes.")
    pos_weight = neg_count / pos_count
    return torch.tensor([pos_weight], dtype=torch.float32, device=DEVICE)


def save_json(path: Path, payload: Dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def calculate_binary_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> Dict[str, float]:
    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    has_both_classes = np.unique(y_true).size > 1
    roc_auc = roc_auc_score(y_true, y_prob) if has_both_classes else float("nan")
    avg_precision = average_precision_score(y_true, y_prob) if has_both_classes else float("nan")
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "specificity": specificity,
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc,
        "average_precision": avg_precision,
    }
    return metrics


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, save_path: Path):
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title("Confusion Matrix")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Benign", "Malignant"])
    ax.set_yticklabels(["Benign", "Malignant"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="black" if cm[i, j] < cm.max() else "white")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)


def plot_roc_curve(y_true: np.ndarray, y_prob: np.ndarray, save_path: Path):
    if np.unique(y_true).size <= 1:
        plt.figure(figsize=(6, 5))
        plt.text(0.5, 0.5, "ROC AUC undefined: only one class present", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        return

    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"ROC-AUC = {auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_loss_curve(train_losses: List[float], val_losses: List[float], save_path: Path):
    plt.figure(figsize=(7, 5))
    plt.plot(train_losses, label="Training loss")
    plt.plot(val_losses, label="Validation loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_pr_curve(y_true: np.ndarray, y_prob: np.ndarray, save_path: Path):
    from sklearn.metrics import precision_recall_curve

    if np.unique(y_true).size <= 1:
        plt.figure(figsize=(6, 5))
        plt.text(0.5, 0.5, "PR-AUC undefined: only one class present", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        return

    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    avg_precision = average_precision_score(y_true, y_prob)
    plt.figure(figsize=(6, 5))
    plt.plot(recall, precision, label=f"AP = {avg_precision:.3f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def run_sanity_check(train_df: pd.DataFrame, image_dir: Path, transform, device: torch.device):
    sample_rows = train_df.head(4).copy()
    dataset = DermImageDataset(sample_rows, image_dir, transform=transform)
    loader = DataLoader(dataset, batch_size=2, shuffle=False, num_workers=0)

    model = DermInsightDenseNet201().to(device)
    model.eval()
    criterion = nn.BCEWithLogitsLoss()

    print("\n=== SANITY CHECK: IMAGE LOADING, LABELS, AND FORWARD PASS ===")
    for batch_idx, (images, labels, names) in enumerate(loader):
        print(f"Batch {batch_idx}: images shape={tuple(images.shape)}, labels={labels.cpu().tolist()}, names={list(names)}")
        with torch.no_grad():
            logits = model(images.to(device))
            probs = torch.sigmoid(logits)
            print(f"Output logits shape={tuple(logits.shape)}, probabilities={probs.cpu().numpy().tolist()}")
            loss = criterion(logits, labels.to(device).float())
            print(f"Loss value: {loss.item():.6f}\n")

    return model


def evaluate_model(model: nn.Module, data_loader: DataLoader, criterion: nn.Module, device: torch.device) -> Tuple[float, Dict[str, float], np.ndarray, np.ndarray]:
    model.eval()
    total_loss = 0.0
    all_probs = []
    all_labels = []

    with torch.no_grad():
        for images, labels, _ in data_loader:
            images = images.to(device)
            labels = labels.to(device).float()
            logits = model(images)
            loss = criterion(logits, labels)
            total_loss += loss.item() * images.size(0)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.extend(probs.tolist())
            all_labels.extend(labels.cpu().numpy().astype(int).tolist())

    y_true = np.asarray(all_labels, dtype=int)
    y_prob = np.asarray(all_probs, dtype=float)
    loss = total_loss / len(y_true)
    metrics = calculate_binary_metrics(y_true, y_prob)
    return loss, metrics, y_true, y_prob


def train_model(args):
    set_seed()
    root = Path(__file__).resolve().parents[2]
    train_csv = root / "data" / "processed" / "train.csv"
    val_csv = root / "data" / "processed" / "val.csv"
    test_csv = root / "data" / "processed" / "test.csv"
    image_dir = root / "data" / "raw" / "train_images"

    train_df = pd.read_csv(train_csv)
    val_df = pd.read_csv(val_csv)
    test_df = pd.read_csv(test_csv)

    if args.max_train_samples is not None:
        train_df = train_df.head(args.max_train_samples).copy()
    if args.max_val_samples is not None:
        val_df = val_df.head(args.max_val_samples).copy()

    train_patients = set(train_df["patient_id"].astype(str))
    val_patients = set(val_df["patient_id"].astype(str))
    test_patients = set(test_df["patient_id"].astype(str))
    assert train_patients.isdisjoint(val_patients), "Patient overlap between train and validation"
    assert train_patients.isdisjoint(test_patients), "Patient overlap between train and test"
    assert val_patients.isdisjoint(test_patients), "Patient overlap between validation and test"

    train_dataset = DermImageDataset(train_df, image_dir, transform=build_transform(is_train=True))
    val_dataset = DermImageDataset(val_df, image_dir, transform=build_transform(is_train=False))
    test_dataset = DermImageDataset(test_df, image_dir, transform=build_transform(is_train=False))

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0, pin_memory=False)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0, pin_memory=False)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0, pin_memory=False)

    print(f"Device: {DEVICE}")
    print(f"Train set size: {len(train_df)} | Validation set size: {len(val_df)} | Test set size: {len(test_df)}")
    print(f"Class counts: train benign={int((train_df['target']==0).sum())}, malignant={int((train_df['target']==1).sum())}")

    pos_weight = compute_class_weights(train_df)
    print(f"Weighted binary loss positive class weight: {pos_weight.item():.4f}")

    model = DermInsightDenseNet201().to(DEVICE)
    for name, param in model.named_parameters():
        if "head" not in name:
            param.requires_grad = False

    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)

    if args.sanity_check:
        run_sanity_check(train_df, image_dir, build_transform(is_train=False), DEVICE)

    results_dir = root / "results"
    plots_dir = results_dir / "plots"
    metrics_dir = results_dir / "metrics"
    models_dir = root / "models"
    for d in [plots_dir, metrics_dir, models_dir]:
        d.mkdir(parents=True, exist_ok=True)

    best_auc = -1.0
    best_state = None
    train_losses: List[float] = []
    val_losses: List[float] = []
    val_auc_history: List[float] = []
    val_metrics_history: List[Dict[str, float]] = []

    for epoch in range(args.epochs):
        model.train()
        epoch_loss = 0.0
        for batch_idx, (images, labels, _) in enumerate(train_loader):
            images = images.to(DEVICE)
            labels = labels.to(DEVICE).float()
            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * images.size(0)
            if (batch_idx + 1) % max(1, len(train_loader) // 10) == 0 or batch_idx == len(train_loader) - 1:
                print(f"Epoch {epoch + 1}/{args.epochs} batch {batch_idx + 1}/{len(train_loader)} loss={loss.item():.4f}", flush=True)

        train_loss = epoch_loss / len(train_df)
        train_losses.append(train_loss)

        val_loss, metrics, y_true, y_prob = evaluate_model(model, val_loader, criterion, DEVICE)
        val_losses.append(val_loss)
        val_auc_history.append(metrics["roc_auc"])
        val_metrics_history.append(metrics)
        print(f"Epoch {epoch + 1}/{args.epochs} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_auc={metrics['roc_auc']:.4f} | val_f1={metrics['f1']:.4f}")

        if np.isfinite(metrics["roc_auc"]) and metrics["roc_auc"] > best_auc:
            best_auc = metrics["roc_auc"]
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
            checkpoint_path = models_dir / "densenet201_baseline_best.pt"
            torch.save({"state_dict": best_state, "epoch": epoch + 1, "auc": best_auc}, checkpoint_path)

    if best_state is None:
        best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        print("Warning: no finite validation AUC was observed; using final epoch checkpoint.")

    model.load_state_dict(best_state)
    test_loss, test_metrics, test_true, test_prob = evaluate_model(model, test_loader, criterion, DEVICE)

    y_pred_test = (test_prob >= 0.5).astype(int)
    plot_loss_curve(train_losses, val_losses, plots_dir / "training_validation_loss.png")
    plot_roc_curve(test_true, test_prob, plots_dir / "test_roc_curve.png")
    plot_pr_curve(test_true, test_prob, plots_dir / "test_precision_recall_curve.png")
    plot_confusion_matrix(test_true, y_pred_test, plots_dir / "test_confusion_matrix.png")

    finite_auc_values = [value for value in val_auc_history if np.isfinite(value)]
    if finite_auc_values:
        best_idx = val_auc_history.index(max(finite_auc_values))
        best_val_metrics = val_metrics_history[best_idx]
    elif val_metrics_history:
        best_val_metrics = val_metrics_history[-1]
    else:
        best_val_metrics = {}
    report = {
        "architecture": "DenseNet201 pretrained on ImageNet, final binary classifier replaced with a single-output head",
        "preprocessing": {
            "resize": [224, 224],
            "normalization_mean": [0.485, 0.456, 0.406],
            "normalization_std": [0.229, 0.224, 0.225],
            "training_augmentation": ["RandomHorizontalFlip", "RandomRotation(15°)", "ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05)"]
        },
        "loss_function": "Binary Cross-Entropy with Logits (BCEWithLogitsLoss) with positive class weight",
        "class_imbalance_handling": {
            "method": "Weighted binary loss using positive class weight = negative_count / positive_count",
            "train_positive_count": int((train_df["target"] == 1).sum()),
            "train_negative_count": int((train_df["target"] == 0).sum()),
            "positive_weight": float(pos_weight.item())
        },
        "hyperparameters": {
            "learning_rate": args.learning_rate,
            "batch_size": args.batch_size,
            "epochs": args.epochs,
            "max_train_samples": args.max_train_samples,
            "max_val_samples": args.max_val_samples,
            "optimizer": "AdamW",
            "weight_decay": 1e-4,
            "device": str(DEVICE),
            "seed": SEED,
        },
        "data_splits": {
            "train_size": int(len(train_df)),
            "val_size": int(len(val_df)),
            "test_size": int(len(test_df)),
            "train_positive_fraction": float((train_df["target"] == 1).mean()),
            "val_positive_fraction": float((val_df["target"] == 1).mean()),
            "test_positive_fraction": float((test_df["target"] == 1).mean()),
        },
        "validation_results": best_val_metrics,
        "test_results": test_metrics,
        "train_loss_history": train_losses,
        "val_loss_history": val_losses,
    }

    save_json(metrics_dir / "densenet201_baseline_metrics.json", report)
    save_json(metrics_dir / "densenet201_test_metrics.json", {"test": test_metrics, "test_loss": test_loss})

    print("\n=== FINAL TEST RESULTS ===")
    for k, v in test_metrics.items():
        print(f"{k}: {v:.4f}")
    print(f"Final test loss: {test_loss:.4f}")

    return report


def parse_args():
    parser = argparse.ArgumentParser(description="DenseNet201 image-only baseline for DermInsight AI")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--max-train-samples", type=int, default=None)
    parser.add_argument("--max-val-samples", type=int, default=None)
    parser.add_argument("--sanity-check", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train_model(args)
