DERMINSIGHT AI
EXPERIMENT 1 - DENSENET201 BASELINE
====================================

Purpose
-------
Establish the baseline performance of the DenseNet201 model
before introducing class-imbalance handling.

Model
-----
DenseNet201

Pretraining
-----------
ImageNet pretrained weights

Input
-----
224 x 224 RGB images

Task
----
Binary classification:
0 = Benign
1 = Malignant

Dataset
-------
ISIC 2020

Evaluation artifacts
--------------------
- Training/validation loss
- ROC curve
- Precision-Recall curve
- Confusion matrix
- Grad-CAM visualizations
- Validation metrics
- Test metrics
- Trained model checkpoint

IMPORTANT
---------
This folder contains a copy of the original baseline artifacts.
The original project files are retained separately.