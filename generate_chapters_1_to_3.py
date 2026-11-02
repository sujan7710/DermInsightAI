# -*- coding: utf-8 -*-
"""
DermInsight AI - Chapter 1 to 3 Content Builder (Clean Typography Version)
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

def add_chapter_1(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 1\n1. INTRODUCTION", 1)
    
    add_styled_heading(doc, "1.1 Background", 2)
    add_body_paragraph(
        doc,
        "Cutaneous malignant melanoma represents one of the most aggressive, biologically lethal, and treatment-resistant forms of human cancer. "
        "Although melanoma accounts for approximately one to five percent of all diagnosed skin cancers globally, it is responsible for over eighty "
        "percent of skin cancer-related mortalities worldwide. According to global cancer epidemiological statistics from the World Health Organization (WHO) "
        "and the International Agency for Research on Cancer (IARC), the worldwide incidence of melanoma has risen at an alarming rate over the past four decades, "
        "outpacing almost all other major solid malignancies, particularly among fair-skinned Caucasian populations in North America, Northern Europe, and Australasia."
    )
    add_body_paragraph(
        doc,
        "The clinical lethality of cutaneous melanoma is fundamentally governed by its rapid metastatic dissemination kinetics once vertical invasion penetrates "
        "the dermis and lymphatic vasculature. However, when detected in its earliest intraepidermal or micro-invasive stages (melanoma in situ or Stage I), surgical "
        "excision achieves a five-year relative survival rate exceeding ninety-eight percent. In sharp and tragic contrast, once malignant cells penetrate deep dermal layers "
        "and metastasize to regional lymph nodes or distant visceral organs (Stage IV), the five-year survival drops precipitously below twenty-five percent. Consequently, "
        "early, accurate, and non-invasive detection represents the single most decisive factor determining clinical prognosis and patient survival."
    )
    add_body_paragraph(
        doc,
        "In routine clinical practice, visual examination of suspicious pigmented lesions under naked-eye inspection exhibits notoriously low diagnostic accuracy. "
        "Dermoscopy—a non-invasive epiluminescence microscopy technique that illuminates and magnifies the skin surface while eliminating surface reflection—reveals "
        "sub-surface morphological structures, pigment network patterns, and vascular architectures invisible to the unaided eye. While dermoscopy substantially enhances "
        "diagnostic sensitivity, its clinical efficacy is heavily dependent on specialized dermatological expertise. In primary healthcare settings and underserved rural "
        "clinics where fellowship-trained dermatologists are scarce, general practitioners achieve melanoma diagnostic sensitivity of only sixty to seventy percent. "
        "This persistent diagnostic gap provides compelling motivation for automated computer-aided diagnostic (CAD) systems powered by deep learning."
    )

    add_styled_heading(doc, "1.2 Motivations", 2)
    add_body_paragraph(
        doc,
        "The development of an automated deep learning framework for early melanoma detection is driven by several urgent clinical, epidemiological, and technological factors:"
    )
    add_list_item(
        doc,
        "1. Severe Specialist Shortage and Clinical Triage Bottlenecks: There exists a catastrophic global shortage and severe geographic maldistribution of certified dermatologists. In rural regions, developing nations, and public healthcare systems, patients routinely face waiting lists of four to six months for an initial dermatological consultation. Given the rapid doubling time of nodular melanoma, such clinical delays can transform a curable early-stage lesion into an incurable metastatic disease. An automated screening triage tool can provide immediate, objective risk stratification at the point of primary care."
    )
    add_list_item(
        doc,
        "2. Subjectivity, Fatigue, and Diagnostic Inconsistency: Human visual dermoscopy is inherently subjective and prone to substantial intra-observer and inter-observer variability. Even board-certified dermatologists exhibit diagnostic concordance rates below eighty percent when inspecting ambiguous or early atypical lesions. Cognitive fatigue, high patient volumes, and visual distractors often lead to misdiagnoses. Deep convolutional neural networks offer deterministic, fatigue-free feature extraction capable of recognizing complex non-linear visual patterns across tens of thousands of dermoscopic images."
    )
    add_list_item(
        doc,
        "3. The Class-Imbalance Screening Paradox: Real-world population screening is plagued by the severe class-imbalance problem. In routine clinical encounters, malignant lesions represent less than two percent of all evaluated cutaneous nevi. Conventional machine learning algorithms trained on such heavily skewed distributions inevitably suffer from majority-class bias, achieving seemingly impressive overall accuracy (>98%) while failing to detect the very malignancies they were designed to catch. Overcoming this fundamental mathematical and clinical limitation is the central motivation of this investigation."
    )

    add_styled_heading(doc, "1.3 Scope of the Project", 2)
    add_body_paragraph(
        doc,
        "This research project, conducted under the academic designation BCSE497J — Project-I, focuses on establishing a verified, leakage-free deep learning experimental benchmark for automated binary skin cancer classification. The specific technical and clinical scope encompasses the following core facets:"
    )
    add_list_item(
        doc,
        "1. Ingesting and auditing the official Society for Imaging Informatics in Medicine - International Skin Imaging Collaboration (SIIM-ISIC) 2020 Melanoma Classification dataset, comprising 33,126 high-resolution dermoscopic images corresponding to 2,056 unique patients."
    )
    add_list_item(
        doc,
        "2. Enforcing a strict patient-level partitioning protocol (22,787 training, 5,419 validation, and 4,920 held-out test images) to completely eliminate patient identity leakage across experimental partitions."
    )
    add_list_item(
        doc,
        "3. Implementing an end-to-end deep learning pipeline utilizing an ImageNet-pretrained DenseNet201 (201 layers) architecture as the primary feature extraction backbone."
    )
    add_list_item(
        doc,
        "4. Designing, executing, and empirically verifying four distinct class-imbalance mitigation strategies: positive-weighted binary cross-entropy (W-BCE with pos_weight=50.21), PyTorch WeightedRandomSampler, Focal Loss (alpha=0.75, gamma=2.0), and training-isolated Random Oversampling."
    )
    add_list_item(
        doc,
        "5. Calibrating decision thresholds on validation data and conducting an uncompromised evaluation on the 4,920 held-out test set to quantify sensitivity, specificity, PR-AUC, ROC-AUC, and clinical false-negative risk."
    )
    add_list_item(
        doc,
        "6. Establishing an unvarnished audit of project limitations, explicitly delineating completed image-only vision models from proposed future multimodal tabular metadata fusion and explainability modules."
    )

def add_chapter_2(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 2\n2. PROJECT DESCRIPTION AND GOALS", 1)
    
    add_styled_heading(doc, "2.1 Literature Review", 2)
    add_body_paragraph(
        doc,
        "The application of computer vision and machine learning to automated dermoscopic image analysis has evolved dramatically over the past two decades. "
        "Early diagnostic systems relied on handcrafted morphological feature extraction based on the clinical ABCD rule of dermoscopy (Asymmetry, Border irregularity, "
        "Color variegation, and Diameter > 6mm) or the 7-Point Checklist (Celebi et al., 2019; Adegun & Viriri, 2021). These conventional systems extracted low-level "
        "geometric descriptors, texture features via gray-level co-occurrence matrices (GLCM), and color histograms, feeding them into shallow classifiers such as Support "
        "Vector Machines (SVM) or Random Forests. While foundational, handcrafted systems suffered from poor generalization across diverse imaging devices, illumination "
        "variations, and subtle morphological phenotypes."
    )
    add_body_paragraph(
        doc,
        "A monumental paradigm shift occurred with the advent of deep convolutional neural networks (CNNs). In a landmark study published in Nature, Esteva et al. (2017) "
        "demonstrated that a deep CNN (Inception-v3) pretrained on 1.28 million natural images from ImageNet and fine-tuned on a clinical dataset of 129,450 dermoscopic and "
        "clinical images achieved diagnostic sensitivity and specificity on par with twenty-one board-certified dermatologists across biopsy-proven malignant lesions. "
        "Subsequent clinical validation trials by Haenssle et al. (2018) and Brinker et al. (2019) reinforced these findings, showing that deep learning architectures "
        "outperformed 136 of 157 dermatologists in international multi-reader diagnostic studies."
    )
    add_body_paragraph(
        doc,
        "Transfer learning has emerged as the universal cornerstone of medical computer vision (Yosinski et al., 2014; Deng et al., 2009). Because annotated medical datasets "
        "are orders of magnitude smaller than natural vision benchmarks, training a deep architecture from scratch inevitably leads to catastrophic overfitting. Initializing "
        "backbones with ImageNet-pretrained weights allows early convolutional layers to transfer universal low-level visual representations—such as Gabor-like edge detectors, "
        "color gradients, and textural primitives—while fine-tuning adapts higher-level semantic filters to lesion-specific pathological structures (He et al., 2016; Tan & Le, 2019)."
    )
    add_body_paragraph(
        doc,
        "Among modern deep architectures, the Densely Connected Convolutional Network (DenseNet), introduced by Huang et al. (2017), offers profound structural advantages "
        "for medical image classification. DenseNet introduces direct connections from every layer to all subsequent layers within a dense block: x_l = H_l([x_0, x_1, ..., x_{l-1}]). "
        "This dense connectivity maximizes feature reuse throughout the network, alleviates the vanishing-gradient problem during backpropagation, substantially reduces the number "
        "of trainable parameters compared to traditional ResNets, and retains low-level textural details across all spatial resolutions—a property critically beneficial for "
        "detecting subtle pigment reticulation and atypical vascular structures in skin lesions."
    )
    add_body_paragraph(
        doc,
        "The curation of standardized international benchmark datasets by the International Skin Imaging Collaboration (ISIC) has propelled the field forward (Codella et al., 2018; "
        "Tschandl et al., 2018). While earlier datasets like HAM10000 provided multiclass diagnostic labels for common pigmented lesions, the SIIM-ISIC 2020 Melanoma Classification "
        "Challenge introduced a patient-centric, real-world screening benchmark of 33,126 dermoscopic images (Rotemberg et al., 2021). Unlike previous collections where benign and "
        "malignant classes were artificially balanced, ISIC 2020 mirrors actual population screening prevalence, with malignant melanoma representing only 1.76% of all cases."
    )
    add_body_paragraph(
        doc,
        "Class imbalance presents a severe obstacle in training deep networks (Buda et al., 2018). When optimizing standard cross-entropy loss on a dataset with a 55:1 negative-to-positive "
        "ratio, the gradient contribution from the overwhelming majority class completely drowns out the gradient updates from rare positive examples. To counteract this pathology, "
        "researchers employ cost-sensitive reweighting (Weighted Cross-Entropy), data-level oversampling or undersampling (Chawla et al., 2002), and dynamically scaled loss formulations "
        "such as Focal Loss (Lin et al., 2017). Focal Loss introduces a modulating factor (1 - p_t)^gamma that down-weights easy, well-classified background examples and focuses parameter "
        "updates on hard, ambiguous lesions."
    )
    add_body_paragraph(
        doc,
        "Crucially, the literature emphasizes that standard classification accuracy is completely deceptive when evaluating imbalanced clinical systems (Saito & Rehmsmeier, 2015; "
        "Davis & Goadrich, 2006). A naive dummy classifier that unconditionally predicts 'benign' achieves an accuracy of 98.24% on ISIC 2020 while exhibiting zero clinical utility. "
        "Consequently, threshold-independent ranking metrics such as Area Under the Receiver Operating Characteristic (ROC-AUC) and Precision-Recall Area Under the Curve (PR-AUC / AP) "
        "must be prioritized alongside threshold-calibrated clinical metrics including Sensitivity (Recall), Specificity, and Positive Predictive Value (Precision)."
    )
    add_body_paragraph(
        doc,
        "Furthermore, recent critical audits by Cassidy et al. (2022) revealed widespread methodological flaws in published dermatology AI literature, most notably data leakage "
        "caused by random train-test splitting. Because individual patients frequently contribute multiple dermoscopic images of varying lesions, random image-level partitioning "
        "places images from the same patient into both training and test sets. This enables neural networks to memorize patient-specific skin textures and imaging artifacts rather "
        "than learning generalizable pathological features, artificially inflating reported test performance by 5 to 12% ROC-AUC. Enforcing strict patient-level splitting is therefore "
        "an indispensable prerequisite for scientific validity."
    )
    add_body_paragraph(
        doc,
        "Emerging frontiers in dermatology AI emphasize multimodal metadata fusion—combining dermoscopic images with patient age, sex, and anatomical location (Pacheco & Krohling, 2020; "
        "Kawahara et al., 2019)—as well as model interpretability via Gradient-weighted Class Activation Mapping (Grad-CAM; Selvaraju et al., 2017). Concurrently, algorithmic fairness audits "
        "have revealed stark performance disparities across Fitzpatrick skin phototypes, underscoring that models trained predominantly on light-skinned cohorts generalize poorly to darker "
        "skin tones (Daneshjou et al., 2022; Groh et al., 2021). While these advanced paradigms represent vital long-term goals, establishing a rigorously verified, leakage-free vision "
        "baseline under extreme class imbalance remains the foundational first step."
    )

    add_styled_heading(doc, "2.2 Research Gap", 2)
    add_body_paragraph(
        doc,
        "Despite hundreds of publications on skin lesion classification, a critical research gap persists in the translation of deep learning models to clinically viable screening tools. "
        "Existing studies predominantly report high nominal ROC-AUC (>0.85) and top-line accuracy (>95%), yet fail to investigate or report the actual operational sensitivity and false-negative "
        "rates when models are deployed at concrete classification thresholds under real-world class imbalance (~55:1 ratio)."
    )
    add_body_paragraph(
        doc,
        "Most published pipelines default to an arbitrary 0.5 probability threshold without validation calibration, resulting in models that either miss over 75% of malignant melanomas "
        "or flood clinical workflows with thousands of false-positive alarms. Furthermore, a substantial portion of the literature suffers from unacknowledged patient-level data leakage, "
        "rendering claimed generalization questionable. This project directly addresses this gap by auditing the entire pipeline: enforcing patient-level isolation, systematically benchmarking "
        "four class-imbalance formulations on identical splits, calibrating decision thresholds on validation data, and honestly documenting the true trade-off between sensitivity and specificity."
    )

    add_styled_heading(doc, "2.3 Objectives", 2)
    add_body_paragraph(
        doc,
        "The primary engineering and scientific objectives of this Project-I investigation are defined as follows:"
    )
    add_list_item(
        doc,
        "1. Construct a Leakage-Free Medical Vision Benchmark: Partition the 33,126 dermoscopic images of SIIM-ISIC 2020 into training, validation, and test sets using strict patient-level isolation, verifying that patient set intersections are exactly zero."
    )
    add_list_item(
        doc,
        "2. Implement a Deep Convolutional Backbone: Construct an ImageNet-pretrained DenseNet201 feature extraction and classification pipeline, optimizing preprocessing and normalization."
    )
    add_list_item(
        doc,
        "3. Systematically Benchmark Imbalance Strategies: Implement and train five controlled experimental configurations: Baseline DenseNet201, Weighted Binary Cross-Entropy (W-BCE), PyTorch WeightedRandomSampler, Focal Loss (alpha=0.75, gamma=2.0), and Random Oversampling."
    )
    add_list_item(
        doc,
        "4. Calibrate Operational Decision Thresholds: Perform comprehensive threshold sweeps on validation data to identify operating points that maximize clinical sensitivity while constraining false positives."
    )
    add_list_item(
        doc,
        "5. Conduct Unvarnished Evaluation: Evaluate all models on an identical 4,920 held-out test set, analyzing confusion matrices, PR-AUC, ROC-AUC, and clinical misclassification costs."
    )
    add_list_item(
        doc,
        "6. Establish a Foundation for Multimodal Expansion: Document architectural boundaries and establish reproducible checkpoints for future tabular metadata fusion and explainability modules."
    )

    add_styled_heading(doc, "2.4 Problem Statement", 2)
    add_body_paragraph(
        doc,
        "Formally, given a dataset of dermoscopic skin lesion images D = {(x_i, y_i, p_i)}_{i=1}^N, where x_i in R^{H x W x 3} is a dermoscopic image, y_i in {0, 1} is the ground-truth "
        "histopathological label (0 = benign, 1 = malignant melanoma), and p_i in P represents the unique patient identifier, the objective is to learn a parameterized mapping function "
        "f_theta: x -> [0, 1] that predicts the posterior probability of malignancy p_hat = P(y = 1 | x)."
    )
    add_body_paragraph(
        doc,
        "The optimization problem is constrained by two severe real-world challenges:"
    )
    add_list_item(
        doc,
        "1. Patient-Level Group Constraint: P_train intersect P_val = emptyset, P_train intersect P_test = emptyset, and P_val intersect P_test = emptyset, ensuring that no patient identity information is shared across training and evaluation partitions."
    )
    add_list_item(
        doc,
        "2. Extreme Class Skew: The marginal class distribution satisfies P(y = 1) = 0.0176 and P(y = 0) = 0.9824. Under standard empirical risk minimization, the optimal Bayesian decision boundary collapses to predicting the majority class. The technical challenge is to formulate loss functions and sampling policies that maximize the detection of rare malignant lesions (Recall / Sensitivity) while maintaining clinically acceptable specificity under asymmetric misclassification costs where Cost(FN) >> Cost(FP)."
    )

    add_styled_heading(doc, "2.5 Project Plan", 2)
    add_body_paragraph(
        doc,
        "The project was executed across four structured academic phases during the Project-I research period:"
    )
    add_list_item(
        doc,
        "• Phase 1: Dataset Acquisition, Integrity Verification, and Patient-Level Partitioning (Weeks 1-3)."
    )
    add_list_item(
        doc,
        "• Phase 2: Architecture Construction, Preprocessing Pipeline, and Baseline DenseNet201 Training (Weeks 4-6)."
    )
    add_list_item(
        doc,
        "• Phase 3: Class-Imbalance Formulation Experiments (Weighted BCE, WeightedRandomSampler, Focal Loss, Random Oversampling) and Checkpoint Optimization (Weeks 7-10)."
    )
    add_list_item(
        doc,
        "• Phase 4: Held-Out Test Evaluation, Decision Threshold Calibration, Cost Analysis, and Comprehensive Academic Verification (Weeks 11-13)."
    )

def add_chapter_3(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 3\n3. TECHNICAL SPECIFICATION", 1)
    
    add_styled_heading(doc, "3.1 Requirements", 2)
    add_styled_heading(doc, "3.1.1 Functional Requirements", 3)
    add_body_paragraph(
        doc,
        "The functional requirements define the core operational capabilities of the DermInsight AI deep learning screening framework:"
    )
    add_list_item(
        doc,
        "1. Image Ingestion and Validation: The framework must ingest raw dermoscopic images in standard formats (JPEG/PNG), verify image integrity, check for corrupted headers, and associate image identifiers with ground-truth patient metadata."
    )
    add_list_item(
        doc,
        "2. Deterministic Preprocessing: The system must resize all input images to 224 x 224 pixels using bilinear interpolation and apply channel-wise ImageNet normalization (mean and std)."
    )
    add_list_item(
        doc,
        "3. Patient-Isolated Batch Loading: The dataloader must enforce patient-level isolation and support dynamic batch sampling using PyTorch WeightedRandomSampler for imbalance handling."
    )
    add_list_item(
        doc,
        "4. Feature Extraction and Logit Computation: The framework must feed image tensors through the 201-layer DenseNet backbone, pool feature maps to a 1,920-dimensional representation, and compute raw scalar logits."
    )
    add_list_item(
        doc,
        "5. Probability and Triage Generation: The system must map logits to posterior probabilities via sigmoid activation and categorize lesions into actionable triage tiers (Low Risk, Moderate Suspicion, High Malignancy Risk) based on calibrated decision thresholds."
    )
    add_list_item(
        doc,
        "6. Evaluation Metric Generation: The framework must automatically compute accuracy, precision, sensitivity, specificity, F1-score, ROC-AUC, Average Precision, and confusion matrices."
    )

    add_styled_heading(doc, "3.1.2 Non-Functional Requirements", 3)
    add_body_paragraph(
        doc,
        "The non-functional requirements govern the performance, reliability, and reproducibility of the system:"
    )
    add_list_item(
        doc,
        "1. Inference Latency: The model must achieve a single-image inference latency of less than 150 milliseconds on GPU and under 800 milliseconds on CPU, enabling real-time clinical screening."
    )
    add_list_item(
        doc,
        "2. Numerical Reproducibility: All random processes (weight initialization, augmentations, sampling) must be deterministic by fixing random seeds (SEED = 42) across Python, NumPy, and PyTorch environments."
    )
    add_list_item(
        doc,
        "3. Memory Footprint: Model memory footprint must not exceed 250 MB in RAM/VRAM, permitting deployment on edge clinical devices and standard workstations."
    )
    add_list_item(
        doc,
        "4. Auditability and Integrity: All checkpoints, training logs, prediction CSVs, and evaluation metrics must be saved as immutable disk artifacts with cryptographic tracking."
    )
    add_list_item(
        doc,
        "5. Modularity: The architecture must decouple dataset loading, model backbone, loss computation, and evaluation into modular components to facilitate future multimodal expansion."
    )

    add_styled_heading(doc, "3.2 Feasibility Study", 2)
    add_styled_heading(doc, "3.2.1 Technical Feasibility", 3)
    add_body_paragraph(
        doc,
        "The technical feasibility of the proposed system is substantiated by established computer vision breakthroughs. Deep convolutional neural networks, particularly DenseNet201, "
        "have demonstrated robust feature representation capabilities on complex medical imaging tasks. The availability of high-performance transfer learning via ImageNet-pretrained "
        "weights eliminates the need for millions of labeled dermatological images. PyTorch provides native, optimized implementations of automatic differentiation, GPU acceleration via "
        "CUDA, and modular loss functions (Weighted BCE, Focal Loss), confirming full technical feasibility."
    )

    add_styled_heading(doc, "3.2.2 Economic Feasibility", 3)
    add_body_paragraph(
        doc,
        "The project is highly economically feasible. The entire software stack—including Python, PyTorch, torchvision, scikit-learn, pandas, and Linux/Windows environments—is completely "
        "open-source, incurring zero licensing fees. Training was conducted using standard cloud GPU instances (Google Colab / Kaggle T4 GPUs) and academic workstations with modest compute "
        "costs. In clinical translation, an automated screening system provides massive economic benefits by reducing unnecessary benign biopsies (which cost healthcare systems hundreds of "
        "millions annually) while averting the enormous financial burden of late-stage metastatic melanoma treatments."
    )

    add_styled_heading(doc, "3.2.3 Social Feasibility", 3)
    add_body_paragraph(
        doc,
        "From a social and ethical perspective, DermInsight AI addresses critical public healthcare disparities. In rural and socioeconomically disadvantaged regions where dermatological "
        "care is unavailable, an automated CAD screening tool empowers primary healthcare practitioners to triage high-risk lesions for urgent specialist referral. Furthermore, the system "
        "is explicitly designed as an assistive clinical decision-support tool rather than an autonomous diagnostic agent, preserving the physician-patient relationship and upholding "
        "medical ethics."
    )

    add_styled_heading(doc, "3.3 System Specification", 2)
    add_styled_heading(doc, "3.3.1 Hardware Specification", 3)
    add_table_caption(doc, "Table 3.1: Hardware System Specifications")
    
    t_hw = doc.add_table(rows=6, cols=3)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hw.autofit = False
    t_hw.columns[0].width = Inches(1.8)
    t_hw.columns[1].width = Inches(2.3)
    t_hw.columns[2].width = Inches(2.4)
    set_table_borders(t_hw, "D3D3D3")
    
    hw_data = [
        ("Component", "Training Environment (Cloud)", "Audit & Verification Workstation"),
        ("Processor (CPU)", "Intel Xeon @ 2.20 GHz (2 vCPUs)", "Intel Core i7 / AMD Ryzen (Multi-core)"),
        ("Graphics (GPU)", "NVIDIA Tesla T4 (16 GB GDDR6)", "NVIDIA GeForce / OpenCL / CPU"),
        ("System RAM", "12.7 GB High-RAM Instance", "16.0 GB DDR4/DDR5"),
        ("Primary Storage", "100 GB Cloud Disk", "512 GB NVMe SSD"),
        ("CUDA Compute Capability", "7.5 (Turing Architecture)", "CUDA 12.x / CPU Execution")
    ]
    for r_idx, row in enumerate(hw_data):
        for c_idx, val in enumerate(row):
            cell = t_hw.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F4F7")
            set_cell_margins(cell, 80, 80, 100, 100)

    add_styled_heading(doc, "3.3.2 Software Specification", 3)
    add_table_caption(doc, "Table 3.2: Software Environment Specifications")
    
    t_sw = doc.add_table(rows=8, cols=3)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sw.autofit = False
    t_sw.columns[0].width = Inches(1.8)
    t_sw.columns[1].width = Inches(2.3)
    t_sw.columns[2].width = Inches(2.4)
    set_table_borders(t_sw, "D3D3D3")
    
    sw_data = [
        ("Layer", "Package / Tool", "Version & Configuration"),
        ("Operating System", "Ubuntu Linux / Windows 11", "64-bit Architecture"),
        ("Core Language", "Python", "Version 3.10 / 3.12"),
        ("Deep Learning Framework", "PyTorch", "Version 2.2+ with Torchvision 0.17+"),
        ("CUDA Driver", "NVIDIA CUDA Toolkit", "Version 12.1 / cuDNN 8.9"),
        ("Data Processing", "Pandas & NumPy", "Pandas 2.2+, NumPy 1.26+"),
        ("Scientific Evaluation", "scikit-learn & SciPy", "Version 1.4+"),
        ("Visualization", "Matplotlib & Seaborn", "Matplotlib 3.8+, Seaborn 0.13+")
    ]
    for r_idx, row in enumerate(sw_data):
        for c_idx, val in enumerate(row):
            cell = t_sw.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F4F7")
            set_cell_margins(cell, 80, 80, 100, 100)

    # Add Figure 3.1: Dataset class distribution
    p_fig = doc.add_paragraph()
    p_fig.paragraph_format.space_before = Pt(14)
    add_figure(
        doc,
        os.path.join(FIG_DIR, 'dataset_class_distribution.png'),
        "Figure 3.1: SIIM-ISIC 2020 Dataset Lesion Class Distribution on Logarithmic Scale (32,542 Benign vs. 584 Malignant)",
        width_inches=5.6
    )

print("Chapters 1 to 3 updated with clean typography.")
