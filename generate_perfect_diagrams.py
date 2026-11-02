# -*- coding: utf-8 -*-
"""
DermInsight AI - Clean Publication-Quality Diagram Generator
Generates clean, non-overlapping architectural and UML diagrams.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FIG_DIR = r'C:\Users\sujan\Downloads\DermInsightAI-20261026T173409Z-1-001\DermInsightAI\REPORT_FIGURES'
os.makedirs(FIG_DIR, exist_ok=True)

def draw_rounded_card(ax, x, y, w, h, title, body_lines, header_bg='#e2e8f0', body_bg='#ffffff', border_color='#64748b'):
    """Draws a clean professional rounded card with a distinct header and body."""
    card = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.15', facecolor=body_bg, edgecolor=border_color, linewidth=1.5, zorder=2)
    ax.add_patch(card)
    
    header_h = 0.65
    header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, boxstyle='round,pad=0.15', facecolor=header_bg, edgecolor=border_color, linewidth=1.5, zorder=3)
    ax.add_patch(header)
    
    ax.text(x + w/2, y + h - header_h/2, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0f172a', zorder=4)
    
    body_y = y + (h - header_h)/2 + 0.1
    ax.text(x + w/2, body_y, '\n'.join(body_lines), ha='center', va='center', fontsize=9.0, color='#334155', linespacing=1.35, zorder=4)

def draw_clean_arrow(ax, x1, y1, x2, y2, label=None, label_pos='above', color='#334155'):
    """Draws a clean arrow with clear, non-overlapping label with white pill background."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=7, headlength=7, shrink=0.03),
                zorder=5)
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        if label_pos == 'above':
            ly = my + 0.28
            lx = mx
        elif label_pos == 'below':
            ly = my - 0.28
            lx = mx
        elif label_pos == 'left':
            lx = mx - 0.35
            ly = my
        else: # right
            lx = mx + 0.35
            ly = my
            
        ax.text(lx, ly, label, ha='center', va='center', fontsize=8.5, fontweight='semibold', color='#1e293b',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#cbd5e1', linewidth=1.0, alpha=0.95),
                zorder=6)

# =============================================================================
# 1. Level-1 Data Flow Diagram (DFD) — Figure 4.1 in Chapter 4
# =============================================================================
def generate_dfd():
    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)

    # External Entity: Clinician (Left)
    entity_left = patches.FancyBboxPatch((0.8, 4.3), 2.2, 1.8, boxstyle='round,pad=0.2', facecolor='#e0e7ff', edgecolor='#3730a3', linewidth=2, zorder=2)
    ax.add_patch(entity_left)
    ax.text(1.9, 5.2, 'Dermatologist /\nClinical Specialist\n(External Entity)', ha='center', va='center', fontsize=10, fontweight='bold', color='#1e1b4b', zorder=4)

    # Process 1.0 (Bubble)
    p1 = patches.Circle((5.3, 5.2), radius=1.35, facecolor='#eff6ff', edgecolor='#2563eb', linewidth=2, zorder=2)
    ax.add_patch(p1)
    ax.text(5.3, 5.75, '1.0 Preprocessing', ha='center', va='center', fontsize=10, fontweight='bold', color='#1e40af', zorder=4)
    ax.text(5.3, 4.85, 'Image Validation\nResize 224x224\nImageNet Normalization', ha='center', va='center', fontsize=8.2, color='#1e3a8a', linespacing=1.2, zorder=4)

    # Process 2.0 (Bubble)
    p2 = patches.Circle((9.3, 5.2), radius=1.35, facecolor='#ecfdf5', edgecolor='#059669', linewidth=2, zorder=2)
    ax.add_patch(p2)
    ax.text(9.3, 5.75, '2.0 Feature Extraction', ha='center', va='center', fontsize=10, fontweight='bold', color='#065f46', zorder=4)
    ax.text(9.3, 4.85, 'DenseNet201 Backbone\n1920-d Pooling\nLogit Computation (z)', ha='center', va='center', fontsize=8.2, color='#047857', linespacing=1.2, zorder=4)

    # Process 3.0 (Bubble)
    p3 = patches.Circle((13.3, 5.2), radius=1.35, facecolor='#fffbeb', edgecolor='#d97706', linewidth=2, zorder=2)
    ax.add_patch(p3)
    ax.text(13.3, 5.75, '3.0 Classification', ha='center', va='center', fontsize=10, fontweight='bold', color='#92400e', zorder=4)
    ax.text(13.3, 4.85, 'Sigmoid Probability\nOptimal Threshold (tau)\nTriage Risk Mapping', ha='center', va='center', fontsize=8.2, color='#b45309', linespacing=1.2, zorder=4)

    # Data Store D1: ISIC 2020 Store (Bottom Left)
    d1 = patches.Rectangle((3.8, 1.0), 3.0, 1.5, facecolor='#f8fafc', edgecolor='#475569', linewidth=1.8, zorder=2)
    ax.add_patch(d1)
    ax.text(5.3, 2.0, 'D1 | ISIC 2020 Data Store', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f172a', zorder=4)
    ax.text(5.3, 1.45, '33,126 Dermoscopic Images\nPatient Identifiers & Metadata', ha='center', va='center', fontsize=8.2, color='#475569', zorder=4)

    # Data Store D2: Model Checkpoints (Bottom Center)
    d2 = patches.Rectangle((7.8, 1.0), 3.0, 1.5, facecolor='#fef2f2', edgecolor='#dc2626', linewidth=1.8, zorder=2)
    ax.add_patch(d2)
    ax.text(9.3, 2.0, 'D2 | Trained Checkpoints', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#991b1b', zorder=4)
    ax.text(9.3, 1.45, 'Verified State Dicts\n(EXP_01 - EXP_05 Checkpoints)', ha='center', va='center', fontsize=8.2, color='#b91c1c', zorder=4)

    # Output Entity: Diagnostic Report (Bottom Right)
    entity_report = patches.FancyBboxPatch((12.0, 1.0), 2.6, 1.5, boxstyle='round,pad=0.2', facecolor='#f0fdf4', edgecolor='#16a34a', linewidth=2, zorder=2)
    ax.add_patch(entity_report)
    ax.text(13.3, 2.0, 'Diagnostic Triage Report', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#14532d', zorder=4)
    ax.text(13.3, 1.45, '3-Tier Risk Category\nConfusion Matrix & Metrics', ha='center', va='center', fontsize=8.2, color='#15803d', zorder=4)

    # Connecting Arrows with clear spacing
    draw_clean_arrow(ax, 3.0, 5.2, 3.95, 5.2, label='Dermoscopic Image', label_pos='above')
    draw_clean_arrow(ax, 6.65, 5.2, 7.95, 5.2, label='Normalized Tensor', label_pos='above')
    draw_clean_arrow(ax, 10.65, 5.2, 11.95, 5.2, label='Scalar Logit (z)', label_pos='above')
    draw_clean_arrow(ax, 13.3, 3.85, 13.3, 2.5, label='Calibrated Prediction', label_pos='right')
    draw_clean_arrow(ax, 5.3, 2.5, 5.3, 3.85, label='Raw Image Stream', label_pos='left')
    draw_clean_arrow(ax, 9.3, 2.5, 9.3, 3.85, label='Load Weights', label_pos='left')

    plt.title('Figure 4.2: Level-1 Data Flow Diagram (DFD) of the DermInsight AI Framework', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'data_flow_diagram.png'), dpi=300)
    plt.close()
    print("DFD generated.")

# =============================================================================
# 2. System Architecture Diagram — Figure 4.1 in Chapter 4
# =============================================================================
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)

    # Tier 1: Data Ingestion & Patient Partitioning (Top Row)
    draw_rounded_card(ax, 0.8, 7.2, 4.2, 2.2, "1. Ingestion & Partitioning", 
                      ["SIIM-ISIC 2020 Archive (33,126 Images)", "2,056 Unique Patients", "Strict Patient-Level Isolation", "Zero Identity Leakage (0 Overlap)"],
                      header_bg='#dbeafe', body_bg='#f8fafc', border_color='#2563eb')

    draw_rounded_card(ax, 5.9, 7.2, 4.2, 2.2, "2. Preprocessing & Augmentation", 
                      ["Resize: 224 x 224 Bilinear", "ImageNet Normalization (Mean/Std)", "RandomHorizontalFlip(p=0.5)", "RandomRotation(15°), ColorJitter"],
                      header_bg='#dbeafe', body_bg='#f8fafc', border_color='#2563eb')

    draw_rounded_card(ax, 11.0, 7.2, 4.2, 2.2, "3. Partition Allocation", 
                      ["Train Split: 22,787 (445 Malignant)", "Validation Split: 5,419 (71 Malignant)", "Held-Out Test: 4,920 (68 Malignant)", "Unchanged Test Prevalence (1.38%)"],
                      header_bg='#dbeafe', body_bg='#f8fafc', border_color='#2563eb')

    # Tier 2: Deep Feature Extraction & Imbalance Mitigation (Middle Row)
    draw_rounded_card(ax, 0.8, 3.8, 6.8, 2.6, "4. DenseNet201 Deep Feature Extractor", 
                      ["ImageNet-1K Pretrained Weights (Transfer Learning)", "201 Densely Connected Layers (4 Dense Blocks)", "Concatenative Feature Reuse: x_l = H_l([x_0, ..., x_{l-1}])", "Global Adaptive AvgPool -> 1,920-d Latent Embedding", "Single-Output Linear Classification Head (Logits z)"],
                      header_bg='#dcfce7', body_bg='#f0fdf4', border_color='#16a34a')

    draw_rounded_card(ax, 8.4, 3.8, 6.8, 2.6, "5. Class-Imbalance Mitigation Objectives", 
                      ["1. Weighted BCE: Penalty Multiplier w_+ = 50.2067", "2. WeightedRandomSampler: Inverse-Frequency Batch Sampling", "3. Focal Loss: Dynamic Scaling (alpha=0.75, gamma=2.0)", "4. Random Oversampling: Minority Re-sampling on Train Set", "AdamW Optimizer (lr=1e-4, weight_decay=1e-4)"],
                      header_bg='#fef3c7', body_bg='#fffbeb', border_color='#d97706')

    # Tier 3: Threshold Calibration & Diagnostic Triage (Bottom Row)
    draw_rounded_card(ax, 0.8, 0.6, 6.8, 2.4, "6. Validation-Driven Threshold Calibration", 
                      ["Fine-Grained Validation Sweep: tau in [0.01, 0.99]", "Optimal Operating Thresholds: tau* = 0.50, 0.73, 0.86", "Optimization Criteria: Max F1 / Sensitivity vs Specificity", "Test Set Kept Completely Frozen During Calibration"],
                      header_bg='#f3e8ff', body_bg='#faf5ff', border_color='#9333ea')

    draw_rounded_card(ax, 8.4, 0.6, 6.8, 2.4, "7. Clinical Triage & Held-Out Test Evaluation", 
                      ["Held-Out Test Assessment (N=4,920 Patients)", "3-Tier Triage: Low Risk / Intermediate / High Suspicion", "Audited Metrics: Sensitivity, Specificity, ROC-AUC, AP", "Cost-Sensitive Clinical Misclassification Analysis"],
                      header_bg='#fee2e2', body_bg='#fff5f5', border_color='#dc2626')

    # Connecting Flow Arrows
    draw_clean_arrow(ax, 5.0, 8.3, 5.9, 8.3)
    draw_clean_arrow(ax, 10.1, 8.3, 11.0, 8.3)
    draw_clean_arrow(ax, 13.1, 7.2, 13.1, 6.6)
    draw_clean_arrow(ax, 13.1, 6.6, 4.2, 6.6)
    draw_clean_arrow(ax, 4.2, 6.6, 4.2, 6.4)
    draw_clean_arrow(ax, 7.6, 5.1, 8.4, 5.1)
    draw_clean_arrow(ax, 11.8, 3.8, 11.8, 3.2)
    draw_clean_arrow(ax, 11.8, 3.2, 4.2, 3.2)
    draw_clean_arrow(ax, 4.2, 3.2, 4.2, 3.0)
    draw_clean_arrow(ax, 7.6, 1.8, 8.4, 1.8)

    plt.title('Figure 4.1: End-to-End System Architecture of the DermInsight AI Screening Framework', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'system_architecture.png'), dpi=300)
    plt.close()
    print("System Architecture diagram generated.")

# =============================================================================
# 3. Use Case Diagram — Figure 4.3 in Chapter 4
# =============================================================================
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)

    # System boundary box
    sys_box = patches.Rectangle((4.5, 0.5), 8.8, 7.0, facecolor='#f8fafc', edgecolor='#475569', linewidth=2, linestyle='--', zorder=1)
    ax.add_patch(sys_box)
    ax.text(8.9, 7.15, 'DermInsight AI Screening System Boundary', ha='center', va='center', fontsize=11, fontweight='bold', color='#1e293b')

    # Actor Card (Left)
    actor_box = patches.FancyBboxPatch((0.8, 2.8), 2.6, 2.4, boxstyle='round,pad=0.2', facecolor='#e0e7ff', edgecolor='#3730a3', linewidth=2, zorder=2)
    ax.add_patch(actor_box)
    ax.text(2.1, 4.4, '<<Actor>>', ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#4338ca', zorder=4)
    ax.text(2.1, 3.5, 'Dermatologist /\nClinical Practitioner\n(Primary Actor)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e1b4b', zorder=4)

    # Use Case Ellipses (Vertically stacked with 1.4 spacing)
    use_cases = [
        ("UC-1: Ingest & Preprocess Lesion Image", 6.0),
        ("UC-2: Execute Deep DenseNet201 Inference", 4.5),
        ("UC-3: Select Operational Decision Threshold", 3.0),
        ("UC-4: Generate Diagnostic Triage & Risk Report", 1.5)
    ]

    for title, y_pos in use_cases:
        ellipse = patches.FancyBboxPatch((5.8, y_pos - 0.45), 6.2, 0.9, boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#0284c7', linewidth=1.8, zorder=2)
        ax.add_patch(ellipse)
        ax.text(8.9, y_pos, title, ha='center', va='center', fontsize=9.5, fontweight='semibold', color='#0369a1', zorder=4)
        
        # Connection line from Actor to Use Case edge (x=5.8)
        ax.plot([3.4, 5.8], [4.0, y_pos], color='#334155', linewidth=1.5, zorder=3)

    plt.title('Figure 4.3: Use Case Diagram for the DermInsight AI Clinical Screening System', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'use_case_diagram.png'), dpi=300)
    plt.close()
    print("Use Case diagram generated.")

# =============================================================================
# 4. UML Class Diagram — Figure 4.4 in Chapter 4
# =============================================================================
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)

    def draw_uml_class(ax, x, y, w, h, class_name, stereotype, attrs, methods):
        # Outer border
        card = patches.Rectangle((x, y), w, h, facecolor='#ffffff', edgecolor='#334155', linewidth=1.8, zorder=2)
        ax.add_patch(card)
        
        # Header box
        header_h = 1.0
        h_box = patches.Rectangle((x, y + h - header_h), w, header_h, facecolor='#e2e8f0', edgecolor='#334155', linewidth=1.8, zorder=3)
        ax.add_patch(h_box)
        ax.text(x + w/2, y + h - 0.32, stereotype, ha='center', va='center', fontsize=8.0, fontstyle='italic', color='#475569', zorder=4)
        ax.text(x + w/2, y + h - 0.70, class_name, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0f172a', zorder=4)
        
        # Divider 1
        attr_h = (h - header_h) * 0.45
        ax.plot([x, x + w], [y + h - header_h - attr_h, y + h - header_h - attr_h], color='#334155', linewidth=1.2, zorder=3)
        
        # Attributes
        ax.text(x + 0.2, y + h - header_h - 0.2, '\n'.join(attrs), ha='left', va='top', fontsize=8.2, color='#1e293b', linespacing=1.35, zorder=4)
        
        # Methods
        ax.text(x + 0.2, y + h - header_h - attr_h - 0.2, '\n'.join(methods), ha='left', va='top', fontsize=8.2, color='#1e293b', linespacing=1.35, zorder=4)

    # Class 1: DermImageDataset
    draw_uml_class(ax, 0.8, 1.5, 4.3, 5.2, "DermImageDataset", "<<PyTorch Dataset>>",
                   ["- dataframe: pd.DataFrame", "- image_dir: Path", "- transform: transforms.Compose", "- is_training: bool"],
                   ["+ __len__(): int", "+ __getitem__(idx: int): Tuple", "+ _load_image(path: Path): Image", "+ get_patient_id(idx: int): str"])

    # Class 2: DermInsightDenseNet201
    draw_uml_class(ax, 5.8, 1.5, 4.4, 5.2, "DermInsightDenseNet201", "<<nn.Module>>",
                   ["- backbone: DenseNet (201 layers)", "- num_features: int = 1920", "- classifier: nn.Linear(1920, 1)", "- pretrained: bool = True"],
                   ["+ forward(x: Tensor): Tensor", "+ extract_features(x: Tensor): Tensor", "+ predict_proba(x: Tensor): float", "+ get_logits(x: Tensor): Tensor"])

    # Class 3: ClinicalEvaluator
    draw_uml_class(ax, 10.9, 1.5, 4.3, 5.2, "ClinicalEvaluator", "<<Evaluation Engine>>",
                   ["- threshold: float = 0.50", "- cost_matrix: CostMatrix", "- true_labels: np.ndarray", "- pred_probs: np.ndarray"],
                   ["+ compute_metrics(y, p, tau): Dict", "+ sweep_thresholds(val_loader): float", "+ generate_confusion_matrix(): ndarray", "+ plot_roc_pr_curves(): void"])

    # Relationship Arrows
    draw_clean_arrow(ax, 5.1, 4.5, 5.8, 4.5, label='feeds tensors [B, 3, 224, 224]', label_pos='above')
    draw_clean_arrow(ax, 10.2, 4.5, 10.9, 4.5, label='delivers raw logits (z)', label_pos='above')

    plt.title('Figure 4.4: UML Class Diagram of the Implemented Deep Learning Pipeline Architecture', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'class_diagram.png'), dpi=300)
    plt.close()
    print("Class diagram generated.")

# =============================================================================
# 5. UML Sequence Diagram — Figure 4.5 in Chapter 4
# =============================================================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(14, 8.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)

    actors = [
        ("Clinician /\nUser", 1.8),
        ("DermImage\nDataset", 4.5),
        ("DenseNet201\nBackbone", 7.2),
        ("Threshold\nCalibrator", 9.9),
        ("Clinical Triage\nEngine", 12.6)
    ]

    for name, x in actors:
        # Actor box
        card = patches.FancyBboxPatch((x - 1.0, 7.2), 2.0, 0.9, boxstyle='round,pad=0.15', facecolor='#e2e8f0', edgecolor='#334155', linewidth=1.5, zorder=2)
        ax.add_patch(card)
        ax.text(x, 7.65, name, ha='center', va='center', fontsize=9.0, fontweight='bold', color='#0f172a', zorder=4)
        
        # Lifeline (vertical dashed line)
        ax.plot([x, x], [0.8, 7.2], color='#94a3b8', linestyle='--', linewidth=1.5, zorder=1)

    # 6 Steps
    steps = [
        (1.8, 4.5, 6.2, "1: Submit Dermoscopic Image (JPEG)", 'solid'),
        (4.5, 7.2, 5.2, "2: Stream Preprocessed Tensor [1, 3, 224, 224]", 'solid'),
        (7.2, 9.9, 4.2, "3: Forward Logit z & Probability p_hat", 'solid'),
        (9.9, 12.6, 3.2, "4: Apply Calibrated Operating Threshold (tau*)", 'solid'),
        (12.6, 1.8, 2.2, "5: Return Diagnostic Triage & Risk Report", 'dashed'),
        (1.8, 1.8, 1.2, "6: Review Alert & Prioritize Biopsy", 'self')
    ]

    for x1, x2, y, label, style in steps:
        if style == 'self':
            # self-loop arrow
            ax.plot([x1, x1 + 0.8, x1 + 0.8, x1], [y + 0.3, y + 0.3, y - 0.1, y - 0.1], color='#1e293b', linewidth=1.5, zorder=3)
            ax.annotate('', xy=(x1, y - 0.1), xytext=(x1 + 0.2, y - 0.1),
                        arrowprops=dict(facecolor='#1e293b', edgecolor='#1e293b', width=1.2, headwidth=6, headlength=6), zorder=4)
            ax.text(x1 + 0.95, y + 0.1, label, ha='left', va='center', fontsize=8.5, fontweight='semibold', color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#cbd5e1', linewidth=1.0), zorder=5)
        else:
            ls = '--' if style == 'dashed' else '-'
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(facecolor='#1e293b', edgecolor='#1e293b', width=1.3, headwidth=6, headlength=6, linestyle=ls), zorder=3)
            mx = (x1 + x2)/2
            ax.text(mx, y + 0.28, label, ha='center', va='center', fontsize=8.5, fontweight='semibold', color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#cbd5e1', linewidth=1.0, alpha=0.95), zorder=5)

    plt.title('Figure 4.5: UML Sequence Diagram for Dermoscopic Image Ingestion, Inference, and Triage Output', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'sequence_diagram.png'), dpi=300)
    plt.close()
    print("Sequence diagram generated.")

if __name__ == "__main__":
    generate_dfd()
    generate_system_architecture()
    generate_use_case_diagram()
    generate_class_diagram()
    generate_sequence_diagram()
    print("All 5 diagrams successfully generated with zero overlapping text!")
