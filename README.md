# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube blend two main ideas: **content-based filtering**, which matches a user's stated or inferred taste against the actual attributes of an item (genre, tempo, mood), and **collaborative filtering**, which uses the behavior of *other* similar users (likes, skips, replays, playlist co-occurrence) to surface things a single user's own history wouldn't reveal. Production systems layer in context (time of day, session behavior) and learned embeddings on top of both. This simulation only implements the content-based half — there is no multi-user interaction data, so every recommendation is a direct comparison between a song's attributes and one user's declared preferences. Numeric features like energy are scored by *closeness* to the user's target value rather than by "higher is better," since a user asking for calm, low-energy music shouldn't get penalized for not returning the highest-energy song in the catalog.

**Data flow:** Input (user preferences) → Process (loop over every song in the catalog, scoring each one independently against the user profile) → Output (sort all scored songs and return the top `k`). Keeping scoring and ranking as separate steps means the per-song scoring logic can be tested and reused (e.g., for `explain_recommendation`) independently of how the final list is ordered or truncated.

**`Song` features used in this system:**
- `genre` — coarse style category (e.g., pop, lofi, jazz)
- `mood` — direct vibe label (e.g., happy, chill, intense, moody, relaxed, focused)
- `energy` — intensity, 0–1 scale
- `tempo_bpm` — beats per minute
- `valence` — musical positivity, 0–1 scale
- `danceability` — how suited the track is to movement, 0–1 scale
- `acousticness` — how acoustic vs. electronic/produced the track sounds, 0–1 scale

**`UserProfile` information stored:**
- `favorite_genre` — the genre the user prefers
- `favorite_mood` — the mood/vibe the user is looking for
- `target_energy` — the energy level the user wants (matched by closeness, not maximized)
- `likes_acoustic` — whether the user prefers acoustic-leaning or produced/electronic sound

### Algorithm Recipe

Each song is scored against the user's profile using additive point rules:

| Rule | Points | Logic |
|---|---|---|
| Genre match | **+2.0** | `song.genre == user.favorite_genre` |
| Mood match | **+1.0** | `song.mood == user.favorite_mood` |
| Energy closeness | **up to +1.0** | `1 - abs(song.energy - user.target_energy)` |
| Acousticness bonus | **+0.5** | `user.likes_acoustic` is `True` and `song.acousticness > 0.6` |

Max possible score is 4.5. Genre is weighted 2x mood because genre is the tighter identity signal in this catalog (12 distinct genres across 18 songs, mostly 1–2 songs each) while mood repeats more loosely (e.g., "chill" spans lofi, ambient, folk, and classical tracks that don't otherwise sound alike). Energy and acousticness act as continuous tiebreakers rather than primary axes.

**How songs are chosen:**
Every song in the catalog is scored independently against the user's profile (the *scoring rule*), then the full list is sorted by score and the top `k` songs are returned (the *ranking rule*). Keeping these two steps separate means the per-song scoring logic can be tested and reused (e.g., for `explain_recommendation`) independently of how the final list is ordered or truncated.

### Expected Biases

- **Over-prioritizing genre.** Because genre match is worth 2x mood, this system might surface a technically genre-matching song that feels like the wrong vibe, while passing over a strong mood match in a different genre — e.g., recommending an "intense" rock song to someone who wanted "intense" hip hop over a perfectly chill lofi track that matches their mood but not their genre.
- **Binary categorical matching.** Genre and mood scoring is all-or-nothing (1.0 or 0.0) — there's no partial credit for adjacent genres (e.g., "indie pop" vs "pop") or related moods (e.g., "chill" vs "relaxed"), so the system can rank a loosely-related song below one that happens to hit an exact string match.
- **Small, uneven catalog.** With only 18 songs and some genres/moods represented once, users with niche `favorite_genre`/`favorite_mood` combinations will get thin or repetitive top-`k` lists regardless of how well-tuned the weights are.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

## Sample Recommendation Output

```
Loaded songs: 18

User profile: genre=lofi, mood=chill, energy=0.4

Top recommendations:

1. Midnight Coding (by LoRoom) - Score: 3.98
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98)

2. Library Rain (by Paper Lanterns) - Score: 3.95
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.95)

3. Focus Flow (by LoRoom) - Score: 3.00
   Because: genre match (+2.0), energy closeness (+1.00)

4. Wildflower Road (by Sable & Wren) - Score: 1.95
   Because: mood match (+1.0), energy closeness (+0.95)

5. Spacewalk Thoughts (by Orbit Bloom) - Score: 1.88
   Because: mood match (+1.0), energy closeness (+0.88)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



