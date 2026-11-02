# DermInsight AI: Architecture & Documentation

This directory contains the system architecture diagrams, UML diagrams, data flow diagrams (DFD), experimental lineage, and audit records.

---

## Architecture & System Diagrams

All visual diagrams are available in high resolution under [`docs/figures/`](./figures/):

| Figure Name | File Path | Description |
|:---|:---|:---|
| **System Architecture** | [`docs/figures/FIG_4_1_system_architecture.png`](./figures/FIG_4_1_system_architecture.png) | End-to-end deep learning framework, data loader, DenseNet-201 backbone, classification head, loss weighting, and operating threshold |
| **Data Flow Diagram (Level 0)** | [`docs/figures/FIG_4_3_dfd_level0.png`](./figures/FIG_4_3_dfd_level0.png) | Context-level DFD depicting data interaction between user/practitioner, preprocessing engine, model inference, and diagnostic report |
| **Data Flow Diagram (Level 1)** | [`docs/figures/FIG_4_4_dfd_level1.png`](./figures/FIG_4_4_dfd_level1.png) | Detailed DFD breaking down dataset partitioning, data augmentation, PyTorch forward pass, sigmoid activation, and decision thresholding |
| **UML Class Diagram** | [`docs/figures/FIG_4_6_class_diagram.png`](./figures/FIG_4_6_class_diagram.png) | Object-oriented design showing `DermImageDataset`, `DenseNet201Classifier`, `Trainer`, `Evaluator`, and `MetricLogger` classes |
| **UML Sequence Diagram** | [`docs/figures/FIG_4_7_sequence_diagram.png`](./figures/FIG_4_7_sequence_diagram.png) | Time-ordered execution flow from image ingestion to model inference, calibration, and output visualization |
| **UML Use Case Diagram** | [`docs/figures/FIG_4_5_use_case.png`](./figures/FIG_4_5_use_case.png) | Actors (Researcher, Clinician) and use cases (Train Model, Evaluate Checkpoint, Tune Operating Threshold, Generate Report) |
| **Experiment Lineage** | [`docs/figures/FIG_4_2_experiment_lineage.png`](./figures/FIG_4_2_experiment_lineage.png) | Evolution from baseline transfer learning through sampling and loss function iterations |
| **Split Distribution** | [`docs/figures/FIG_5_2_split_distribution.png`](./figures/FIG_5_2_split_distribution.png) | Class distribution across Train (22,787), Validation (5,419), and Test (4,920) sets |
| **Evaluation Protocol** | [`docs/figures/FIG_5_3_evaluation_protocol.png`](./figures/FIG_5_3_evaluation_protocol.png) | Dual-phase protocol: validation threshold optimization followed by held-out test evaluation |
| **ROC & PR Comparisons** | [`docs/figures/cross_experiment_roc_comparison.png`](./figures/cross_experiment_roc_comparison.png) | Comparative ROC and Precision-Recall curves across all 5 models |
| **Confusion Matrices** | [`docs/figures/FIG_7_2_confusion_matrices.png`](./figures/FIG_7_2_confusion_matrices.png) | Side-by-side test confusion matrices for all 5 verified experiments |

---

## Research Audits & Manifests

- **[`PROJECT_INVENTORY.md`](./PROJECT_INVENTORY.md):** Complete catalog of all verified files, experiments, checkpoints, and parameters.
- **[`REPORT_CLAIM_AUDIT.md`](./REPORT_CLAIM_AUDIT.md):** Audit linking every quantitative claim to its verifiable source file.
- **[`REPORT_REVISION_SUMMARY.md`](./REPORT_REVISION_SUMMARY.md):** Comprehensive history of academic revisions, guideline alignments, and document updates.
- **[`organization_manifest.json`](./organization_manifest.json):** Cryptographic SHA-256 manifest of organized Colab and Drive artifacts.
