# -*- coding: utf-8 -*-
"""
DermInsight AI - Master Academic Report Generator
Generates the comprehensive verified final report conforming strictly to the VIT Project-I Template.
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from build_helpers import (
    set_cell_margins, set_cell_background, set_table_borders,
    add_styled_heading, add_body_paragraph, add_figure, add_table_caption
)

PROJECT_ROOT = r'C:\Users\sujan\Downloads\DermInsightAI-20261026T173409Z-1-001\DermInsightAI'
FIG_DIR = os.path.join(PROJECT_ROOT, 'REPORT_FIGURES')
OUTPUT_DOCX = os.path.join(PROJECT_ROOT, 'DermInsight_AI_Project_I_Report_Verified.docx')
OUTPUT_PDF = os.path.join(PROJECT_ROOT, 'DermInsight_AI_Project_I_Report_Verified.pdf')

def build_report():
    doc = Document()
    
    # Page setup - 1 inch margins all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # =========================================================================
    # 1. TITLE PAGE
    # =========================================================================
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.space_before = Pt(0)
    p_header.paragraph_format.space_after = Pt(18)
    r_hdr = p_header.add_run("B.Tech. BCSE497J - Project-I\n")
    r_hdr.font.name = 'Times New Roman'
    r_hdr.font.size = Pt(14)
    r_hdr.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.5
    p_title.paragraph_format.space_after = Pt(28)
    r_title = p_title.add_run("AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Submitted in partial fulfillment of the requirements for the degree of\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    
    r_deg = p_sub.add_run("Bachelor of Technology\nin\nComputer Science and Engineering\n\nby\n")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(13)
    r_deg.font.bold = True
    r_deg.font.italic = False

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.line_spacing = 1.3
    p_auth.paragraph_format.space_after = Pt(24)
    
    authors = [
        ("23BCB0165", "ALAN JOHN ANAND"),
        ("23BCE2002", "SUJAN M"),
        ("23BCE2107", "RAMACHANDRAN SIVASANKAR")
    ]
    for reg, name in authors:
        r_auth = p_auth.add_run(f"{reg}\t\t{name}\n")
        r_auth.font.name = 'Times New Roman'
        r_auth.font.size = Pt(12)
        r_auth.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_after = Pt(24)
    r_sup = p_guide.add_run("Under the Supervision of\n")
    r_sup.font.name = 'Times New Roman'
    r_sup.font.size = Pt(12)
    
    r_gname = p_guide.add_run("Dr. Krishna Rani Samal\n")
    r_gname.font.name = 'Times New Roman'
    r_gname.font.size = Pt(13)
    r_gname.font.bold = True
    
    r_gdes = p_guide.add_run("Associate Professor\nSchool of Computer Science and Engineering (SCOPE)\n")
    r_gdes.font.name = 'Times New Roman'
    r_gdes.font.size = Pt(12)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(18)
    p_inst.paragraph_format.space_after = Pt(0)
    
    r_inst = p_inst.add_run("School of Computer Science and Engineering (SCOPE)\nVELLORE INSTITUTE OF TECHNOLOGY\nVellore - 632014, Tamil Nadu, India\nOctober 2026")
    r_inst.font.name = 'Times New Roman'
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True

    # =========================================================================
    # 2. DECLARATION (Page i)
    # =========================================================================
    doc.add_page_break()
    p_dec_h = doc.add_paragraph()
    p_dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec_h.paragraph_format.space_before = Pt(24)
    p_dec_h.paragraph_format.space_after = Pt(20)
    r = p_dec_h.add_run("DECLARATION")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    add_body_paragraph(
        doc,
        "We hereby declare that the project entitled \"AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER\" "
        "submitted by us, for the award of the degree of Bachelor of Technology in Computer Science and Engineering to Vellore Institute "
        "of Technology (VIT), is a record of bonafide research work carried out by us under the supervision of Dr. Krishna Rani Samal, "
        "Associate Professor, School of Computer Science and Engineering (SCOPE)."
    )
    add_body_paragraph(
        doc,
        "We further declare that the work reported in this project has not been submitted and will not be submitted, either in part or in "
        "full, for the award of any other degree or diploma in this institute or any other institute or university. All experimental results, "
        "model checkpoints, evaluation metrics, and implementation codes presented in this report represent authentic work conducted during "
        "the academic period."
    )
    
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(40)
    p_sig.paragraph_format.space_after = Pt(10)
    r_pl = p_sig.add_run("Place : Vellore\nDate  : 27-10-2026\n\n\n")
    r_pl.font.name = 'Times New Roman'
    r_pl.font.size = Pt(12)
    
    p_cands = doc.add_paragraph()
    p_cands.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for reg, name in authors:
        rc = p_cands.add_run(f"___________________________\n{name} ({reg})\n\n")
        rc.font.name = 'Times New Roman'
        rc.font.size = Pt(11)
        rc.font.bold = True

    # =========================================================================
    # 3. CERTIFICATE (Page ii)
    # =========================================================================
    doc.add_page_break()
    p_cert_h = doc.add_paragraph()
    p_cert_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_h.paragraph_format.space_before = Pt(24)
    p_cert_h.paragraph_format.space_after = Pt(20)
    r = p_cert_h.add_run("CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    add_body_paragraph(
        doc,
        "This is to certify that the project entitled \"AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER\" "
        "submitted by ALAN JOHN ANAND (Reg. No: 23BCB0165), SUJAN M (Reg. No: 23BCE2002), and RAMACHANDRAN SIVASANKAR "
        "(Reg. No: 23BCE2107), School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, for the award "
        "of the degree of Bachelor of Technology in Computer Science and Engineering, is a record of bonafide work carried out by them "
        "under my supervision during Fall Semester 2026, as per the VIT code of academic and research ethics."
    )
    add_body_paragraph(
        doc,
        "The contents of this report have not been submitted and will not be submitted either in part or in full, for the award of any "
        "other degree or diploma in this institute or any other institute or university. The project fulfills the requirements and "
        "regulations of the University and in my opinion meets the necessary standards for submission."
    )

    p_csig = doc.add_paragraph()
    p_csig.paragraph_format.space_before = Pt(36)
    p_csig.paragraph_format.space_after = Pt(40)
    r_cpl = p_csig.add_run("Place : Vellore\nDate  : 27-10-2026\n\n\n\n")
    r_cpl.font.name = 'Times New Roman'
    r_cpl.font.size = Pt(12)
    
    t_cert = doc.add_table(rows=1, cols=2)
    t_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cert.autofit = False
    t_cert.columns[0].width = Inches(3.2)
    t_cert.columns[1].width = Inches(3.2)
    
    c1 = t_cert.cell(0, 0)
    p1 = c1.paragraphs[0]
    p1.add_run("______________________________\nSignature of the Guide\nDr. Krishna Rani Samal\nAssociate Professor, SCOPE")
    p1.runs[0].font.name = 'Times New Roman'
    p1.runs[0].font.size = Pt(11)
    
    c2 = t_cert.cell(0, 1)
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("______________________________\nExaminer(s)\n\n\n")
    p2.runs[0].font.name = 'Times New Roman'
    p2.runs[0].font.size = Pt(11)

    p_hod = doc.add_paragraph()
    p_hod.paragraph_format.space_before = Pt(30)
    p_hod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h = p_hod.add_run("_________________________________________\nHead of the Department\nDepartment of Computer Science and Engineering\nSchool of Computer Science and Engineering (SCOPE)")
    r_h.font.name = 'Times New Roman'
    r_h.font.size = Pt(11)
    r_h.font.bold = True

    # =========================================================================
    # 4. ACKNOWLEDGEMENTS (Page iii)
    # =========================================================================
    doc.add_page_break()
    p_ack_h = doc.add_paragraph()
    p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_h.paragraph_format.space_before = Pt(24)
    p_ack_h.paragraph_format.space_after = Pt(20)
    r = p_ack_h.add_run("ACKNOWLEDGEMENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    add_body_paragraph(
        doc,
        "We are deeply grateful to the management of Vellore Institute of Technology (VIT) for providing us with the opportunity, "
        "computational resources, and high-performance infrastructure to undertake this B.Tech Project-I research endeavor. Their continuous "
        "commitment to fostering an intellectually stimulating and research-driven environment has been instrumental in shaping our work."
    )
    add_body_paragraph(
        doc,
        "Our sincere thanks to Dr. Jaisankar N, Dean of the School of Computer Science and Engineering (SCOPE), for his visionary leadership, "
        "unwavering support, and constant encouragement. His dedication to academic excellence and promoting rigorous scientific inquiry has "
        "been an invaluable source of inspiration throughout the semester."
    )
    add_body_paragraph(
        doc,
        "We express our profound appreciation to the Head of the Department of Computer Science and Engineering, SCOPE, for insightful administrative "
        "guidance, resource allocation, and maintaining high academic standards that enabled us to execute our deep learning experiments smoothly."
    )
    add_body_paragraph(
        doc,
        "We are immensely thankful to our project supervisor and guide, Dr. Krishna Rani Samal, Associate Professor, SCOPE, for her dedicated mentorship, "
        "technical wisdom, and constructive critiques. Her patient guidance, insistence on empirical integrity, and methodical evaluation of class-imbalance "
        "challenges in medical imaging were vital to the successful completion and honest verification of this project."
    )
    add_body_paragraph(
        doc,
        "Finally, we thank our faculty members, laboratory staff, peer reviewers, and families for their encouragement, moral support, and assistance "
        "during every stage of this research endeavor."
    )

    p_sig_ack = doc.add_paragraph()
    p_sig_ack.paragraph_format.space_before = Pt(30)
    p_sig_ack.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sa = p_sig_ack.add_run("Alan John Anand (23BCB0165)\nSujan M (23BCE2002)\nRamachandran Sivasankar (23BCE2107)")
    r_sa.font.name = 'Times New Roman'
    r_sa.font.size = Pt(11)
    r_sa.font.bold = True

    # =========================================================================
    # 5. ABSTRACT (Page x)
    # =========================================================================
    doc.add_page_break()
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_h.paragraph_format.space_before = Pt(24)
    p_abs_h.paragraph_format.space_after = Pt(20)
    r = p_abs_h.add_run("ABSTRACT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True

    add_body_paragraph(
        doc,
        "Malignant melanoma represents the deadliest form of skin cancer, accounting for the vast majority of skin cancer mortalities "
        "despite comprising less than five percent of total cutaneous malignancies. While early-stage surgical resection yields five-year survival "
        "rates exceeding 98%, late-stage metastatic prognosis drops drastically below 25%. Consequently, automated computer-aided screening systems "
        "capable of triaging high-risk dermoscopic lesions possess transformative clinical utility. However, real-world dermoscopy datasets suffer "
        "from extreme class imbalance, where malignant cases constitute a microscopic fraction of clinical encounters. Furthermore, published "
        "benchmarks frequently report high nominal accuracy while masking catastrophic false-negative rates or suffering from subtle patient-level "
        "data leakage across evaluation splits."
    )
    add_body_paragraph(
        doc,
        "This project, titled DermInsight AI, develops an automated deep learning framework for early skin cancer screening utilizing the official "
        "SIIM-ISIC 2020 Melanoma Classification benchmark comprising 33,126 high-resolution dermoscopic images across 2,056 unique patients. To establish "
        "a clinically valid evaluation baseline, a strict patient-level partitioning protocol was enforced, isolating 22,787 training images (1,439 patients), "
        "5,419 validation images (307 patients), and 4,920 held-out test images (310 patients) with zero patient overlap, thereby eliminating identity leakage. "
        "Using an ImageNet-pretrained DenseNet201 deep convolutional backbone with 201 densely connected layers, we conduct a systematic empirical "
        "audit of four fundamental class-imbalance mitigation strategies: positive-weighted binary cross-entropy (W-BCE with positive weight 50.21), "
        "PyTorch WeightedRandomSampler, Focal Loss (alpha=0.75, gamma=2.0), and training-isolated Random Oversampling, paired with validation-driven decision "
        "threshold calibration."
    )
    add_body_paragraph(
        doc,
        "Extensive evaluation across all checkpoints reveals a critical clinical insight: while class-imbalance interventions significantly enhance "
        "ranking discrimination—improving validation ROC-AUC from 0.8472 to 0.9188 and held-out test ROC-AUC to 0.8708—threshold-dependent triage "
        "exposes a severe diagnostic dilemma. At standard decision thresholds, unweighted models collapse toward specificity, identifying only 13 to 25 "
        "of the 68 malignant test lesions and generating up to 55 false negatives. Conversely, high-sensitivity operating points produce excessive false "
        "positives. Our findings demonstrate that nominal accuracy (97.2%) is dangerously misleading for medical screening, underscore the necessity "
        "of cost-sensitive threshold tuning, and establish empirical foundations for future multimodal fusion and explainable triage deployment."
    )
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(14)
    r_kw_lbl = p_kw.add_run("Keywords: ")
    r_kw_lbl.font.name = 'Times New Roman'
    r_kw_lbl.font.size = Pt(11)
    r_kw_lbl.font.bold = True
    
    r_kw = p_kw.add_run("Melanoma Screening, Deep Learning, DenseNet201, Class Imbalance, ISIC 2020, Medical Computer Vision, Patient-Level Splitting, Cost-Sensitive Evaluation.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.size = Pt(11)
    r_kw.font.italic = True

    # =========================================================================
    # 6. TABLE OF CONTENTS (Placeholder table that will be populated with exact pages)
    # =========================================================================
    doc.add_page_break()
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.paragraph_format.space_before = Pt(20)
    p_toc_h.paragraph_format.space_after = Pt(16)
    r = p_toc_h.add_run("TABLE OF CONTENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    # Table of contents table
    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False
    toc_table.columns[0].width = Inches(0.8)
    toc_table.columns[1].width = Inches(4.9)
    toc_table.columns[2].width = Inches(0.8)
    
    hdr = toc_table.rows[0].cells
    hdr[0].paragraphs[0].add_run("Sl.No").font.bold = True
    hdr[1].paragraphs[0].add_run("Contents").font.bold = True
    hdr[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(11)

    # =========================================================================
    # 7. LIST OF FIGURES
    # =========================================================================
    doc.add_page_break()
    p_lof_h = doc.add_paragraph()
    p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_h.paragraph_format.space_before = Pt(20)
    p_lof_h.paragraph_format.space_after = Pt(16)
    r = p_lof_h.add_run("List of Figures")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    lof_table = doc.add_table(rows=1, cols=3)
    lof_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    lof_table.autofit = False
    lof_table.columns[0].width = Inches(1.2)
    lof_table.columns[1].width = Inches(4.5)
    lof_table.columns[2].width = Inches(0.8)
    
    l_hdr = lof_table.rows[0].cells
    l_hdr[0].paragraphs[0].add_run("Figure No.").font.bold = True
    l_hdr[1].paragraphs[0].add_run("Title").font.bold = True
    l_hdr[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in l_hdr:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(11)

    # =========================================================================
    # 8. LIST OF TABLES
    # =========================================================================
    doc.add_page_break()
    p_lot_h = doc.add_paragraph()
    p_lot_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_h.paragraph_format.space_before = Pt(20)
    p_lot_h.paragraph_format.space_after = Pt(16)
    r = p_lot_h.add_run("List of Tables")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    lot_table = doc.add_table(rows=1, cols=3)
    lot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    lot_table.autofit = False
    lot_table.columns[0].width = Inches(1.2)
    lot_table.columns[1].width = Inches(4.5)
    lot_table.columns[2].width = Inches(0.8)
    
    t_hdr = lot_table.rows[0].cells
    t_hdr[0].paragraphs[0].add_run("Table No.").font.bold = True
    t_hdr[1].paragraphs[0].add_run("Title").font.bold = True
    t_hdr[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in t_hdr:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(11)

    # =========================================================================
    # 9. LIST OF ABBREVIATIONS (Alphabetical Order)
    # =========================================================================
    doc.add_page_break()
    p_abb_h = doc.add_paragraph()
    p_abb_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abb_h.paragraph_format.space_before = Pt(20)
    p_abb_h.paragraph_format.space_after = Pt(16)
    r = p_abb_h.add_run("List of Abbreviations")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    abbreviations = [
        ("AP", "Average Precision"),
        ("AUC", "Area Under the Curve"),
        ("BCE", "Binary Cross-Entropy"),
        ("CAD", "Computer-Aided Diagnosis"),
        ("CNN", "Convolutional Neural Network"),
        ("DenseNet", "Densely Connected Convolutional Network"),
        ("DFD", "Data Flow Diagram"),
        ("FN", "False Negative"),
        ("FOCAL", "Focal Loss Objective"),
        ("FP", "False Positive"),
        ("GPU", "Graphics Processing Unit"),
        ("Grad-CAM", "Gradient-weighted Class Activation Mapping"),
        ("HAM10000", "Human Against Machine with 10,000 Training Images Dataset"),
        ("IEEE", "Institute of Electrical and Electronics Engineers"),
        ("ISBI", "International Symposium on Biomedical Imaging"),
        ("ISIC", "International Skin Imaging Collaboration"),
        ("ML", "Machine Learning"),
        ("MLP", "Multi-Layer Perceptron"),
        ("PR", "Precision-Recall"),
        ("PR-AUC", "Precision-Recall Area Under the Curve"),
        ("RAM", "Random Access Memory"),
        ("ROC", "Receiver Operating Characteristic"),
        ("ROC-AUC", "Receiver Operating Characteristic Area Under the Curve"),
        ("ROS", "Random Oversampling"),
        ("SCOPE", "School of Computer Science and Engineering"),
        ("SIIM", "Society for Imaging Informatics in Medicine"),
        ("TN", "True Negative"),
        ("TNR", "Times New Roman / True Negative Rate"),
        ("TP", "True Positive"),
        ("UML", "Unified Modeling Language"),
        ("VIT", "Vellore Institute of Technology"),
        ("W-BCE", "Weighted Binary Cross-Entropy")
    ]

    t_abb = doc.add_table(rows=len(abbreviations), cols=2)
    t_abb.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_abb.autofit = False
    t_abb.columns[0].width = Inches(1.8)
    t_abb.columns[1].width = Inches(4.7)
    set_table_borders(t_abb, "E0E0E0")
    
    for idx, (abbr, full) in enumerate(abbreviations):
        row = t_abb.rows[idx]
        c0 = row.cells[0]
        c1 = row.cells[1]
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        r0 = p0.add_run(abbr)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.font.bold = True
        r1 = p1.add_run(full)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    # =========================================================================
    # 10. SYMBOLS AND NOTATIONS
    # =========================================================================
    doc.add_page_break()
    p_sym_h = doc.add_paragraph()
    p_sym_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sym_h.paragraph_format.space_before = Pt(20)
    p_sym_h.paragraph_format.space_after = Pt(16)
    r = p_sym_h.add_run("Symbols and Notations")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    symbols = [
        ("α (Alpha)", "Balancing factor for positive class in Focal Loss formulation (α = 0.75)"),
        ("γ (Gamma)", "Focusing parameter for down-weighting easy negative examples in Focal Loss (γ = 2.0)"),
        ("η (Eta)", "Optimizer learning rate schedule parameter (η = 0.0001)"),
        ("λ (Lambda)", "L2 weight decay regularization coefficient in AdamW optimizer (λ = 0.0001)"),
        ("μ (Mu)", "Channel-wise pixel normalization mean vector ([0.485, 0.456, 0.406])"),
        ("σ (Sigma)", "Channel-wise pixel normalization standard deviation vector ([0.229, 0.224, 0.225])"),
        ("τ (Tau)", "Decision classification probability threshold for positive malignant assignment"),
        ("L_BCE", "Binary Cross-Entropy loss objective function"),
        ("L_WBCE", "Positive-weighted Binary Cross-Entropy loss objective function"),
        ("L_FL", "Focal Loss objective function"),
        ("w_+", "Positive minority class loss multiplier weight (w_+ = 50.2067)"),
        ("y", "Ground truth binary lesion target label (0 = Benign, 1 = Malignant)"),
        ("p_hat", "Model predicted probability of malignancy produced via sigmoid activation σ(z)"),
        ("z", "Unnormalized raw scalar logit output produced by the linear classification head")
    ]

    t_sym = doc.add_table(rows=len(symbols), cols=2)
    t_sym.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sym.autofit = False
    t_sym.columns[0].width = Inches(1.8)
    t_sym.columns[1].width = Inches(4.7)
    set_table_borders(t_sym, "E0E0E0")
    
    for idx, (sym, desc) in enumerate(symbols):
        row = t_sym.rows[idx]
        c0 = row.cells[0]
        c1 = row.cells[1]
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        r0 = p0.add_run(sym)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.font.bold = True
        r1 = p1.add_run(desc)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    print("Preliminary pages created.")
    return doc, toc_table, lof_table, lot_table

if __name__ == "__main__":
    doc, toc_t, lof_t, lot_t = build_report()
    doc.save(os.path.join(PROJECT_ROOT, "temp_prelim.docx"))
    print("Preliminary pages saved successfully.")
