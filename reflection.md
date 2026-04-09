# Profile Comparison Reflections

---

## High-Energy Pop vs. Chill Lofi

These two profiles are essentially opposites and the results show it clearly. The pop profile surfaces bright, fast, produced tracks while the lofi profile surfaces slow, quiet, acoustic-leaning ones. What makes this comparison interesting is that both profiles scored their top results nearly identically — around 5.9 out of 6 — which means the scoring is working symmetrically. High energy is rewarded for high-energy users and penalized for low-energy users in equal measure. The system does not have a hidden preference for one end of the spectrum.

---

## Chill Lofi vs. Deep Intense Rock

The lofi profile got three songs from its own genre in the top three. The rock profile got one. That gap is entirely a catalog problem — there are three lofi songs and only one rock song. The scoring logic is the same for both users, but the lofi user benefits from having more options to compete among. This is the clearest example of catalog bias in the system. It is not that the rock user is being treated unfairly by the math — it is that the data was not built with them equally in mind.

---

## Deep Intense Rock vs. EDGE: Sad but High-Energy

Both profiles want high energy. The rock profile gets songs that actually feel high energy. The sad-but-high-energy blues profile gets Rainy Season — a slow, melancholic track — ranked first, because the genre and mood labels matched perfectly and outweighed the energy mismatch. The difference between these two outputs explains why label-matching and feel-matching are not the same thing. The rock profile asked for something and got it. The blues profile asked for something contradictory and the system picked the label side of the contradiction rather than the numerical side.

---

## EDGE: Genre Not in Catalog vs. EDGE: All Mid-Range Values

Both of these profiles get no genre bonus at all — one because the genre does not exist in the catalog, the other because the genre match happens to score poorly against mid-range energy. The missing-genre profile (bossa nova) actually does well because its mood and energy targets land near Jazz and Lofi songs that feel right. The mid-range profile struggles more because 0.5 energy sits in a gap between two clusters in the catalog — most songs lean clearly low or clearly high. Neither profile crashes the system, but the mid-range user consistently gets recommendations that feel less satisfying, which reveals that the catalog itself is polarized in a way that disadvantages users with moderate tastes.

---

## Why Gym Hero Keeps Showing Up for Happy Pop Users

Gym Hero is a pop song, so it earns the full genre bonus. Its energy is 0.93 — very close to what a high-energy pop user wants — and its valence is high, meaning it sounds bright and positive. On paper, almost everything about it matches a happy pop profile except the mood label says "intense" instead of "happy." That one label difference costs it 1.0 point, which is why it ranks second rather than first. But to a real listener, "intense pop" and "happy pop" can feel quite different — one is a workout track, the other is a feel-good song. The system sees the numbers and the genre and thinks they are almost the same. A human ear knows they are not.
