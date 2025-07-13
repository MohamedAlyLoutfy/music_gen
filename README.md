# 🎵 Music Generation

This repository contains tools and scripts to prepare, analyze, and preprocess music data for fine-tuning a generative model. The project is structured into several stages:

* `data_preparation`: Prepares datasets for training.
* `finetuning_audiocraft`: Fine-tunes the [AudioCraft](https://github.com/facebookresearch/audiocraft) model.
* `finetuning_audio_ldm`: Fine-tunes the [AudioLDM](https://github.com/haoheliu/AudioLDM-training-finetuning) model.
* `SLURM`: SLURM batch jobs for training and inference.
* `testing`: Evaluation tools for generated outputs.

---

## 📁 Project Structure

```
MusicGeneration/
├── data_preparation/
│   ├── analyzer.py
│   ├── analyze_single.py
│   ├── chunk_audio.py
│   ├── demucs.py
│   ├── demucs_instruments.py
│   ├── generate_mels.py
│   ├── metadata_adder.py
│   ├── metadata_generation.py
│   └── resample.py
├── finetuning_audiocraft/
│   └── (Modified AudioCraft repo and custom scripts)
├── finetuning_audio_ldm/
│   └── (Modified AudioLDM repo and custom scripts)
├── SLURM/
│   ├── slurm_inference_musicgen
│   ├── slurm_inference_pretrained
│   └── slurm_musicgen_text
├── testing/
│   ├── CLAP/
│   ├────── clap_testing.py
│   ├── FAD/
│   └────── fad_testing.py
└── README.md
```

---

## 🚀 Data Preparation

The data preparation pipeline involves the following stages:

1. **Source Separation** using [Demucs](https://github.com/facebookresearch/demucs)
2. **Resampling** to 32kHz
3. **Chunking** into consistent-length audio segments
4. **Feature Extraction** (e.g., mel spectrograms)
5. **Musical Analysis** (BPM, key, etc.)
6. **Metadata Enrichment** (automated & manual)

---

## 🛠️ Finetuning AudioCraft

### 📂 `finetuning_audiocraft/`

This folder contains a cloned and modified version of the [AudioCraft](https://github.com/facebookresearch/audiocraft) repository, adapted for our custom training pipeline.

#### 🔧 Key Features:

* Custom datasets
* Training on pre-chunked and labeled `.wav` pairs

> Make sure to follow AudioCraft’s [installation instructions](https://github.com/facebookresearch/audiocraft#installation), and then replace or integrate your files with this folder.

---
## 🛠️ Finetuning AudioLDM

### 📂 `audio_ldm_fine_tune/`

This folder contains a cloned and modified version of the [AudioLDM](https://github.com/haoheliu/AudioLDM-training-finetuning) repository, adapted for our custom training pipeline.

#### 🔧 Key Features:

* Added multi conditioning

---
## 🧵 SLURM Scripts

### 📂 `SLURM/`

Contains SLURM batch job scripts used for launching training and inference on compute clusters.

#### 🔁 `slurm_inference_musicgen`

* Runs inference using musicgen finetunned checkpoint

#### 🔎 `slurm_inference_pretrained`

* Runs inference using pretrained model.

#### 🔎 `slurm_text_musicgen`

* AudioLDM Finetunning script.

#### 🔎 `slurm_audio_ldm`

* AudioLDM Finetunning script.
#### 🔎 `slurm_inference_ldm`

* AudioLDM Finetunning script.
Make sure to adjust paths, job names, and resource allocations as needed for your cluster.

---

## 🧪 Testing
# 🎧 Frechet Audio Distance (FAD) Evaluation

This project evaluates the similarity between two sets of audio files using **Frechet Audio Distance (FAD)** with the **VGGish model**.

FAD is commonly used to measure the quality of generated audio against a reference dataset (e.g., ground truth). A **lower FAD score indicates better quality** and higher similarity to the reference.

---

## 📦 Step 1: Clone the Repository

```bash
git clone https://github.com/gudgud96/frechet-audio-distance.git
cd frechet-audio-distance
```
## 🐍 Step 2: Set Up Python Environment
Make sure you are using Python 3.8–3.10. Then install the required dependencies:
```bash
pip install -r requirements.txt
```
## 📁 Step 3: Prepare Your Audio Data

#### Organize your .wav files in the following structure:

path/to/project/
├── target/
│   └── target1.wav
├── pre_trained/
    └── generated1.wav

    The target/ folder contains reference audio.

    The pre_trained/ folder contains generated audio for evaluation.
## 🧠 Step 4: Run FAD Evaluation
```
python fad_testing.py
```

### 📁 `testing/CLAP/clap_testing.py`

This script evaluates genre similarity between generated audio and a set of text prompts using the [CLAP model](https://huggingface.co/laion/clap-htsat-fused).

#### 🔍 What it does:

* Loads a pretrained CLAP audio-text model
* Embeds a list of **genre text prompts** (e.g., `"rock"`, `"pop"`, `"disco"`)
* Iterates over `.wav` files in a directory and computes audio embeddings
* Measures cosine similarity with text embeddings
* Outputs CSV results with genre predictions

#### 📂 Example Usage

```python
audio_dir = "/path/to/generated/audio"
```

```bash
python testing/CLAP/clap_testing.py
```

#### 📋 Output Example

| file             | best\_genre | best\_score | score\_disco | score\_rock | score\_pop |
| ---------------- | ----------- | ----------- | ------------ | ----------- | ---------- |
| track\_01.wav    | rock        | 0.873       | 0.65         | 0.87        | 0.71       |
| sample\_beat.wav | pop         | 0.812       | 0.63         | 0.75        | 0.81       |

---

## 🧰 Setup

Install dependencies:

```bash
pip install librosa soundfile numpy pandas tqdm python-dotenv openai
```

Install Demucs:

```bash
pip install demucs
```

---

## 📈 Example Pipeline

1. Place raw `.wav`/`.mp3` files in a folder.
2. Run Demucs:

   ```bash
   python demucs.py
   ```
3. Resample output:

   ```bash
   python resample.py
   ```
4. Chunk the audio:

   ```bash
   python chunk_audio.py
   ```
5. Generate mel spectrograms:

   ```bash
   python generate_mels.py
   ```
6. Analyze musical features:

   ```bash
   python analyzer.py
   ```
7. Generate metadata:

   ```bash
   python metadata_generation.py
   ```

---

## 👥 Contributors

* Mohamed Youssef
* Selim Elbindary

