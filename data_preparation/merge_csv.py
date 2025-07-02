import pandas as pd

# List of CSV file paths
csv_files = [
    "/home/selim/Downloads/musical_analysis_moh(in).csv",
    "/media/selim/New Volume/MusicGen/musical_analysis_complete1.csv",
    "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis.csv",
    # add more files as needed
]

# Read and concatenate all CSV files
combined_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Save to a new CSV file
path = "/media/selim/New Volume/MusicGen/metadata.csv"
combined_df.to_csv(path, index=False)

print(f"CSV files merged successfully into '{path}'")
