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
    # Remove Markdown code block markers and trim whitespace
    match = re.search(r"{.*}", content, re.DOTALL)
    if match:
        return match.group(0)
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
            model="gpt-4o",  # or "gpt-4o" if you have quota
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()
        cleaned_content = clean_json_response(content)
        print(f"content: {cleaned_content}")
        # Try to load the JSON response
        metadata = json.loads(cleaned_content)
        return metadata

    except json.JSONDecodeError as je:
        print(f"JSON error for '{song_name}': {je}")
    except Exception as e:
        print(f"Error for '{song_name}': {e}")

    return {
        "song_name": song_name,
        "mood": "error",
        "instruments": "error",
        "genre": "error"
    }

def update_csv_with_metadata(input_csv_path, output_csv_path):
    updated_rows = []

    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)

        if 'mood' not in headers:
            headers += ['mood', 'instruments', 'genre']
        updated_rows.append(headers)

        for row in reader:
            # Extract actual song name after first dash
            parts = row[0].split('-', 1)
            song_name = parts[1].strip() if len(parts) > 1 else row[0].strip()

            print(f"Processing: {song_name}")
            metadata = query_song_metadata(song_name)

            row += [metadata['mood'], metadata['instruments'], metadata['genre']]
            updated_rows.append(row)

            time.sleep(3)  # Respect rate limits

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(updated_rows)

    print(f"\n✅ Done! Updated CSV saved to: {output_csv_path}")
# Example usage
if __name__ == "__main__":
    update_csv_with_metadata('/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_201.csv', '/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_filled.csv')
