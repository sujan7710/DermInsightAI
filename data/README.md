# DermInsight AI: Dataset Documentation

## Overview

DermInsight AI is trained and evaluated on the **SIIM-ISIC 2020 Melanoma Classification Challenge** dataset hosted by the International Skin Imaging Collaboration (ISIC).

- **Total Ground Truth Images:** 33,126 dermoscopic lesion images
- **Total Unique Patients:** 2,056 unique individuals
- **Target Variable:** Binary classification (`0` = Benign, `1` = Malignant Melanoma)
- **Class Imbalance:** 32,542 Benign (98.24%) vs. 584 Malignant (1.76%) — an extreme ~55.7:1 imbalance ratio.

---

## Patient-Level Partitioning & Leakage Elimination

To avoid patient-level data leakage (where lesions from the same patient appear across both training and evaluation splits), the dataset was partitioned at the **patient identifier level (`patient_id`)**:

| Partition | Total Samples | Benign ($y=0$) | Malignant ($y=1$) | Malignant % | Unique Patients | Patient Overlap |
|:---|---:|---:|---:|---:|---:|:---:|
| **Train** | 22,787 | 22,342 | 445 | 1.95% | 1,439 | **0** |
| **Validation** | 5,419 | 5,348 | 71 | 1.31% | 307 | **0** |
| **Test** | 4,920 | 4,852 | 68 | 1.38% | 310 | **0** |
| **Total** | **33,126** | **32,542** | **584** | **1.76%** | **2,056** | **0** |

*Verification:* $1,439 + 307 + 310 = 2,056$. Overlap across all splits is strictly zero.

---

## Directory Structure

```
data/
├── README.md                              # This dataset documentation file
├── processed/
│   ├── train.csv                          # Training partition metadata (22,787 rows)
│   ├── val.csv                            # Validation partition metadata (5,419 rows)
│   └── test.csv                           # Held-out test partition metadata (4,920 rows)
└── raw/
    ├── ISIC_2020_Training_GroundTruth.csv    # Official ISIC 2020 ground truth (33,126 rows)
    ├── ISIC_2020_Training_GroundTruth_v2.csv # ISIC 2020 ground truth including lesion_id
    └── train_images/                         # [Excluded from Git] 3,496 local sample images (~1.43 GB)
```

---

## Data Acquisition & Reproduction

Due to GitHub repository limits and dataset redistribution licensing, raw JPEG dermoscopic images in `data/raw/train_images/` are excluded from the repository.

To download the full image collection:
1. Visit the [ISIC Archive](https://www.isic-archive.com/) or the [Kaggle SIIM-ISIC 2020 Melanoma Classification Challenge](https://www.kaggle.com/c/siim-isic-melanoma-classification/data).
2. Download the training image archive (`train.zip` or JPEG folder).
3. Extract images into:
   ```
   DermInsightAI/data/raw/train_images/
   ```
4. Each image filename corresponds to the `image_name` column in the provided split CSVs (e.g., `ISIC_2637011.jpg`).
