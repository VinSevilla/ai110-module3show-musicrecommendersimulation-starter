# TA Guide: Music Recommender Simulation

Quick reference for helping students with this assignment. Not meant for students — this is your cheat sheet.

---

## Assignment Overview

**Goal:** Students build a small **content-based recommender system** for music. Given a catalog of songs (`data/songs.csv`) and a user's stated taste (`UserProfile`), the system scores every song and returns the top matches, along with a plain-language explanation of *why* each song was picked.

The assignment has two deliverables layered on top of the code:

1. **Working code** — implement song/user data structures, a scoring function, and ranking logic.
2. **Written reflection** — a `model_card.md` (industry-style ML documentation) plus a short `reflection.md`, where students explain their design choices and identify bias/fairness issues in their own system.

**What students should learn:**

- How real recommenders (Spotify, Netflix, YouTube) turn raw feature data into ranked suggestions.
- How to design a **weighted scoring function** that blends categorical and numerical signals.
- Why "closer to what the user wants" is a different (and often better) model than "bigger number = better."
- How small design decisions (feature weights, dataset composition) create bias — even with no ill intent.
- How to document a model's intended use, limitations, and risks (a "model card"), which is standard practice at real ML companies.

This is a **Module 3** assignment, so it assumes students already know Python basics (functions, classes, lists/dicts) and are being introduced to applied ML/recommender concepts conceptually, not mathematically.

---

## Core Concepts

### 1. Content-based filtering
**Simple terms:** Recommend items by comparing their *features* (genre, energy, mood...) directly to what the user says they like — no need for other users' data.
**Why it matters:** It's the easiest recommender to reason about and debug, and it's the foundation before students see collaborative filtering (which uses *other users'* behavior instead of item features) in later material.
**Takeaway:** If you can describe an item as a list of numbers/categories, and describe a user preference the same way, you can build a recommender by comparing the two lists.

### 2. Feature representation & normalization
**Simple terms:** Every song is reduced to a handful of numbers on the same 0–1 scale (energy, valence, acousticness) plus two category labels (genre, mood). `tempo_bpm` and `danceability` exist in the data but are deliberately *not* used in scoring — the student cut them because they're redundant with energy.
**Why it matters:** Mixing scales (e.g., comparing a 0–1 value directly to a 60–170 bpm value) silently breaks a scoring formula. Real feature engineering is as much about *removing* redundant signals as adding new ones.
**Takeaway:** Before combining features into one score, make sure they live on comparable scales.

### 3. Categorical vs. numerical scoring
**Simple terms:** Genre and mood are yes/no checks (bonus points if they match exactly). Energy, valence, and acousticness are scored by *distance* — how close the song's number is to the user's target number.
**Why it matters:** Real-world attributes aren't all the same "shape." Some are labels (can't be "70% metal"), others are continuous (energy can be almost right). Treating them differently is intentional design, not an inconsistency.
**Takeaway:** Ask "is this attribute a category or a continuum?" before deciding how to score it.

### 4. "Closeness to target" vs. "higher is better"
**Simple terms:** The numeric part of the score is `1 - abs(song_value - user_target)`. A user who wants energy = 0.5 is equally penalized by a song at 0.2 or 0.8.
**Why it matters:** This is the single most important conceptual idea in the assignment. Naive implementations often assume "more energy = better," which is wrong for taste — a chill-lofi listener does *not* want the highest-energy song in the catalog.
**Takeaway:** Preference modeling is about matching a target, not maximizing a value. This shows up constantly in ML (e.g., regression toward a target vs. classification "pick the max").

### 5. Weighted linear scoring
**Simple terms:** Each feature's contribution gets multiplied by a weight before being summed (`genre: 1.0, mood: 1.0, energy: ×3.0, valence: ×1.0, acousticness: ×0.5`) — see [src/recommender.py:74-97](src/recommender.py#L74-L97).
**Why it matters:** Weights encode *business/design opinions* about which signals matter most. Changing a single weight can flip which songs win — see the model card's discussion of the genre-weight experiment (2.0 → 1.0) and the energy-weight experiment (1.5 → 3.0).
**Takeaway:** A scoring formula is never "neutral" — every weight is a value judgment, and tuning it is a real, ongoing part of building ML products.

### 6. Ranking / top-k selection
**Simple terms:** Score every candidate, sort descending, take the first `k`.
**Why it matters:** This "score everything, then sort" pattern is the backbone of nearly all ranking systems (search results, ad ranking, feeds).
**Takeaway:** Separate *scoring* (how good is this one item) from *ranking* (how do all items compare) — they're different responsibilities and should be different functions/tests.

### 7. Bias & fairness in recommenders
**Simple terms:** Because genre gets a flat match bonus, and some genres have only one song in the catalog, that lone song rockets to the top for anyone who likes that genre — regardless of whether it's actually a good match. This is a **filter bubble** in miniature.
**Why it matters:** This is the same failure mode as real platforms over-recommending within a narrow lane, or a single item dominating a sparse category. Bias here comes from the *interaction* of data sparsity + weighting, not from any single "buggy" line of code.
**Takeaway:** Bias audits require testing edge cases (sparse categories, conflicting preferences) — not just typical/expected inputs.

### 8. Model cards (responsible AI documentation)
**Simple terms:** A structured write-up — intended use, how it works, data, strengths, limitations/bias, evaluation, future work — that any ML team should produce for a model before it ships.
**Why it matters:** This mirrors real model cards used by Google, HuggingFace, and OpenAI. It's the industry answer to "how do we make sure someone understands what this model can/can't do before relying on it?"
**Takeaway:** Documenting limitations is not optional polish — it's a core deliverable of shipping a model responsibly.

---

## Implementation Walkthrough

### `data/songs.csv`
18 hand-authored songs (expanded from a 10-song starter set) spanning genres like pop, lofi, rock, ambient, jazz, synthwave, hip-hop, classical, metal, r&b, folk, electronic, and blues. Each row has `energy`, `valence`, `danceability`, `acousticness` on 0–1 scales and `tempo_bpm` in real BPM.

### `src/recommender.py` — the core logic, split into two parallel implementations
This file actually contains **two separate solutions to the same problem**, and it's important to know both exist:

1. **OOP path** ([Song](src/recommender.py#L4), [UserProfile](src/recommender.py#L21), [Recommender](src/recommender.py#L32) classes) — required by `tests/test_recommender.py`. In this repo, `Recommender.recommend()` and `explain_recommendation()` are **still stubs** (`return self.songs[:k]` / a placeholder string). This path was never finished.
2. **Functional path** ([load_songs](src/recommender.py#L48), [score_song](src/recommender.py#L69), [recommend_songs](src/recommender.py#L102)) — this is the one that's actually implemented and used by `main.py`:
   - `load_songs` reads the CSV and casts every field to the right type (`int`/`float`), returning a list of dicts.
   - `score_song` computes a single song's score (0–6 max) against a user-preference dict, returning `(score, reasons)` — the `reasons` list is what powers the human-readable explanation.
   - `recommend_songs` calls `score_song` on every song, sorts descending by score, and returns the top `k` as `(song, score, explanation)` tuples.

**Why this matters for you as a TA:** if a student says "my tests pass, I'm done," check *which* implementation they actually finished. It's easy to fully build the functional path (because `main.py` gives immediate visual feedback) while leaving the graded `Recommender` class untouched.

### `src/main.py`
Defines a list of `PROFILES` — three "normal" user profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three deliberate **edge cases**: conflicting mood/energy, a genre absent from the catalog, and an all-0.5 "average" user. Calls `recommend_songs` per profile and pretty-prints the top 3 with scores and explanations. This design — testing normal *and* adversarial inputs — is itself a good practice to point out to students.

### `tests/test_recommender.py`
Two tests against the **OOP path only** (`Recommender`, `Song`, `UserProfile`). Important gotcha (see Common Mistakes below): both tests currently pass even though `Recommender.recommend()` is an unimplemented stub, because the fixture's first song already happens to be pop/happy. The tests aren't actually verifying sorting logic.

### `conftest.py`
Adds the project root to `sys.path` so `from src.recommender import ...` resolves regardless of where `pytest` is invoked from.

### `model_card.md` / `reflection.md`
Written artifacts, not code. `model_card.md` follows a 9-section template (name, intended use, how it works, data, strengths, limitations/bias, evaluation, future work, personal reflection). `reflection.md` documents specific experiments comparing profiles (e.g., why "Gym Hero" keeps appearing for happy-pop users despite being labeled "intense").

---

## Common Student Mistakes

1. **Implementing only one of the two paths.** They finish `score_song`/`recommend_songs` (because `main.py` shows nice output) and never touch the `Recommender` class the tests grade.
   - *Why it happens:* the functional path gives instant visual gratification; the class stubs are easy to forget since nothing calls them by default.
   - *Symptom:* `pytest` passes, but a rubric checking `Recommender.recommend()` fails, or manual inspection shows it still returns `self.songs[:k]` unsorted.
   - *Fix:* Point them to both locations in [src/recommender.py](src/recommender.py) and ask them to make `Recommender.recommend()` call the same scoring logic (or vice versa — refactor `score_song` to be reusable by both).

2. **"Higher is better" instead of "closest to target."**
   - *Why it happens:* it's the more intuitive first instinct — "more energy points = more energy score."
   - *Symptom:* a user who wants low energy (chill/lofi) gets recommended the most intense songs in the catalog.
   - *Fix:* Have them print `song["energy"]` vs `user_prefs["energy"]` side by side for their top result. If the top song's energy is always the catalog max/min regardless of user target, this is the bug.

3. **Mixing unnormalized features into the score** (e.g., accidentally including `tempo_bpm` or `danceability` without scaling).
   - *Why it happens:* copy-pasting the energy/valence pattern without checking the scale of the new feature.
   - *Symptom:* scores wildly out of the expected 0–6 range, or one feature completely dominates the ranking no matter the weight given to it.
   - *Fix:* Check each raw feature is 0–1 before it enters a weighted sum.

4. **Tautological / weak tests.** Same trap as the starter `tests/test_recommender.py` — asserting on data that would pass even with zero real logic.
   - *Why it happens:* it's tempting to write a test that just checks "did it run and return the right shape" instead of "did it rank correctly."
   - *Symptom:* tests are green, but running `main.py` (or manual inspection) shows obviously wrong output.
   - *Fix:* Have students design a fixture where the *correct* answer and the *naive/broken* answer would produce different top results — e.g., put the best-matching song last in the input list, not first.

5. **Mutating shared state in a loop.** `main.py` does `profile.pop("label")` then restores it after use ([src/main.py:82-85](src/main.py#L82-L85)). Students copying this pattern elsewhere sometimes forget the restore step, or mutate a dict that's reused across iterations.
   - *Why it happens:* dicts are mutable and passed by reference; it's easy to not realize a "temporary" mutation persists.
   - *Symptom:* the second/third profile in a loop behaves as if a field is missing, or a `KeyError` appears on iteration 2 but not iteration 1.
   - *Fix:* Suggest copying the dict (`dict(profile)`) instead of popping/restoring in place.

6. **Import/path errors when running tests.**
   - *Why it happens:* running `pytest` from a subdirectory, or a missing/broken `conftest.py`.
   - *Symptom:* `ModuleNotFoundError: No module named 'src'` or `'recommender'`.
   - *Fix:* Confirm they're running `pytest` from the project root, and that `conftest.py` exists and inserts the root into `sys.path`.

7. **CSV type bugs.** Forgetting `int()`/`float()` casts, or a typo in a column name in `load_songs`.
   - *Why it happens:* `csv.DictReader` returns everything as strings by default; it's easy to forget one field.
   - *Symptom:* `TypeError: unorderable types` when sorting, or scores that silently compare as strings (`"0.9" > "0.85"` is actually `True` lexically here, so this can be sneaky — but `"0.2" > "0.1"` also works lexically for single digits, meaning the bug can hide until a two-digit or edge value exposes it).
   - *Fix:* Print `type(song["energy"])` — should be `float`, not `str`.

8. **Over-weighting a categorical match (filter bubble).** Genre weight too high compared to numerical features.
   - *Why it happens:* it feels intuitive that "matching genre" should dominate.
   - *Symptom:* the same one or two songs from a niche genre always rank #1 regardless of how well the numeric features actually match.
   - *Fix:* This isn't necessarily a "bug" — it's a design tradeoff worth discussing. Ask them to try lowering the genre weight and see if results feel more reasonable (this is literally the experiment documented in `model_card.md`).

9. **Not handling `k` larger than the catalog, or an empty catalog.**
   - *Why it happens:* students test only with the default `k=3` or `k=5` against an 18-song catalog and never try edge values.
   - *Symptom:* no crash (Python list slicing handles overflow gracefully) — but if a student adds validation logic expecting an exact-length list, an `IndexError` or wrong-length result can surface.
   - *Fix:* Ask "what happens if k=100?" as a quick check — comfortingly, `list[:100]` on a shorter list just returns what's available.

---

## Teaching Notes

**Q: "My tests pass, why are you saying I'm not done?"**
> Two separate implementations exist in this file — one using classes (`Recommender`), one using plain functions (`recommend_songs`). The tests only check the class version. Walk through `tests/test_recommender.py` with them and ask: "what does `Recommender.recommend()` currently return no matter what?" (Answer: just the first `k` songs, unsorted — it never even looks at the user profile.)

**Q: "Why does a song with energy 0.5 score badly when my target is exactly 0.5?"**
> That would actually be a bug worth investigating — at `song.energy == user.target`, `abs(diff)` should be 0, so the score contribution should be at its *maximum*. If it's scoring low, check the formula for a sign error or reversed subtraction.

**Q: "Why is Gym Hero always showing up for my happy-pop profile even though it's not that similar?"**
> Great question to bounce back at them — this is literally the scenario documented in `reflection.md`/`model_card.md`. Have them look at each individual feature score (genre, mood, energy, valence) rather than just the total, to see which single strong signal (usually genre + energy) is overriding everything else.

**Q: "How do I pick the 'right' weights?"**
> There isn't one. Weights encode opinions about what matters most for taste-matching, and the "right" answer depends on what behavior you want. Encourage them to try a few configurations and describe the *tradeoff* in the model card, rather than searching for a single correct number.

**Q: "What's the point of writing a model card? It's not code."**
> This is the part of the assignment that mirrors what real ML teams do before shipping a model — Google, HuggingFace, and others publish model cards publicly. The goal is forcing them to articulate what their system is good at, what it's bad at, and who could be hurt by trusting it — skills that matter more as models get more complex, not less.

**Useful analogies:**
- **Scoring as matchmaking, not leaderboard.** This is like a dating-app compatibility score, not a "best restaurant in town" ranking. A 70 bpm chill song isn't "worse" than a 150 bpm song — it's just aiming at a different target.
- **Filter bubble as "always recommending your hometown."** If a matchmaking app always puts people from your hometown at the top regardless of actual compatibility, that's what happens here when a genre has only one song — it wins by default, not by merit.
- **Weights as recipe proportions.** Too much of one ingredient (genre weight) drowns out the rest of the dish (numeric features), even if the other ingredients are individually well-measured.

---

## Debugging Checklist

Run through this before diving into a student's code:

**Environment / setup**
- [ ] Virtual environment activated? (`source .venv/bin/activate`)
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] Running commands from the **project root**, not a subfolder?
- [ ] `pytest` run from root so `conftest.py`'s `sys.path` insert applies?
- [ ] `python -m src.main` (module form) rather than `python src/main.py` if imports are relative to `src/`?

**Data loading**
- [ ] Does `load_songs("data/songs.csv")` return 18 dicts, not an empty list or 0?
- [ ] Are numeric fields actually `float`/`int` (`type(song["energy"])`), not strings?
- [ ] Any typo in a CSV column name vs. the dict key used in code?

**Scoring logic**
- [ ] Print the individual score components (genre, mood, energy, valence, acousticness) for one song — do they sum to the reported total?
- [ ] Is the numeric scoring symmetric (`1 - abs(diff)`), not directional (`song_value * weight`)?
- [ ] Do all raw feature values feeding into a weighted sum live on a 0–1 scale?
- [ ] Try a user profile where you know the "obviously correct" top song by inspection — does the code agree?

**Ranking**
- [ ] Is the sort descending (`reverse=True`) and keyed on score, not title or id?
- [ ] Does the top result change sensibly when you flip a user's target from 0.1 to 0.9?

**Tests**
- [ ] Which implementation (`Recommender` class vs. functional `recommend_songs`) do the tests actually cover?
- [ ] Would the test still pass if you replaced the real logic with `return self.songs[:k]`? If yes, the test isn't validating anything meaningful.

**Bias / edge cases**
- [ ] What happens with a genre that doesn't exist in the catalog at all?
- [ ] What happens with conflicting preferences (e.g., wants high energy but favorite genre/mood is typically low-energy)?
- [ ] Does one genre with very few songs dominate results unfairly?

---

## Real-World Connections

- **Spotify Discover Weekly / Daily Mixes** and **YouTube "Up Next"** use the same core loop — build a taste profile from behavior, score the catalog, rank, and surface the top matches. This assignment's `UserProfile` stands in for what those systems infer from listening history instead of a manual form.
- **Amazon "customers also bought" / "similar items"** and **Netflix content-based signals** are content-based filtering in the same sense as this assignment (before being blended with collaborative signals).
- **Search and ad ranking systems** at any scale use "score everything, sort, take top-k" — the exact pattern in `recommend_songs`. Feature weighting there is a full engineering discipline (learning-to-rank, click-through-rate models) rather than hand-picked constants, but the underlying idea is identical.
- **Model cards** are a real industry artifact — Google's Model Cards framework and HuggingFace's model card format are the direct inspiration for `model_card.md`. Increasingly, publishing one is expected (and in some jurisdictions, required under emerging AI regulation) before a model ships.
- **A/B testing and offline weight tuning**, as documented in this project's genre/energy weight experiments, mirror how real recommender teams iterate — try a change, evaluate the effect on real outcomes, document why the change was kept or reverted.
- **Filter bubbles and popularity bias** are actively studied fairness problems in production recommenders (e.g., concerns about political content or genre lock-in on real platforms) — the sparse-genre bias found here is a small, safe sandbox version of a well-known real issue.

---

## Key Takeaways

Top 10 things students should walk away remembering:

1. A recommender is fundamentally just **score every candidate → rank → return top-k**. Everything else is refinement.
2. **"Closest to target" is not the same as "highest value."** Get this backwards and the whole system optimizes for the wrong thing.
3. **Feature weights are opinions, not facts.** Changing one number can completely change what the system feels like to use — that's a design decision, not just a bug to "get right."
4. **Data shape creates bias just as much as algorithm choice does.** A perfectly fair scoring formula can still produce unfair results if the underlying dataset is lopsided.
5. **Normalize before you combine.** Mixing features on different scales silently breaks weighted formulas.
6. **A green test suite doesn't mean correct behavior.** Always sanity-check that a test could actually fail if the logic were wrong.
7. **Keep one source of truth.** When a codebase has two parallel implementations of the same idea (as this one does), it's easy to finish one and forget the other — consolidate when possible.
8. **Mutating shared/passed-in data structures is a common source of subtle, hard-to-reproduce bugs.** Prefer copies over in-place mutation plus manual restoration.
9. **Document limitations, not just capabilities.** A model card that only lists strengths isn't finished — the valuable part is being honest about where and why the system fails.
10. **Tune by experimenting and recording results**, not by guessing at a "correct" formula once. Iteration with documentation is how real systems improve.
