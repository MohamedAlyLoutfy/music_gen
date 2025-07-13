import torch
from transformers import AutoProcessor, ClapModel
import torchaudio
import os
import numpy as np
from pathlib import Path
from tqdm import tqdm
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load CLAP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = ClapModel.from_pretrained("laion/clap-htsat-fused").to(device)
processor = AutoProcessor.from_pretrained("laion/clap-htsat-fused")

# Example genre prompts
text_prompts = ["disco", "rock", "pop"]

def embed_texts(texts):
    inputs = processor(text=texts, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        return model.get_text_features(**inputs).cpu()

def embed_audio(audio_path):
    import torchaudio
    import torch
    import numpy as np

    waveform, sr = torchaudio.load(audio_path)

    # Ensure mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Resample to 48kHz
    if sr != 48000:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=48000)
        waveform = resampler(waveform)

    # Ensure waveform is at least 1 second long
    min_length = 48000  # 1 second
    if waveform.shape[1] < min_length:
        print(f"⚠️ Skipping {audio_path}: too short ({waveform.shape[1]} samples)")
        return None

    # Clamp to 30 seconds max
    max_length = 30 * 48000
    waveform = waveform[:, :max_length]

    # Ensure float32 type
    waveform = waveform.to(torch.float32)

    # Convert to numpy float32 for CLAP processor
    waveform_np = waveform.squeeze(0).numpy().astype(np.float32)  # Shape: (samples,)
    inputs = processor(audios=waveform_np, sampling_rate=48000, return_tensors="pt").to(device)

    with torch.no_grad():
        return model.get_audio_features(**inputs).cpu()



# Load all audio files in a directory
# audio_dir = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/test_res/"
# audio_dir = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/results_audioLDM/inference_results/infer_07-01-19_40_cfg_scale_3.5_ddim_200_n_cand_3/"
audio_dir = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/survey/survey/Musicgen/pretrained/"
audio_files = list(Path(audio_dir).glob("*.wav"))

text_embeds = embed_texts(text_prompts)

results = []

for audio_file in tqdm(audio_files):
    audio_embed = embed_audio(audio_file)

    # Cosine similarity with each genre
    sims = cosine_similarity(audio_embed.numpy(), text_embeds.numpy())[0]
    best_idx = np.argmax(sims)
    result = {
        "file": audio_file.name,
        "best_genre": text_prompts[best_idx],
        "best_score": sims[best_idx]
    }

    # Add individual genre scores
    for i, genre in enumerate(text_prompts):
        result[f"score_{genre}"] = sims[i]

    results.append(result)

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("clap_genre_similarity_results.csv", index=False)
print("Done. Results saved to 'clap_genre_similarity_results.csv'")
