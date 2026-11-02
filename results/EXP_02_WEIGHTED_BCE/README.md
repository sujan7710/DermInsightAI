DERMINSIGHT AI
EXPERIMENT 2 - WEIGHTED BCE
===========================

Purpose
-------
Improve handling of the severe class imbalance present in
the ISIC 2020 binary classification task.

Starting point
--------------
DenseNet201 baseline model from Experiment 1.

Main methodological change
---------------------------
Weighted Binary Cross-Entropy with Logits loss
(BCEWithLogitsLoss).

Positive class weight
---------------------
50.2067

Training
--------
Train samples: 22,787
Positive: 445
Negative: 22,342

Validation
----------
Validation samples: 5,419
Positive: 71
Negative: 5,348

Best epoch
----------
3

Baseline validation ROC-AUC
---------------------------
0.8472

Best Stage 2B validation ROC-AUC
--------------------------------
0.9188

Improvement
-----------
+0.0716

Final test results
------------------
ROC-AUC:     0.8298
PR-AUC:      0.1288
Threshold:   0.86
Sensitivity: 0.2206
Specificity: 0.9831
Precision:   0.1546
F1-score:    0.1818
Accuracy:    0.9726

Test confusion matrix
---------------------
TN = 4770
FP = 82
FN = 53
TP = 15

Status
------
Experiment completed.