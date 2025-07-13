import os
import argparse
import torch
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--melody", type=str, required=True,
                        help="Path to input vocal .wav file (must be 32kHz mono)")
    parser.add_argument("--description", type=str, required=True,
                        help="Text prompt for generation, e.g. 'disco, upbeat'")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="Folder to save the generated audio")
    parser.add_argument("--duration", type=int, default=30,
                        help="Duration of output audio in seconds")

    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(args.output_dir, exist_ok=True)

    # Load model from checkpoint directory (automatically finds latest checkpoint)
    # print("🔁 Loading model...")
    # model = MusicGen.get_pretrained(args.ckpt)
    # model.set_generation_params(duration=args.duration)
    # model.to(device)
    # Load the melody pretrained model
    model = MusicGen.get_pretrained("melody")
    model.set_generation_params(duration=args.duration)  # adjust duration as needed

    # Load your checkpoint and apply weights to lm
    print("Loading fine-tuned checkpoint...")
    # ckpt = torch.load(args.ckpt, map_location=device)
    # if "model" not in ckpt:
    #     raise RuntimeError("Checkpoint missing 'model' key.")
    # model.lm.load_state_dict(ckpt["model"])
    model.lm.eval()
    model.lm.eval().to(device)

    # Load melody (vocal track)
    print(f"🎧 Loading melody from: {args.melody}")
    melody, sr = torchaudio.load(args.melody)
    if sr != 32000:
        raise ValueError(f"Expected 32kHz input audio, but got {sr}")
    melody = melody.mean(dim=0, keepdim=True).to(device)  # Convert to mono if needed

    # Run generation
    print("🎶 Generating audio with conditioning...")
    with torch.no_grad():
        generated_audio = model.generate_with_chroma(
            descriptions=[args.description],
            melody_wavs=melody,
            melody_sample_rate=32000
        )

    # Save result
    output_path = os.path.join(args.output_dir, "generated_output.wav")
    audio_write(output_path.replace(".wav", ""), generated_audio[0].cpu(), model.sample_rate, strategy="loudness")

    print(f"✅ Done! Output saved to: {output_path}")


if __name__ == "__main__":
    main()
