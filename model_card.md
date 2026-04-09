# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **Shazoo 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

This is a classroom project that recommends songs based on a user's taste profile. You give it a genre, a mood, and some numeric targets like energy level, and it finds the songs in the catalog that match most closely. It assumes the user already knows what they like and can describe it. This isn't meant for real users — it's just for learning how recommender systems work under the hood.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Basically the system looks at 5 things about each song — genre, mood, energy, valence (how positive it sounds), and acousticness (how produced vs. organic it sounds). It compares those to what the user said they want and gives each song a score out of 6.

Genre and mood are simple yes or no checks. If the song's genre matches yours, it gets +2 points. Mood match is +1. For energy, valence, and acousticness, it measures how close the song is to your target value — the closer, the more points. Energy carries the most weight because it has the widest range across songs.

The scores get added up and the songs are sorted from highest to lowest. Top results get returned with a plain explanation of why each one made the cut.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

The catalog has 18 songs total. The original dataset only had 10, so I added 8 more to cover genres and moods that were missing. Genres now include pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, hip-hop, classical, metal, r&b, folk, electronic, and blues. Moods range from happy and chill to angry, sad, and euphoric.

That said, 18 songs is still really small. Most genres only have one song, which means the recommender doesn't have much to choose from when a user's genre is a niche one. There's also no representation of things like Latin music, K-pop, or anything non-English. The data was made up by hand so it doesn't reflect how real listeners actually behave.

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

It works really well when the user's genre is well represented in the catalog. The Chill Lofi and High-Energy Pop profiles both gave results that felt spot on — like exactly what someone with those tastes would want. The scoring also handles opposite ends of the spectrum well, so a high-energy user and a low-energy user both get results that make sense without one side being favored over the other. Another thing that works well is the explanation — every recommendation tells you exactly why it was picked, which makes the whole thing feel transparent and easy to understand.

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

First thing I'd fix is how genre matching works. Right now rock and metal get treated like they have nothing in common, which is obviously wrong. Grouping genres into broader families like "guitar-based" or "electronic" would make the recommendations feel a lot more natural.

Second, I'd add some diversity enforcement so the top 5 results aren't all the same genre. If someone likes lofi there are only 3 lofi songs anyway, but in a bigger catalog this would become a real problem fast.

Third, I'd want the system to learn from what the user actually does. Like if they skip a song or replay it, instead of relying on a profile they fill out manually. That feedback loop is what makes real recommenders actually get better over time.

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

Building this made me realize how much work goes into something that feels simple on the surface. When Spotify says "because you listened to X," there's a whole scoring and ranking system behind that and even a basic version of it has a lot of edge cases and tradeoffs to think through.

The most surprising thing was how much the genre bonus dominated everything. I thought energy would be the most important factor since music "feeling" a certain way seems more personal than just a label, but the flat +2 for genre matching kept overriding everything else. It took actually running the experiments to see that.
