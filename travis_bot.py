import json
from mood_keywords import keywords

# Load the songs database
with open("songs.json") as f:
    songs = json.load(f)

# Greeting
print("🎧 Welcome to the Travis Scott bot")
print("Tell me how you’re feeling, and I’ll find a Travis Scott song for that vibe.")
print("You can also optionally name an album (e.g., Rodeo, UTOPIA, Astroworld).")

# User input
user_input = input("What's your mood? (e.g., sad, party, chill): ").strip().lower()
album_input = input("Optional: Pick a specific album (or leave blank): ").strip().lower()


# Match moods based on user input
matched_moods = []
for mood, words in keywords.items():
    if any(word in user_input for word in words):
        matched_moods.append(mood)

# Get valid albums from the database
all_albums = set(song["album"] for song in songs)

# Handle non-existent album
if album_input and album_input not in all_albums:
    print(f"❌ The album '{album_input}' doesn't exist in the database.")
    print("Available albums are: Owl Pharaoh, Days Before Rodeo, Rodeo, Birds in the Trap Sing McKnight, ASTROWORLD, JACKBOYS, UTOPIA, JACKBOYS 2")
else:
    # Filter songs based on mood and album
    recommendations = [
        song["title"] for song in songs
        if (not album_input or song["album"] == album_input)
        and any(m in song["mood"] for m in matched_moods)
    ]

    if matched_moods:
        if recommendations:
            print("\n🎵 You should listen to:")
            for rec in recommendations:
                print("- " + rec)
        else:
            if album_input:
                print(f"😕 No {', '.join(matched_moods)} songs found in the album '{album_input}'.")
            else:
                print("😕 No Travis songs match that vibe. Try another mood.")
    else:
        print("❓ ❌ I didn’t catch a clear mood. Try saying something like 'I want songs for a party playlist!' or 'I feel sad 😕'.")
