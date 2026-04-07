# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version of the simple music recommender revolves around only 5 features: genre, mood, energy, valence, and "acousticness". This is to reduce the complexity of the system by removing redundancy. For example, songs with high temp or "dancability" tend to have high energy so the they were removed. As far as the algorithm goes, it is broken into two main parts: categorically and numerically. The categorical part of the score is based on genre and mood, while the numerical part uses energy, valence, and acoustics to handle audio relevancy. Visually, this creates a nonlinear scoring system where preference is not determined by a "higher is better" approach, but rather recommends based on how closely a song is to the users personal preference score that initially is set by whatever signals the user gives you.

More specifically, this is what the system gets right. It is Preference-centered, not directional. It rewards closeness to a target rather than "more = better." A user who wants energy = 0.5 gets penalized equally for 0.2 and 0.8, that symmetry is correct for taste. It is also simple and interpretable. Every score is a plain number in [0, 1]. Easy to debug, easy to explain to a non-technical user. Some of the limitations are that it involves a lot of assumptions. For example, it assumes all differences are equally bad. It also Assumes the user knows their exact preference, which may result in a cold start problem.

Conceptually, building a profile of what someone likes, then finding things that match it how I feel this project reflects the core logic of most recommendation systems.

---

## How The System Works

Explain your design in plain language.
Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world recommenders like Spotify or Netflix work by building a profile of what a person likes and then finding content that matches it. They observe what users play, skip, and repeat. Over time they build a picture of your taste and use it to score every available option, ranking the closest matches first. My version prioritizes the same core loop.

My version of the simple music recommender characterizes a song using only 5 features: genre, mood, energy, valence, and "acousticness". This is to reduce the complexity of the system by removing redundancy. For example, songs with high temp or "dancability" tend to have high energy so the they were removed. As far as the algorithm goes, the 'Recommender' is broken into two main parts: categorically and numerically. The categorical part of the score is based on genre and mood, while the numerical part uses energy, valence, and acoustics to handle audio relevancy. Visually, this creates a nonlinear scoring system where preference is not determined by a "higher is better" approach, but rather recommends based on how closely a song is to the users personal preference score that initially is set by whatever signals the user gives you. It is Preference-centered, not directional. It rewards closeness to a target rather than "more = better." A user who wants energy = 0.5 gets penalized equally for 0.2 and 0.8, that symmetry is correct for taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Output

Running `python src/main.py` with the default pop/happy profile produces:

![Terminal output showing top 5 recommendations](Screenshot%202026-04-07%20at%2011.48.37%20AM.png)

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

The system considers five things about each song: its genre, its mood, how energetic it is, how positive it sounds, and how acoustic or produced it feels.

It compares those five things against what the user told it they prefer. Two of those comparisons are simple yes-or-no checks, so either the song's genre matches the user's favorite genre, or it doesn't. Same goes for mood. If it matches, the song gets bonus points. If it doesn't, it gets nothing.
The other three: energy, positivity, and acousticness are numerically scored. If the user wants high-energy music and a song is very close to that target, it scores near-perfectly for that feature. The further a song drifts from the target in either direction, the lower it scores. There is no "higher is always better", a song that is too intense scores just as poorly as one that is too quiet, if the user's target is somewhere in the middle.

Each of the five features contributes a different amount to the final number. Genre match is worth the most because it is the strongest signal of what someone likes. Mood is worth less because the boundary is softer — two moods can feel similar even if they have different labels. Energy carries the most weight of the three numerical features because it has the widest range across the catalog and tends to determine whether a song feels right more than the others. Finally, all five contributions are added together into a single score between 0 and 6. The songs with the highest scores are the ones recommended.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:

- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:

- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:

- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
```
