# REPORT CLAIM AUDIT: DERMINSIGHT AI
**Audit Date:** October 2026  
**Auditor:** Senior ML Auditor & Academic Lead  

This document tracks every key empirical claim made in the project, against its verifiable source artifact in `DermInsightAI`.

| Claim Category | Specific Claim Statement | Verification Source & File Path | Verification Status | Discrepancy / Audit Observation | Included in Final Report |
|:---|:---|:---|:---:|:---|:---:|
| **Dataset Size** | ISIC 2020 training collection contains 33,126 images | `data/raw/ISIC_2020_Training_GroundTruth.csv` (33,126 rows) | **VERIFIED** | Matches official ISIC 2020 dataset size. | Yes |
| **Patient Count** | Total unique patients across dataset is 2,056 | `data/processed/train.csv`, `val.csv`, `test.csv` (nunique=1439, 307, 310) | **VERIFIED** | Sum = 1439 + 307 + 310 = 2,056 patients. | Yes |
| **Class Imbalance** | Extreme class imbalance: 32,542 benign (98.24%) vs. 584 malignant (1.76%) | `data/raw/ISIC_2020_Training_GroundTruth.csv` | **VERIFIED** | Malignant positive class constitutes only 1.76% of dataset. | Yes |
| **Data Partitioning** | Train = 22,787, Val = 5,419, Test = 4,920 | `data/processed/{train,val,test}.csv` | **VERIFIED** | Exact row counts match: 22,787 + 5,419 + 4,920 = 33,126. | Yes |
| **Patient Leakage** | Patient-level splitting completely avoids patient overlap | `data/processed/{train,val,test}.csv` patient set intersection checks | **VERIFIED** | Intersections between all split pairs are exactly 0. Zero patient leakage. | Yes |
| **Duplicate Images** | 425 duplicate images were excluded before splitting | ISIC 2020 documentation vs `data/processed/` | **DISCREPANCY** | Split files retain all 33,126 images. Duplicate exclusion was NOT executed. | Yes (Noted as Limitation) |
| **Backbone Model** | DenseNet201 pretrained on ImageNet-1K with single output linear head | `src/EXP_01_BASELINE/densenet201_baseline.py`, checkpoints | **VERIFIED** | `in_features = backbone.classifier.in_features`, `Linear(in_features, 1)`. | Yes |
| **Input Dimensions** | Resized to 224x224, ImageNet normalized | `src/EXP_01_BASELINE/densenet201_baseline.py` lines 120-140 | **VERIFIED** | Standard ImageNet mean/std used across all scripts. | Yes |
| **Exp 1: Val ROC-AUC** | Best validation ROC-AUC = 0.8472 | `results/EXP_01_BASELINE/metrics/densenet201_baseline_metrics.json` | **VERIFIED** | Exact value: 0.8471562. | Yes |
| **Exp 1: Test ROC-AUC** | Test ROC-AUC = 0.8000 | `results/EXP_01_BASELINE/metrics/densenet201_test_metrics.json` | **VERIFIED** | Exact value: 0.7999733. | Yes |
| **Exp 1: Test Sensitivity** | Test Sensitivity = 91.18% (62/68) | `results/EXP_01_BASELINE/metrics/densenet201_test_metrics.json` | **VERIFIED** | 62 TP / 68 positive test cases detected. | Yes |
| **Exp 1: Test Specificity** | Test Specificity = 41.90% | `results/EXP_01_BASELINE/metrics/densenet201_test_metrics.json` | **VERIFIED** | 2033 TN / 4852 negative test cases (2819 False Positives). | Yes |
| **Exp 1: Test Precision** | Test Precision = 2.15% | `results/EXP_01_BASELINE/metrics/densenet201_test_metrics.json` | **VERIFIED** | 62 TP / (62 + 2819) = 2.152%. | Yes |
| **Exp 1: Threshold** | Operating decision threshold = 0.50 | `src/EXP_01_BASELINE/densenet201_baseline.py` | **VERIFIED** | Code defaults to `threshold=0.5`. Pos-weight shifted logits high. | Yes |
| **Exp 2: Positive Weight** | Positive class loss weight = 50.2067 | `results/EXP_02_WEIGHTED_BCE/metrics/stage2b_weighted_bce_metrics.json` | **VERIFIED** | Exactly 22342 / 445 = 50.20674. | Yes |
| **Exp 2: Best Epoch** | Best validation epoch = Epoch 3 | `stage2b_weighted_bce_metrics.json` | **VERIFIED** | Val AUC peaked at Epoch 3 (0.9188). Early stopped at 6. | Yes |
| **Exp 2: Val ROC-AUC** | Best validation ROC-AUC = 0.9188 | `stage2b_test_evaluation.json` | **VERIFIED** | Exact value: 0.91876389 (+0.0716 over baseline). | Yes |
| **Exp 2: Threshold** | Validation selected threshold = 0.86 | `stage2b_test_evaluation.json`, threshold analysis CSV | **VERIFIED** | Selected on validation set to balance sensitivity/specificity. | Yes |
| **Exp 2: Test ROC-AUC** | Test ROC-AUC = 0.8298 | `stage2b_test_evaluation.json` | **VERIFIED** | Exact value: 0.8298185. | Yes |
| **Exp 2: Test Sensitivity** | Test Sensitivity = 22.06% (15/68) | `stage2b_test_evaluation.json` | **VERIFIED** | 15 TP, 53 FN out of 68 malignant lesions. | Yes |
| **Exp 2: Test Specificity** | Test Specificity = 98.31% | `stage2b_test_evaluation.json` | **VERIFIED** | 4770 TN, 82 FP out of 4852 benign lesions. | Yes |
| **Exp 2: Test F1** | Test F1-Score = 18.18% | `stage2b_test_evaluation.json` | **VERIFIED** | F1: 0.181818. Accuracy: 97.26%. | Yes |
| **Exp 3: Sampling** | PyTorch WeightedRandomSampler balances class sampling | `results/EXP_03_WEIGHTED_SAMPLER/` config & history | **VERIFIED** | Epoch 2 best; Test ROC-AUC=0.8218, Sensitivity=36.76%, Specificity=96.85%. | Yes |
| **Exp 4: Focal Loss** | Focal loss with alpha=0.75, gamma=2.0 | `results/EXP_04_FOCAL_LOSS/` checkpoint metadata | **VERIFIED** | Epoch 5 best; Test ROC-AUC=0.8601, Sensitivity=14.71%, Specificity=99.24%. | Yes |
| **Exp 5: Random Oversample** | Random Oversampling via WeightedRandomSampler on training set only | `results/EXP_05_RANDOM_OVERSAMPLING/` | **VERIFIED** | Val AUC=0.9082, Test AUC=0.8708, Val threshold=0.729635. | Yes |
| **Exp 5: Test Sensitivity** | Test Sensitivity = 19.12% (13/68) | `exp05_final_test_metrics.json` | **VERIFIED** | 13 TP, 55 FN out of 68 malignant lesions. | Yes |
| **Exp 5: AP vs PR-AUC** | AP = 0.1041, PR-AUC = 0.0975 | `exp05_final_test_metrics.json` | **VERIFIED** | AP is weighted average precision; PR-AUC is trapezoidal integration. | Yes |
| **Exp 6: Status** | Incomplete / unverified | Workspace inspection | **UNVERIFIED** | No files or checkpoints exist for Experiment 6. Reported as incomplete attempt. | Yes (Noted in Ch 6 & 7) |
| **Grad-CAM Explanations** | Visual Grad-CAM heatmaps exist | `results/EXP_01_BASELINE/gradcam/` (empty) | **NOT PRESENT** | No heatmaps exist on disk. Classified as planned future work. | Future Work Only |
| **Metadata Fusion** | Tabular patient metadata incorporated in CNN | `src/` model code | **NOT PRESENT** | Architecture is image-only. Multimodal fusion classified as future work. | Future Work Only |
| **Skin-Tone / Fairness** | Evaluation performed across Fitzpatrick skin types | Dataset CSVs | **NOT PRESENT** | ISIC 2020 lacks skin-tone labels. Subgroup fairness classified as future work. | Future Work Only |
