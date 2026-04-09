# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

The biggest bias I found from testing is how the genre match bonus kind of creates a "filter bubble." Since it gives a flat +2.0 boost for an exact genre match, users almost always end up seeing songs only from their preferred genre at the top, even if other songs are actually a better fit based on their features. This becomes unfair for genres that only have one song in the dataset, like blues or classical, because that one song automatically ranks highest just for matching the label. Another issue is that the system treats genres as completely separate categories. For example, rock, metal, and synthwave might sound really similar in terms of energy or mood, but the model doesn't recognize that. So a rock listener would never get recommended a metal song, even if it's almost identical in feel. When I reduced the genre weight during testing, the recommendations got noticeably better. The system started suggesting songs across genres and focused more on how the music actually sounds instead of just relying on the label.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

I tested six profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and three edge cases (a sad-but-high-energy blues user, a user with no matching genre, and a perfectly average user). Chill Lofi and High-Energy Pop worked the best—the results actually felt like what someone with those tastes would want, mainly because there were enough songs in those genres to compete.
The most surprising case was Deep Intense Rock. A pop song (Gym Hero) kept ranking second because it matched the "intense" mood and had similar energy, even though it's not rock. This shows the system relies more on energy than genre, which can feel off to real users. The biggest issue showed up with the sad-but-high-energy profile. A slow blues song still ranked first just because it matched the genre and mood, even though the energy was completely wrong. So the system ends up rewarding labels over how the music actually feels, which would probably frustrate users.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps
