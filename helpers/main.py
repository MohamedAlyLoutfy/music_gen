71% of storage used … 
If you run out, you can't create, edit and upload files.

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
import subprocess
import glob
import shutil
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchaudio


# ----------------------------
# 1. Downloading Music
# ----------------------------
def download_music_from_youtube(url, output_dir="downloaded_music"):
    """
    Download audio from a YouTube URL using yt-dlp and save it to output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    try:
        subprocess.run(command, check=True)
        print("Download complete.")
    except subprocess.CalledProcessError as e:
        print("Error downloading audio:", e)


# ----------------------------
# 2. Separate Audio into Stems (Voice and Beat)
# ----------------------------
def separate_audio_spleeter(input_file, output_dir="separated_audio"):
    """
    Uses Spleeter’s 4-stem separation to split audio into vocals, drums, bass, and other.
    Returns the paths of the separated vocal and drum files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = [
        "spleeter",
        "separate",
        "-p", "spleeter:4stems",
        "-o", output_dir,
        input_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Separation complete for {input_file}.")
    except subprocess.CalledProcessError as e:
        print("Error during separation:", e)
        return None, None

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(output_dir, base_name)
    vocal_file = os.path.join(output_path, "vocals.wav")
    drums_file = os.path.join(output_path, "drums.wav")
    if os.path.exists(vocal_file) and os.path.exists(drums_file):
        return vocal_file, drums_file
    else:
        print("Expected separated files not found.")
        return None, None


# ----------------------------
# 3. Prepare Dataset for Model Training with Normalization
# ----------------------------
def compute_logmel(audio_path, sr=22050, n_mels=128, hop_length=512):
    """
    Load an audio file and compute its log-mel spectrogram.
    """
    y, sr = librosa.load(audio_path, sr=sr)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop_length)
    log_S = librosa.power_to_db(S, ref=np.max)
    return log_S


class VoiceBeatDataset(Dataset):
    """
    A PyTorch dataset class that holds pairs of vocal and drum log-mel spectrograms.
    Computes global normalization statistics for drum (target) spectrograms.
    """

    def __init__(self, separated_dir, sr=22050, n_mels=128, hop_length=512):
        self.vocal_files = []
        self.drums_files = []
        self.sr = sr
        self.n_mels = n_mels
        self.hop_length = hop_length

        for song_dir in glob.glob(os.path.join(separated_dir, "*")):
            vocal_path = os.path.join(song_dir, "vocals.wav")
            drums_path = os.path.join(song_dir, "drums.wav")
            if os.path.exists(vocal_path) and os.path.exists(drums_path):
                self.vocal_files.append(vocal_path)
                self.drums_files.append(drums_path)

        # Compute global normalization statistics for drum spectrograms
        all_values = []
        for f in self.drums_files:
            spec = compute_logmel(f, sr=self.sr, n_mels=self.n_mels, hop_length=self.hop_length)
            all_values.extend(spec.flatten())
        all_values = np.array(all_values)
        self.mean = np.mean(all_values)
        self.std = np.std(all_values)
        print("Global drum spectrogram mean:", self.mean, "std:", self.std)

    def __len__(self):
        return len(self.vocal_files)

    def __getitem__(self, idx):
        vocal_spec = compute_logmel(self.vocal_files[idx], sr=self.sr, n_mels=self.n_mels, hop_length=self.hop_length)
        drums_spec = compute_logmel(self.drums_files[idx], sr=self.sr, n_mels=self.n_mels, hop_length=self.hop_length)
        # Normalize the drum spectrogram
        drums_spec = (drums_spec - self.mean) / self.std

        vocal_tensor = torch.tensor(vocal_spec, dtype=torch.float32).unsqueeze(0)
        drums_tensor = torch.tensor(drums_spec, dtype=torch.float32).unsqueeze(0)
        return vocal_tensor, drums_tensor


# ----------------------------
# 4. Define the Model: Improved U-Net Generator
# ----------------------------
class UNetBeatGenerator(nn.Module):
    """
    A U-Net style generator that takes a vocal spectrogram as input and generates a corresponding drum spectrogram.
    """

    def __init__(self):
        super(UNetBeatGenerator, self).__init__()
        # Encoder
        self.enc1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        self.pool1 = nn.MaxPool2d(2)
        self.enc2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        self.pool2 = nn.MaxPool2d(2)
        self.enc3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        self.pool3 = nn.MaxPool2d(2)
        # Bottleneck
        self.bottleneck = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )
        # Decoder
        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec3 = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        self.up2 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec2 = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        self.up1 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)
        self.dec1 = nn.Sequential(
            nn.Conv2d(64, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        self.out_conv = nn.Conv2d(32, 1, kernel_size=1)

    def forward(self, x):
        enc1 = self.enc1(x)  # [B, 32, H, W]
        enc2 = self.enc2(self.pool1(enc1))  # [B, 64, H/2, W/2]
        enc3 = self.enc3(self.pool2(enc2))  # [B, 128, H/4, W/4]
        bottleneck = self.bottleneck(self.pool3(enc3))  # [B, 256, H/8, W/8]

        up3 = self.up3(bottleneck)  # [B, 128, H/4, W/4]
        cat3 = torch.cat([up3, enc3], dim=1)  # [B, 256, H/4, W/4]
        dec3 = self.dec3(cat3)  # [B, 128, H/4, W/4]

        up2 = self.up2(dec3)  # [B, 64, H/2, W/2]
        cat2 = torch.cat([up2, enc2], dim=1)  # [B, 128, H/2, W/2]
        dec2 = self.dec2(cat2)  # [B, 64, H/2, W/2]

        up1 = self.up1(dec2)  # [B, 32, H, W]
        cat1 = torch.cat([up1, enc1], dim=1)  # [B, 64, H, W]
        dec1 = self.dec1(cat1)  # [B, 32, H, W]

        out = self.out_conv(dec1)
        return torch.tanh(out)


# ----------------------------
# 5. Define Loss Functions and Training with Scheduler
# ----------------------------
def spectral_convergence_loss(pred, target):
    """
    Compute spectral convergence loss as the Frobenius norm of the difference divided by that of the target.
    """
    return torch.norm(target - pred, p='fro') / (torch.norm(target, p='fro') + 1e-7)


def train_model(model, dataset, num_epochs=300, batch_size=8, learning_rate=1e-4, device="cpu"):
    """
    Train the generator model on the dataset using a combination of MSE and spectral convergence losses.
    """
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    criterion = nn.MSELoss()
    # Use ReduceLROnPlateau scheduler to adjust lr based on epoch loss
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10, verbose=True)

    model.train()
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for vocal_spec, drums_spec in dataloader:
            vocal_spec = vocal_spec.to(device)
            drums_spec = drums_spec.to(device)
            optimizer.zero_grad()
            pred_drums = model(vocal_spec)
            loss_mse = criterion(pred_drums, drums_spec)
            loss_sc = spectral_convergence_loss(pred_drums, drums_spec)
            loss = loss_mse + 0.1 * loss_sc
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        avg_loss = epoch_loss / len(dataloader)
        scheduler.step(avg_loss)
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {avg_loss:.4f}")
    return model


# ----------------------------
# 6. Inference: Generate Beat and Combine with Voice
# ----------------------------
def generate_beat(model, voice_audio_path, sr=22050, n_mels=128, hop_length=512, device="cpu", target_mean=0,
                  target_std=1):
    """
    Given a voice audio file and the trained model, generate a beat waveform.
    The network output is scaled back using the normalization statistics.
    """
    log_mel = compute_logmel(voice_audio_path, sr=sr, n_mels=n_mels, hop_length=hop_length)
    input_tensor = torch.tensor(log_mel, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
    model.eval()
    with torch.no_grad():
        pred_spec = model(input_tensor).cpu().squeeze().numpy()

    # Invert normalization of the output
    pred_spec = pred_spec * target_std + target_mean

    # Diagnostic: Print min and max of predicted spectrogram
    print("Predicted spectrogram stats: min =", np.min(pred_spec), "max =", np.max(pred_spec))

    # Optional scaling if amplitude is too low
    scale_factor = 1000.0  # adjust as needed
    if np.max(np.abs(pred_spec)) < 1e-4:
        print("Output is very low amplitude; scaling by", scale_factor)
        pred_spec = pred_spec * scale_factor

    mel_spec = librosa.db_to_power(pred_spec)
    S = librosa.feature.inverse.mel_to_stft(mel_spec, sr=sr, n_fft=2048)
    y = librosa.griffinlim(S, hop_length=hop_length, n_iter=32)
    return y, sr


def combine_voice_and_beat(voice_audio_path, beat_audio_array, sr,
                           output_dir="final_outputs",
                           voice_output_file="voice.wav",
                           beat_output_file="beat.wav",
                           mix_output_file="final_mix.wav"):
    """
    Save the generated beat, the original voice, and a final mix of both as separate audio files.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the beat audio array directly to a file.
    beat_file_path = os.path.join(output_dir, beat_output_file)
    torchaudio.save(beat_file_path, torch.tensor(beat_audio_array).unsqueeze(0), sample_rate=sr)

    # Copy the original voice (vocal) file to the output directory.
    voice_dest_path = os.path.join(output_dir, voice_output_file)
    shutil.copy(voice_audio_path, voice_dest_path)

    # Load both audio files for combining
    voice_segment = AudioSegment.from_file(voice_dest_path)
    beat_segment = AudioSegment.from_file(beat_file_path)
    duration = min(len(voice_segment), len(beat_segment))
    voice_segment = voice_segment[:duration]
    beat_segment = beat_segment[:duration]

    # Overlay (mix) the two audio segments
    combined = voice_segment.overlay(beat_segment)
    mix_file_path = os.path.join(output_dir, mix_output_file)
    combined.export(mix_file_path, format="wav")

    print(f"Voice track saved to: {voice_dest_path}")
    print(f"Beat track saved to: {beat_file_path}")
    print(f"Final mix saved to: {mix_file_path}")


# ----------------------------
# 7. Main Pipeline
# ----------------------------
def main_pipeline():
    music_dir = "downloaded_music"
    sep_dir = "separated_audio"

    # STEP 1: Download a sample music file.
    sample_url = "https://www.youtube.com/watch?v=iDTRkMbRPx8"
    print("Downloading music...")
    download_music_from_youtube(sample_url, output_dir=music_dir)

    # STEP 2: Separate audio into stems.
    downloaded_files = glob.glob(os.path.join(music_dir, "*.mp3"))
    if not downloaded_files:
        print("No downloaded files found. Exiting.")
        return

    for file in downloaded_files:
        print(f"Separating audio for {file} ...")
        separate_audio_spleeter(file, output_dir=sep_dir)

    # STEP 3: Prepare dataset.
    print("Preparing dataset...")
    dataset = VoiceBeatDataset(separated_dir=sep_dir)
    if len(dataset) == 0:
        print("No valid data found in separated audio. Exiting.")
        return

    # STEP 4: Train the model.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = UNetBeatGenerator()
    print("Training the model (this may take some time)...")
    model = train_model(model, dataset, num_epochs=500, batch_size=8, learning_rate=1e-4, device=device)

    # STEP 5: Inference – generate beat for one vocal sample.
    test_vocal = dataset.vocal_files[0]
    print(f"Generating beat for {test_vocal} ...")
    generated_beat, sr = generate_beat(model, test_vocal, device=device,
                                       target_mean=dataset.mean, target_std=dataset.std)

    # STEP 6: Save the beat, voice, and final mix as separate files.
    combine_voice_and_beat(test_vocal, generated_beat, sr)


if __name__ == "__main__":
    main_pipeline()

