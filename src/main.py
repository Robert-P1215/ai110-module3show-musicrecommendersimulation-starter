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

    # Distinct user preference profiles
    user_profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    }

    # Adversarial / edge-case profiles designed to stress-test the scoring logic
    edge_case_profiles = {
        "Conflicting Preferences (high energy, sad mood)": {
            "genre": "classical", "mood": "sad", "energy": 0.9
        },
        "Out-of-Range Energy (> 1.0)": {
            "genre": "pop", "mood": "happy", "energy": 1.5
        },
        "Negative Energy": {
            "genre": "rock", "mood": "intense", "energy": -0.5
        },
        "Nonexistent Genre/Mood": {
            "genre": "vaporwave", "mood": "euphoric", "energy": 0.5
        },
        "Acoustic Lover Wanting Metal": {
            "genre": "metal", "mood": "intense", "energy": 0.95, "likes_acoustic": True
        },
    }

    for profile_name, user_prefs in {**user_profiles, **edge_case_profiles}.items():
        print(f"\n=== {profile_name} ===")
        print(f"User profile: {user_prefs}")
        print("\nTop recommendations:\n")
        try:
            recommendations = recommend_songs(user_prefs, songs, k=5)
        except Exception as exc:
            print(f"   ERROR: {type(exc).__name__}: {exc}")
            continue
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} (by {song['artist']}) - Score: {score:.2f}")
            print(f"   Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
