# DermInsight AI: Experimental Results & Benchmarks

This directory contains empirical evaluation results, confusion matrices, ROC/PR curves, and threshold analysis across all verified experiments on the **held-out test set (4,920 samples; 4,852 benign, 68 malignant)**.

---

## Master Comparison Table

| Metric | EXP_01 Baseline | EXP_02 Weighted BCE | EXP_03 Weighted Sampler | EXP_04 Focal Loss | EXP_05 Oversampling |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Strategy** | Pos Weight ($50.21$) | Pos Weight + Opt $\tau$ | WeightedRandomSampler | Focal ($\alpha=0.75, \gamma=2$) | Random Oversampling |
| **Operating Threshold ($\tau$)** | $0.50$ | **$0.86$** | $0.50$ | $0.50$ | **$0.7296$** |
| **Validation ROC-AUC** | 0.8472 | **0.9188** | 0.9062 | 0.9181 | 0.9082 |
| **Test ROC-AUC** | 0.8000 | 0.8298 | 0.8218 | 0.8601 | **0.8708** |
| **Test Average Precision (AP)** | 0.0626 | 0.1288 | 0.1286 | **0.1402** | 0.1041 |
| **Test PR-AUC (trapezoidal)** | — | 0.1288 | — | — | 0.0975 |
| **Accuracy** | 42.58% | 97.26% | 96.02% | **98.07%** | 97.15% |
| **Sensitivity (Recall)** | **91.18%** | 22.06% | 36.76% | 14.71% | 19.12% |
| **Specificity** | 41.90% | 98.31% | 96.85% | **99.24%** | 98.25% |
| **Precision (PPV)** | 2.15% | 15.46% | 14.04% | **21.28%** | 13.27% |
| **F1-Score** | 4.20% | 18.18% | **20.33%** | 17.39% | 15.66% |
| **True Negatives (TN)** | 2,033 | 4,770 | 4,699 | **4,815** | 4,767 |
| **False Positives (FP)** | 2,819 | 82 | 153 | **37** | 85 |
| **False Negatives (FN)** | **6** | 53 | 43 | 58 | 55 |
| **True Positives (TP)** | **62** | 15 | 25 | 10 | 13 |
| **Total Test Samples** | 4,920 | 4,920 | 4,920 | 4,920 | 4,920 |

---

## Directory Organization

```
results/
├── README.md                              # This summary document
├── stage2b_test_evaluation.json           # EXP_02 root evaluation metrics
├── stage2b_validation_threshold_analysis.csv # EXP_02 threshold sweep
├── stage2b_weighted_bce_metrics.json      # EXP_02 training metrics
├── EXP_01_BASELINE/
│   ├── metrics/ (densenet201_baseline_metrics.json, densenet201_test_metrics.json)
│   └── plots/ (test_confusion_matrix.png, test_roc_curve.png, test_precision_recall_curve.png, training_validation_loss.png)
├── EXP_02_WEIGHTED_BCE/
│   ├── final_evaluation/ (stage2b_test_evaluation.json)
│   ├── metrics/ (stage2b_weighted_bce_metrics.json)
│   ├── threshold_analysis/ (stage2b_validation_threshold_analysis.csv)
│   └── plots/ (stage2b_test_confusion_matrix.png, stage2b_threshold_analysis.png, stage2b_threshold_f1.png, stage2b_threshold_precision.png, stage2b_threshold_sensitivity.png, stage2b_threshold_specificity.png)
├── EXP_03_WEIGHTED_SAMPLER/
│   ├── test_metrics_threshold_0.5.json
│   ├── test_predictions.csv (4,920 individual predictions)
│   ├── training_history.json
│   └── plots/ (test_confusion_matrix.png, test_precision_recall_curve.png, test_probability_distribution.png, test_roc_curve.png, training_validation_loss.png, validation_roc_auc.png)
├── EXP_04_FOCAL_LOSS/
│   ├── test_metrics_threshold_0.5.json
│   ├── test_predictions.csv (4,920 individual predictions)
│   ├── training_history.json
│   └── plots/ (test_confusion_matrix.png, test_precision_recall_curve.png, test_probability_distribution.png, test_roc_curve.png)
└── EXP_05_RANDOM_OVERSAMPLING/
    ├── training_history.json
    ├── training_summary.json
    └── final_evaluation/ (exp05_confusion_matrix.png, exp05_final_test_metrics.csv, exp05_final_test_metrics.json, exp05_test_precision_recall_curve.png, exp05_test_predictions.csv, exp05_test_roc_curve.png)
```
