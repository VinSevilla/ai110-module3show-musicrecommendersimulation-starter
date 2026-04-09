"""
Command line runner for the Music Recommender Simulation.

Runs multiple user profiles — including normal and adversarial edge cases —
to evaluate how the scoring logic behaves across different inputs.
"""

from recommender import load_songs, recommend_songs


PROFILES = [
    # --- Standard profiles ---
    {
        "label":        "High-Energy Pop",
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.85,
        "valence":      0.82,
        "acousticness": 0.10,
    },
    {
        "label":        "Chill Lofi",
        "genre":        "lofi",
        "mood":         "chill",
        "energy":       0.38,
        "valence":      0.58,
        "acousticness": 0.80,
    },
    {
        "label":        "Deep Intense Rock",
        "genre":        "rock",
        "mood":         "intense",
        "energy":       0.92,
        "valence":      0.45,
        "acousticness": 0.08,
    },
    # --- Adversarial / edge case profiles ---
    {
        "label":        "EDGE: Conflicting Mood vs Energy (sad but high-energy)",
        "genre":        "blues",
        "mood":         "sad",
        "energy":       0.95,   # blues catalog has low energy — genre match will win
        "valence":      0.20,
        "acousticness": 0.75,
    },
    {
        "label":        "EDGE: Genre That Doesn't Exist in Catalog",
        "genre":        "bossa nova",  # no match in CSV — categorical score always 0
        "mood":         "relaxed",
        "energy":       0.40,
        "valence":      0.70,
        "acousticness": 0.85,
    },
    {
        "label":        "EDGE: All Mid-Range Numerical Values (0.5 across the board)",
        "genre":        "ambient",
        "mood":         "focused",
        "energy":       0.50,
        "valence":      0.50,
        "acousticness": 0.50,
    },
]


def print_results(label: str, user_prefs: dict, recommendations: list) -> None:
    print("\n" + "=" * 55)
    print(f"  {label}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 55)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{i}  {song['title']} by {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f} / 6.00")
        print(f"       Why:   {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        label = profile.pop("label")
        recommendations = recommend_songs(profile, songs, k=3)
        print_results(label, profile, recommendations)
        profile["label"] = label  # restore so PROFILES stays intact


if __name__ == "__main__":
    main()
