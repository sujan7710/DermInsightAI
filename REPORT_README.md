# DERMINSIGHT AI — FINAL VERIFIED RESEARCH REPORT DOCUMENTATION
**Project Title:** AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER  
**Application Prototype Name:** DermInsight AI  
**Course:** BCSE497J — Project-I  
**Degree:** B.Tech in Computer Science and Engineering  
**School:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Vellore  
**Authors:**
- Sujan M. (Reg. No: 23BCE2002)
- Ramachandran Sivasankar (Reg. No: 23BCE2107)
- Alan John Anand (Reg. No: 23BCB0165)
**Faculty Guide:** Dr. Krishna Rani Samal, Associate Professor, SCOPE  
**Report Period:** Fall Semester 2026 / October 2026  

---

## 1. Overview of Generated Files

The following verified research artifacts have been generated and saved directly in the project root:

1. **`DermInsight_AI_Project_I_Report_Verified.docx` (2.03 MB, 55 Pages)**
   - The master editable academic report conforming strictly to the official VIT BCSE497J - Project-I formatting template.
   - Every single chapter begins on a new page.
   - All placeholders have been eliminated; exact page numbers are populated in the Table of Contents, List of Figures, and List of Tables.
   - Contains all genuine project figures, architectural diagrams, confusion matrices, ROC/PR curves, and 32 authentic peer-reviewed references.

2. **`DermInsight_AI_Project_I_Report_Verified.pdf` (1.64 MB, 55 Pages)**
   - The official rendered PDF publication generated via native Microsoft Word automation, ensuring exact layout fidelity, font rendering, and figure scaling.

3. **`PROJECT_INVENTORY.md`**
   - Comprehensive inventory auditing all accessible directories, files, model checkpoints, dataset splits, code scripts, and experimental logs.

4. **`REPORT_CLAIM_AUDIT.md`**
   - Claim-by-claim verification matrix matching every numerical result, threshold, and clinical finding in the report to its exact underlying file path and cryptographic evidence.

5. **`EXPERIMENT_COMPARISON.csv`**
   - Master structured data table providing cross-experiment comparisons across all five completed experiments on identical held-out test splits.

6. **`REPORT_FIGURES/`**
   - High-resolution (300 DPI) publication-quality figures:
     - `dataset_class_distribution.png`
     - `system_architecture.png`
     - `data_flow_diagram.png`
     - `use_case_diagram.png`
     - `class_diagram.png`
     - `sequence_diagram.png`
     - `cross_experiment_roc_comparison.png`
     - `cross_experiment_pr_comparison.png`
     - `cross_experiment_metrics_bar_chart.png`

---

## 2. Key Audited Research Findings

1. **Patient-Level Isolation Verified:**
   - SIIM-ISIC 2020 archive (33,126 images across 2,056 patients) was audited.
   - Splitting strictly enforces patient-level isolation: Train (22,787 images, 1,439 patients), Val (5,419 images, 307 patients), Held-out Test (4,920 images, 310 patients).
   - Zero patient overlap exists between partitions, eliminating data leakage.

2. **Completed Experiments Benchmarked:**
   - **EXP 01 (Baseline DenseNet201):** Trained with W-BCE (pos_weight=50.21); at threshold 0.50, achieved 91.18% sensitivity (62/68 TP) but low specificity (41.90%, 2,819 FP).
   - **EXP 02 (Weighted BCE Fine-Tuning):** Validation ROC-AUC 0.9188 (+0.0716 over baseline); at validation-calibrated threshold 0.86, achieved 98.31% specificity and 97.26% accuracy, but sensitivity collapsed to 22.06% (15/68 TP, 53 FN).
   - **EXP 03 (PyTorch WeightedRandomSampler):** Best balanced clinical triage model; achieved 36.76% sensitivity and 96.85% specificity at threshold 0.50, minimizing total misclassification cost ($460,600).
   - **EXP 04 (Focal Loss, alpha=0.75, gamma=2.0):** High specificity (99.24%) and precision (21.28%), but severe minority under-prediction yielded 14.71% sensitivity (58 FN).
   - **EXP 05 (Random Oversampling, Train Only):** Highest test ranking discrimination (ROC-AUC = 0.8708, AP = 0.1041); at validation threshold 0.7296, achieved 19.12% sensitivity and 98.25% specificity.

3. **Status of Incomplete / Future Modules:**
   - **Experiment 6:** Incomplete attempt; no saved checkpoints or evaluation logs exist in the repository. Honestly documented as an aborted exploration.
   - **Grad-CAM Heatmaps:** Folder exists but is empty; documented as planned future work.
   - **Multimodal Tabular Metadata Fusion & Fitzpatrick Skin-Tone Fairness:** Audited and formally scoped for Project-II.
