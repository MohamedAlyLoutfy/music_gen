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

def clean_json_response(content):
    """Extract and return first JSON object from a string (removes markdown code blocks)"""
    match = re.search(r"{.*?}", content, re.DOTALL)
    if match:
        return match.group(0).strip()
    return content.strip()

def query_song_metadata(song_name):
    prompt = f"""You are a music expert. For the song "{song_name}", respond in the following JSON format:

{{
  "song_name": "{song_name}",
  "mood": "",
  "instruments": "",
  "genre": ""
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
        print(f"content: {cleaned}")
        return json.loads(cleaned)

    except Exception as e:
        raise RuntimeError(f"Error querying metadata for '{song_name}': {e}")

def update_csv_with_metadata(input_csv_path, output_csv_path):
    processed_songs = set()

    # Read output file to get songs that already have genre filled
    if os.path.exists(output_csv_path):
        with open(output_csv_path, mode='r', encoding='utf-8') as outfile:
            reader = csv.reader(outfile)
            headers = next(reader)
            genre_index = headers.index("genre") if "genre" in headers else -1

            for row in reader:
                if row and genre_index >= 0 and row[0] and row[genre_index].strip():
                    processed_songs.add(row[0].strip())

    # Open files
    with open(input_csv_path, mode='r', encoding='utf-8') as infile, \
         open(output_csv_path, mode='a', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        input_headers = next(reader)
        full_headers = input_headers + ['mood', 'instruments', 'genre']

        writer = csv.writer(outfile)

        # Write headers if file is empty
        if os.stat(output_csv_path).st_size == 0:
            writer.writerow(full_headers)

        for row in reader:
            raw_name = row[0].strip()
            if raw_name in processed_songs:
                print(f"✅ Skipping (already has genre): {raw_name}")
                continue

            # Extract song name after the first dash
            parts = raw_name.split('-', 1)
            song_name = parts[1].strip() if len(parts) > 1 else raw_name

            print(f"🔍 Processing: {song_name}")

            try:
                metadata = query_song_metadata(song_name)
                row += [metadata["mood"], metadata["instruments"], metadata["genre"]]
                writer.writerow(row)
                outfile.flush()
                time.sleep(1.5)
            except Exception as e:
                print(f"❌ {e}")
                print("🛑 Stopping script due to error.")
                break

    print(f"\n✅ Done. Results written to: {output_csv_path}")

# Example usage
if __name__ == "__main__":
    update_csv_with_metadata('/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_201.csv', '/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_filled.csv')
