# -*- coding: utf-8 -*-
"""
DermInsight AI - Chapter 4 to 6 Content Builder (Revised Human-Edited Version)
Written in an authentic, natural undergraduate engineering research style.
Explains design choices, architectural details, and experimental methodology
with technical precision and clear practical reasoning.
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
        "From the start, we wanted DermInsight AI to be modular. Each stage of the pipeline handles one job "
        "and one job only—data loading, feature learning, imbalance handling, or threshold tuning. "
        "We did this on purpose. In our experience, lumping everything into a single monolithic script makes it "
        "dangerously easy to leak patient data across splits or ship uncalibrated predictions without realizing it. "
        "Figure 4.1 lays out the four stages we settled on."
    )
    add_body_paragraph(
        doc,
        "Stage one pulls raw dermoscopic images from the SIIM-ISIC 2020 archive along with the metadata CSV. "
        "It inspects patient IDs and routes every image from a given person into exactly one partition—train, val, or test. "
        "No exceptions. Stage two handles the visual preprocessing: resizing to 224×224, normalizing channels with ImageNet "
        "statistics, and passing tensors into a 201-layer DenseNet backbone. The third stage is where we tackle the brutal "
        "55:1 class imbalance through specialized loss functions and sampling tricks. "
        "And the last stage? It takes raw logits, pushes them through a sigmoid, and compares the resulting probabilities "
        "against thresholds we calibrated on the validation set. Out comes a clear clinical risk level."
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
        "Figure 4.2 shows our Level-1 Data Flow Diagram. A clinical user—or, during development, an automated test "
        "script—feeds in an unprocessed dermoscopic image. Process 1.0 checks the image is valid, resizes it to "
        "224×224, and normalizes pixel values to match what the ImageNet-pretrained backbone expects. "
        "Process 2.0 grabs the verified model weights from the Checkpoint Store (D1) and runs a forward pass through "
        "DenseNet201, producing an unbounded scalar logit."
    )
    add_body_paragraph(
        doc,
        "Then Process 3.0 kicks in. It takes that logit, applies our pre-calculated decision thresholds, slots the "
        "score into one of three risk tiers, and spits out a screening report. We made the report auditable so that "
        "a clinician can always trace back which checkpoint and which threshold produced a particular recommendation."
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
        "Who actually uses this system? Figure 4.3 maps it out. We designed for three kinds of users: general "
        "practitioners doing routine mole checks, dermatologists who need a second opinion tool, and researchers "
        "running batch evaluations on archived datasets. All three start the same way—load a lesion image into the pipeline."
    )
    add_body_paragraph(
        doc,
        "After inference, the system shows both a raw probability and a categorical risk label. One thing we thought "
        "was important: letting users pick their own operating threshold. A GP screening hundreds of patients probably "
        "wants maximum sensitivity, even at the cost of more false alarms. A dermatologist might lean toward higher "
        "specificity to cut down on unnecessary biopsies. The interface also lets anyone pull up detailed metrics—confusion "
        "matrices, ROC curves, the works."
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
        "Figure 4.4 shows the UML class diagram for our Python/PyTorch codebase. Three classes do the heavy lifting:"
    )
    add_list_item(
        doc,
        "1. DermImageDataset — extends torch.utils.data.Dataset. It reads the metadata CSV, resolves image paths, "
        "opens RGB images with PIL, and applies either stochastic augmentations (for training) or deterministic "
        "transforms (for eval). Pretty standard PyTorch pattern."
    )
    add_list_item(
        doc,
        "2. DermInsightDenseNet201 — extends torch.nn.Module. We wrap the torchvision DenseNet201 backbone, swap out "
        "the 1,000-class classifier with nn.Identity(), then bolt on a single nn.Linear(1920, 1) layer for binary logits."
    )
    add_list_item(
        doc,
        "3. Evaluator / ThresholdCalibrator — this one handles threshold sweeps, confusion matrix computation "
        "(TN, FP, FN, TP at each candidate threshold), and generates ROC and Precision-Recall curves for both val and test."
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
        "Figure 4.5 traces what happens at runtime when someone feeds an image into the pipeline. "
        "The dataset loader receives the path, loads the image, and produces a standardized tensor. That tensor gets "
        "shipped to the GPU. DenseNet201 runs its forward pass—all 201 layers—and returns one scalar logit."
    )
    add_body_paragraph(
        doc,
        "The calibrator then applies the sigmoid function to get a probability, compares it against the chosen threshold, "
        "and packages everything into a structured result: predicted label, confidence score, and a clinical recommendation. "
        "The whole thing takes under 20 ms on a Tesla T4."
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
        "We picked DenseNet201 (Huang et al., 2017) as our feature extractor, and here's why. "
        "In a regular CNN, layer l only sees the output of layer l-1: x_l = H_l(x_{l-1}). DenseNet does "
        "something different. Every layer inside a dense block receives the feature maps from all previous layers, "
        "concatenated together:"
    )
    add_formula(
        doc,
        "x_l = H_l([x_0, x_1, x_2, ..., x_{l-1}])"
    )
    add_body_paragraph(
        doc,
        "Here, [x_0, x_1, ..., x_{l-1}] is just the channel-wise concatenation of every preceding feature map. "
        "H_l(·) is a composite function—Batch Normalization, then ReLU, then a 3×3 convolution."
    )
    add_body_paragraph(
        doc,
        "Why does this matter for dermoscopy? Two reasons. First, feature reuse. Early layers learn edges and "
        "texture patterns, and those stay directly accessible to deeper layers without fading out. That's useful "
        "when you need to catch fine skin structures—things like delicate pigment reticula or subtle peripheral "
        "streaks that can signal early melanoma. Second, the dense connections create shorter gradient paths during "
        "backpropagation. Training through 201 layers is hard; vanishing gradients are a real concern. But with all "
        "those shortcut connections, gradients have many routes back to early layers. "
        "Compared to the bigger ResNet variants, DenseNet201 gets strong representational power out of roughly 20 million parameters."
    )
    add_body_paragraph(
        doc,
        "Architecturally, DenseNet201 has four dense blocks separated by transition layers that downsample using "
        "1×1 convolutions and 2×2 average pooling. To adapt it for our binary problem, we stripped off the original "
        "1,000-class fully connected head and replaced it with nn.Identity(). That exposes the 1,920-dimensional "
        "feature vector from global average pooling. On top of that, we added a single linear layer: z = W·x + b, "
        "where W ∈ ℝ^{1×1920} and b ∈ ℝ. The scalar logit z goes through a standard logistic sigmoid:"
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
        "This is probably the single most important engineering decision in the whole project. "
        "In the SIIM-ISIC 2020 dataset, lots of patients contributed multiple lesion photos. Some people with "
        "dysplastic nevus syndrome have dozens of images in the archive. If we had split images randomly, different "
        "lesions from the same person would end up in both training and test sets. So why is that a problem?"
    )
    add_body_paragraph(
        doc,
        "Because lesions on the same body share skin tone, hair density, background lighting, and camera angle. "
        "A deep network can easily latch onto those patient-specific cues instead of learning real malignancy patterns. "
        "Test performance would look great on paper but fall apart on new patients. We've read enough papers that made "
        "this mistake to know we didn't want to repeat it."
    )
    add_body_paragraph(
        doc,
        "Our solution was strict patient-level grouping. We grouped by patient_id and assigned all of a person's "
        "images to exactly one partition. Table 5.2 shows how the data ended up distributed. We double-checked that "
        "the patient ID intersection between every pair of splits is empty—zero overlap."
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
        "On the preprocessing side, we resized every image to 224×224 and normalized using ImageNet channel moments "
        "(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]). During training, we applied random horizontal "
        "flips with probability 0.5, random rotations up to 15 degrees, and mild color jitter (brightness, contrast, "
        "and saturation each at 0.1). Nothing too aggressive—we didn't want the augmentations to distort clinical "
        "features beyond recognition. Val and test images only got the deterministic resize and normalize, no randomness."
    )

    add_styled_heading(doc, "5.3 Class-Imbalance Formulations & Strategies", 2)
    add_body_paragraph(
        doc,
        "Only 1.76% of our images are malignant. That's a brutal imbalance—roughly 55 benign images for every "
        "malignant one. A naïve classifier that just predicts \"benign\" every single time would score 98.24% accuracy. "
        "Obviously useless for cancer screening. We tried four different strategies to make the model actually pay "
        "attention to the minority class."
    )
    
    add_styled_heading(doc, "5.3.1 Weighted Binary Cross-Entropy Loss", 3)
    add_body_paragraph(
        doc,
        "Standard BCE with logits treats every sample equally:"
    )
    add_formula(
        doc,
        "L_BCE(z, y) = - [ y · log(σ(z)) + (1 - y) · log(1 - σ(z)) ]"
    )
    add_body_paragraph(
        doc,
        "With 22,342 benign samples and just 445 malignant ones in our training set, the negative examples "
        "produce over 50 times the total gradient. The network basically ignores the positives. "
        "To fix this, we added a weight w_+ on the positive term:"
    )
    add_formula(
        doc,
        "L_WBCE(z, y) = - [ w_+ · y · log(σ(z)) + (1 - y) · log(1 - σ(z)) ]"
    )
    add_body_paragraph(
        doc,
        "We computed w_+ straight from the training split counts: w_+ = N_neg / N_pos = 22,342 / 445 = 50.2067. "
        "By scaling positive-class errors by about 50.21, we force the optimizer to treat a missed melanoma as "
        "roughly 50 times worse than a false alarm. In practice, we passed this weight directly to PyTorch's "
        "BCEWithLogitsLoss via the pos_weight argument."
    )

    add_styled_heading(doc, "5.3.2 PyTorch WeightedRandomSampler", 3)
    add_body_paragraph(
        doc,
        "Instead of messing with the loss, this approach changes which samples the model sees during training. "
        "Every training image i gets a sampling weight inversely proportional to its class frequency: "
        "w_i = 1 / N_{c(i)}, where c(i) is 0 or 1. Mini-batches are then drawn with replacement according to "
        "these weights."
    )
    add_body_paragraph(
        doc,
        "The practical effect is that each batch ends up with roughly equal numbers of benign and malignant examples. "
        "We can then use plain unweighted BCE loss—the balanced sampling does the work of making the model pay "
        "attention to both classes. We found this easier to tune than loss weighting, though the final results "
        "differed in interesting ways."
    )

    add_styled_heading(doc, "5.3.3 Focal Loss Formulation", 3)
    add_body_paragraph(
        doc,
        "Focal Loss, introduced by Lin et al. (2017), takes a different angle. Rather than reweighting by class, "
        "it down-weights easy examples—the ones the model already classifies correctly with high confidence—and "
        "puts more focus on hard, ambiguous cases:"
    )
    add_formula(
        doc,
        "L_FL(p_t) = - α_t · (1 - p_t)^γ · log(p_t)"
    )
    add_body_paragraph(
        doc,
        "Here p_t is the model's estimated probability for the correct class. We set α = 0.75 to give slight extra "
        "weight to positives, and γ = 2.0 as the focusing exponent. Consider a clearly benign lesion where "
        "p_t = 0.99. The modulating factor (1 − 0.99)² = 0.0001 shrinks that sample's loss by a factor of 10,000. "
        "Easy negatives basically vanish from the gradient, letting the optimizer concentrate on the borderline cases "
        "that actually matter for improving sensitivity."
    )

    add_styled_heading(doc, "5.3.4 Random Oversampling Strategy", 3)
    add_body_paragraph(
        doc,
        "The simplest approach: just duplicate minority-class images in the training set until both classes "
        "have equal counts. Straightforward, but we were careful about one thing—oversampling only happens inside "
        "the training dataloader. Val and test sets stay completely untouched at their natural prevalence rates. "
        "Anything else would compromise the integrity of our evaluation."
    )

    add_styled_heading(doc, "5.4 Checkpoint Selection & Early Stopping", 2)
    add_body_paragraph(
        doc,
        "We trained all models with AdamW (Loshchilov & Hutter, 2019), using a learning rate of 1e-4 and weight "
        "decay of 1e-4. For checkpoint selection, we saved the model weights at whichever epoch had the best "
        "validation ROC-AUC—not validation loss. Why not loss? Because in heavily imbalanced tasks, loss can keep "
        "improving while minority-class sensitivity quietly degrades. ROC-AUC captures ranking quality across all "
        "thresholds, which is what we actually care about."
    )
    add_body_paragraph(
        doc,
        "Early stopping patience was set to 3 epochs. If val ROC-AUC didn't improve for three consecutive epochs, "
        "we stopped training and rolled back to the best checkpoint. This kept training runs short—typically 5 to 8 "
        "epochs—and helped prevent overfitting."
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
        "Here's something that isn't obvious until you've actually trained on imbalanced data: the default "
        "threshold of τ = 0.5 almost never works well. When we weight positive errors heavily during training, "
        "the model's predicted probabilities shift upward—toward 1.0—and a 0.5 cutoff floods you with false "
        "positives. On the flip side, an unweighted model produces tiny probabilities for almost everything, "
        "so τ = 0.5 misses most cancers entirely."
    )
    add_body_paragraph(
        doc,
        "We addressed this by sweeping τ from 0.01 to 0.99 in steps of 0.01, but only on the validation set. "
        "At each candidate threshold we computed sensitivity, specificity, and F1-score, then picked the threshold "
        "that best balanced catching cancers against avoiding false alarms. The test set was completely frozen during "
        "this process. We didn't peek at test results even once while tuning thresholds—that would defeat the point "
        "of having a held-out set."
    )

    add_styled_heading(doc, "5.6 Evaluation & Testing Protocol on Held-Out Test Set", 2)
    add_body_paragraph(
        doc,
        "Every trained checkpoint was evaluated on the same 4,920 held-out test images. We reported two types "
        "of metrics. Threshold-independent ones—ROC-AUC and Average Precision—tell us how well the model ranks "
        "malignant cases above benign ones, regardless of where you draw the line. Threshold-dependent ones—Sensitivity, "
        "Specificity, Precision, F1-score, and the full confusion matrix (TN, FP, FN, TP)—show what happens at "
        "a specific operating point."
    )
    add_body_paragraph(
        doc,
        "We believe both types matter. A model with a great AUC but terrible sensitivity at every practical threshold "
        "isn't useful in the clinic. And a model with high sensitivity at one hand-picked threshold might just be "
        "overfitting to the validation set if we aren't careful. Reporting both keeps us honest."
    )

def add_chapter_6(doc):
    doc.add_page_break()
    add_styled_heading(doc, "CHAPTER 6\n6. PROJECT DEMONSTRATION", 1)
    
    add_styled_heading(doc, "6.1 Demonstration Workflow & Environment", 2)
    add_body_paragraph(
        doc,
        "To show that DermInsight AI actually works end-to-end, we built standalone demo scripts in Python. "
        "You can feed in a single dermoscopic image for interactive use, or point the script at a folder of images "
        "for batch evaluation. When you run the script, it loads whichever model checkpoint you specify, sets up "
        "the preprocessing pipeline, processes the images, and prints out risk assessments."
    )
    add_body_paragraph(
        doc,
        "Nothing fancy about the interface—it's command-line driven. "
        "But it does everything the pipeline needs to do, from loading weights to writing output reports."
    )

    add_styled_heading(doc, "6.2 Preprocessing & Batch Dataloader Execution", 2)
    add_body_paragraph(
        doc,
        "During a demo run, each image is loaded from disk with PIL and checked for three-channel RGB formatting. "
        "We resize to 224×224, normalize with ImageNet stats, and stack everything into 4D tensors of shape "
        "[B, 3, 224, 224]. The dataloader uses pinned host memory, which lets us transfer batches to the GPU "
        "with minimal latency. Even across hundreds of test images, the data loading step isn't the bottleneck."
    )

    add_styled_heading(doc, "6.3 Model Inference Execution Demonstration", 2)
    add_body_paragraph(
        doc,
        "Each batch passes through all 201 layers of DenseNet. On an NVIDIA Tesla T4 GPU, forward-pass latency "
        "averaged 12 to 18 milliseconds per image. On a multi-core CPU it was slower—around 140 milliseconds per "
        "image—but still feasible for clinical use where you're processing one lesion at a time. The linear head "
        "produces a scalar logit z, and we push it through the sigmoid to get p̂ = P(malignant | x)."
    )

    add_styled_heading(doc, "6.4 Threshold Calibration & Triage Generation", 2)
    add_body_paragraph(
        doc,
        "A raw probability number isn't very helpful for a busy clinician. What does \"0.47\" mean? Should they worry? "
        "To make the output actionable, we map scores into a three-tier triage scheme:"
    )
    add_list_item(
        doc,
        "1. Tier 1 — Low Suspicion (p̂ < 0.30): Looks like a typical benign lesion. Recommended action: routine "
        "annual skin check, nothing urgent."
    )
    add_list_item(
        doc,
        "2. Tier 2 — Intermediate Suspicion (0.30 ≤ p̂ < τ*): Borderline or atypical features present. We'd "
        "suggest a 3-month digital dermoscopy follow-up or a second clinical opinion."
    )
    add_list_item(
        doc,
        "3. Tier 3 — High Risk (p̂ ≥ τ*): Characteristics strongly associated with melanoma. This triggers "
        "an immediate clinical alert and urgent referral for specialist biopsy."
    )

    add_styled_heading(doc, "6.5 Output Visualizations Demonstration", 2)
    add_body_paragraph(
        doc,
        "After a batch run finishes, the demo scripts automatically generate visual summaries. These include "
        "confusion matrices with exact TP, TN, FP, and FN counts; ROC curves plotting sensitivity against "
        "1-specificity across all candidate thresholds; and precision-recall curves that are especially informative "
        "given the low 1.38% test prevalence."
    )
    add_body_paragraph(
        doc,
        "We also generate threshold sensitivity plots. These show, at a glance, how shifting the decision boundary "
        "trades off between missed cancers and false alarms. In our experience, these plots were some of the most "
        "useful outputs for understanding each model's behavior—more informative than any single summary number."
    )

print("Revised Chapters 4 to 6 written.")
