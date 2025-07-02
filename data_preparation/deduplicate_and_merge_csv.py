import csv
import sys
from collections import OrderedDict

def clean_song_name(raw_name):
    """Normalize song name string to avoid duplicates due to formatting differences."""
    return raw_name.strip().strip('"')

def deduplicate_csv(input_path, output_path):
    # Stores unique song rows by 'Song' field
    song_map = OrderedDict()

    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames or []

        for row in reader:
            song_name = clean_song_name(row["Song"])
            if song_name not in song_map:
                song_map[song_name] = row
            else:
                # Merge fields from duplicate into original if missing
                existing = song_map[song_name]
                for key in ["Mood", "Genre", "Instruments"]:
                    if not existing.get(key, "").strip() and row.get(key, "").strip():
                        existing[key] = row[key]

    # Write back deduplicated rows
    with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(song_map.values())

    print(f"✅ Cleaned CSV written to: {output_path}")

# Example usage
if __name__ == "__main__":
    deduplicate_csv("/selim/separated_old/htdemucs/musical_analysis_complete.csv",
                    "/selim/separated_old/htdemucs/musical_analysis_complete1.csv")
