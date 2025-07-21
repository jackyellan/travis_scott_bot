import json

with open("songs.json") as f:
    songs = json.load(f)

print("Welcome to the Travis Scott bot, your Travis Scott song recommender!")
print("I can suggest songs based on your mood or create a playlist for you.")

user_input = input("What's your mood? (e.g., sad, party, chill): ")
album_input = input("Optional: Want to pick a specific album? (Leave blank if not): ").strip()

keywords = {
    "party": ["party", "turn up", "lit", "hype"],
    "sad": ["sad", "cry", "breakup", "depressed"],
    "chill": ["chill", "relax", "smoke", "vibe"],
    "angry": ["mad", "angry", "rage"]
}

matched_moods = []

for mood, words in keywords.items():
    for word in words:
        if word in user_input.lower():
            matched_moods.append(mood)

#get list of valid albums
all_albums = set(song["album"] for song in songs)

# If user gave an album, validate it
if album_input and album_input not in all_albums:
    print(f"❌ The album '{album_input}' doesn't exist in the database.")
    print("Try one like: " + ", ".join(sorted(all_albums)))
else:
    #filter songs by mood and optional album
    recommendations = [
        song["title"] for song in songs
        if (not album_input or song["album"] == album_input)
        and any(m in song["mood"] for m in matched_moods)
    ]

    if matched_moods:
        if recommendations:
            print("🎵 You should listen to:")
            for rec in recommendations:
                print("- " + rec)
        else:
            if album_input:
                print(f"😕 There are no {', '.join(matched_moods)} songs in '{album_input}'.")
            else:
                print("😕 No Travis songs match that vibe. Try a different mood.")
    else:
        print("❓ I didn't catch a clear mood. Try saying something like 'I feel hype' or 'I’m sad'.")

