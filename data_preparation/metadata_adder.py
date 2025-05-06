import csv
import json
import re

# Replace this with the full text content you posted
text = """
Processing: ABBA - Dancing Queen (Official Music Video)
content: {
  "song_name": "ABBA - Dancing Queen (Official Music Video)",
  "mood": "joyful, nostalgic, energetic",
  "instruments": "piano, guitar, bass, drums, strings, synthesizer, vocals",
  "genre": "pop, disco"
}
Processing: ABBA - I Have A Dream (from ABBA In Concert)
content: {
  "song_name": "ABBA - I Have A Dream (from ABBA In Concert)",
  "mood": "uplifting, inspirational",
  "instruments": "vocals, piano, guitar, strings, flute",
  "genre": "pop"
}
Processing: ABBA - Knowing Me, Knowing You (Official Music Video)
content: {
  "song_name": "ABBA - Knowing Me, Knowing You (Official Music Video)",
  "mood": "melancholic, reflective",
  "instruments": "vocals, electric guitar, bass guitar, drums, synthesizer",
  "genre": "pop, disco"
}
Processing: ABBA - Lay All Your Love On Me (Official Lyric Video)
content: {
  "song_name": "ABBA - Lay All Your Love On Me (Official Lyric Video)",
  "mood": "passionate and dramatic",
  "instruments": "synthesizer, drum machine, bass guitar, vocals",
  "genre": "disco, pop"
}
Processing: ABBA - Mamma Mia (Official Music Video)
content: {
  "song_name": "ABBA - Mamma Mia (Official Music Video)",
  "mood": "upbeat, nostalgic",
  "instruments": "piano, guitar, bass, drums, synthesizer",
  "genre": "pop, disco"
}
Processing: ABBA - Money, Money, Money (Official Music Video)
content: {
  "song_name": "ABBA - Money, Money, Money (Official Music Video)",
  "mood": "dramatic, theatrical, ambitious",
  "instruments": "piano, strings, bass guitar, drums, vocals",
  "genre": "pop, disco"
}
Processing: ABBA - SOS (Official Music Video)
content: {
  "song_name": "ABBA - SOS (Official Music Video)",
  "mood": "melancholic yet uplifting",
  "instruments": "piano, guitar, bass, drums, synthesizer, vocals",
  "genre": "pop, pop rock"
}
Processing: ABBA - Super Trouper
content: {
  "song_name": "ABBA - Super Trouper",
  "mood": "uplifting, nostalgic",
  "instruments": "synthesizers, guitar, bass, drums, vocals",
  "genre": "pop, disco"
}
Processing: ABBA - Take A Chance On Me (Official Music Video)
content: {
  "song_name": "ABBA - Take A Chance On Me (Official Music Video)",
  "mood": "upbeat, hopeful",
  "instruments": "vocals, synthesizers, piano, bass guitar, drums",
  "genre": "Pop, Disco"
}
Processing: ABBA - The Winner Takes It All
content: {
  "song_name": "ABBA - The Winner Takes It All",
  "mood": "melancholic, reflective",
  "instruments": "piano, vocals, synthesizer, bass guitar, drums",
  "genre": "pop"
}
Processing: Adele - Easy On Me (Official Lyric Video)
content: {
  "song_name": "Adele - Easy On Me (Official Lyric Video)",
  "mood": "melancholic, reflective",
  "instruments": "piano, subtle orchestral strings",
  "genre": "pop, soul"
}
Processing: Adele - Hello
content: {
  "song_name": "Adele - Hello",
  "mood": "melancholic, reflective",
  "instruments": "piano, drums, strings, vocals",
  "genre": "soul, pop"
}
Processing: Adele - Hometown Glory (Official Music Video)
content: {
  "song_name": "Adele - Hometown Glory (Official Music Video)",
  "mood": "nostalgic, emotional",
  "instruments": "piano, strings, vocals",
  "genre": "soul, pop"
}
Processing: Adele - Love In The Dark
content: {
  "song_name": "Adele - Love In The Dark",
  "mood": "melancholic, heartfelt",
  "instruments": "piano, strings",
  "genre": "soul, pop"
}
Processing: Adele - Rolling in the Deep (Official Music Video)
content: {
  "song_name": "Adele - Rolling in the Deep (Official Music Video)",
  "mood": "empowering, intense",
  "instruments": "vocals, piano, drums, guitar, bass",
  "genre": "soul, pop, blues"
}
Processing: Adele - Send My Love (To Your New Lover)
content: {
  "song_name": "Adele - Send My Love (To Your New Lover)",
  "mood": "empowered, reflective",
  "instruments": "acoustic guitar, percussion, vocals",
  "genre": "pop"
}
Processing: Adele - Set Fire to the Rain
content: {
  "song_name": "Adele - Set Fire to the Rain",
  "mood": "emotional, powerful, dramatic",
  "instruments": "piano, drums, strings, vocals",
  "genre": "pop, soul"
}
Processing: Adele - Skyfall (Official Lyric Video)
content: {
  "song_name": "Adele - Skyfall (Official Lyric Video)",
  "mood": "dramatic, intense, cinematic",
  "instruments": "piano, strings, brass, percussion",
  "genre": "pop, orchestral, soundtrack"
}
Processing: Adele - Someone Like You (Official Music Video)
content: {
  "song_name": "Adele - Someone Like You (Official Music Video)",
  "mood": "melancholic, heartfelt, reflective",
  "instruments": "piano, vocals",
  "genre": "soul, pop"
}
Processing: Adele - When We Were Young
content: {
  "song_name": "Adele - When We Were Young",
  "mood": "nostalgic, emotional",
  "instruments": "piano, strings, drums, vocals",
  "genre": "soul, pop"
}
Processing: Avicii - Heaven (Tribute Video)
content: {
  "song_name": "Avicii - Heaven (Tribute Video)",
  "mood": "uplifting, emotional",
  "instruments": "synthesizers, piano, electronic drums, guitars",
  "genre": "progressive house, electronic"
}
Processing: Avicii - Hey Brother
content: {
  "song_name": "Avicii - Hey Brother",
  "mood": "uplifting, emotional",
  "instruments": "acoustic guitar, piano, brass, electronic synths, percussion",
  "genre": "country-inspired electronic dance music (EDM)"
}
Processing: Avicii - Levels
content: {
  "song_name": "Avicii - Levels",
  "mood": "uplifting, energetic",
  "instruments": "synthesizers, piano, electronic drums, bassline",
  "genre": "progressive house"
}
Processing: Avicii - Swedish House Mafia ft. John Martin - Don't You Worry Child (Official Video)
content: {
  "song_name": "Avicii - Swedish House Mafia ft. John Martin - Don't You Worry Child (Official Video)",
  "mood": "uplifting",
  "instruments": "synthesizers, piano, drums, vocals",
  "genre": "progressive house"
}
Processing: Avicii - The Days (Lyric Video)
content: {
  "song_name": "Avicii - The Days (Lyric Video)",
  "mood": "uplifting, nostalgic",
  "instruments": "guitar, piano, synthesizers, drums",
  "genre": "progressive house, pop"
}
Processing: Avicii - Waiting For Love
content: {
  "song_name": "Avicii - Waiting For Love",
  "mood": "uplifting, energetic",
  "instruments": "synthesizers, piano, bass, drums",
  "genre": "progressive house, electronic dance music"
}
Processing: Avicii - Wake Me Up (Lyrics)
content: {
  "song_name": "Avicii - Wake Me Up (Lyrics)",
  "mood": "uplifting, reflective",
  "instruments": "acoustic guitar, synthesizers, drum machine",
  "genre": "electronic dance music (EDM), folktronica"
}
Processing: Avicii - Without You “Audio” ft. Sandro Cavazza
content: {
  "song_name": "Avicii - Without You “Audio” ft. Sandro Cavazza",
  "mood": "uplifting, empowering",
  "instruments": "synthesizers, piano, electronic drums, vocals",
  "genre": "Progressive House, EDM"
}
Processing: Avicii - アヴィーチで有名な曲　6選　メドレー1
content: {
  "song_name": "Avicii - アヴィーチで有名な曲　6選　メドレー1",
  "mood": "uplifting, energetic",
  "instruments": "synthesizers, piano, electronic drums, vocal samples",
  "genre": "electronic dance music (EDM), progressive house"
}
Processing: Avicii vs Nicky Romero - I Could Be The One (Nicktim)
content: {
  "song_name": "Avicii vs Nicky Romero - I Could Be The One (Nicktim)",
  "mood": "uplifting, energetic",
  "instruments": "synthesizers, drum machine, piano",
  "genre": "progressive house"
}
Processing: Billie Eilish - BIRDS OF A FEATHER
content: {
  "song_name": "Billie Eilish - BIRDS OF A FEATHER",
  "mood": "melancholic",
  "instruments": "piano, strings, vocals",
  "genre": "indie pop"
}
Processing: Billie Eilish - Bellyache (Official Music Video)
content: {
  "song_name": "Billie Eilish - Bellyache (Official Music Video)",
  "mood": "haunting, introspective, melancholic",
  "instruments": "acoustic guitar, synthesizers, bass, subtle percussion",
  "genre": "indie pop, electronic"
}
Processing: Billie Eilish - CHIHIRO (Official Music Video)
content: {
  "song_name": "Billie Eilish - CHIHIRO (Official Music Video)",
  "mood": "",
  "instruments": "",
  "genre": ""
}
Processing: Billie Eilish - Happier Than Ever (Official Music Video)
content: {
  "song_name": "Billie Eilish - Happier Than Ever (Official Music Video)",
  "mood": "emotional, cathartic",
  "instruments": "guitar, drums, synthesizer, vocals",
  "genre": "pop, alternative/indie"
}
Processing: Billie Eilish - LUNCH (Official Music Video)
content: {
  "song_name": "Billie Eilish - LUNCH (Official Music Video)",
  "mood": "unknown",
  "instruments": "unknown",
  "genre": "unknown"
}
Processing: Billie Eilish - L’AMOUR DE MA VIE (Official Lyric Video)
content: {
  "song_name": "Billie Eilish - L’AMOUR DE MA VIE (Official Lyric Video)",
  "mood": "",
  "instruments": "",
  "genre": ""
}
Processing: Billie Eilish - Ocean Eyes (Official Music Video)
content: {
  "song_name": "Billie Eilish - Ocean Eyes (Official Music Video)",
  "mood": "dreamy, melancholic",
  "instruments": "vocals, synthesizer, percussion",
  "genre": "indie pop"
}
Processing: Billie Eilish - THE GREATEST (Official Lyric Video)
content: {
  "song_name": "Billie Eilish - THE GREATEST (Official Lyric Video)",
  "mood": "",
  "instruments": "",
  "genre": ""
}
Processing: Billie Eilish - WILDFLOWER
content: {
  "song_name": "Billie Eilish - WILDFLOWER",
  "mood": "unavailable",
  "instruments": "unavailable",
  "genre": "unavailable"
}
Processing: Billie Eilish - everything i wanted (Official Music Video)
content: {
  "song_name": "Billie Eilish - everything i wanted (Official Music Video)",
  "mood": "melancholic, introspective",
  "instruments": "piano, synthesizers, electronic beats",
  "genre": "electropop, alternative pop"
}
Processing: Cairokee - Ana Negm  كايروكي - أنا نجم
content: {
  "song_name": "Cairokee - Ana Negm  كايروكي - أنا نجم",
  "mood": "empowering",
  "instruments": "electric guitar, drums, bass, keyboard",
  "genre": "rock"
}
Processing: Cairokee - Basrah w Atoh كايروكي - بسرح واتوه
content: {
  "song_name": "Cairokee - Basrah w Atoh كايروكي - بسرح واتوه",
  "mood": "introspective",
  "instruments": "electric guitar, drums, bass guitar, synthesizer",
  "genre": "alternative rock"
}
Processing: Cairokee - Dinosaur (Official Music Video) ⧸ كايروكي - الديناصور
content: {
  "song_name": "Cairokee - Dinosaur (Official Music Video) ⧸ كايروكي - الديناصور",
  "mood": "rebellious, energetic",
  "instruments": "electric guitar, drums, bass, synthesizer, vocals",
  "genre": "rock, alternative"
}
Processing: Cairokee - James Dean (Official Music Video) كايروكي - جيمس دين
content: {
  "song_name": "Cairokee - James Dean (Official Music Video) كايروكي - جيمس دين",
  "mood": "rebellious",
  "instruments": "electric guitar, drums, bass, synthesizer, vocals",
  "genre": "alternative rock"
}
"""

# Parse the text into a dictionary of song metadata
def extract_metadata_from_text(text):
    entries = {}
    pattern = r'content:\s*({.*?})'
    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        try:
            json_str = match.group(1)
            data = json.loads(json_str)
            title = data["song_name"].strip()
            entries[title] = {
                "mood": data["mood"],
                "instruments": data["instruments"],
                "genre": data["genre"]
            }
        except json.JSONDecodeError:
            continue

    return entries

# Update the CSV
def update_csv_with_text(input_csv, output_csv, text):
    metadata_map = extract_metadata_from_text(text)
    updated_rows = []

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        if 'mood' not in headers:
            headers += ['mood', 'instruments', 'genre']
        updated_rows.append(headers)

        for row in reader:
            raw_name = row[0].strip()
            parts = raw_name.split('-', 1)
            song_key = parts[1].strip() if len(parts) > 1 else raw_name

            metadata = metadata_map.get(song_key)
            if metadata:
                row += [metadata['mood'], metadata['instruments'], metadata['genre']]
                print(f"✅ Matched and updated: {song_key}")
            else:
                row += ["", "", ""]
                print(f"⚠️ No match found: {song_key}")

            updated_rows.append(row)

    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(updated_rows)

    print(f"\n✅ Done. Output written to {output_csv}")

# Run the function
if __name__ == "__main__":
    update_csv_with_text('/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_201.csv', '/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_filled.csv', text)
