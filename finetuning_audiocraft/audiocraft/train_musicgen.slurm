#!/bin/bash

# === SLURM CONFIGURATION ===
#SBATCH --partition=slowlane                  # Use the slowlane partition
#SBATCH --account=student                     # Use the student account
#SBATCH --nodes=1                             # Request 1 node
#SBATCH --ntasks=1                            # Run a single task
#SBATCH --cpus-per-task=8                     # Allocate 8 CPU cores to the task
#SBATCH --mem=60G                             # Request up to 60 GB RAM (limit for student_project)
#SBATCH --gpus=A40:1                          # Request 1 A40 GPU
#SBATCH --time=0-12:00:00                     # Max run time: 12 hours
#SBATCH --output=%u_musicgen_%j.out           # Output file: e.g., gs113316_musicgen_123456.out
#SBATCH --job-name=musicgen-finetune          # Job name
#SBATCH --mail-user=selimelbindary@gmail.com  # Email for notifications
#SBATCH --mail-type=END,FAIL                  # Notify on end or failure

# === JOB EXECUTION ===

# Load environment
module purge
module load Miniconda3
source ${EBROOTMINICONDA3}/bin/activate
conda activate musicgen

# Move into scratch directory
cd $SCRATCH_DIR

# Copy dataset zip from BeeGFS to local scratch (if not already present)
echo "📦 Copying dataset to scratch..."
rsync -u /mnt/beegfs/home/gs113316/MusicGen_32_tokens.zip .

# Unzip tokenized dataset
echo "📂 Unzipping dataset..."
unzip -q MusicGen_32_tokens.zip

# Run training
echo "🚀 Starting training..."
cd /mnt/beegfs/home/gs113316/audiocraft

dora run solver=musicgen_vocal \
  dset.train.manifest=$SCRATCH_DIR/MusicGen_32_tokens/train/musicgen_tokens.pt \
  dset.train.num_samples=721 \
  dset.valid.manifest=$SCRATCH_DIR/MusicGen_32_tokens/val/musicgen_tokens.pt \
  dset.valid.num_samples=93

# Sync training outputs (checkpoints, logs) back to BeeGFS
echo "✅ Syncing outputs to BeeGFS..."
rsync -av $SCRATCH_DIR/outputs/ /mnt/beegfs/home/gs113316/experiments/audiocraft/outputs/
