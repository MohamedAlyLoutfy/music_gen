import os
import torch
import torchaudio
import random
from tqdm import tqdm
from audiocraft.models import EncodecModel


def tokenize_musicgen_dataset(input_folders, output_file, model):
    dataset = []

    for subdir in tqdm(input_folders, desc=f"Tokenizing to {output_file}"):
        song_path = os.path.join(input_path, subdir)
        vocals_path = os.path.join(song_path, "vocals.wav")
        music_path = os.path.join(song_path, "no_vocals.wav")

        if not (os.path.exists(vocals_path) and os.path.exists(music_path)):
            print(f"Skipping {subdir}: missing vocals or no_vocals.")
            continue

        vocals, sr_v = torchaudio.load(vocals_path)
        music, sr_m = torchaudio.load(music_path)

        if sr_v != 32000 or sr_m != 32000:
            raise ValueError(f"{subdir}: Audio must be 32kHz!")

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

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    torch.save(dataset, output_file)
    print(f"\n✅ Saved {len(dataset)} items to: {output_file}")


# === Main setup ===
# Change these to your actual paths
input_path = "/media/selim/New Volume1/MusicGen_32khz"
output_path = "/media/selim/New Volume1/MusicGen_32_tokens"

split_ratio = 0.9  # 90% train, 10% val
random.seed(42)

# Load song directories
all_dirs = sorted([d for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))])
random.shuffle(all_dirs)

split_index = int(len(all_dirs) * split_ratio)
train_dirs = all_dirs[:split_index]
val_dirs = all_dirs[split_index:]

# Load EnCodec model
model = EncodecModel.encodec_model_32khz()
model.set_target_bandwidth(6.0)
model.eval()

# Run tokenization
tokenize_musicgen_dataset(train_dirs, os.path.join(output_path, "train", "musicgen_tokens.pt"), model)
tokenize_musicgen_dataset(val_dirs, os.path.join(output_path, "val", "musicgen_tokens.pt"), model)
