import csv
import json
import re

# Replace this with the full text content you posted
text = """
content: {
  "song_name": "Billie Eilish - CHIHIRO (Official Music Video)",
  "Mood": "Mysterious, Dreamy",
  "Instruments": "Synthesizers, Piano, Electronic Beats",
  "Genre": "Alternative Pop, Experimental"
}
✅ Skipping (already has genre): 234 - Billie Eilish - Happier Than Ever (Official Music Video)
✅ Skipping (already has genre): 235 - Billie Eilish - LUNCH (Official Music Video)
🔍 Processing: Billie Eilish - L’AMOUR DE MA VIE (Official Lyric Video)
content: {
  "song_name": "Billie Eilish - L’AMOUR DE MA VIE (Official Lyric Video)",
  "Mood": "Melancholic",
  "Instruments": "Synth, Piano, Soft Percussion",
  "Genre": "Indie Pop"
}
✅ Skipping (already has genre): 237 - Billie Eilish - Ocean Eyes (Official Music Video)
🔍 Processing: Billie Eilish - THE GREATEST (Official Lyric Video)
content: {
  "song_name": "Billie Eilish - THE GREATEST (Official Lyric Video)",
  "Mood": "Melancholic, Reflective",
  "Instruments": "Synthesizers, Percussion, Piano",
  "Genre": "Alternative/Indie Pop"
}
✅ Skipping (already has genre): 239 - Billie Eilish - WILDFLOWER
✅ Skipping (already has genre): 240 - Billie Eilish - everything i wanted (Official Music Video)
✅ Skipping (already has genre): 241 - Cairokee - Ana Negm  كايروكي - أنا نجم
✅ Skipping (already has genre): 242 - Cairokee - Basrah w Atoh كايروكي - بسرح واتوه
✅ Skipping (already has genre): 243 - Cairokee - Dinosaur (Official Music Video) ⧸ كايروكي - الديناصور
✅ Skipping (already has genre): 244 - Cairokee - James Dean (Official Music Video) كايروكي - جيمس دين
🔍 Processing: Cairokee - Kol Haga Bet'ady Studio Session كل حاجة بتعدي - كايروكي من الاستوديو
content: {
  "song_name": "Cairokee - Kol Haga Bet'ady Studio Session كل حاجة بتعدي - كايروكي من الاستوديو",
  "Mood": "Reflective, Uplifting",
  "Instruments": "Acoustic Guitar, Piano, Drums, Vocals",
  "Genre": "Alternative Rock, Acoustic"
}
🔍 Processing: Cairokee - Layla Studio Session ليلى - كايروكي من الاستوديو
content: {
  "song_name": "Cairokee - Layla Studio Session ليلى - كايروكي من الاستوديو",
  "Mood": "Melancholic and introspective",
  "Instruments": "Acoustic guitar, piano, percussion, vocals",
  "Genre": "Alternative rock, acoustic"
}
🔍 Processing: Cairokee - Roma كايروكي - روما
content: {
  "song_name": "Cairokee - Roma كايروكي - روما",
  "Mood": "Melancholic and introspective",
  "Instruments": "Electric guitar, drums, bass, synthesizers",
  "Genre": "Alternative rock"
}
🔍 Processing: Cairokee - Samurai كايروكي - ساموراي
content: {
  "song_name": "Cairokee - Samurai كايروكي - ساموراي",
  "Mood": "Energetic and rebellious",
  "Instruments": "Electric guitar, drums, bass, synthesizers",
  "Genre": "Alternative rock with Middle Eastern influences"
}
🔍 Processing: Cairokee - علي باب السيما - من مسلسل ريفو
content: {
  "song_name": "Cairokee - علي باب السيما - من مسلسل ريفو",
  "Mood": "Nostalgic, Reflective",
  "Instruments": "Electric Guitar, Drums, Bass, Keyboard",
  "Genre": "Alternative Rock, Indie"
}
🔍 Processing: Cairokee Ft. @saramoullablad5231  - Nefsy Ahbek  كايروكي مع سارة مول البلاد - نفسي احبك
content: {
  "song_name": "Cairokee Ft. @saramoullablad5231  - Nefsy Ahbek  كايروكي مع سارة مول البلاد - نفسي احبك",
  "Mood": "Emotional",
  "Instruments": "Acoustic guitar, Piano, Percussion",
  "Genre": "Arabic Rock"
}
🔍 Processing: Coldplay & The Chainsmokers  - Something Just Like This (Lyric)
content: {
  "song_name": "Coldplay & The Chainsmokers  - Something Just Like This (Lyric)",
  "Mood": "uplifting, nostalgic, romantic",
  "Instruments": "synthesizers, drum machine, piano, guitar, vocals",
  "Genre": "electropop"
}
🔍 Processing: Coldplay - A Sky Full Of Stars (Official Video)
content: {
  "song_name": "Coldplay - A Sky Full Of Stars (Official Video)",
  "Mood": "uplifting, euphoric",
  "Instruments": "piano, acoustic guitar, electronic beats, synthesizers",
  "Genre": "progressive house, pop-rock"
}
🔍 Processing: Coldplay - Adventure Of A Lifetime (Official Video)
content: {
  "song_name": "Coldplay - Adventure Of A Lifetime (Official Video)",
  "Mood": "uplifting, energetic",
  "Instruments": "guitar, bass, drums, synthesizers",
  "Genre": "Alternative rock, pop rock"
}
🔍 Processing: Coldplay - Hymn For The Weekend (Official Video)
content: {
  "song_name": "Coldplay - Hymn For The Weekend (Official Video)",
  "Mood": "uplifting, celebratory",
  "Instruments": "piano, guitar, percussion, brass, vocals",
  "Genre": "Pop rock, alternative rock"
}
🔍 Processing: Coldplay - Paradise (Official Video)
content: {
  "song_name": "Coldplay - Paradise (Official Video)",
  "Mood": "Uplifting, Emotional",
  "Instruments": "Piano, Strings, Synthesizers, Drums, Electric Guitar",
  "Genre": "Alternative Rock, Pop Rock"
}
🔍 Processing: Coldplay - The Scientist (Official 4K Video)
content: {
  "song_name": "Coldplay - The Scientist (Official 4K Video)",
  "Mood": "Melancholic, Reflective",
  "Instruments": "Piano, Guitar, Drums, Bass",
  "Genre": "Alternative Rock"
}
🔍 Processing: Coldplay - Viva La Vida (Official Video)
content: {
  "song_name": "Coldplay - Viva La Vida (Official Video)",
  "Mood": "Majestic, Uplifting, Reflective",
  "Instruments": "Strings, Percussion, Synthesizers, Piano",
  "Genre": "Alternative Rock, Baroque Pop"
}
🔍 Processing: Coldplay - WE PRAY (TINI Version) (Official)
content: {
  "song_name": "Coldplay - WE PRAY (TINI Version) (Official)",
  "Mood": "",
  "Instruments": "",
  "Genre": ""
}
🔍 Processing: Coldplay - Yellow (Official Video)
content: {
  "song_name": "Coldplay - Yellow (Official Video)",
  "Mood": "Melancholic, Romantic, Uplifting",
  "Instruments": "Electric guitar, Acoustic guitar, Bass guitar, Drums, Vocals",
  "Genre": "Alternative Rock, Post-Britpop"
}
🔍 Processing: Coldplay - feelslikeimfallinginlove (Official Lyric Visualiser)
content: {
  "song_name": "Coldplay - feelslikeimfallinginlove (Official Lyric Visualiser)",
  "Mood": "Romantic, Dreamy",
  "Instruments": "Synthesizers, Drums, Guitar",
  "Genre": "Alternative Pop, Synth-pop"
}
🔍 Processing: Ed Sheeran - 2step (feat. Lil Baby) - [Official Video]
content: {
  "song_name": "Ed Sheeran - 2step (feat. Lil Baby) - [Official Video]",
  "Mood": "Energetic",
  "Instruments": "Guitar, Synth, Drums",
  "Genre": "Pop, Hip-Hop"
}
🔍 Processing: Ed Sheeran - Azizam (Official Music Video)
content: {
  "song_name": "Ed Sheeran - Azizam (Official Music Video)",
  "Mood": "",
  "Instruments": "",
  "Genre": ""
}
🔍 Processing: Ed Sheeran - Bad Habits [Official Video]
content: {
  "song_name": "Ed Sheeran - Bad Habits [Official Video]",
  "Mood": "Energetic, Dark, Danceable",
  "Instruments": "Synthesizers, Drum Machine, Electric Guitar, Bass",
  "Genre": "Pop, Dance-Pop, Synth-Pop"
}
🔍 Processing: Ed Sheeran - Curtains [Official Video]
content: {
  "song_name": "Ed Sheeran - Curtains [Official Video]",
  "Mood": "Reflective, Emotional",
  "Instruments": "Acoustic Guitar, Piano, Drums, Strings",
  "Genre": "Pop"
}
🔍 Processing: Ed Sheeran - Eyes Closed [Official Video]
content: {
  "song_name": "Ed Sheeran - Eyes Closed [Official Video]",
  "Mood": "Melancholy, Reflective",
  "Instruments": "Acoustic guitar, Piano, Percussion, Strings",
  "Genre": "Pop"
}
🔍 Processing: Ed Sheeran - Shape of You (Official Music Video)
content: {
  "song_name": "Ed Sheeran - Shape of You (Official Music Video)",
  "Mood": "Playful, Romantic, Energetic",
  "Instruments": "Acoustic Guitar, Percussion, Synthesizers, Marimba-like Tones",
  "Genre": "Pop"
}
🔍 Processing: Ed Sheeran - Shivers [Official Video]
content: {
  "song_name": "Ed Sheeran - Shivers [Official Video]",
  "Mood": "Upbeat, Romantic, Energetic",
  "Instruments": "Guitar, Synthesizer, Drums, Bass",
  "Genre": "Pop"
}
🔍 Processing: Ed Sheeran - Thinking Out Loud (Official Music Video)
content: {
  "song_name": "Ed Sheeran - Thinking Out Loud (Official Music Video)",
  "Mood": "Romantic",
  "Instruments": "Guitar, Piano, Strings",
  "Genre": "Pop, Soul"
}
🔍 Processing: Ed Sheeran - Under the Tree (from “That Christmas”)
content: {
  "song_name": "Ed Sheeran - Under the Tree (from “That Christmas”)",
  "Mood": "Festive, Romantic",
  "Instruments": "Acoustic Guitar, Piano, Strings, Sleigh Bells",
  "Genre": "Pop, Christmas"
}
🔍 Processing: Ed Sheeran, Pokémon - Celestial [Official Video]
content: {
  "song_name": "Ed Sheeran, Pokémon - Celestial [Official Video]",
  "Mood": "uplifting",
  "Instruments": "acoustic guitar, piano, electronic beats, vocals",
  "Genre": "pop"
}
🔍 Processing: Lady Gaga & Bradley Cooper - Shallow (A Star is Born)
content: {
  "song_name": "Lady Gaga & Bradley Cooper - Shallow (A Star is Born)",
  "Mood": "Emotional, Introspective, Powerful",
  "Instruments": "Acoustic Guitar, Piano, Vocals",
  "Genre": "Pop, Country, Acoustic"
}
🔍 Processing: Lady Gaga - Abracadabra (Official Music Video)
content: {
  "song_name": "Lady Gaga - Abracadabra (Official Music Video)",
  "Mood": "N/A",
  "Instruments": "N/A",
  "Genre": "N/A"
}
🔍 Processing: Lady Gaga - Alejandro (Official Music Video)
content: {
  "song_name": "Lady Gaga - Alejandro (Official Music Video)",
  "Mood": "Melancholic, Dramatic",
  "Instruments": "Synthesizers, Electronic Beats, Strings, Percussion",
  "Genre": "Electropop, Synthpop"
}
🔍 Processing: Lady Gaga - Always Remember Us This Way (Lyrics)
content: {
  "song_name": "Lady Gaga - Always Remember Us This Way (Lyrics)",
  "Mood": "Emotional, Romantic, Nostalgic",
  "Instruments": "Piano, Acoustic Guitar, Vocals",
  "Genre": "Pop, Ballad"
}
🔍 Processing: Lady Gaga - Bad Romance (Official Music Video)
content: {
  "song_name": "Lady Gaga - Bad Romance (Official Music Video)",
  "Mood": "Dark, Dramatic, Empowering",
  "Instruments": "Synthesizers, Drum Machines, Electronic Beats, Vocals",
  "Genre": "Electropop, Dance-Pop"
}
🔍 Processing: Lady Gaga - Bloody Mary (Official Audio)
content: {
  "song_name": "Lady Gaga - Bloody Mary (Official Audio)",
  "Mood": "Dark, Mysterious, Haunting",
  "Instruments": "Synthesizers, Percussion, Bass, Vocal Harmonies",
  "Genre": "Electropop, Dark Pop"
}
🔍 Processing: Lady Gaga - Disease (Official Music Video)
content: {
  "song_name": "Lady Gaga - Disease (Official Music Video)",
  "Mood": "N/A",
  "Instruments": "N/A",
  "Genre": "N/A"
}
🔍 Processing: Lady Gaga - Judas (Official Music Video)
content: {
  "song_name": "Lady Gaga - Judas (Official Music Video)",
  "Mood": "Dramatic, Energetic, Dark",
  "Instruments": "Synthesizers, Drum Machines, Electric Guitar, Vocal Effects",
  "Genre": "Electropop, Dance-pop"
}
🔍 Processing: Lady Gaga - Poker Face (Official Music Video)
content: {
  "song_name": "Lady Gaga - Poker Face (Official Music Video)",
  "Mood": "Playful, Confident, Mysterious",
  "Instruments": "Synthesizer, Drum Machine, Electronic Beats, Vocals",
  "Genre": "Electropop, Dance-Pop"
}
🔍 Processing: Lady Gaga, Bruno Mars - Die With A Smile (Official Music Video)
content: {
  "song_name": "Lady Gaga, Bruno Mars - Die With A Smile (Official Music Video)",
  "Mood": "Uplifting and emotional",
  "Instruments": "Piano, guitar, drums, synthesizers, and orchestral elements",
  "Genre": "Pop with soul and electronic influences"
}
🔍 Processing: Queen - Another One Bites the Dust (Official Video)
content: {
  "song_name": "Queen - Another One Bites the Dust (Official Video)",
  "Mood": "Energetic",
  "Instruments": "Bass guitar, Electric guitar, Drums, Piano, Synthesizer, Vocals",
  "Genre": "Funk Rock"
}
🔍 Processing: Queen - Crazy Little Thing Called Love (Official Video)
content: {
  "song_name": "Queen - Crazy Little Thing Called Love (Official Video)",
  "Mood": "Playful, Energetic",
  "Instruments": "Guitar, Bass, Drums, Piano, Vocals",
  "Genre": "Rockabilly, Rock"
}
🔍 Processing: Queen - Don't Stop Me Now (Official Video)
content: {
  "song_name": "Queen - Don't Stop Me Now (Official Video)",
  "Mood": "Energetic, Uplifting",
  "Instruments": "Piano, Electric Guitar, Bass Guitar, Drums, Vocals",
  "Genre": "Rock"
}
🔍 Processing: Queen - Fat Bottomed Girls (Official Video)
content: {
  "song_name": "Queen - Fat Bottomed Girls (Official Video)",
  "Mood": "Energetic",
  "Instruments": "Electric guitar, Bass guitar, Drums, Vocals",
  "Genre": "Rock"
}
🔍 Processing: Queen - Killer Queen (Top Of The Pops, 1974)
content: {
  "song_name": "Queen - Killer Queen (Top Of The Pops, 1974)",
  "Mood": "Sophisticated, Playful",
  "Instruments": "Piano, Guitar, Bass, Drums, Vocals",
  "Genre": "Glam Rock, Art Rock"
}
🔍 Processing: Queen - Save Me (Official Video)
content: {
  "song_name": "Queen - Save Me (Official Video)",
  "Mood": "Melancholic, Reflective, Emotional",
  "Instruments": "Piano, Electric Guitar, Bass Guitar, Drums, Vocals",
  "Genre": "Rock, Ballad"
}
🔍 Processing: Queen - Somebody To Love (Official Video)
content: {
  "song_name": "Queen - Somebody To Love (Official Video)",
  "Mood": "Soulful, Emotional, Uplifting",
  "Instruments": "Vocals, Piano, Guitar, Bass, Drums",
  "Genre": "Rock, Gospel-inspired"
}
🔍 Processing: Queen - The Show Must Go On (Official Video)
content: {
  "song_name": "Queen - The Show Must Go On (Official Video)",
  "Mood": "Resilient, Emotional, Powerful",
  "Instruments": "Electric guitar, Synthesizer, Bass guitar, Drums, Piano, Vocals",
  "Genre": "Rock, Symphonic Rock"
}
🔍 Processing: Queen - You're My Best Friend (Official Video)
content: {
  "song_name": "Queen - You're My Best Friend (Official Video)",
  "Mood": "Warm, Joyful, Heartfelt",
  "Instruments": "Electric Piano, Bass Guitar, Electric Guitar, Drums, Vocals",
  "Genre": "Rock, Pop Rock"
}
🔍 Processing: Queen – Bohemian Rhapsody (Official Video Remastered)
content: {
  "song_name": "Queen – Bohemian Rhapsody (Official Video Remastered)",
  "Mood": "dramatic, emotional, theatrical",
  "Instruments": "piano, guitar, bass, drums, vocals",
  "Genre": "progressive rock, opera rock"
}
🔍 Processing: The Beatles - And I Love Her (Remastered 2009)
content: {
  "song_name": "The Beatles - And I Love Her (Remastered 2009)",
  "Mood": "Romantic",
  "Instruments": "Acoustic guitar, bass, claves, bongos",
  "Genre": "Pop, Ballad"
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
                "mood": data["Mood"],
                "instruments": data["Instruments"],
                "genre": data["Genre"]
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
    update_csv_with_text('/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_filled.csv', '/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs/musical_analysis_filled1.csv', text)
