import os
import torch
import torchaudio
from tqdm import tqdm
from audiocraft.models import EncodecModel
from pathlib import Path

def tokenize_musicgen_dataset(input_folder: str, output_folder: str):
    """
    Tokenizes a folder of 32kHz vocals/non-vocals pairs using EnCodec and saves to a .pt file.

    Args:
        input_folder (str): Path to dataset (subfolders with vocals.wav + non_vocals.wav).
        output_folder (str): Path to save the output .pt file.
    """
    # Load EnCodec (32kHz)
    model = EncodecModel.encodec_model_32khz()
    model.set_target_bandwidth(6.0)
    model.eval()

    dataset = []

    song_dirs = sorted([d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))])

    for subdir in tqdm(song_dirs, desc="Tokenizing songs"):
        song_path = os.path.join(input_folder, subdir)
        vocals_path = os.path.join(song_path, "vocals.wav")
        music_path = os.path.join(song_path, "no_vocals.wav")

        if not (os.path.exists(vocals_path) and os.path.exists(music_path)):
            print(f"Skipping {subdir}: missing vocals or non_vocals.")
            continue

        vocals, sr_v = torchaudio.load(vocals_path)
        music, sr_m = torchaudio.load(music_path)

        if sr_v != 32000 or sr_m != 32000:
            raise ValueError(f"{subdir}: Audio must be 32kHz!")

        # Trim to same length
        min_len = min(vocals.shape[-1], music.shape[-1])
        vocals = vocals[:, :min_len]
        music = music[:, :min_len]

        with torch.no_grad():
            vocals_tokens = model.encode([vocals])[0]
            music_tokens = model.encode([music])[0]

        dataset.append({
            "input_tokens": vocals_tokens.cpu(),
            "target_tokens": music_tokens.cpu(),
            "id": subdir
        })

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "musicgen_tokens.pt")
    torch.save(dataset, output_path)
    print(f"\n✅ Tokenization complete. Saved {len(dataset)} items to: {output_path}")


# === Call the function here ===
# Change these to your actual paths:
input_path = "/media/selim/New Volume1/MusicGen_32khz"
output_path = "/media/selim/New Volume1/MusicGen_32_tokens"

tokenize_musicgen_dataset(input_path, output_path)