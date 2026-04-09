from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with correctly typed values."""
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return total (0–6) and reason list."""
    score = 0.0
    reasons = []

    # Genre match — halved from 2.0 to 1.0 (experiment: reduce filter bubble dominance)
    if song["genre"] == user_prefs["genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    # Mood match — secondary categorical signal
    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity — doubled from ×1.5 to ×3.0 (experiment: audio feel over label)
    energy_score = (1 - abs(song["energy"] - user_prefs["energy"])) * 3.0
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f}/3.00)")

    # Valence similarity — separates bright from dark tracks
    valence_score = (1 - abs(song["valence"] - user_prefs["valence"])) * 1.0
    score += valence_score
    reasons.append(f"valence similarity ({valence_score:.2f}/1.00)")

    # Acousticness similarity — supporting feature
    acoustic_score = (1 - abs(song["acousticness"] - user_prefs["acousticness"])) * 0.5
    score += acoustic_score
    reasons.append(f"acousticness similarity ({acoustic_score:.2f}/0.50)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top k sorted by score descending."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return ranked[:k]
