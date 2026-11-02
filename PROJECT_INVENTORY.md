# PROJECT INVENTORY AND RESEARCH AUDIT: DERMINSIGHT AI
**Project Title:** AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER  
**Application / Research Prototype Name:** DermInsight AI  
**Course:** BCSE497J — Project-I  
**Degree:** B.Tech in Computer Science and Engineering  
**School:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Vellore  
**Authors:**
- Sujan M. (Reg. No: 23BCE2002)
- Ramachandran Sivasankar (Reg. No: 23BCE2107)
- Alan John Anand (Reg. No: 23BCB0165)
**Faculty Guide:** Dr. Krishna Rani Samal  
**Audit Date:** October 2026  

---

## 1. Actual Project Root and Accessible Workspaces

- **Top-level Workspace Root:** `C:\Users\sujan\Downloads\DermInsightAI-20261026T173409Z-1-001`
- **Active Project Root:** `C:\Users\sujan\Downloads\DermInsightAI-20261026T173409Z-1-001\DermInsightAI`
- **Execution Environment:** Windows 11, PowerShell, Python 3.12, PyTorch 2.x, scikit-learn, torchvision.

---

## 2. Accessible Directories

```
DermInsightAI/
├── data/
│   ├── processed/
│   │   ├── train.csv (22,787 records, 1,439 patients)
│   │   ├── val.csv (5,419 records, 307 patients)
│   │   └── test.csv (4,920 records, 310 patients)
│   └── raw/
│       ├── ISIC_2020_Training_GroundTruth.csv (33,126 records)
│       ├── ISIC_2020_Training_GroundTruth_v2.csv (33,126 records, includes lesion_id)
│       └── train_images/ (3,496 JPEG image samples locally accessible)
├── documentation/
│   └── organization_manifest.json (Cryptographic SHA-256 manifest of organized Colab/Drive artifacts)
├── models/
│   ├── EXP_01_BASELINE/densenet201_baseline_best.pt (70.30 MB)
│   ├── EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt (70.38 MB)
│   ├── EXP_03_WEIGHTED_SAMPLER/densenet201_weighted_sampler_best.pt (70.36 MB)
│   ├── EXP_04_FOCAL_LOSS/densenet201_focal_loss_best.pt (70.35 MB)
│   └── EXP_05_RANDOM_OVERSAMPLING/densenet201_random_oversampling_best.pt (208.96 MB)
├── results/
│   ├── EXP_01_BASELINE/
│   │   ├── metrics/ (densenet201_baseline_metrics.json, densenet201_test_metrics.json)
│   │   ├── plots/ (test_confusion_matrix.png, test_precision_recall_curve.png, test_roc_curve.png, training_validation_loss.png)
│   │   ├── confusion_matrix/ (empty)
│   │   └── gradcam/ (empty)
│   ├── EXP_02_WEIGHTED_BCE/
│   │   ├── final_evaluation/stage2b_test_evaluation.json
│   │   ├── metrics/stage2b_weighted_bce_metrics.json
│   │   ├── threshold_analysis/stage2b_validation_threshold_analysis.csv
│   │   └── plots/ (stage2b_test_confusion_matrix.png, stage2b_threshold_analysis.png, stage2b_threshold_f1.png, stage2b_threshold_precision.png, stage2b_threshold_sensitivity.png, stage2b_threshold_specificity.png)
│   ├── EXP_03_WEIGHTED_SAMPLER/
│   │   ├── test_metrics_threshold_0.5.json
│   │   ├── test_predictions.csv (4,920 test predictions)
│   │   ├── training_history.json
│   │   └── plots/ (test_confusion_matrix.png, test_precision_recall_curve.png, test_probability_distribution.png, test_roc_curve.png, training_validation_loss.png, validation_roc_auc.png)
│   ├── EXP_04_FOCAL_LOSS/
│   │   ├── test_metrics_threshold_0.5.json
│   │   ├── test_predictions.csv (4,920 test predictions)
│   │   ├── training_history.json
│   │   └── plots/ (test_confusion_matrix.png, test_precision_recall_curve.png, test_probability_distribution.png, test_roc_curve.png)
│   └── EXP_05_RANDOM_OVERSAMPLING/
│       ├── training_history.json
│       ├── training_summary.json
│       └── final_evaluation/ (exp05_confusion_matrix.png, exp05_final_test_metrics.csv, exp05_final_test_metrics.json, exp05_test_precision_recall_curve.png, exp05_test_predictions.csv, exp05_test_roc_curve.png)
└── src/
    ├── densenet201_baseline.py
    ├── EXP_01_BASELINE/densenet201_baseline.py
    └── EXP_02_WEIGHTED_BCE/
        ├── stage2b_weighted_bce.py
        ├── stage2b_final_evaluation.py
        └── stage2b_visual_results.py
```

---

## 3. Dataset and Data Split Verification

### 3.1 Primary Dataset
- **Name:** SIIM-ISIC 2020 Melanoma Classification Challenge Dataset
- **Total Images in Ground Truth:** 33,126
- **Total Patients:** 2,056 unique patients
- **Class Labels:** Binary (0 = Benign, 1 = Malignant melanoma)
- **Overall Imbalance:** 32,542 Benign (98.24%) vs. 584 Malignant (1.76%) — a ~55.7 : 1 ratio.

### 3.2 Patient-Level Partitioning Audit
The processed split CSV files were audited for patient-level isolation:

| Partition | Total Images | Benign (0) | Malignant (1) | Malignant % | Unique Patients | Overlap with Other Splits |
|:---|---:|---:|---:|---:|---:|:---:|
| **Train** | 22,787 | 22,342 | 445 | 1.95% | 1,439 | **0** |
| **Validation** | 5,419 | 5,348 | 71 | 1.31% | 307 | **0** |
| **Test** | 4,920 | 4,852 | 68 | 1.38% | 310 | **0** |
| **Total** | **33,126** | **32,542** | **584** | **1.76%** | **2,056** | **0** |

**Leakage Audit Finding:** Patient-level isolation is strictly 100% verified. Every single patient exists in exactly one split ($1,439 + 307 + 310 = 2,056$). Patient-level data leakage between training, validation, and testing sets is completely eliminated.

### 3.3 Duplicate Image Handling Audit
- In the official ISIC 2020 challenge documentation, 425 duplicate/near-duplicate image pairs were identified by the organizers.
- **Audit in Codebase:** The codebase retains all 33,126 images across the splits ($22,787 + 5,419 + 4,920 = 33,126$). No duplicate filtering script was executed prior to splitting. This is documented as a dataset property and limitation in the audit.

---

## 4. Model Architecture and Preprocessing Pipeline

### 4.1 Architecture
- **Base Architecture:** DenseNet201 (Densely Connected Convolutional Networks, 201 layers).
- **Weights:** ImageNet-1K pretrained weights (`DenseNet201_Weights.IMAGENET1K_V1`).
- **Classification Head:** The 1000-class classifier was replaced with a single linear output layer: `nn.Linear(backbone.classifier.in_features, 1)` outputting raw logits for binary classification.
- **Image-only Pipeline:** The current implemented model does not ingest tabular metadata (age, sex, anatomical site). It operates strictly on dermoscopic image tensors.

### 4.2 Preprocessing and Augmentation
- **Input Dimensions:** Resized to $224 \times 224$ pixels via bilinear interpolation.
- **Tensor Conversion:** Converted to PyTorch tensor format $[0.0, 1.0]$.
- **Normalization:** Standard ImageNet channel-wise normalization:
  - Mean: $\mu = [0.485, 0.456, 0.406]$
  - Standard Deviation: $\sigma = [0.229, 0.224, 0.225]$
- **Training Augmentations:**
  - `RandomHorizontalFlip(p=0.5)`
  - `RandomRotation(degrees=15)`
  - `ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05)`
- **Validation and Test Preprocessing:** Deterministic resize to $224 \times 224$ and ImageNet normalization. No random augmentations applied to validation or test splits.

---

## 5. Experiment Inventory and Verification Status

Five distinct experiments were identified, audited, and verified from actual disk artifacts:

### Experiment 1: DenseNet201 Baseline
- **Method:** ImageNet pretrained DenseNet201 trained for 3 epochs with AdamW ($lr=10^{-4}$, weight decay=$10^{-4}$, batch size=32).
- **Imbalance Handling in Code:** Trained with `BCEWithLogitsLoss(pos_weight=50.2067)`.
- **Classification Threshold:** Standard threshold of $\tau = 0.5$.
- **Validation ROC-AUC:** 0.8472 (Average Precision: 0.0811).
- **Held-out Test Performance:**
  - Test ROC-AUC: 0.8000 (0.79997)
  - Test Average Precision: 0.0626
  - Accuracy: 42.58%
  - Sensitivity / Recall: 91.18% (62 / 68 malignant detected)
  - Specificity: 41.90% (2,033 / 4,852 benign correct)
  - Precision: 2.15% (62 / 2,881 predicted malignant)
  - F1-Score: 4.20% (0.0420)
  - Test Confusion Matrix: TN = 2,033, FP = 2,819, FN = 6, TP = 62 (Total = 4,920).
- **Status:** **Completed and 100% verified.**

### Experiment 2: DenseNet201 with Weighted BCE
- **Method:** Initialized from the baseline checkpoint; fine-tuned up to 8 epochs (early stopped at epoch 6, best checkpoint at epoch 3) with `BCEWithLogitsLoss(pos_weight=50.2067)` and learning rate scheduling.
- **Operating Threshold:** Selected on validation data by maximizing F1 / balancing trade-offs: $\tau = 0.86$.
- **Validation Performance at Epoch 3:**
  - Best Validation ROC-AUC: 0.9188 (+0.0716 over baseline)
  - Validation PR-AUC: 0.1747
  - Validation Sensitivity: 30.99%, Specificity: 98.50%, Precision: 21.57%, F1: 25.43%
- **Held-out Test Performance ($\tau = 0.86$):**
  - Test ROC-AUC: 0.8298
  - Test PR-AUC: 0.1288
  - Accuracy: 97.26%
  - Sensitivity / Recall: 22.06% (15 / 68 malignant detected)
  - Specificity: 98.31% (4,770 / 4,852 benign correct)
  - Precision: 15.46% (15 / 97 predicted malignant)
  - F1-Score: 18.18% (0.1818)
  - Test Confusion Matrix: TN = 4,770, FP = 82, FN = 53, TP = 15 (Total = 4,920).
- **Status:** **Completed and 100% verified.**

### Experiment 3: DenseNet201 with WeightedRandomSampler
- **Method:** PyTorch `WeightedRandomSampler` applied to training dataloader to balance batch sampling frequencies. Standard `BCEWithLogitsLoss()`. Batch size 64, AdamW ($lr=10^{-4}$). Best epoch: 2.
- **Operating Threshold:** Evaluated at $\tau = 0.5$.
- **Validation ROC-AUC:** 0.9062 (AP: 0.1894).
- **Held-out Test Performance ($\tau = 0.5$):**
  - Test ROC-AUC: 0.8218
  - Test Average Precision: 0.1286
  - Accuracy: 96.02%
  - Sensitivity / Recall: 36.76% (25 / 68 malignant detected)
  - Specificity: 96.85% (4,699 / 4,852 benign correct)
  - Precision: 14.04% (25 / 178 predicted malignant)
  - F1-Score: 20.33% (0.2033)
  - Test Confusion Matrix: TN = 4,699, FP = 153, FN = 43, TP = 25 (Total = 4,920).
- **Status:** **Completed and 100% verified.**

### Experiment 4: DenseNet201 with Focal Loss
- **Method:** Focal Loss ($\alpha=0.75$, $\gamma=2.0$) to down-weight easy negative examples and focus on hard minority examples. 5 epochs trained. Best epoch: 5.
- **Operating Threshold:** Evaluated at $\tau = 0.5$.
- **Validation ROC-AUC:** 0.9181 (AP: 0.1800).
- **Held-out Test Performance ($\tau = 0.5$):**
  - Test ROC-AUC: 0.8601
  - Test Average Precision: 0.1402
  - Accuracy: 98.07%
  - Sensitivity / Recall: 14.71% (10 / 68 malignant detected)
  - Specificity: 99.24% (4,815 / 4,852 benign correct)
  - Precision: 21.28% (10 / 47 predicted malignant)
  - F1-Score: 17.39% (0.1739)
  - Test Confusion Matrix: TN = 4,815, FP = 37, FN = 58, TP = 10 (Total = 4,920).
- **Status:** **Completed and 100% verified.**

### Experiment 5: DenseNet201 with Random Oversampling
- **Method:** Random oversampling using `WeightedRandomSampler` on the training partition only. Validation and test sets remain unchanged. Standard `BCEWithLogitsLoss()`. Best epoch: 2.
- **Operating Threshold:** Validation-selected maximum F1 threshold: $\tau = 0.729635$.
- **Validation Performance at Epoch 2:**
  - Best Validation ROC-AUC: 0.9082
  - Validation Average Precision: 0.2176
- **Held-out Test Performance ($\tau = 0.729635$):**
  - Test ROC-AUC: 0.8708
  - Test Average Precision: 0.1041
  - Test PR-AUC (trapezoidal): 0.0975
  - Accuracy: 97.15%
  - Sensitivity / Recall: 19.12% (13 / 68 malignant detected)
  - Specificity: 98.25% (4,767 / 4,852 benign correct)
  - Precision: 13.27% (13 / 98 predicted malignant)
  - F1-Score: 15.66% (0.1566)
  - Test Confusion Matrix: TN = 4,767, FP = 85, FN = 55, TP = 13 (Total = 4,920).
- **Status:** **Completed and 100% verified.**

### Experiment 6: Status
- **Status:** **Incomplete / Unverified / Non-existent in accessible workspace.**
- No checkpoint, training script, predictions, or metrics files exist for Experiment 6. It will be reported honestly in Chapter 6 & 7 as an uncompleted/aborted research iteration.

---

## 6. Discrepancies and Clarifications Discovered During Audit

1. **Baseline Training Loss Formulation:**
   - In the prior narrative, Experiment 1 was referred to as "Standard BCE". However, audit of `densenet201_baseline_metrics.json` and `densenet201_baseline.py` confirms that the baseline was actually trained with `pos_weight=50.2067`. At the default decision threshold $\tau = 0.5$, this positive class weighting pushed the uncalibrated logits positive, yielding an extreme sensitivity of 91.18% (62/68) at the expense of an enormous false positive rate (2,819 FP out of 4,852 benign cases; specificity = 41.90%).
   - In Experiment 2, the exact same loss weight was retained, but the decision threshold was rigorously calibrated on the validation set ($\tau = 0.86$), shifting the operating point to high specificity (98.31%) while collapsing sensitivity to 22.06%.

2. **Average Precision vs. Trapezoidal PR-AUC in Experiment 5:**
   - In `exp05_final_test_metrics.json`, both `test_average_precision = 0.10412` (scikit-learn `average_precision_score`, which is a weighted mean of precisions at each threshold) and `test_pr_auc = 0.09754` (trapezoidal integration via `auc(recall, precision)`) are present. Both are mathematically valid but represent slightly different discrete approximations of the area under the PR curve. The distinction is explicitly documented.

3. **Status of Planned Architectural Modules:**
   - **Grad-CAM Visualizations:** The directory `results/EXP_01_BASELINE/gradcam` is empty. No Grad-CAM heatmap images or activation mapping scripts exist in the repository.
   - **Tabular Metadata Fusion (Age, Sex, Anatomical Site):** Metadata columns exist in `train.csv`, `val.csv`, and `test.csv`, but the model architectures in `src/` are exclusively CNN vision heads processing image pixels. No multimodal fusion network (e.g., cross-attention, MLP concatenation) was implemented.
   - **Fairness & Fitzpatrick Skin-tone Analysis:** The ISIC 2020 dataset does not provide Fitzpatrick skin-tone annotations. No fairness subgroup evaluations exist.
   - **Interactive Web Application:** No web application files (Streamlit, Flask, React) exist in the local workspace.
   - **Reporting Decision:** These modules are classified strictly as **Planned Future Work (Chapter 8)** and clearly distinguished from the completed deep learning vision experiments.

---

## 7. Audit Summary Table of Verified Model Checkpoints

| Checkpoint Path | Architecture | File Size | Epoch | Metric in Checkpoint | Verified Loadable |
|:---|:---|:---:|:---:|:---|:---:|
| `models/EXP_01_BASELINE/densenet201_baseline_best.pt` | DenseNet201 | 70.30 MB | 3 | Val AUC: 0.8472 | Yes |
| `models/EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt` | DenseNet201 | 70.38 MB | 3 | Val AUC: 0.9188 | Yes |
| `models/EXP_03_WEIGHTED_SAMPLER/densenet201_weighted_sampler_best.pt` | DenseNet201 | 70.36 MB | 2 | Val AUC: 0.9062 | Yes |
| `models/EXP_04_FOCAL_LOSS/densenet201_focal_loss_best.pt` | DenseNet201 | 70.35 MB | 5 | Val AUC: 0.9181 | Yes |
| `models/EXP_05_RANDOM_OVERSAMPLING/densenet201_random_oversampling_best.pt` | DenseNet201 | 208.96 MB | 2 | Val AUC: 0.9082 | Yes |
