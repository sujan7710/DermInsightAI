# -*- coding: utf-8 -*-
"""
DermInsight AI - Chapter 1 to 3 Content Builder (Revised Human-Edited Version)
Reflects authentic undergraduate engineering research writing: direct, clear,
project-specific, and free of formulaic AI buzzwords.
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
        "Melanoma kills more people than every other form of skin cancer combined. That single fact shaped "
        "the entire direction of our project. Even though melanoma makes up roughly one to three percent of "
        "all skin cancer diagnoses, it's responsible for the overwhelming majority of deaths. Timing is "
        "everything here — catch it early, while the tumor is still sitting in the top layer of skin, and "
        "five-year survival hovers around ninety-nine percent. Let it grow deeper, spread to lymph nodes "
        "or distant organs, and that number crashes below twenty-five percent. Late-stage treatments exist, "
        "but they're expensive and the long-term outcomes are often disappointing. So early detection isn't "
        "just preferable — it's really the only reliable way to save lives."
    )
    add_body_paragraph(
        doc,
        "Spotting melanoma early sounds simple in theory. In practice, it's anything but. Young melanomas "
        "can look almost identical to harmless moles, seborrheic keratoses, or slightly irregular nevi. "
        "Dermoscopy helps — it uses magnification and polarized light to reveal structures beneath the skin "
        "surface, things like pigment networks, globules, streaks, and unusual vascular patterns that aren't "
        "visible to the naked eye. But reading dermoscopic images well takes years of specialized training. "
        "At most primary care clinics and community health centers, where patients first show up with a "
        "suspicious spot, there's usually no trained dermatologist in the building. General practitioners "
        "do their best, but their diagnostic accuracy is noticeably lower. "
        "That gap — between what a specialist could catch and what a frontline doctor actually does catch — "
        "is exactly where an automated screening tool could make a real difference."
    )

    add_styled_heading(doc, "1.2 Motivations", 2)
    add_body_paragraph(
        doc,
        "We built DermInsight AI because we kept running into three problems that felt both urgent and solvable:"
    )
    add_list_item(
        doc,
        "1. Long waits for specialists: In many public and regional hospitals, getting a dermatologist "
        "appointment can take weeks, sometimes months. Aggressive melanomas — particularly the nodular "
        "kind — can double in thickness during that waiting period. That's a direct threat to patient "
        "survival. An automated triage layer sitting in primary care could flag the dangerous cases right "
        "away, so doctors know which referrals can't wait."
    )
    add_list_item(
        doc,
        "2. Inconsistent diagnoses: Dermoscopy is subjective. Two experienced clinicians looking at "
        "the same borderline lesion disagree more often than you'd expect — concordance drops below "
        "eighty percent on ambiguous cases. A trained model won't get tired, distracted, or biased "
        "by what it saw five minutes ago. It gives the same answer every time for the same input, "
        "which makes it a useful second opinion, even if it isn't perfect."
    )
    add_list_item(
        doc,
        "3. The class imbalance problem: This one surprised us the most when we first dug into the "
        "SIIM-ISIC 2020 dataset. Only 584 out of 33,126 images are malignant — that's just 1.76%. "
        "A naive model that blindly labels everything as benign gets 98.24% accuracy while catching "
        "exactly zero cancers. Designing a training pipeline that doesn't fall into this trap became "
        "the central technical challenge of our work."
    )

    add_styled_heading(doc, "1.3 Scope of the Project", 2)
    add_body_paragraph(
        doc,
        "We carried out this project under course code BCSE497J — Project-I. The goal was to build "
        "a reproducible deep learning pipeline for binary melanoma classification and stress-test it "
        "under realistic conditions. Here's what falls inside our scope:"
    )
    add_list_item(
        doc,
        "1. Dataset Ingestion and Audit: We worked with the full SIIM-ISIC 2020 challenge dataset — "
        "33,126 dermoscopic images from 2,056 unique patients. Before training anything, we audited "
        "every metadata field and verified image integrity."
    )
    add_list_item(
        doc,
        "2. Patient-Level Splitting: We enforced complete patient isolation across our three splits: "
        "training (22,787 images from 1,439 patients), validation (5,419 images from 307 patients), "
        "and test (4,920 images from 310 patients). No patient appears in more than one split. Period."
    )
    add_list_item(
        doc,
        "3. Deep Learning Architecture: We used a DenseNet201 pretrained on ImageNet as our backbone "
        "feature extractor, replacing the original classification head with a single linear layer "
        "(1920→1) for binary prediction."
    )
    add_list_item(
        doc,
        "4. Class-Imbalance Investigation: We trained and compared four different strategies for handling "
        "the ~55:1 skew: positive-weighted binary cross-entropy (W-BCE with pos_weight=50.21), "
        "PyTorch WeightedRandomSampler, Focal Loss (alpha=0.75, gamma=2.0), and random oversampling "
        "of the minority class."
    )
    add_list_item(
        doc,
        "5. Validation Threshold Calibration: Rather than just picking 0.5 as our decision cutoff, "
        "we swept a range of thresholds on the validation set to find operating points that actually "
        "balance sensitivity and false alarm rate."
    )
    add_list_item(
        doc,
        "6. Transparent Reporting: Every model was tested on the same 4,920 held-out images. We report "
        "full confusion matrices, ROC-AUC, Average Precision, and — most importantly — exact false-negative "
        "counts. No cherry-picking."
    )
    add_list_item(
        doc,
        "7. Project Boundaries: We want to be upfront about what we didn't do. This phase is strictly "
        "image-only. Fusing in patient metadata (age, sex, body site) and adding Grad-CAM explainability "
        "maps are planned for Project-II, but we aren't claiming them as done here."
    )

def add_chapter_2(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 2\n2. PROJECT DESCRIPTION AND GOALS", 1)
    
    add_styled_heading(doc, "2.1 Literature Review", 2)
    add_body_paragraph(
        doc,
        "Skin lesion analysis has changed dramatically over the past fifteen or so years. The field "
        "moved from hand-designed feature pipelines to deep learning, and we spent a good chunk of "
        "our early project weeks reading through that history. It helped us figure out which "
        "architecture to start with, which evaluation mistakes to avoid, and how to structure our "
        "imbalance experiments."
    )
    add_body_paragraph(
        doc,
        "The earliest automated systems tried to mimic what dermatologists do by hand — check "
        "asymmetry, border irregularity, color variation, and diameter (the ABCD rule), or run through "
        "the 7-Point Checklist (Celebi et al., 2019; Adegun & Viriri, 2021). These approaches used "
        "classic image processing: segment the lesion boundary with active contours or Otsu thresholding, "
        "pull out shape descriptors and GLCM textures, then feed those features into an SVM or a shallow "
        "Random Forest. The appeal was interpretability. The problem was fragility. Border segmentation "
        "broke constantly across different cameras, lighting conditions, and skin tones."
    )
    add_body_paragraph(
        doc,
        "Everything shifted when Esteva et al. (2017) showed that an Inception-v3 network, pretrained on "
        "ImageNet's 1.28 million images and then fine-tuned on clinical photos, could match twenty-one "
        "board-certified dermatologists on diagnostic sensitivity and specificity. That paper got a lot of "
        "attention, and for good reason — it proved that deep convolutional filters can pick up on subtle "
        "dermoscopic textures directly from raw pixels, skipping the whole manual feature engineering step. "
        "Follow-up reader studies by Haenssle et al. (2018) and Brinker et al. (2019) backed this up."
    )
    add_body_paragraph(
        doc,
        "But why transfer learning? Why not train from scratch? The short answer is data. "
        "Dermatology datasets are tiny compared to ImageNet. If you initialize a deep network with random "
        "weights and train it on, say, a few hundred malignant dermoscopy images, it overfits almost "
        "immediately. Starting from ImageNet-pretrained weights gives the early layers useful edge "
        "detectors, color gradient filters, and textural primitives that transfer surprisingly well to "
        "medical images (Deng et al., 2009; Yosinski et al., 2014; He et al., 2016; Tan & Le, 2019). "
        "You only need to fine-tune the deeper, task-specific layers."
    )
    add_body_paragraph(
        doc,
        "We picked DenseNet201 (Huang et al., 2017) as our backbone for a specific reason. In a standard "
        "CNN, each layer only sees the output of the layer right before it. DenseNet wires things differently — "
        "within each dense block, every layer gets the feature maps from all preceding layers concatenated "
        "together: x_l = H_l([x_0, x_1, ..., x_{l-1}]). What does that buy us in practice? Three things. "
        "It encourages heavy feature reuse across layers. It keeps fine-grained low-level details — like "
        "delicate pigment network patterns — alive all the way to the final classifier. And it helps with "
        "vanishing gradients while actually needing fewer parameters than a comparably deep ResNet."
    )
    add_body_paragraph(
        doc,
        "On the data side, public benchmarks from the International Skin Imaging Collaboration (ISIC) "
        "have been a game-changer (Codella et al., 2018; Tschandl et al., 2018). Earlier datasets like "
        "HAM10000 offered reasonably balanced multi-class labels. The SIIM-ISIC 2020 dataset (Rotemberg "
        "et al., 2021) is a different beast entirely: 33,126 images from a real screening population, "
        "with malignant cases at just 1.76%. That prevalence is clinically realistic, which is great for "
        "relevance — but it creates serious optimization headaches (Buda et al., 2018)."
    )
    add_body_paragraph(
        doc,
        "The literature offers several strategies for dealing with imbalance. Weighted cross-entropy "
        "multiplies the loss on minority-class samples by a penalty factor, so the model pays a heavier "
        "price for missing a melanoma. Focal Loss, introduced by Lin et al. (2017), takes a different "
        "angle — it adds a (1 - p_t)^gamma modulating term that automatically downweights the easy, "
        "well-classified benign samples and focuses the gradient signal on the hard, borderline cases. "
        "Then there are data-level fixes like oversampling (Chawla et al., 2002), which change the "
        "sampling distribution during training without touching the loss function at all. We wanted "
        "to try each of these and see which one actually helps on our dataset."
    )
    add_body_paragraph(
        doc,
        "One thing we learned from the literature that really stuck with us: accuracy is misleading on "
        "imbalanced datasets. Saito & Rehmsmeier (2015) and Davis & Goadrich (2006) both make this "
        "point clearly. When ninety-eight percent of your images are benign, a model that just says "
        "'benign' for everything looks great on accuracy. Precision-Recall curves, Average Precision, "
        "and sensitivity at fixed thresholds tell you much more about whether the model is actually "
        "catching melanomas."
    )
    add_body_paragraph(
        doc,
        "And then there's the leakage issue. Cassidy et al. (2022) showed that a lot of published "
        "dermatology studies don't properly separate patients across train and test splits. When images "
        "from the same patient end up on both sides, the model can memorize skin tone, lighting, "
        "even camera artifacts — and reported AUC can be inflated by up to 10%. "
        "We took that warning seriously and made patient-level splitting non-negotiable in our pipeline."
    )
    add_body_paragraph(
        doc,
        "Recent papers also point toward multimodal fusion — combining pixel data with patient age, "
        "sex, and lesion location (Pacheco & Krohling, 2020; Kawahara et al., 2019) — along with "
        "explainability via Grad-CAM (Selvaraju et al., 2017) and fairness audits across Fitzpatrick "
        "skin types (Daneshjou et al., 2022; Groh et al., 2021). These are all important for real clinical "
        "deployment. But we decided early on that our priority for Project-I was to get the vision baseline "
        "right first — leakage-free, honestly evaluated, under realistic class skew — before layering "
        "anything else on top."
    )

    add_styled_heading(doc, "2.2 Research Gap", 2)
    add_body_paragraph(
        doc,
        "Plenty of published papers claim accuracy above 95% and ROC-AUC over 0.85 for skin lesion "
        "classification. Those numbers sound impressive until you look at what's behind them. Most "
        "of these studies evaluate at a default threshold of 0.5 and don't examine what happens to "
        "sensitivity and specificity under the kind of extreme imbalance we see in real screening "
        "populations (~55:1 ratio). Our own experiments show this gap clearly: a model can hit 97% "
        "accuracy and an ROC-AUC of 0.83 while still missing over 75% of actual melanomas. That's "
        "clinically useless."
    )
    add_body_paragraph(
        doc,
        "On top of that, a lot of benchmarks never confirm whether patient-level isolation was "
        "actually enforced, leaving their test scores vulnerable to identity leakage. We designed "
        "our project specifically to fill this gap: strict patient-level splits, systematic testing "
        "of multiple imbalance strategies on identical data partitions, threshold calibration on "
        "validation data, and complete transparency about false-negative counts."
    )

    add_styled_heading(doc, "2.3 Objectives", 2)
    add_body_paragraph(
        doc,
        "Given those gaps, we set ourselves six concrete objectives for Project-I:"
    )
    add_list_item(
        doc,
        "1. Leakage-Free Data Pipeline: Audit the SIIM-ISIC 2020 dataset and split all 33,126 images "
        "into train, validation, and test sets using patient-level isolation. Zero patient overlap — "
        "we verified this programmatically."
    )
    add_list_item(
        doc,
        "2. Baseline Architecture Implementation: Set up an ImageNet-pretrained DenseNet201 with "
        "a single-output binary logit head and confirm it handles our input dimensions correctly."
    )
    add_list_item(
        doc,
        "3. Controlled Imbalance Benchmarking: Train and compare four imbalance-handling strategies — "
        "Baseline DenseNet201, Weighted BCE (pos_weight=50.21), PyTorch WeightedRandomSampler, "
        "Focal Loss (alpha=0.75, gamma=2.0), and Random Oversampling — all on the exact same splits."
    )
    add_list_item(
        doc,
        "4. Operational Threshold Calibration: Run threshold sweeps on the validation set to find "
        "decision boundaries that actually balance melanoma recall against false alarm rate."
    )
    add_list_item(
        doc,
        "5. Independent Test Evaluation: Test every trained checkpoint on the 4,920 held-out images. "
        "Report confusion matrices, sensitivity, specificity, precision, F1, and PR curves."
    )
    add_list_item(
        doc,
        "6. Honest Auditing and Scope Definition: Keep an audit matrix of all verified checkpoints, "
        "be clear about limitations, and lay the groundwork for multimodal Project-II work."
    )

    add_styled_heading(doc, "2.4 Problem Statement", 2)
    add_body_paragraph(
        doc,
        "At its core, we're solving a supervised binary classification problem — but under two conditions "
        "that make it much harder than a standard image classification task. The dataset can be written as "
        "D = {(x_i, y_i, p_i)}_{i=1}^N, where x_i in R^{224 x 224 x 3} is a preprocessed dermoscopic "
        "image, y_i in {0, 1} is the ground-truth label (0 for benign, 1 for malignant melanoma), "
        "and p_i in P is the patient identifier."
    )
    add_body_paragraph(
        doc,
        "Two constraints govern the entire learning setup:"
    )
    add_list_item(
        doc,
        "1. Patient-Level Group Isolation: We partition the patient set P into three disjoint subsets — "
        "P_train, P_val, and P_test — with P_train intersect P_val = emptyset, P_train intersect P_test "
        "= emptyset, and P_val intersect P_test = emptyset. No images from any evaluation patient can "
        "appear during training."
    )
    add_list_item(
        doc,
        "2. Skewed Posterior Estimation: Malignant cases sit at just 1.76% of the data. We need to "
        "learn parameters theta for a model f_theta(x) that maps an unseen image x to a malignancy "
        "probability p_hat in [0, 1]. The model has to catch as many melanomas as possible without "
        "flooding clinics with false positives — because in practice, missing a cancer is far worse "
        "than ordering one extra biopsy."
    )

    add_styled_heading(doc, "2.5 Project Plan", 2)
    add_body_paragraph(
        doc,
        "We broke the semester into four phases. In hindsight, the timeline was tight, but we stuck "
        "to it:"
    )
    add_list_item(
        doc,
        "• Phase 1: Data Ingestion and Leakage Audit (Weeks 1–3). We downloaded the raw ISIC 2020 "
        "metadata, verified patient counts, built patient-isolated split CSVs, and double-checked "
        "that no patient leaked across boundaries."
    )
    add_list_item(
        doc,
        "• Phase 2: Pipeline Setup and Baseline Training (Weeks 4–6). We wrote the PyTorch dataset "
        "classes, plugged in the pretrained DenseNet201, set up augmentation, and ran our first "
        "baseline training loop."
    )
    add_list_item(
        doc,
        "• Phase 3: Imbalance Handling Experiments (Weeks 7–10). This was the meat of the project. "
        "We trained and logged four imbalance configurations: Weighted BCE, WeightedRandomSampler, "
        "Focal Loss, and Random Oversampling."
    )
    add_list_item(
        doc,
        "• Phase 4: Validation Calibration, Testing, and Verification (Weeks 11–13). We swept "
        "thresholds on the validation set, ran final evaluations on all checkpoints against the "
        "held-out test set, generated ROC/PR comparison plots, and compiled the audit matrix."
    )

def add_chapter_3(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 3\n3. TECHNICAL SPECIFICATION", 1)
    
    add_styled_heading(doc, "3.1 Requirements", 2)
    add_styled_heading(doc, "3.1.1 Functional Requirements", 3)
    add_body_paragraph(
        doc,
        "Below is what the DermInsight AI pipeline needs to actually do — from loading images "
        "to producing a triage recommendation:"
    )
    add_list_item(
        doc,
        "1. Image Ingestion and Format Checking: The system loads JPEG and PNG dermoscopy files, "
        "checks that RGB channels are valid (no grayscale mismatches), catches truncated or "
        "corrupted headers, and links each filename to its metadata row."
    )
    add_list_item(
        doc,
        "2. Standardized Preprocessing: Every input image gets resized to 224 x 224 via bilinear "
        "interpolation. RGB channels are normalized with ImageNet mean and standard deviation. "
        "Nothing fancy here — we kept it simple and consistent."
    )
    add_list_item(
        doc,
        "3. Patient-Grouped Batch Generation: Dataloaders pull batches only from their assigned "
        "split. When we use WeightedRandomSampler, the loader adjusts sampling weights so "
        "malignant images show up more often in each batch."
    )
    add_list_item(
        doc,
        "4. Feature Extraction and Logit Output: An input tensor passes through all 201 DenseNet "
        "layers, gets pooled down to a 1,920-dimensional vector, and then a single linear layer "
        "produces one scalar logit."
    )
    add_list_item(
        doc,
        "5. Calibrated Triage Assignment: Raw logits go through a sigmoid to get probabilities. "
        "Based on the validation-calibrated threshold, each image is sorted into one of three tiers: "
        "Low Suspicion, Moderate Suspicion, or High Malignancy Alert."
    )
    add_list_item(
        doc,
        "6. Performance Metric Computation: The evaluation module computes confusion matrix counts "
        "(TN, FP, FN, TP), then derives sensitivity, specificity, precision, accuracy, F1-scores, "
        "ROC-AUC, and Average Precision from those."
    )

    add_styled_heading(doc, "3.1.2 Non-Functional Requirements", 3)
    add_body_paragraph(
        doc,
        "Beyond what the system does, here are the engineering constraints we held ourselves to:"
    )
    add_list_item(
        doc,
        "1. Inference Speed: A single forward pass has to finish within 50 milliseconds on a "
        "modern GPU and under 250 milliseconds on a multi-core CPU. Nobody wants to wait around "
        "during a screening session."
    )
    add_list_item(
        doc,
        "2. Reproducibility: We fix random seeds (SEED = 42) across Python, NumPy, and PyTorch. "
        "Every run — weight init, batch shuffling, augmentation — should give the same results."
    )
    add_list_item(
        doc,
        "3. Memory Footprint: Model weights stay under 250 MB on disk and in RAM/VRAM. The system "
        "should run on a reasonable workstation or clinic laptop — no server farm required."
    )
    add_list_item(
        doc,
        "4. Auditability: Checkpoints, evaluation logs, prediction CSVs, and confusion matrices "
        "all get saved as permanent files. Each file is tagged with matching experiment identifiers "
        "so we can trace any result back to its source."
    )
    add_list_item(
        doc,
        "5. Modularity: Data loading, network definitions, loss functions, and evaluation scripts "
        "live in separate modules. Swapping in a new architecture shouldn't require rewriting the "
        "dataset code."
    )

    add_styled_heading(doc, "3.2 Feasibility Study", 2)
    add_styled_heading(doc, "3.2.1 Technical Feasibility", 3)
    add_body_paragraph(
        doc,
        "We didn't have to build anything exotic. Transfer learning with DenseNet201 is a well-trodden "
        "path in biomedical imaging. PyTorch handles GPU acceleration through CUDA, comes with built-in "
        "weighted loss functions, and its dataloader utilities are battle-tested. Training on 224 x 224 "
        "images with a single NVIDIA Tesla T4 (16 GB VRAM) takes only about 10 to 15 minutes per epoch. "
        "That's very manageable, even on free cloud platforms."
    )

    add_styled_heading(doc, "3.2.2 Economic Feasibility", 3)
    add_body_paragraph(
        doc,
        "Cost-wise, we spent almost nothing. Python, PyTorch, torchvision, scikit-learn — all open source. "
        "We trained on Google Colab and Kaggle GPU instances, which are free for the workloads we needed. "
        "Looking ahead, a screening tool like this could also save money in clinical settings: fewer "
        "unnecessary biopsies on benign lesions (each one costs the healthcare system hundreds of dollars) "
        "and earlier catches that avoid the enormous expense of treating late-stage melanoma."
    )

    add_styled_heading(doc, "3.2.3 Social Feasibility", 3)
    add_body_paragraph(
        doc,
        "The social case is straightforward. In rural areas and underserved communities, dermatologists "
        "are scarce. A reliable computer-aided triage tool can help make sure patients with suspicious "
        "lesions get referred quickly instead of waiting in a queue. We want to be clear, though: we see "
        "this as an assistive tool for primary care doctors, not something that replaces them. The clinician "
        "always has the final say."
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

    p_fig = doc.add_paragraph()
    p_fig.paragraph_format.space_before = Pt(14)
    add_figure(
        doc,
        os.path.join(FIG_DIR, 'dataset_class_distribution.png'),
        "Figure 3.1: SIIM-ISIC 2020 Dataset Lesion Class Distribution on Logarithmic Scale (32,542 Benign vs. 584 Malignant)",
        width_inches=5.6
    )

print("Revised Chapters 1 to 3 written.")
