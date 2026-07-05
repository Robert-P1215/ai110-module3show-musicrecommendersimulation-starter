"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ImportError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nUser profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print("\nTop recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} (by {song['artist']}) - Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
