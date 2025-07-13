import csv
import os
import time
from openai import OpenAI
from dotenv import load_dotenv
import json
import re


# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(base_url="https://models.inference.ai.azure.com",api_key=os.getenv("GITHUB_AI_KEI"))

if not client.api_key:
    raise ValueError("OpenAI API key not found. Make sure it's set in the .env file.")

EXPECTED_HEADERS = ["Song", "BPM", "Key", "Instruments", "Mood", "Genre", "Loop files"]

def clean_json_response(content):
    match = re.search(r"{.*?}", content, re.DOTALL)
    if match:
        return match.group(0).strip()
    return content.strip()

def query_song_metadata(song_name):
    prompt = f"""You are a music expert. For the song "{song_name}", respond in the following JSON format:

{{
  "song_name": "{song_name}",
  "Mood": "",
  "Instruments": "",
  "Genre": ""
}}

Only respond with the JSON.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4o" if available
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content
        cleaned = clean_json_response(content)
        return json.loads(cleaned)

    except Exception as e:
        raise RuntimeError(f"Error querying metadata for '{song_name}': {e}")

def update_csv_with_metadata(input_csv_path, output_csv_path):
    # Read input CSV
    with open(input_csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        input_rows = list(reader)

    # Load existing output if present
    existing_rows = []
    existing_by_song = {}

    if os.path.exists(output_csv_path):
        with open(output_csv_path, mode='r', encoding='utf-8') as out:
            out_reader = csv.DictReader(out)
            existing_rows = list(out_reader)
            for row in existing_rows:
                existing_by_song[row["Song"].strip()] = row

    # Ensure all expected headers are present
    all_headers = list(EXPECTED_HEADERS)
    if existing_rows:
        for h in existing_rows[0].keys():
            if h not in all_headers:
                all_headers.append(h)

    # Build updated list
    updated_rows = []

    for row in input_rows:
        song = row["Song"].strip()

        # Merge with existing row if it exists
        existing_row = existing_by_song.get(song, {h: "" for h in all_headers})
        merged_row = {**existing_row, **row}

        if merged_row.get("Genre", "").strip():
            print(f"✅ Skipping (Genre already filled): {song}")
            updated_rows.append(merged_row)
            continue

        # Extract song name for query
        parts = song.split('-', 1)
        song_name = parts[1].strip() if len(parts) > 1 else song

        print(f"🔍 Processing: {song_name}")
        try:
            metadata = query_song_metadata(song_name)

            # Update the fields
            merged_row["Mood"] = metadata.get("Mood", "")
            merged_row["Instruments"] = metadata.get("Instruments", "")
            merged_row["Genre"] = metadata.get("Genre", "")

            print(f"✅ Updated: {song}")
            updated_rows.append(merged_row)
            time.sleep(1.5)
        except Exception as e:
            print(f"❌ {e}")
            print("🛑 Stopping script due to error.")
            break

    # Write entire updated list
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=all_headers)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"\n✅ Done. Output written to: {output_csv_path}")

# Example usage
if __name__ == "__main__":
    update_csv_with_metadata('/selim/separated_old/htdemucs/musical_analysis_201.csv',
                             '/selim/separated_old/htdemucs/musical_analysis_complete.csv')
