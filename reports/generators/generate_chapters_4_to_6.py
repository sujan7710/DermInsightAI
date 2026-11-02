# -*- coding: utf-8 -*-
"""
DermInsight AI - Chapter 4 to 6 Content Builder (Clean Typography Version)
"""

import os
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from build_helpers import (
    add_styled_heading, add_body_paragraph, add_list_item, add_formula,
    add_figure, add_table_caption, set_cell_margins, set_cell_background, set_table_borders
)

PROJECT_ROOT = r'C:\Users\sujan\Downloads\DermInsightAI-20261026T173409Z-1-001\DermInsightAI'
FIG_DIR = os.path.join(PROJECT_ROOT, 'REPORT_FIGURES')

def add_chapter_4(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 4\n4. DESIGN APPROACH AND DETAILS", 1)
    
    add_styled_heading(doc, "4.1 System Architecture", 2)
    add_body_paragraph(
        doc,
        "The DermInsight AI architectural framework is engineered as an end-to-end modular pipeline designed specifically for high-throughput, "
        "reproducible, and clinically honest dermoscopic lesion screening. As illustrated in Figure 4.1, the framework is architecturally structured "
        "into four decoupled stages: (1) Ingestion and Patient-Level Partitioning, (2) Deep Convolutional Feature Extraction, (3) Class-Imbalance "
        "Mitigation and Optimization, and (4) Decision Threshold Calibration and Triage Evaluation."
    )
    add_body_paragraph(
        doc,
        "The first stage ingests raw dermoscopic images from the SIIM-ISIC 2020 archive and enforces patient identity isolation, ensuring that all lesions "
        "from any individual patient are grouped exclusively into either the training, validation, or test partition. The second stage applies deterministic "
        "resizing and ImageNet standardization before routing tensors to a 201-layer DenseNet backbone. The third stage incorporates specialized objective "
        "functions and sampling distributions to counteract extreme class imbalance. The fourth stage subjects unnormalized logits to validation-driven "
        "threshold calibration, mapping raw probabilities into high-confidence clinical triage categories."
    )

    add_figure(
        doc,
        os.path.join(FIG_DIR, 'system_architecture.png'),
        "Figure 4.1: End-to-End System Architecture of the DermInsight AI Screening Framework",
        width_inches=6.0
    )

    add_styled_heading(doc, "4.2 Design", 2)
    add_styled_heading(doc, "4.2.1 Data Flow Diagram", 3)
    add_body_paragraph(
        doc,
        "The functional data transformations throughout the pipeline are formally modeled via the Level-1 Data Flow Diagram (DFD) shown in Figure 4.2. "
        "The clinical user or automated PACS interface provides raw dermoscopic image files. Process 1.0 (Validation and Preprocessing) resizes the image "
        "to 224 x 224 pixels and applies channel-wise ImageNet tensor normalization. Process 2.0 (Inference Engine) loads verified model checkpoint weights "
        "from the Checkpoint Store (D1) and executes the DenseNet201 forward pass, producing a scalar logit. Process 3.0 (Calibrated Thresholding) evaluates "
        "the logit against the calibrated decision threshold, categorizing the lesion into clinical risk categories and generating an auditable diagnostic report."
    )

    add_figure(
        doc,
        os.path.join(FIG_DIR, 'data_flow_diagram.png'),
        "Figure 4.2: Level-1 Data Flow Diagram (DFD) Illustrating Image Ingestion, Preprocessing, Inference, and Triage Generation",
        width_inches=5.8
    )

    add_styled_heading(doc, "4.2.2 Use Case Diagram", 3)
    add_body_paragraph(
        doc,
        "Figure 4.3 depicts the system Use Case Diagram, illustrating user interactions with the screening system. The primary actor—a dermatologist, general practitioner, "
        "or clinical researcher—interacts with four core system use cases: (1) Input Lesion Image, (2) Trigger Model Inference, (3) Select Operational Decision Threshold, "
        "and (4) View Comprehensive Diagnostic Metrics. This design ensures that clinicians retain complete control over the screening sensitivity-specificity trade-off."
    )

    add_figure(
        doc,
        os.path.join(FIG_DIR, 'use_case_diagram.png'),
        "Figure 4.3: Use Case Diagram for the DermInsight AI Clinical Screening Interface",
        width_inches=5.4
    )

    add_styled_heading(doc, "4.2.3 Class Diagram", 3)
    add_body_paragraph(
        doc,
        "The object-oriented software architecture implemented in the Python codebase is modeled in the UML Class Diagram shown in Figure 4.4. "
        "The system comprises three core structural modules:"
    )
    add_list_item(
        doc,
        "• DermImageDataset: Encapsulates lesion metadata, manages on-the-fly image loading from disk via PIL, and applies PyTorch torchvision transforms."
    )
    add_list_item(
        doc,
        "• DermInsightDenseNet201: Inherits from torch.nn.Module, encapsulates the torchvision DenseNet201 backbone, replaces the 1000-class classifier with an nn.Identity() module, and attaches a single-output linear classification layer (nn.Linear(1920, 1))."
    )
    add_list_item(
        doc,
        "• Evaluator: Implements threshold sweep logic, calculates confusion matrix parameters (TN, FP, FN, TP), and generates ROC and PR curve metrics."
    )

    add_figure(
        doc,
        os.path.join(FIG_DIR, 'class_diagram.png'),
        "Figure 4.4: UML Class Diagram of the Implemented PyTorch Deep Learning Pipeline",
        width_inches=5.8
    )

    add_styled_heading(doc, "4.2.4 Sequence Diagram", 3)
    add_body_paragraph(
        doc,
        "The dynamic execution sequence during a screening evaluation session is illustrated in the UML Sequence Diagram (Figure 4.5). "
        "The clinician submits a dermoscopic image to the pipeline. The dataset loader processes the image and returns a normalized tensor. "
        "The DenseNet201 model executes the forward pass and returns raw logits. The ThresholdCalibrator evaluates the posterior probability "
        "against the optimal validation threshold and routes the classified prediction and risk metrics back to the clinician."
    )

    add_figure(
        doc,
        os.path.join(FIG_DIR, 'sequence_diagram.png'),
        "Figure 4.5: UML Sequence Diagram for Dermoscopic Image Ingestion, Inference, and Triage Output",
        width_inches=5.8
    )

def add_chapter_5(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 5\n5. METHODOLOGY AND TESTING", 1)
    
    add_styled_heading(doc, "5.1 Deep Learning Pipeline Architecture (DenseNet201)", 2)
    add_body_paragraph(
        doc,
        "The deep convolutional backbone selected for this framework is DenseNet201 (Densely Connected Convolutional Networks with 201 layers). "
        "In a conventional convolutional network, the output of the (l-1)-th layer serves as the input to the l-th layer: x_l = H_l(x_{l-1}). In contrast, "
        "DenseNet introduces direct iterative connections from every layer to all subsequent layers within a dense block:"
    )
    add_formula(
        doc,
        "x_l = H_l([x_0, x_1, x_2, ..., x_{l-1}])"
    )
    add_body_paragraph(
        doc,
        "where [x_0, x_1, ..., x_{l-1}] represents the channel-wise concatenation of feature maps produced by all preceding layers, and H_l(·) denotes a composite "
        "non-linear transformation comprising Batch Normalization (BN), Rectified Linear Unit (ReLU), and a 3x3 convolution."
    )
    add_body_paragraph(
        doc,
        "DenseNet201 is structured into four sequential dense blocks interconnected by transition layers that perform downsampling via 1x1 convolutions and 2x2 average pooling. "
        "To adapt this architecture for binary melanoma classification, the original 1000-class ImageNet fully connected head was replaced by an identity mapping, exposing "
        "the final 1,920-dimensional feature embedding. A custom linear projection layer was attached: z = W · x + b, where W in R^{1 x 1920} and b in R. "
        "The predicted probability of malignancy is obtained via the standard logistic sigmoid activation:"
    )
    add_formula(
        doc,
        "p_hat = σ(z) = 1 / (1 + exp(-z))"
    )

    add_table_caption(doc, "Table 5.1: DenseNet201 Feature Extractor Architectural Details")
    t_arch = doc.add_table(rows=8, cols=4)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_arch.autofit = False
    t_arch.columns[0].width = Inches(1.8)
    t_arch.columns[1].width = Inches(2.2)
    t_arch.columns[2].width = Inches(1.2)
    t_arch.columns[3].width = Inches(1.3)
    set_table_borders(t_arch, "D3D3D3")
    
    arch_data = [
        ("Network Stage", "Layer Configuration", "Output Size", "Feature Maps"),
        ("Input Stage", "7x7 Conv, Stride 2, 3x3 MaxPool", "56 x 56", "64 channels"),
        ("Dense Block 1", "6 Bottleneck Layers (1x1 & 3x3 conv)", "56 x 56", "256 channels"),
        ("Transition 1", "1x1 Conv, 2x2 Average Pooling", "28 x 28", "128 channels"),
        ("Dense Block 2", "12 Bottleneck Layers (1x1 & 3x3 conv)", "28 x 28", "512 channels"),
        ("Transition 2", "1x1 Conv, 2x2 Average Pooling", "14 x 14", "256 channels"),
        ("Dense Block 3", "48 Bottleneck Layers (1x1 & 3x3 conv)", "14 x 14", "1,792 channels"),
        ("Dense Block 4 & Head", "32 Bottleneck Layers, Global AvgPool, Linear Head", "1 x 1", "1,920 -> 1 logit")
    ]
    for r_idx, row in enumerate(arch_data):
        for c_idx, val in enumerate(row):
            cell = t_arch.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F4F7")
            set_cell_margins(cell, 60, 60, 80, 80)

    add_styled_heading(doc, "5.2 Patient-Level Splitting & Data Preprocessing", 2)
    add_body_paragraph(
        doc,
        "A critical methodological contribution of this project is the rigorous enforcement of patient-level isolation. In the SIIM-ISIC 2020 dataset, multiple "
        "dermoscopic images often originate from the same patient (e.g., individual patients with multiple atypical dysplastic nevi). If images are randomly split, "
        "the model easily memorizes patient-specific features such as underlying skin pigmentation, age-related solar elastosis, and device lighting conditions, causing "
        "severe data leakage and falsely optimistic test scores. To prevent this, patient identifiers (patient_id) were audited, grouping all images belonging to a patient "
        "into exactly one partition."
    )

    add_table_caption(doc, "Table 5.2: Verified Patient-Level Dataset Splitting and Class Distribution")
    t_spl = doc.add_table(rows=5, cols=6)
    t_spl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_spl.autofit = False
    t_spl.columns[0].width = Inches(1.1)
    t_spl.columns[1].width = Inches(1.0)
    t_spl.columns[2].width = Inches(1.1)
    t_spl.columns[3].width = Inches(1.0)
    t_spl.columns[4].width = Inches(1.0)
    t_spl.columns[5].width = Inches(1.3)
    set_table_borders(t_spl, "D3D3D3")
    
    spl_data = [
        ("Partition", "Total Images", "Benign (0)", "Malignant (1)", "Malignant %", "Unique Patients"),
        ("Training", "22,787", "22,342", "445", "1.95%", "1,439 patients"),
        ("Validation", "5,419", "5,348", "71", "1.31%", "307 patients"),
        ("Held-out Test", "4,920", "4,852", "68", "1.38%", "310 patients"),
        ("Total Dataset", "33,126", "32,542", "584", "1.76%", "2,056 patients")
    ]
    for r_idx, row in enumerate(spl_data):
        for c_idx, val in enumerate(row):
            cell = t_spl.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F4F7")
            elif r_idx == 4:
                run.font.bold = True
            set_cell_margins(cell, 60, 60, 80, 80)

    add_body_paragraph(
        doc,
        "Preprocessing across all experiments adhered to strict standardization: input images were resized to 224 x 224 pixels and normalized using ImageNet "
        "channel statistics (mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]). Training data was augmented on-the-fly using RandomHorizontalFlip (p=0.5), "
        "RandomRotation (degrees=15), and ColorJitter (brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05). Validation and test sets received deterministic resizing "
        "and normalization with zero stochastic augmentation, preventing evaluation artifacts."
    )

    add_styled_heading(doc, "5.3 Class-Imbalance Formulations & Strategies", 2)
    add_body_paragraph(
        doc,
        "To systematically evaluate the impact of class imbalance on deep feature learning, four distinct strategies were formulated and implemented:"
    )
    
    add_styled_heading(doc, "5.3.1 Weighted Binary Cross-Entropy Loss", 3)
    add_body_paragraph(
        doc,
        "The standard Binary Cross-Entropy with Logits loss is mathematically defined as:"
    )
    add_formula(
        doc,
        "L_BCE(z, y) = - [ y · log(σ(z)) + (1 - y) · log(1 - σ(z)) ]"
    )
    add_body_paragraph(
        doc,
        "Under extreme imbalance, gradients from y=0 overwhelm y=1. To counteract this, a positive class weight w_+ is introduced:"
    )
    add_formula(
        doc,
        "L_WBCE(z, y) = - [ w_+ · y · log(σ(z)) + (1 - y) · log(1 - σ(z)) ]"
    )
    add_body_paragraph(
        doc,
        "In our training set, the ratio of negative to positive examples is w_+ = N_neg / N_pos = 22,342 / 445 = 50.2067. Scaling positive loss by 50.2067 "
        "forces the optimizer to penalize false negatives 50.2 times more heavily than false positives during backpropagation."
    )

    add_styled_heading(doc, "5.3.2 PyTorch WeightedRandomSampler", 3)
    add_body_paragraph(
        doc,
        "Rather than modifying the loss function, the PyTorch WeightedRandomSampler alters the data-sampling probability distribution across mini-batches. "
        "Each training sample i is assigned a sampling weight w_i inversely proportional to its class prevalence: w_i = 1 / N_{c(i)}, where c(i) in {0, 1}. "
        "Mini-batches of size B are drawn with replacement according to multinomial probabilities p_i = w_i / (sum w_k), ensuring that the network encounters "
        "an equal representation of benign and malignant lesions during stochastic gradient descent."
    )

    add_styled_heading(doc, "5.3.3 Focal Loss Formulation", 3)
    add_body_paragraph(
        doc,
        "Focal Loss (Lin et al., 2017) dynamically focuses learning on hard ambiguous examples while down-weighting easy, well-classified majority instances:"
    )
    add_formula(
        doc,
        "L_FL(p_t) = - α_t · (1 - p_t)^γ · log(p_t)"
    )
    add_body_paragraph(
        doc,
        "where p_t is the model's estimated probability for the true ground-truth class, alpha_t in [0, 1] balances class prevalence (configured to alpha = 0.75), "
        "and gamma >= 0 is the focusing parameter (configured to gamma = 2.0). When an easy negative sample is classified with high confidence (e.g., p_t = 0.99), "
        "the modulating factor (1 - 0.99)^2 = 0.0001 reduces its loss contribution by four orders of magnitude."
    )

    add_styled_heading(doc, "5.3.4 Random Oversampling Strategy", 3)
    add_body_paragraph(
        doc,
        "Random Oversampling replicates minority positive instances within the training dataloader to achieve balanced epoch encounters. Importantly, oversampling "
        "was applied strictly to the training partition (22,787 samples). Validation (5,419) and test (4,920) sets were left completely untouched to preserve natural "
        "population prevalence during evaluation."
    )

    add_styled_heading(doc, "5.4 Checkpoint Selection & Early Stopping", 2)
    add_body_paragraph(
        doc,
        "Model training was managed using the AdamW optimizer (Loshchilov & Hutter, 2019) with an initial learning rate of 1e-4 and weight decay of 1e-4. "
        "Checkpoint selection was governed by validation ROC-AUC. An early stopping mechanism with a patience of 3 epochs monitored validation discrimination, "
        "saving the best state dictionary when validation ROC-AUC reached a peak."
    )

    add_table_caption(doc, "Table 5.3: Master Training Hyperparameters and Experimental Configurations")
    t_hyp = doc.add_table(rows=7, cols=3)
    t_hyp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hyp.autofit = False
    t_hyp.columns[0].width = Inches(2.2)
    t_hyp.columns[1].width = Inches(2.1)
    t_hyp.columns[2].width = Inches(2.2)
    set_table_borders(t_hyp, "D3D3D3")
    
    hyp_data = [
        ("Hyperparameter / Setting", "Baseline & Weighted BCE", "Samplers & Focal Loss"),
        ("Backbone Architecture", "DenseNet201 (Pretrained ImageNet)", "DenseNet201 (Pretrained ImageNet)"),
        ("Optimizer & Weight Decay", "AdamW (weight decay = 0.0001)", "AdamW (weight decay = 0.0001)"),
        ("Base Learning Rate", "0.0001 (Cosine Annealing)", "0.0001 (Fixed / Plateau)"),
        ("Batch Size & Input Size", "64 / 32; 224 x 224 pixels", "64 / 32; 224 x 224 pixels"),
        ("Checkpoint Selection Metric", "Validation ROC-AUC", "Validation ROC-AUC"),
        ("Early Stopping Patience", "3 Epochs (Max Epochs: 5 - 8)", "3 Epochs (Max Epochs: 5 - 8)")
    ]
    for r_idx, row in enumerate(hyp_data):
        for c_idx, val in enumerate(row):
            cell = t_hyp.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F4F7")
            set_cell_margins(cell, 60, 60, 80, 80)

    add_styled_heading(doc, "5.5 Classification Threshold Calibration Methodology", 2)
    add_body_paragraph(
        doc,
        "In imbalanced medical classification, the default decision threshold tau = 0.5 is arbitrary and clinically suboptimal. In our methodology, the optimal "
        "decision threshold tau* was calibrated exclusively on the validation set by conducting fine-grained sweeps across tau in [0.01, 0.99] with a step size of 0.01. "
        "The optimal operating threshold was selected to maximize the validation F1-score or balance sensitivity against specificity. Crucially, the test partition "
        "remained completely frozen during threshold calibration, preventing any data leakage into operational decision boundaries."
    )

    add_styled_heading(doc, "5.6 Evaluation & Testing Protocol on Held-Out Test Set", 2)
    add_body_paragraph(
        doc,
        "Final performance was evaluated on the isolated 4,920 held-out test images. Threshold-independent ranking performance was evaluated via ROC-AUC and Average "
        "Precision (AP / PR-AUC). Threshold-dependent classification performance was evaluated at the calibrated operational threshold tau* by computing True Negatives (TN), "
        "False Positives (FP), False Negatives (FN), and True Positives (TP), deriving Accuracy, Sensitivity (Recall), Specificity, Precision, and F1-score."
    )

def add_chapter_6(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 6\n6. PROJECT DEMONSTRATION", 1)
    
    add_styled_heading(doc, "6.1 Demonstration Workflow & Environment", 2)
    add_body_paragraph(
        doc,
        "The practical utility of the DermInsight AI deep learning pipeline was demonstrated through end-to-end execution scripts implemented in PyTorch. "
        "The execution environment operates either as an interactive Python CLI or automated inference batch script capable of processing single dermoscopic images "
        "or multi-patient clinical batches. The workflow loads the verified DenseNet201 checkpoint, initializes the preprocessing transform pipeline, extracts image tensors, "
        "and computes calibrated diagnostic risk assessments."
    )

    add_styled_heading(doc, "6.2 Preprocessing & Batch Dataloader Execution", 2)
    add_body_paragraph(
        doc,
        "During demonstration execution, raw images are ingested from disk via PIL, verified for correct 3-channel RGB dimensionality, resized to 224 x 224 pixels using "
        "bilinear interpolation, and normalized against ImageNet channel statistics. The batch dataloader constructs 4-dimensional tensors of shape [B, 3, 224, 224] "
        "and transfers them to GPU memory in pinned memory buffers, achieving sub-second dataloading throughput across hundreds of test lesions."
    )

    add_styled_heading(doc, "6.3 Model Inference Execution Demonstration", 2)
    add_body_paragraph(
        doc,
        "The forward inference pass feeds the preprocessed tensor through the 201 layers of DenseNet. Feature extraction takes 12 to 18 milliseconds per image on an NVIDIA "
        "Tesla T4 GPU (and approximately 140 milliseconds on multi-core CPU). The output linear head produces raw unbounded scalar logits z, which are mapped through a sigmoid "
        "activation to produce posterior probability p_hat = P(malignant | x)."
    )

    add_styled_heading(doc, "6.4 Threshold Calibration & Triage Generation", 2)
    add_body_paragraph(
        doc,
        "To provide actionable clinical decision support, continuous probabilities are mapped into a 3-tier clinical triage categorization system:"
    )
    add_list_item(
        doc,
        "• Tier 1: Low Suspicion / Routine Follow-up (p_hat < 0.30): Lesion exhibits predominantly benign structural characteristics; recommend annual skin check."
    )
    add_list_item(
        doc,
        "• Tier 2: Intermediate / Moderate Suspicion (0.30 <= p_hat < tau*): Borderline lesion showing ambiguous atypical features; recommend 3-month digital dermoscopy monitoring."
    )
    add_list_item(
        doc,
        "• Tier 3: High Risk / Urgent Dermatological Referral (p_hat >= tau*): High probability of malignant melanoma; generate immediate clinical alert and prioritize for urgent biopsy."
    )

    add_styled_heading(doc, "6.5 Output Visualizations Demonstration", 2)
    add_body_paragraph(
        doc,
        "The demonstration scripts generate comprehensive visual evaluation artifacts upon batch completion, including formatted confusion matrices displaying exact "
        "counts of TN, FP, FN, and TP, empirical ROC curves plotting sensitivity against 1-specificity across all potential operating thresholds, precision-recall curves "
        "highlighting precision trade-offs under class imbalance, and threshold-sensitivity sweeps illustrating how shifting decision boundaries affects clinical false negatives."
    )

print("Chapters 4 to 6 updated with clean typography.")
