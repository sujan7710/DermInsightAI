# DermInsight AI: Notebooks & Colab Environment

## Execution Environment

All deep learning experiments in DermInsight AI were developed and executed using **Google Colab Pro** with high-memory GPU runtimes (NVIDIA Tesla T4 / V100 GPU instances, 16GB VRAM, CUDA 12.x).

As recorded in `docs/organization_manifest.json`, artifacts were synchronized via Google Drive under `/content/drive/MyDrive/DermInsightAI/`.

---

## Script Equivalents in `src/`

The core model pipelines are structured as modular Python scripts for production reproducibility:

| Experiment | Modular Script | Description |
|:---|:---|:---|
| **EXP_01_BASELINE** | `src/EXP_01_BASELINE/densenet201_baseline.py` | Full DenseNet-201 baseline training and evaluation pipeline |
| **EXP_02_WEIGHTED_BCE** | `src/EXP_02_WEIGHTED_BCE/stage2b_weighted_bce.py` | Fine-tuning pipeline with positive-class weighting |
| **EXP_02 Evaluation** | `src/EXP_02_WEIGHTED_BCE/stage2b_final_evaluation.py` | Multi-threshold evaluation and metrics extraction |
| **EXP_02 Visualization** | `src/EXP_02_WEIGHTED_BCE/stage2b_visual_results.py` | Generation of ROC, PR, threshold, and confusion matrix plots |

---

## Interactive Reproduction in Jupyter / Colab

To run these experiments interactively in Jupyter or Google Colab:
1. Clone this repository into your environment:
   ```bash
   git clone <repository_url>
   cd DermInsightAI
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the baseline training directly:
   ```bash
   python src/EXP_01_BASELINE/densenet201_baseline.py \
       --data_dir data \
       --output_dir results/EXP_01_BASELINE \
       --batch_size 32 \
       --epochs 3 \
       --learning_rate 1e-4
   ```
4. Run evaluation using pre-trained checkpoints in `models/`:
   ```bash
   python src/EXP_02_WEIGHTED_BCE/stage2b_final_evaluation.py
   ```
