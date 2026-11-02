# DermInsight AI: An Automated Deep Learning Framework for Early Detection of Skin Cancer

[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org/)
[![Torchvision](https://img.shields.io/badge/Torchvision-0.15+-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Git LFS](https://img.shields.io/badge/Git%20LFS-Tracked-orange.svg?logo=git-lfs)](https://git-lfs.github.com/)
[![Academic Project](https://img.shields.io/badge/VIT-BCSE497J%20Project--I-800000.svg)](https://vit.ac.in/)

> **Academic Research Project**  
> **Course:** BCSE497J — Project-I (B.Tech in Computer Science and Engineering)  
> **Institution:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India  
> **Authors:**  
> - **Sujan M.** (Reg. No: 23BCE2002)  
> - **Ramachandran Sivasankar** (Reg. No: 23BCE2107)  
> - **Alan John Anand** (Reg. No: 23BCB0165)  
> **Faculty Guide:** Dr. Krishna Rani Samal, Associate Professor, SCOPE, VIT Vellore  
> **Academic Year:** 2026

---

## Table of Contents

1. [Project Title & Overview](#1-project-title--overview)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Dataset Description](#4-dataset-description)
5. [Dataset Imbalance Challenge](#5-dataset-imbalance-challenge)
6. [DenseNet-201 and Transfer Learning](#6-densenet-201-and-transfer-learning)
7. [Explanation of Verified Experiments](#7-explanation-of-verified-experiments)
8. [Experiment Comparison Table](#8-experiment-comparison-table)
9. [Evaluation Metrics](#9-evaluation-metrics)
10. [System Architecture](#10-system-architecture)
11. [Project Directory Structure](#11-project-directory-structure)
12. [Installation Instructions](#12-installation-instructions)
13. [How to Run the Project](#13-how-to-run-the-project)
14. [Limitations and Future Improvements](#14-limitations-and-future-improvements)
15. [Research Prototype Disclaimer](#15-research-prototype-disclaimer)

---

## 1. Project Title & Overview

**DermInsight AI** is an automated deep learning research framework investigating transfer learning and class imbalance mitigation strategies for the early binary detection of malignant melanoma from dermoscopic skin lesion imagery. 

Using the large-scale **SIIM-ISIC 2020 Melanoma Classification Challenge** benchmark (33,126 dermoscopic images from 2,056 unique patients), this project systematically evaluates five distinct class-imbalance mitigation methodologies built upon a deep **DenseNet-201** convolutional neural network backbone. 

The primary contribution of this research is a transparent, empirically audited investigation into the severe trade-offs between sensitivity (detecting life-threatening malignancies) and specificity (minimizing unnecessary invasive biopsies) in clinical diagnostic settings where benign lesions outnumber malignant lesions by ~55.7 to 1.

---

## 2. Problem Statement

Malignant melanoma represents only about 1% of all diagnosed skin cancers, yet it accounts for over 75% of all skin cancer-related mortalities worldwide. The World Health Organization (WHO) and American Cancer Society report that when melanoma is detected early at a localized stage (Stage I), the 5-year relative survival rate exceeds **99%**. However, once the tumor invades deeper dermal layers or metastasizes to distant lymph nodes and organs (Stage IV), the 5-year survival rate plummets below **30%**.

Dermoscopy is a non-invasive in-vivo imaging technique that magnifies subsurface skin structures; however, clinical diagnostic accuracy heavily depends on dermatologist experience, with novice clinicians exhibiting diagnostic sensitivity below 65%. 

While automated computer vision systems offer immense potential for clinical triage, real-world dermoscopic datasets present severe class imbalance (fewer than 2% malignant cases). Standard deep neural networks trained with naive empirical risk minimization suffer from majority-class collapse—achieving misleadingly high overall accuracy (e.g., >98%) while failing to detect lethal malignant tumors (high false negative rate). Addressing this imbalance while maintaining clinically acceptable specificity is the core engineering challenge addressed by DermInsight AI.

---

## 3. Project Objectives

1. **Investigate Deep Transfer Learning:** Adapt DenseNet-201 pre-trained on ImageNet-1K to extract high-level discriminative features from $224 \times 224$ dermoscopic lesion images.
2. **Guarantee Zero Patient-Level Leakage:** Enforce strict patient-level partitioning across training, validation, and testing partitions so that lesions from the same individual never cross split boundaries.
3. **Benchmark Five Imbalance Strategies:** Formulate, train, and empirically evaluate five distinct imbalance mitigation paradigms:
   - Baseline positive-class loss re-weighting
   - Fine-tuning with Weighted Binary Cross-Entropy (BCE) and validation-driven threshold optimization
   - Batch-level re-balancing via PyTorch `WeightedRandomSampler`
   - Dynamically focused classification using Lin et al. Focal Loss ($\alpha=0.75, \gamma=2.0$)
   - Resampling via training-partition Random Oversampling
4. **Conduct Rigorous Held-Out Evaluation:** Benchmark all checkpoints on an identical held-out test split of 4,920 images across both threshold-independent discriminative metrics (ROC-AUC, Average Precision) and threshold-dependent clinical operating metrics (Sensitivity, Specificity, Precision, F1-Score, Confusion Matrices).
5. **Maintain Empirical Transparency:** Provide complete reproducibility through open-source training pipelines, verifiable model checkpoints, raw predictions, and auditable metrics manifests.

---

## 4. Dataset Description

DermInsight AI is trained, validated, and evaluated on the official **SIIM-ISIC 2020 Melanoma Classification Challenge** dataset provided by the International Skin Imaging Collaboration (ISIC).

- **Total Ground Truth Images:** 33,126 dermoscopic JPEG images
- **Total Unique Patients:** 2,056 unique individuals
- **Target Label:** Binary classification (`0` = Benign lesion, `1` = Malignant melanoma)
- **Overall Class Split:** 32,542 Benign (98.24%) vs. 584 Malignant (1.76%)

### Patient-Level Partitioning Audit

To prevent subtle patient-level data leakage (where multiple lesions from a single patient share anatomical traits, skin tones, or photographic conditions), the dataset was split strictly by unique `patient_id`:

| Partition | Total Images | Benign ($y=0$) | Malignant ($y=1$) | Malignant % | Unique Patients | Patient Leakage |
|:---|---:|---:|---:|---:|---:|:---:|
| **Train** | 22,787 | 22,342 | 445 | 1.95% | 1,439 | **0** |
| **Validation** | 5,419 | 5,348 | 71 | 1.31% | 307 | **0** |
| **Test** | 4,920 | 4,852 | 68 | 1.38% | 310 | **0** |
| **Total** | **33,126** | **32,542** | **584** | **1.76%** | **2,056** | **0** |

*Audit Verification:* The sum of patients across splits ($1,439 + 307 + 310 = 2,056$) matches the exact total unique patients with **zero overlap** between any partitions.

---

## 5. Dataset Imbalance Challenge

The SIIM-ISIC 2020 dataset features an extreme imbalance ratio of **55.7 : 1** (only 1.76% malignant instances).

```
Benign (98.24%):    ████████████████████████████████████████ 32,542 lesions
Malignant (1.76%):  █ 584 lesions
```

### The Clinical Dilemma:
1. **The Majority-Class Illusion:** A naive dummy model predicting "Benign" for every single image achieves **98.24% classification accuracy**, yet possesses **0% sensitivity**—failing every single cancer patient.
2. **False Negatives vs. False Positives:** In clinical oncology, a **False Negative (FN)** means a patient with invasive melanoma is sent home without treatment, leading to preventable death. Conversely, a **False Positive (FP)** results in emotional distress and an unnecessary excisional biopsy.
3. **Threshold Sensitivity:** Under standard binary classification ($\tau = 0.50$), loss functions weighted heavily toward the positive class produce uncalibrated logit shifts, resulting in extremely high sensitivity at the expense of massive false positive cascades. Meticulous operating threshold calibration ($\tau$) is therefore critical.

---

## 6. DenseNet-201 and Transfer Learning

### Architecture Rationale

The feature extraction backbone is **DenseNet-201** (Densely Connected Convolutional Networks, 201 layers; Huang et al., CVPR 2017), pre-trained on ImageNet-1K (`DenseNet201_Weights.IMAGENET1K_V1`).

In DenseNet, each layer receives feature-map inputs from all preceding layers and passes its own feature-maps to all subsequent layers via iterative concatenation:

$$x_\ell = H_\ell([x_0, x_1, x_2, \dots, x_{\ell-1}])$$

This dense connectivity provides key advantages for medical imaging:
- **Alleviation of Vanishing Gradients:** Direct gradient flow through dense connections from deeper layers back to early feature extractors.
- **Substantial Feature Reuse:** Compact feature representations without learning redundant convolutional filters (~20M parameters vs. ~25.6M in ResNet-50 and ~60M in ResNet-152).
- **Multi-Scale Dermatological Feature Capture:** Retains low-level structural boundary features from early layers alongside complex semantic lesion patterns from deeper dense blocks.

### Classification Head & Preprocessing

- **Custom Vision Head:** The default 1,000-class ImageNet classifier was replaced with a single linear output layer:
  ```python
  model.classifier = nn.Linear(backbone.classifier.in_features, 1)
  ```
  The single raw logit $z$ is transformed to probability $\hat{p} \in [0, 1]$ via the sigmoid function $\sigma(z) = \frac{1}{1 + e^{-z}}$.
- **Input Dimensions:** Bilinearly interpolated to $224 \times 224 \times 3$.
- **Normalization:** Standard ImageNet channel-wise normalization: $\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$.
- **Training Augmentations:** `RandomHorizontalFlip(p=0.5)`, `RandomRotation(degrees=15)`, and `ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05)`.
- **Validation/Test Preprocessing:** Strictly deterministic resizing and normalization without random augmentations.

---

## 7. Explanation of Verified Experiments

Five distinct transfer learning experiments were conducted and fully audited from saved disk checkpoints, training histories, and test predictions:

### Experiment 1: DenseNet-201 Baseline (`EXP_01_BASELINE`)
- **Configuration:** DenseNet-201 fine-tuned for 3 epochs with AdamW ($lr=10^{-4}$, weight decay=$10^{-4}$, batch size=32).
- **Imbalance Formulation:** Trained using `BCEWithLogitsLoss(pos_weight=50.2067)` where $w_{pos} = \frac{N_{neg}}{N_{pos}} = \frac{22,342}{445} \approx 50.21$.
- **Decision Threshold:** Standard default $\tau = 0.50$.
- **Behavior:** The aggressive $50.21$ loss penalty pushed uncalibrated logits heavily into positive territory. At $\tau = 0.50$, it detected **91.18% of all cancers (62/68 TP)**, but at the cost of **2,819 False Positives** (specificity collapsed to 41.90%, precision was 2.15%).
- **Verification Status:** Verified (`models/EXP_01_BASELINE/densenet201_baseline_best.pt`, 70.30 MB).

### Experiment 2: DenseNet-201 with Weighted BCE & Threshold Optimization (`EXP_02_WEIGHTED_BCE`)
- **Configuration:** Initialized from baseline, fine-tuned for 6 epochs (best epoch: 3), batch size 64, AdamW with learning rate scheduling.
- **Imbalance Formulation:** Weighted BCE ($w_{pos} = 50.2067$).
- **Threshold Calibration:** Instead of naive $\tau=0.50$, the decision threshold was swept across validation data to balance clinical sensitivity and specificity, selecting optimal $\tau = 0.86$.
- **Behavior:** Achieved a **Validation ROC-AUC of 0.9188** (+0.0716 over baseline) and a Test ROC-AUC of 0.8298. At $\tau = 0.86$, specificity soared to **98.31%** (only 82 false alarms across 4,852 benign lesions), though sensitivity contracted to 22.06% (15/68 TP).
- **Verification Status:** Verified (`models/EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt`, 70.38 MB).

### Experiment 3: DenseNet-201 with WeightedRandomSampler (`EXP_03_WEIGHTED_SAMPLER`)
- **Configuration:** Trained for 5 epochs (best epoch: 2), batch size 64, AdamW ($lr=10^{-4}$).
- **Imbalance Formulation:** Mini-batch balancing via PyTorch `WeightedRandomSampler`, where samples are drawn inversely proportional to class frequencies, paired with standard unweighted BCE loss.
- **Decision Threshold:** Evaluated at $\tau = 0.50$.
- **Behavior:** Best-balanced non-threshold-calibrated model. Achieved **Test ROC-AUC of 0.8218**, **Sensitivity of 36.76% (25/68 TP)**, **Specificity of 96.85% (4,699/4,852 TN)**, and the highest **F1-Score of 20.33%** among all models.
- **Verification Status:** Verified (`models/EXP_03_WEIGHTED_SAMPLER/densenet201_weighted_sampler_best.pt`, 70.36 MB).

### Experiment 4: DenseNet-201 with Focal Loss (`EXP_04_FOCAL_LOSS`)
- **Configuration:** Trained for 5 epochs (best epoch: 5), batch size 32, AdamW ($lr=10^{-4}$).
- **Imbalance Formulation:** Lin et al. Focal Loss with focusing parameter $\gamma = 2.0$ and weighting factor $\alpha = 0.75$:
  $$\mathcal{L}_{\text{Focal}} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$
  Down-weights easy well-classified benign negatives ($p_t \to 1, (1-p_t)^2 \to 0$) to focus gradient updates on hard minority examples.
- **Decision Threshold:** Evaluated at $\tau = 0.50$.
- **Behavior:** Achieved the highest **Specificity (99.24%, only 37 FP)** and highest **Precision (21.28%)**, with a strong **Test ROC-AUC of 0.8601** and Test Average Precision of 0.1402. However, extreme conservative bias suppressed sensitivity to 14.71% (10/68 TP).
- **Verification Status:** Verified (`models/EXP_04_FOCAL_LOSS/densenet201_focal_loss_best.pt`, 70.35 MB).

### Experiment 5: DenseNet-201 with Random Oversampling (`EXP_05_RANDOM_OVERSAMPLING`)
- **Configuration:** Trained for 5 epochs (best epoch: 2), batch size 32, AdamW ($lr=10^{-4}$).
- **Imbalance Formulation:** Random oversampling applied strictly to the training partition; validation and test splits were strictly untouched. Standard BCE loss.
- **Threshold Calibration:** Validation-selected maximum-F1 threshold: $\tau = 0.729635$.
- **Behavior:** Achieved the **highest Test ROC-AUC of 0.8708** across all experiments, demonstrating superior continuous ranking discrimination. Achieved 97.15% accuracy, 98.25% specificity, and 19.12% sensitivity (13/68 TP).
- **Verification Status:** Verified (`models/EXP_05_RANDOM_OVERSAMPLING/densenet201_random_oversampling_best.pt`, 208.96 MB).

### Note on Experiment 6 Status
- In early project documentation, a multimodal tabular-image fusion architecture was conceptualized as Experiment 6. Audit of the repository confirms that no training scripts, checkpoints, predictions, or metrics files were produced for Experiment 6. In accordance with strict academic integrity, Experiment 6 is documented as an uncompleted research iteration and formally designated for future work.

---

## 8. Experiment Comparison Table

All metrics below reflect actual recorded evaluation results on the **identical held-out test partition (4,920 samples: 4,852 benign, 68 malignant)**:

| Metric | EXP_01 Baseline | EXP_02 Weighted BCE | EXP_03 Weighted Sampler | EXP_04 Focal Loss | EXP_05 Oversampling |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Imbalance Strategy** | Pos Weight ($50.21$) | Pos Weight + Calibrated $\tau$ | `WeightedRandomSampler` | Focal ($\alpha=0.75, \gamma=2.0$) | Random Oversampling |
| **Operating Threshold ($\tau$)** | $0.50$ | **$0.86$** | $0.50$ | $0.50$ | **$0.7296$** |
| **Validation ROC-AUC** | 0.8472 | **0.9188** | 0.9062 | 0.9181 | 0.9082 |
| **Test ROC-AUC** | 0.8000 | 0.8298 | 0.8218 | 0.8601 | **0.8708** |
| **Test Average Precision (AP)** | 0.0626 | 0.1288 | 0.1286 | **0.1402** | 0.1041 |
| **Accuracy** | 42.58% | 97.26% | 96.02% | **98.07%** | 97.15% |
| **Sensitivity / Recall** | **91.18%** | 22.06% | 36.76% | 14.71% | 19.12% |
| **Specificity** | 41.90% | 98.31% | 96.85% | **99.24%** | 98.25% |
| **Precision / PPV** | 2.15% | 15.46% | 14.04% | **21.28%** | 13.27% |
| **F1-Score** | 4.20% | 18.18% | **20.33%** | 17.39% | 15.66% |
| **True Negatives (TN)** | 2,033 | 4,770 | 4,699 | **4,815** | 4,767 |
| **False Positives (FP)** | 2,819 | 82 | 153 | **37** | 85 |
| **False Negatives (FN)** | **6** | 53 | 43 | 58 | 55 |
| **True Positives (TP)** | **62** | 15 | 25 | 10 | 13 |
| **Total Test Samples** | 4,920 | 4,920 | 4,920 | 4,920 | 4,920 |

---

## 9. Evaluation Metrics

Because DermInsight AI operates in an extreme class-imbalance regime, multiple complementary evaluation metrics are computed:

1. **ROC-AUC (Receiver Operating Characteristic Area Under the Curve):** Evaluates the probability that the model ranks a randomly chosen malignant lesion higher than a randomly chosen benign lesion across all possible thresholds.
2. **PR-AUC / Average Precision (AP):** Evaluates the area under the precision vs. recall curve. Highly informative for imbalanced clinical benchmarks where the majority class can artificially inflate ROC-AUC.
3. **Sensitivity (Recall / True Positive Rate):**
   $$\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
   Measures the proportion of actual melanomas correctly detected. Critical for avoiding fatal omissions.
4. **Specificity (True Negative Rate):**
   $$\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$
   Measures the proportion of benign lesions correctly cleared. Essential for preventing patient panic and excessive biopsies.
5. **Precision (Positive Predictive Value):**
   $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
   The probability that a lesion flagged by the model as malignant is genuinely cancer.
6. **F1-Score:** The harmonic mean of precision and recall:
   $$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

## 10. System Architecture

The overall system architecture encompasses data ingestion, patient-level partitioning, image preprocessing, DenseNet-201 feature extraction, classification head projection, loss re-weighting, and post-hoc threshold calibration:

```
+-------------------------------------------------------------------------------------------------+
|                                    DERMINSIGHT AI PIPELINE                                      |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|  [ SIIM-ISIC 2020 Dataset ] (33,126 Dermoscopic Images, 2,056 Patients)                         |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Patient-Level Partitioning ] ──> Strictly 0 Patient Leakage                                  |
|        ├── Train Set:       22,787 images (1,439 patients)                                      |
|        ├── Validation Set:   5,419 images (  307 patients)                                      |
|        └── Test Set:         4,920 images (  310 patients)                                      |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Preprocessing & Augmentation Engine ]                                                        |
|        ├── Resize: 224 x 224 pixels                                                             |
|        ├── Normalization: ImageNet Mean [0.485, 0.456, 0.406], Std [0.229, 0.224, 0.225]       |
|        └── Train-time: RandomHorizontalFlip, RandomRotation(15°), ColorJitter                   |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Deep Feature Extraction: DenseNet-201 Backbone ]                                             |
|        ├── Dense Blocks (DenseBlock 1 to 4) + Transition Layers                                 |
|        ├── Feature Reuse via Concatenation: x_l = H([x_0, x_1, ..., x_{l-1}])                   |
|        └── Global Average Pooling: 1920-dimensional feature vector                              |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Custom Vision Classifier Head ]                                                              |
|        └── Linear Layer: nn.Linear(in_features=1920, out_features=1) ──> Raw Logit z            |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Imbalance Mitigation & Training Loss Formulation ]                                           |
|        ├── EXP 01: BCE with pos_weight = 50.21                                                  |
|        ├── EXP 02: Fine-Tuning with pos_weight = 50.21 & Validation Threshold Optimization      |
|        ├── EXP 03: PyTorch WeightedRandomSampler + Standard BCE                                 |
|        ├── EXP 04: Focal Loss (alpha = 0.75, gamma = 2.0)                                       |
|        └── EXP 05: Training-Partition Random Oversampling + Standard BCE                        |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Sigmoid Activation & Operating Threshold Calibration ]                                       |
|        ├── Predicted Probability: p = 1 / (1 + exp(-z))                                         |
|        └── Binary Decision: y_hat = 1 if p >= tau else 0                                        |
|             │                                                                                   |
|             ▼                                                                                   |
|  [ Evaluation & Metric Extraction ]                                                             |
|        └── Confusion Matrix, ROC-AUC, PR-AUC, Sensitivity, Specificity, F1-Score                |
+-------------------------------------------------------------------------------------------------+
```

High-resolution visual diagrams are cataloged in [`docs/figures/`](./docs/figures/):
- **System Architecture:** [`docs/figures/FIG_4_1_system_architecture.png`](./docs/figures/FIG_4_1_system_architecture.png)
- **Data Flow Diagram (Level 0):** [`docs/figures/FIG_4_3_dfd_level0.png`](./docs/figures/FIG_4_3_dfd_level0.png)
- **Data Flow Diagram (Level 1):** [`docs/figures/FIG_4_4_dfd_level1.png`](./docs/figures/FIG_4_4_dfd_level1.png)
- **UML Class Diagram:** [`docs/figures/FIG_4_6_class_diagram.png`](./docs/figures/FIG_4_6_class_diagram.png)
- **UML Sequence Diagram:** [`docs/figures/FIG_4_7_sequence_diagram.png`](./docs/figures/FIG_4_7_sequence_diagram.png)
- **UML Use Case Diagram:** [`docs/figures/FIG_4_5_use_case.png`](./docs/figures/FIG_4_5_use_case.png)

---

## 11. Project Directory Structure

```
DermInsightAI/
├── .gitattributes                         # Git LFS tracking configuration for model weights
├── .gitignore                             # Exclusion of caches, venvs, secrets, and raw images
├── LICENSE                                # MIT Open Source License
├── requirements.txt                       # Python dependencies (PyTorch, torchvision, etc.)
├── EXPERIMENT_COMPARISON.csv              # Master tabular comparison of all 5 experiments
│
├── data/
│   ├── README.md                          # Dataset documentation & acquisition guide
│   ├── processed/
│   │   ├── train.csv                      # Training partition (22,787 samples, 1,439 patients)
│   │   ├── val.csv                        # Validation partition (5,419 samples, 307 patients)
│   │   └── test.csv                       # Held-out test partition (4,920 samples, 310 patients)
│   └── raw/
│       ├── ISIC_2020_Training_GroundTruth.csv    # Official ISIC 2020 ground truth (33,126 rows)
│       ├── ISIC_2020_Training_GroundTruth_v2.csv # Ground truth with lesion IDs
│       └── train_images/                  # [Git-ignored] Raw ISIC JPEG image directory
│
├── models/
│   ├── README.md                          # Registry of checkpoints and PyTorch loading guide
│   ├── EXP_01_BASELINE/densenet201_baseline_best.pt              # 70.30 MB (Git LFS)
│   ├── EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt   # 70.38 MB (Git LFS)
│   ├── EXP_03_WEIGHTED_SAMPLER/densenet201_weighted_sampler_best.pt # 70.36 MB (Git LFS)
│   ├── EXP_04_FOCAL_LOSS/densenet201_focal_loss_best.pt          # 70.35 MB (Git LFS)
│   └── EXP_05_RANDOM_OVERSAMPLING/densenet201_random_oversampling_best.pt # 208.96 MB (Git LFS)
│
├── results/
│   ├── README.md                          # Experimental results documentation
│   ├── stage2b_test_evaluation.json       # Root evaluation file for EXP_02
│   ├── stage2b_validation_threshold_analysis.csv # Validation threshold analysis table
│   ├── stage2b_weighted_bce_metrics.json  # Training metric log
│   ├── EXP_01_BASELINE/                   # Metrics and plots (ROC, PR, confusion matrix)
│   ├── EXP_02_WEIGHTED_BCE/               # Metrics, threshold plots, confusion matrix
│   ├── EXP_03_WEIGHTED_SAMPLER/           # Metrics, test predictions, ROC/PR plots
│   ├── EXP_04_FOCAL_LOSS/                 # Metrics, test predictions, probability distributions
│   └── EXP_05_RANDOM_OVERSAMPLING/        # Metrics, predictions, ROC/PR curves
│
├── src/
│   ├── README.md                          # Source code guide and execution commands
│   ├── densenet201_baseline.py            # Standalone baseline training and evaluation script
│   ├── EXP_01_BASELINE/
│   │   └── densenet201_baseline.py        # Baseline pipeline with positive-class weighting
│   └── EXP_02_WEIGHTED_BCE/
│       ├── stage2b_weighted_bce.py        # Fine-tuning pipeline with learning rate scheduling
│       ├── stage2b_final_evaluation.py    # Validation threshold search & test evaluation
│       └── stage2b_visual_results.py      # Plotting suite for publication figures
│
├── notebooks/
│   └── README.md                          # Colab GPU runtime documentation and reproduction notes
│
├── docs/
│   ├── README.md                          # Documentation index
│   ├── organization_manifest.json         # SHA-256 cryptographic file manifest
│   ├── PROJECT_INVENTORY.md               # Research inventory
│   ├── REPORT_CLAIM_AUDIT.md              # Empirical claims audit
│   ├── REPORT_REVISION_SUMMARY.md         # Revision summary
│   └── figures/                           # High-resolution architectural and UML diagrams
│
└── reports/
    ├── README.md                          # Reports and publications index
    ├── DermInsight_AI_Project_I_Report_Final_v3.pdf  # Final academic dissertation (PDF, 55+ pages)
    ├── DermInsight_AI_Project_I_Report_Final_v3.docx # Final academic dissertation (DOCX)
    ├── DermInsight_AI_IEEE_Conference_Paper.pdf      # IEEE format conference paper (PDF)
    ├── DermInsight_AI_IEEE_Conference_Paper.docx     # IEEE format conference paper (DOCX)
    └── DermInsight_AI_Review_3.pptx                  # Project defense slide deck (PowerPoint)
```

---

## 12. Installation Instructions

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git and [Git LFS](https://git-lfs.github.com/) (required to pull model checkpoints)
- CUDA-enabled GPU (NVIDIA GPU with 8GB+ VRAM recommended; CPU mode supported for inference)

### 1. Clone Repository with Git LFS
```bash
# Install Git LFS hooks on your machine
git lfs install

# Clone the repository
git clone <repository_url>
cd DermInsightAI

# Pull all model checkpoints tracked by Git LFS
git lfs pull
```

### 2. Set Up Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 13. How to Run the Project

### Step 1: Download ISIC 2020 Images
Download the ISIC 2020 image collection from [ISIC Archive](https://www.isic-archive.com/) or Kaggle. Place the images into:
```
data/raw/train_images/
```

### Step 2: Train the Baseline Model (`EXP_01_BASELINE`)
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

### Step 3: Run Weighted BCE Fine-Tuning (`EXP_02_WEIGHTED_BCE`)
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

### Step 4: Calibrate Operating Threshold & Evaluate Held-Out Test Set
```bash
python src/EXP_02_WEIGHTED_BCE/stage2b_final_evaluation.py \
    --model_path models/EXP_02_WEIGHTED_BCE/densenet201_stage2b_weighted_bce.pt \
    --data_dir data \
    --output_dir results/EXP_02_WEIGHTED_BCE
```

### Step 5: Generate Publication Figures
```bash
python src/EXP_02_WEIGHTED_BCE/stage2b_visual_results.py
```

---

## 14. Limitations and Future Improvements

In the spirit of honest and transparent scientific inquiry, several important limitations of the current implementation are identified:

1. **Image-Only Architecture:** The current implementation processes $224 \times 224$ dermoscopic images only. The SIIM-ISIC 2020 dataset includes clinical tabular metadata (patient age, sex, and anatomical lesion site) in `train.csv`, `val.csv`, and `test.csv`. Developing a multimodal cross-attention fusion network to jointly model image features and patient metadata is planned for Project-II.
2. **Duplicate Image Pairs:** The official ISIC 2020 documentation identifies 425 duplicate or near-duplicate lesion pairs. All 33,126 images were retained in the local split files without running a pre-split deduplication filter.
3. **Demographic and Skin-Tone Bias:** The ISIC 2020 dataset does not contain Fitzpatrick skin phototype annotations. Dermoscopic AI models are known to suffer performance degradation on darker skin phototypes (Fitzpatrick Types IV–VI). Evaluating subgroup fairness across diverse demographic cohorts is an essential future milestone.
4. **Grad-CAM Saliency Visualizations:** Saliency mapping scripts (`results/EXP_01_BASELINE/gradcam`) are planned but not yet implemented in the codebase.
5. **No Clinical Trials:** The model has been evaluated strictly on offline retrospective benchmark splits. It has not undergone prospective clinical evaluation or dermatologist reader studies.

---

## 15. Research Prototype Disclaimer

> [!CAUTION]
> **RESEARCH AND EDUCATIONAL PROTOTYPE ONLY**
> 
> DermInsight AI is an academic research prototype developed strictly for scientific exploration and educational evaluation as part of the **BCSE497J — Project-I** course at **Vellore Institute of Technology (VIT), Vellore**.
> 
> - **NOT A MEDICAL DEVICE:** This software is **NOT** a certified medical device and has **NOT** been evaluated, approved, or cleared by the United States Food and Drug Administration (FDA), the European Medicines Agency (EMA), the Central Drugs Standard Control Organisation (CDSCO), or any other regulatory health authority.
> - **NOT FOR CLINICAL DIAGNOSIS:** This software is **NOT** intended for clinical diagnosis, patient screening, treatment planning, or direct clinical decision support. It must **NEVER** be used as a substitute for professional medical examination, diagnosis, or advice from a licensed board-certified dermatologist or qualified medical physician.
> - **NO LIABILITY:** The authors and institution provide this codebase "as is" without warranty of any kind, either express or implied.
