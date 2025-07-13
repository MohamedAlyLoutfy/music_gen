# 🎵 Music Generation

This repository contains tools and scripts to prepare, analyze, and preprocess music data for fine-tuning a generative model. The project is structured into several stages:

* `data_preparation`: Prepares datasets for training.
* `finetuning_audiocraft`: Fine-tunes the [AudioCraft](https://github.com/facebookresearch/audiocraft) model.
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
│   ├── resample.py
├── finetuning_audiocraft/
│   └── (Modified AudioCraft repo and custom scripts)
├── SLURM/
│   ├── slurm_inference_musicgen
│   ├── slurm_inference_pretrained
│   └── slurm_musicgen_text
├── testing/
│   └── CLAP/
│       └── clap_testing.py
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

## 🧵 SLURM Scripts

### 📂 `SLURM/`

Contains SLURM batch job scripts used for launching training and inference on compute clusters.

#### 🔁 `slurm_inference_musicgen`

* Runs inference using musicgen finetunned checkpoint

#### 🔎 `slurm_inference_pretrained`

* Runs inference using pretrained model.

#### 🔎 `slurm_text_musicgen`

* MusicGen Finetunning script.


Make sure to adjust paths, job names, and resource allocations as needed for your cluster.

---

## 🧪 Testing

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

