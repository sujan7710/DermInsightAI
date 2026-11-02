# -*- coding: utf-8 -*-
"""
DermInsight AI - Master Report Compiler
Assembles all sections, executes Word COM to determine exact rendered page numbers,
populates Table of Contents, List of Figures, and List of Tables, and exports DOCX & PDF.
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from build_helpers import (
    set_cell_margins, set_cell_background, set_table_borders
)

import generate_report_prelim as prelim
import generate_chapters_1_to_3 as ch13
import generate_chapters_4_to_6 as ch46
import generate_chapters_7_to_end as ch7end

PROJECT_ROOT = r'C:\Users\sujan\Downloads\DermInsightAI-20261026T173409Z-1-001\DermInsightAI'
DOCX_OUT = os.path.join(PROJECT_ROOT, 'DermInsight_AI_Project_I_Report_Verified.docx')
PDF_OUT = os.path.join(PROJECT_ROOT, 'DermInsight_AI_Project_I_Report_Verified.pdf')
TEMP_DOCX = os.path.join(PROJECT_ROOT, 'temp_rendered_draft.docx')

def assemble_full_document():
    print("Assembling preliminary pages...")
    doc, toc_t, lof_t, lot_t = prelim.build_report()
    
    print("Adding Chapters 1, 2, 3...")
    ch13.add_chapter_1(doc)
    ch13.add_chapter_2(doc)
    ch13.add_chapter_3(doc)
    
    print("Adding Chapters 4, 5, 6...")
    ch46.add_chapter_4(doc)
    ch46.add_chapter_5(doc)
    ch46.add_chapter_6(doc)
    
    print("Adding Chapters 7, 8, References, Appendix...")
    ch7end.add_chapter_7(doc)
    ch7end.add_chapter_8(doc)
    ch7end.add_chapter_9_references(doc)
    ch7end.add_appendix_a(doc)
    
    doc.save(TEMP_DOCX)
    print(f"Draft document saved to {TEMP_DOCX}")
    return toc_t, lof_t, lot_t

def measure_pages_with_word_com():
    import win32com.client
    print("Initializing Word COM engine to measure rendered page numbers...")
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    
    try:
        w_doc = word.Documents.Open(TEMP_DOCX)
        total_pages = w_doc.ComputeStatistics(2) # 2 = wdStatisticPages
        print(f"Rendered document total pages: {total_pages}")
        
        # Track items
        heading_pages = {}
        fig_pages = {}
        tbl_pages = {}
        
        for para in w_doc.Paragraphs:
            text = para.Range.Text.strip()
            if not text:
                continue
            
            # Headings
            for key in [
                "1. INTRODUCTION", "1.1 Background", "1.2 Motivations", "1.3 Scope of the Project",
                "2. PROJECT DESCRIPTION AND GOALS", "2.1 Literature Review", "2.2 Research Gap", "2.3 Objectives", "2.4 Problem Statement", "2.5 Project Plan",
                "3. TECHNICAL SPECIFICATION", "3.1 Requirements", "3.1.1 Functional", "3.1.2 Non-Functional", "3.2 Feasibility Study", "3.2.1 Technical", "3.2.2 Economic", "3.2.3 Social", "3.3 System Specification", "3.3.1 Hardware", "3.3.2 Software",
                "4. DESIGN APPROACH AND DETAILS", "4.1 System Architecture", "4.2 Design", "4.2.1 Data Flow Diagram", "4.2.2 Use Case Diagram", "4.2.3 Class Diagram", "4.2.4 Sequence Diagram",
                "5. METHODOLOGY AND TESTING", "5.1 Deep Learning Pipeline Architecture", "5.2 Patient-Level Splitting", "5.3 Class-Imbalance Formulations", "5.4 Checkpoint Selection", "5.5 Classification Threshold", "5.6 Evaluation & Testing Protocol",
                "6. PROJECT DEMONSTRATION", "6.1 Demonstration Workflow", "6.2 Preprocessing & Batch Dataloader", "6.3 Model Inference", "6.4 Threshold Calibration", "6.5 Output Visualizations",
                "7. RESULT AND DISCUSSION", "7.1 Cross-Experiment Quantitative", "7.2 Detailed Analysis by Experiment", "7.2.1 Experiment 1", "7.2.2 Experiment 2", "7.2.3 Experiment 3", "7.2.4 Experiment 4", "7.2.5 Experiment 5", "7.3 Sensitivity vs. Specificity", "7.4 Why Accuracy is Misleading", "7.5 Cost-Sensitive Analysis", "7.6 Analysis of Incomplete",
                "8. CONCLUSION", "8.1 Summary of Completed", "8.2 Key Scientific Findings", "8.3 Observed Research Limitations", "8.4 Future Research Directions",
                "9. REFERENCES", "APPENDIX A"
            ]:
                if key not in heading_pages and key.lower() in text.lower():
                    pg = para.Range.Information(3) # wdActiveEndAdjustedPageNumber
                    heading_pages[key] = pg
            
            # Figures
            if text.startswith("Figure "):
                parts = text.split(":")
                if len(parts) >= 2:
                    fig_id = parts[0].strip()
                    if fig_id not in fig_pages:
                        pg = para.Range.Information(3)
                        fig_pages[fig_id] = pg

            # Tables
            if text.startswith("Table "):
                parts = text.split(":")
                if len(parts) >= 2:
                    tbl_id = parts[0].strip()
                    if tbl_id not in tbl_pages:
                        pg = para.Range.Information(3)
                        tbl_pages[tbl_id] = pg
                        
        print(f"Extracted {len(heading_pages)} headings, {len(fig_pages)} figures, {len(tbl_pages)} tables.")
        w_doc.Close(False)
    finally:
        word.Quit()
        
    return heading_pages, fig_pages, tbl_pages

def compile_final_document(heading_pages, fig_pages, tbl_pages):
    print("Compiling final document with exact page numbers in TOC, LOF, and LOT...")
    
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. Title Page
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

    # 2. Declaration
    doc.add_page_break()
    p_dec_h = doc.add_paragraph()
    p_dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec_h.paragraph_format.space_before = Pt(24)
    p_dec_h.paragraph_format.space_after = Pt(20)
    r = p_dec_h.add_run("DECLARATION")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    ch13.add_body_paragraph(
        doc,
        "We hereby declare that the project entitled \"AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER\" "
        "submitted by us, for the award of the degree of Bachelor of Technology in Computer Science and Engineering to Vellore Institute "
        "of Technology (VIT), is a record of bonafide research work carried out by us under the supervision of Dr. Krishna Rani Samal, "
        "Associate Professor, School of Computer Science and Engineering (SCOPE)."
    )
    ch13.add_body_paragraph(
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

    # 3. Certificate
    doc.add_page_break()
    p_cert_h = doc.add_paragraph()
    p_cert_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_h.paragraph_format.space_before = Pt(24)
    p_cert_h.paragraph_format.space_after = Pt(20)
    r = p_cert_h.add_run("CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    ch13.add_body_paragraph(
        doc,
        "This is to certify that the project entitled \"AN AUTOMATED DEEP LEARNING FRAMEWORK FOR EARLY DETECTION OF SKIN CANCER\" "
        "submitted by ALAN JOHN ANAND (Reg. No: 23BCB0165), SUJAN M (Reg. No: 23BCE2002), and RAMACHANDRAN SIVASANKAR "
        "(Reg. No: 23BCE2107), School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, for the award "
        "of the degree of Bachelor of Technology in Computer Science and Engineering, is a record of bonafide work carried out by them "
        "under my supervision during Fall Semester 2026, as per the VIT code of academic and research ethics."
    )
    ch13.add_body_paragraph(
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

    # 4. Acknowledgements
    doc.add_page_break()
    p_ack_h = doc.add_paragraph()
    p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_h.paragraph_format.space_before = Pt(24)
    p_ack_h.paragraph_format.space_after = Pt(20)
    r = p_ack_h.add_run("ACKNOWLEDGEMENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    ch13.add_body_paragraph(
        doc,
        "We are deeply grateful to the management of Vellore Institute of Technology (VIT) for providing us with the opportunity, "
        "computational resources, and high-performance infrastructure to undertake this B.Tech Project-I research endeavor. Their continuous "
        "commitment to fostering an intellectually stimulating and research-driven environment has been instrumental in shaping our work."
    )
    ch13.add_body_paragraph(
        doc,
        "Our sincere thanks to Dr. Jaisankar N, Dean of the School of Computer Science and Engineering (SCOPE), for his visionary leadership, "
        "unwavering support, and constant encouragement. His dedication to academic excellence and promoting rigorous scientific inquiry has "
        "been an invaluable source of inspiration throughout the semester."
    )
    ch13.add_body_paragraph(
        doc,
        "We express our profound appreciation to the Head of the Department of Computer Science and Engineering, SCOPE, for insightful administrative "
        "guidance, resource allocation, and maintaining high academic standards that enabled us to execute our deep learning experiments smoothly."
    )
    ch13.add_body_paragraph(
        doc,
        "We are immensely thankful to our project supervisor and guide, Dr. Krishna Rani Samal, Associate Professor, SCOPE, for her dedicated mentorship, "
        "technical wisdom, and constructive critiques. Her patient guidance, insistence on empirical integrity, and methodical evaluation of class-imbalance "
        "challenges in medical imaging were vital to the successful completion and honest verification of this project."
    )
    ch13.add_body_paragraph(
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

    # 5. Abstract
    doc.add_page_break()
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_h.paragraph_format.space_before = Pt(24)
    p_abs_h.paragraph_format.space_after = Pt(20)
    r = p_abs_h.add_run("ABSTRACT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True

    ch13.add_body_paragraph(
        doc,
        "Malignant melanoma represents the deadliest form of skin cancer, accounting for the vast majority of skin cancer mortalities "
        "despite comprising less than five percent of total cutaneous malignancies. While early-stage surgical resection yields five-year survival "
        "rates exceeding 98%, late-stage metastatic prognosis drops drastically below 25%. Consequently, automated computer-aided screening systems "
        "capable of triaging high-risk dermoscopic lesions possess transformative clinical utility. However, real-world dermoscopy datasets suffer "
        "from extreme class imbalance, where malignant cases constitute a microscopic fraction of clinical encounters. Furthermore, published "
        "benchmarks frequently report high nominal accuracy while masking catastrophic false-negative rates or suffering from subtle patient-level "
        "data leakage across evaluation splits."
    )
    ch13.add_body_paragraph(
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
    ch13.add_body_paragraph(
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

    # 6. Table of Contents (Populated with exact pages)
    doc.add_page_break()
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.paragraph_format.space_before = Pt(20)
    p_toc_h.paragraph_format.space_after = Pt(16)
    r = p_toc_h.add_run("TABLE OF CONTENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    toc_items = [
        ("", "Abstract", "x"),
        ("1.", "INTRODUCTION", heading_pages.get("1. INTRODUCTION", 1)),
        ("1.1", "Background", heading_pages.get("1.1 Background", 1)),
        ("1.2", "Motivations", heading_pages.get("1.2 Motivations", 1)),
        ("1.3", "Scope of the Project", heading_pages.get("1.3 Scope of the Project", 2)),
        ("2.", "PROJECT DESCRIPTION AND GOALS", heading_pages.get("2. PROJECT DESCRIPTION AND GOALS", 3)),
        ("2.1", "Literature Review", heading_pages.get("2.1 Literature Review", 3)),
        ("2.2", "Research Gap", heading_pages.get("2.2 Research Gap", 5)),
        ("2.3", "Objectives", heading_pages.get("2.3 Objectives", 5)),
        ("2.4", "Problem Statement", heading_pages.get("2.4 Problem Statement", 6)),
        ("2.5", "Project Plan", heading_pages.get("2.5 Project Plan", 6)),
        ("3.", "TECHNICAL SPECIFICATION", heading_pages.get("3. TECHNICAL SPECIFICATION", 7)),
        ("3.1", "Requirements", heading_pages.get("3.1 Requirements", 7)),
        ("3.1.1", "Functional Requirements", heading_pages.get("3.1.1 Functional", 7)),
        ("3.1.2", "Non-Functional Requirements", heading_pages.get("3.1.2 Non-Functional", 7)),
        ("3.2", "Feasibility Study", heading_pages.get("3.2 Feasibility Study", 8)),
        ("3.2.1", "Technical Feasibility", heading_pages.get("3.2.1 Technical", 8)),
        ("3.2.2", "Economic Feasibility", heading_pages.get("3.2.2 Economic", 8)),
        ("3.2.3", "Social Feasibility", heading_pages.get("3.2.3 Social", 8)),
        ("3.3", "System Specification", heading_pages.get("3.3 System Specification", 9)),
        ("3.3.1", "Hardware Specification", heading_pages.get("3.3.1 Hardware", 9)),
        ("3.3.2", "Software Specification", heading_pages.get("3.3.2 Software", 9)),
        ("4.", "DESIGN APPROACH AND DETAILS", heading_pages.get("4. DESIGN APPROACH AND DETAILS", 11)),
        ("4.1", "System Architecture", heading_pages.get("4.1 System Architecture", 11)),
        ("4.2", "Design", heading_pages.get("4.2 Design", 12)),
        ("4.2.1", "Data Flow Diagram", heading_pages.get("4.2.1 Data Flow Diagram", 12)),
        ("4.2.2", "Use Case Diagram", heading_pages.get("4.2.2 Use Case Diagram", 13)),
        ("4.2.3", "Class Diagram", heading_pages.get("4.2.3 Class Diagram", 14)),
        ("4.2.4", "Sequence Diagram", heading_pages.get("4.2.4 Sequence Diagram", 15)),
        ("5.", "METHODOLOGY AND TESTING", heading_pages.get("5. METHODOLOGY AND TESTING", 16)),
        ("5.1", "Deep Learning Pipeline Architecture (DenseNet201)", heading_pages.get("5.1 Deep Learning Pipeline Architecture", 16)),
        ("5.2", "Patient-Level Splitting & Data Preprocessing", heading_pages.get("5.2 Patient-Level Splitting", 17)),
        ("5.3", "Class-Imbalance Formulations & Strategies", heading_pages.get("5.3 Class-Imbalance Formulations", 18)),
        ("5.4", "Checkpoint Selection & Early Stopping", heading_pages.get("5.4 Checkpoint Selection", 19)),
        ("5.5", "Classification Threshold Calibration Methodology", heading_pages.get("5.5 Classification Threshold", 20)),
        ("5.6", "Evaluation & Testing Protocol on Held-Out Test Set", heading_pages.get("5.6 Evaluation & Testing Protocol", 20)),
        ("6.", "PROJECT DEMONSTRATION", heading_pages.get("6. PROJECT DEMONSTRATION", 21)),
        ("6.1", "Demonstration Workflow & Environment", heading_pages.get("6.1 Demonstration Workflow", 21)),
        ("6.2", "Preprocessing & Batch Dataloader Execution", heading_pages.get("6.2 Preprocessing & Batch Dataloader", 21)),
        ("6.3", "Model Inference Execution Demonstration", heading_pages.get("6.3 Model Inference", 21)),
        ("6.4", "Threshold Calibration & Triage Generation", heading_pages.get("6.4 Threshold Calibration", 22)),
        ("6.5", "Output Visualizations Demonstration", heading_pages.get("6.5 Output Visualizations", 22)),
        ("7.", "RESULT AND DISCUSSION (COST ANALYSIS as applicable)", heading_pages.get("7. RESULT AND DISCUSSION", 23)),
        ("7.1", "Cross-Experiment Quantitative Performance Comparison", heading_pages.get("7.1 Cross-Experiment Quantitative", 23)),
        ("7.2", "Detailed Analysis by Experiment", heading_pages.get("7.2 Detailed Analysis by Experiment", 24)),
        ("7.3", "Sensitivity vs. Specificity Clinical Trade-offs", heading_pages.get("7.3 Sensitivity vs. Specificity", 29)),
        ("7.4", "Why Accuracy is Misleading in Highly Imbalanced Medical Screening", heading_pages.get("7.4 Why Accuracy is Misleading", 29)),
        ("7.5", "Cost-Sensitive Analysis & False-Negative Clinical Impact", heading_pages.get("7.5 Cost-Sensitive Analysis", 30)),
        ("7.6", "Analysis of Incomplete / Unsuccessful Iterations", heading_pages.get("7.6 Analysis of Incomplete", 31)),
        ("8.", "CONCLUSION", heading_pages.get("8. CONCLUSION", 32)),
        ("8.1", "Summary of Completed Research Work", heading_pages.get("8.1 Summary of Completed", 32)),
        ("8.2", "Key Scientific Findings & Takeaways", heading_pages.get("8.2 Key Scientific Findings", 32)),
        ("8.3", "Observed Research Limitations", heading_pages.get("8.3 Observed Research Limitations", 33)),
        ("8.4", "Future Research Directions", heading_pages.get("8.4 Future Research Directions", 33)),
        ("9.", "REFERENCES", heading_pages.get("9. REFERENCES", 34)),
        ("", "APPENDIX A – SAMPLE CODE", heading_pages.get("APPENDIX A", 37))
    ]

    t_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    t_toc.columns[0].width = Inches(0.8)
    t_toc.columns[1].width = Inches(4.9)
    t_toc.columns[2].width = Inches(0.8)
    set_table_borders(t_toc, "E0E0E0")
    
    # Header
    hdr = t_toc.rows[0].cells
    hdr[0].paragraphs[0].add_run("Sl.No").font.bold = True
    hdr[1].paragraphs[0].add_run("Contents").font.bold = True
    hdr[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(c, "F2F4F7")
        set_cell_margins(c, 50, 50, 60, 60)

    for idx, (sl, item, pg) in enumerate(toc_items, start=1):
        row = t_toc.rows[idx].cells
        p0 = row[0].paragraphs[0]
        p1 = row[1].paragraphs[0]
        p2 = row[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        r0 = p0.add_run(sl)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        
        r1 = p1.add_run(item)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        
        r2 = p2.add_run(str(pg))
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        
        if sl in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."] or item in ["Abstract", "APPENDIX A – SAMPLE CODE"]:
            r0.font.bold = True
            r1.font.bold = True
            r2.font.bold = True
        set_cell_margins(row[0], 35, 35, 50, 50)
        set_cell_margins(row[1], 35, 35, 50, 50)
        set_cell_margins(row[2], 35, 35, 50, 50)

    # 7. List of Figures (Populated)
    doc.add_page_break()
    p_lof_h = doc.add_paragraph()
    p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_h.paragraph_format.space_before = Pt(20)
    p_lof_h.paragraph_format.space_after = Pt(16)
    r = p_lof_h.add_run("List of Figures")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    figures_list = [
        ("Figure 3.1", "SIIM-ISIC 2020 Dataset Lesion Class Distribution on Logarithmic Scale", fig_pages.get("Figure 3.1", 10)),
        ("Figure 4.1", "End-to-End System Architecture of the DermInsight AI Screening Framework", fig_pages.get("Figure 4.1", 11)),
        ("Figure 4.2", "Level-1 Data Flow Diagram (DFD) Illustrating Image Ingestion and Inference", fig_pages.get("Figure 4.2", 12)),
        ("Figure 4.3", "Use Case Diagram for the DermInsight AI Clinical Screening Interface", fig_pages.get("Figure 4.3", 13)),
        ("Figure 4.4", "UML Class Diagram of the Implemented PyTorch Deep Learning Pipeline", fig_pages.get("Figure 4.4", 14)),
        ("Figure 4.5", "UML Sequence Diagram for Dermoscopic Image Ingestion, Inference, and Triage", fig_pages.get("Figure 4.5", 15)),
        ("Figure 7.1", "Experiment 1 (DenseNet201 Baseline) Test Confusion Matrix (Threshold = 0.50)", fig_pages.get("Figure 7.1", 24)),
        ("Figure 7.2", "Experiment 1 Training and Validation Loss Curves Across 3 Epochs", fig_pages.get("Figure 7.2", 24)),
        ("Figure 7.3", "Experiment 2 (DenseNet201 Weighted BCE) Test Confusion Matrix (Threshold = 0.86)", fig_pages.get("Figure 7.3", 25)),
        ("Figure 7.4", "Experiment 2 Validation Set Threshold Calibration Sweep Across Tau in [0.01, 0.99]", fig_pages.get("Figure 7.4", 25)),
        ("Figure 7.5", "Experiment 3 (WeightedRandomSampler) Test Confusion Matrix (Threshold = 0.50)", fig_pages.get("Figure 7.5", 26)),
        ("Figure 7.6", "Experiment 4 (Focal Loss) Test Confusion Matrix (Threshold = 0.50)", fig_pages.get("Figure 7.6", 26)),
        ("Figure 7.7", "Experiment 5 (Random Oversampling) Test Confusion Matrix (Threshold = 0.7296)", fig_pages.get("Figure 7.7", 27)),
        ("Figure 7.8", "Combined Cross-Experiment Test ROC Curves and Operating Points (EXP 01 to EXP 05)", fig_pages.get("Figure 7.8", 28)),
        ("Figure 7.9", "Combined Cross-Experiment Test Precision-Recall (PR) Curves Relative to Prevalence Base Rate", fig_pages.get("Figure 7.9", 28)),
        ("Figure 7.10", "Cross-Experiment Diagnostic Metric Comparison on Held-Out Test Set (N=4,920)", fig_pages.get("Figure 7.10", 28))
    ]

    t_lof = doc.add_table(rows=len(figures_list) + 1, cols=3)
    t_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_lof.autofit = False
    t_lof.columns[0].width = Inches(1.3)
    t_lof.columns[1].width = Inches(4.4)
    t_lof.columns[2].width = Inches(0.8)
    set_table_borders(t_lof, "E0E0E0")
    
    l_hdr = t_lof.rows[0].cells
    l_hdr[0].paragraphs[0].add_run("Figure No.").font.bold = True
    l_hdr[1].paragraphs[0].add_run("Title").font.bold = True
    l_hdr[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in l_hdr:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(c, "F2F4F7")
        set_cell_margins(c, 50, 50, 60, 60)

    for idx, (f_num, f_title, f_pg) in enumerate(figures_list, start=1):
        row = t_lof.rows[idx].cells
        p0 = row[0].paragraphs[0]
        p1 = row[1].paragraphs[0]
        p2 = row[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        r0 = p0.add_run(f_num)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.font.bold = True
        
        r1 = p1.add_run(f_title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        
        r2 = p2.add_run(str(f_pg))
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        set_cell_margins(row[0], 35, 35, 50, 50)
        set_cell_margins(row[1], 35, 35, 50, 50)
        set_cell_margins(row[2], 35, 35, 50, 50)

    # 8. List of Tables (Populated)
    doc.add_page_break()
    p_lot_h = doc.add_paragraph()
    p_lot_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_h.paragraph_format.space_before = Pt(20)
    p_lot_h.paragraph_format.space_after = Pt(16)
    r = p_lot_h.add_run("List of Tables")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    tables_list = [
        ("Table 3.1", "Hardware System Specifications", tbl_pages.get("Table 3.1", 9)),
        ("Table 3.2", "Software Environment Specifications", tbl_pages.get("Table 3.2", 9)),
        ("Table 5.1", "DenseNet201 Feature Extractor Architectural Details", tbl_pages.get("Table 5.1", 16)),
        ("Table 5.2", "Verified Patient-Level Dataset Splitting and Class Distribution", tbl_pages.get("Table 5.2", 17)),
        ("Table 5.3", "Master Training Hyperparameters and Experimental Configurations", tbl_pages.get("Table 5.3", 19)),
        ("Table 7.1", "Master Cross-Experiment Quantitative Performance Comparison on Held-Out Test Set (N=4,920)", tbl_pages.get("Table 7.1", 23)),
        ("Table 7.2", "Clinical Misclassification Cost Matrix Configuration", tbl_pages.get("Table 7.2", 30)),
        ("Table 7.3", "Expected Total Clinical Misclassification Cost Across Imbalance Strategies (Test N=4,920)", tbl_pages.get("Table 7.3", 30))
    ]

    t_lot = doc.add_table(rows=len(tables_list) + 1, cols=3)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_lot.autofit = False
    t_lot.columns[0].width = Inches(1.3)
    t_lot.columns[1].width = Inches(4.4)
    t_lot.columns[2].width = Inches(0.8)
    set_table_borders(t_lot, "E0E0E0")
    
    t_hdr = t_lot.rows[0].cells
    t_hdr[0].paragraphs[0].add_run("Table No.").font.bold = True
    t_hdr[1].paragraphs[0].add_run("Title").font.bold = True
    t_hdr[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in t_hdr:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(c, "F2F4F7")
        set_cell_margins(c, 50, 50, 60, 60)

    for idx, (t_num, t_title, t_pg) in enumerate(tables_list, start=1):
        row = t_lot.rows[idx].cells
        p0 = row[0].paragraphs[0]
        p1 = row[1].paragraphs[0]
        p2 = row[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        r0 = p0.add_run(t_num)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.font.bold = True
        
        r1 = p1.add_run(t_title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        
        r2 = p2.add_run(str(t_pg))
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        set_cell_margins(row[0], 35, 35, 50, 50)
        set_cell_margins(row[1], 35, 35, 50, 50)
        set_cell_margins(row[2], 35, 35, 50, 50)

    # 9. List of Abbreviations
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
        c0, c1 = row.cells[0], row.cells[1]
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        r0 = p0.add_run(abbr)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.font.bold = True
        r1 = p1.add_run(full)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        set_cell_margins(c0, 45, 45, 80, 80)
        set_cell_margins(c1, 45, 45, 80, 80)

    # 10. Symbols and Notations
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
        c0, c1 = row.cells[0], row.cells[1]
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        r0 = p0.add_run(sym)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.font.bold = True
        r1 = p1.add_run(desc)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        set_cell_margins(c0, 45, 45, 80, 80)
        set_cell_margins(c1, 45, 45, 80, 80)

    # Chapters
    print("Appending Chapters 1 to 9...")
    ch13.add_chapter_1(doc)
    ch13.add_chapter_2(doc)
    ch13.add_chapter_3(doc)
    ch46.add_chapter_4(doc)
    ch46.add_chapter_5(doc)
    ch46.add_chapter_6(doc)
    ch7end.add_chapter_7(doc)
    ch7end.add_chapter_8(doc)
    ch7end.add_chapter_9_references(doc)
    ch7end.add_appendix_a(doc)

    doc.save(DOCX_OUT)
    print(f"Final verified Word report saved to: {DOCX_OUT}")

def export_to_pdf():
    import win32com.client
    print("Exporting finalized report to PDF via Microsoft Word COM...")
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    try:
        w_doc = word.Documents.Open(DOCX_OUT)
        w_doc.ExportAsFixedFormat(PDF_OUT, 17) # 17 = wdExportFormatPDF
        w_doc.Close(False)
        print(f"Final verified PDF report saved to: {PDF_OUT}")
    finally:
        word.Quit()

if __name__ == "__main__":
    assemble_full_document()
    heading_p, fig_p, tbl_p = measure_pages_with_word_com()
    compile_final_document(heading_p, fig_p, tbl_p)
    export_to_pdf()
    if os.path.exists(TEMP_DOCX):
        os.remove(TEMP_DOCX)
    print("Master Build Complete! Both DOCX and PDF generated perfectly.")
