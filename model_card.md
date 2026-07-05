# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch takes a small profile (favorite genre, favorite mood, and a target energy level) and picks the top 5 songs from a fixed catalog that best match it. It's a simple content-based recommender: it doesn't learn from behavior, it just compares stated preferences to song tags.

It assumes the user can describe their taste in three simple words/numbers, and that their taste actually exists somewhere in the catalog. It's built for classroom exploration — learning how scoring-based recommenders work — not for real listeners or a production music app.

**Intended use:** teaching/demo tool for understanding rule-based recommendation logic, testing how scoring weights affect rankings, and exploring bias/limitations of simple recommenders.

**Not intended for:** real-world music recommendations, any use involving real user data, or any claim that it "understands" music the way a person does.

---

## 3. How the Model Works  

Think of it like a checklist with points. For every song, VibeMatch asks three questions:

1. Does the song's genre match what the user said they like? If yes, +2 points.
2. Does the song's mood match? If yes, +1 point.
3. How close is the song's energy to the energy the user wants? The closer it is, the more points it gets (up to +1). If it's off by a lot, it gets close to 0.

There's also a small bonus: if the user says they like acoustic songs, and the song is actually acoustic, it gets +0.5 extra points.

Add all that up, and that's the song's score. VibeMatch does this for every song in the catalog, sorts them highest score first, and shows the top 5, along with a plain-English reason ("genre match," "mood match," "energy closeness") for why each one made the list.

The starter code only had placeholder functions — the actual scoring math, the CSV loading, and the "top 5, ranked" logic were built from scratch.

---

## 4. Data  

The catalog is `data/songs.csv` — 18 songs total. Each song has: title, artist, genre, mood, energy (0-1), tempo (bpm), valence, danceability, and acousticness.

There are 13 different genres, but most only appear once (rock, ambient, jazz, synthwave, indie pop, hip hop, metal, reggae, r&b). `lofi` shows up 3 times, and `pop`, `classical`, and `folk` show up twice each. Moods include happy, chill, intense, relaxed, moody, focused, romantic — 8 total, and most also appear only once or twice.

I didn't add or remove any songs — this is the dataset as given. Because it's so small, a lot of musical taste is missing: there's no rap/trap, no electronic/EDM, no world music, and energy levels have a literal gap between 0.55 and 0.75, so nobody who wants "moderately energetic" music is well represented (see Limitations below).

---

## 5. Strengths  

It works best for users with a clear, "extreme" taste that actually exists in the catalog — like someone who wants happy upbeat pop, or someone who wants chill low-energy lofi. For those profiles, the top picks line up with what you'd expect just by reading the song titles and moods.

The scoring correctly captures the intuitive idea that "more matching features = better fit" — a song matching genre AND mood AND energy always beats one matching only one of those. It also never crashes, even on weird or contradictory input, and it always explains its answer, which makes it easy to sanity-check.

For opposite profiles (like Chill Lofi vs. Deep Intense Rock), the recommendation lists don't overlap at all, which matches intuition — those are two very different listeners and they should get very different songs.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

### Discovered Weakness: An "Energy Gap" Filter Bubble

The 18-song catalog has an actual gap in its energy values — every song is either at or below 0.55 energy or at or above 0.75 energy, with nothing in between (`[..., 0.5, 0.55, 0.75, 0.76, ...]`). Because `score_song` scores energy closeness as `1 - abs(song_energy - user_energy)`, any user whose `target_energy` falls in that 0.55–0.75 "moderate" range (e.g. someone who wants mid-tempo, moderately energetic music) is structurally penalized: no song in the catalog can score above about 0.75–0.8 on energy closeness alone, no matter how well its genre or mood matches. This effectively creates a filter bubble that pushes moderate-energy users toward either the "chill" cluster or the "intense" cluster rather than surfacing anything in between, even though that preference is perfectly reasonable. A related, smaller bias comes from genre imbalance in the catalog (`lofi` appears 3 times, `pop`/`classical`/`folk` appear twice, while `rock`, `metal`, `jazz`, `hip hop`, `reggae`, and others each appear only once) — users whose favorite genre is one of those singleton genres get at most one genre-matched song, so the same track dominates rank 1 every time and the rest of their top-5 is filled by mood/energy matches from unrelated genres. Neither issue is a bug in the scoring formula itself; both stem from the training data's coverage rather than the math, but they mean the system's "personalization" is really only as diverse as whatever gaps exist in the 18-song catalog.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles Tested

I tested three "normal" taste profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) plus five adversarial/edge-case profiles (Conflicting Preferences, Out-of-Range Energy, Negative Energy, Nonexistent Genre/Mood, Acoustic Lover Wanting Metal — see below for their raw output). For each normal profile I looked at whether the top 5 songs actually matched the "vibe" a real listener would expect, and whether the explanation strings made sense in plain language.

**What surprised me:** "Gym Hero" (pop, intense mood, energy 0.93) kept showing up as a top-3 recommendation for almost every high-energy profile, even ones that weren't asking for pop or an "intense" mood. In plain terms: the system doesn't actually know what a song "feels like" — it just checks three yes/no/how-close boxes (genre, mood, energy) and adds up points. "Gym Hero" is one of only two pop songs, and it's also one of the most energetic songs in the whole catalog (0.93), so any user who wants "high energy" gets a big energy-closeness score for it even if they never said they wanted pop or "intense." It rides in on energy alone, not because the system understands it's a workout song. That's not a bug exactly — it's just a reminder that the score is an additive checklist, not real music understanding, and a small catalog means the same handful of extreme songs (highest energy, most common genre) reappear across many different profiles.

### Comparing Profile Pairs

- **High-Energy Pop vs. Chill Lofi:** These two are near-total opposites (energy 0.85 vs. 0.4, "happy" vs. "chill" mood), and the results reflect that cleanly — Pop's list is topped by upbeat, danceable tracks like "Sunrise City" and "Gym Hero," while Lofi's list is topped by quiet, low-tempo tracks like "Midnight Coding" and "Library Rain." This makes sense: the two profiles disagree on every single scored feature (genre, mood, and energy target), so their top picks should have almost no overlap, and they don't.

- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy (0.85 and 0.9), but the genre and mood differ (pop/happy vs. rock/intense). The lists share one song — "Gym Hero," a high-energy pop track that also carries an "intense" mood tag — while the rest of each top-5 diverges by genre. This makes sense: whenever a song happens to score well on the *shared* dimension (energy), it can leak into both lists even though the two personas want different genres. It shows the system rewards raw energy overlap even across otherwise different tastes.

- **Chill Lofi vs. Deep Intense Rock:** These are near-opposite on every axis (energy 0.4 vs. 0.9, chill vs. intense mood, lofi vs. rock genre), and their top-5 lists share zero songs. This is the expected/valid result — a system that mixed these two audiences together would clearly be broken.

- **Conflicting Preferences vs. High-Energy Pop:** The "Conflicting Preferences" profile (classical/sad/0.9) asks for a mood — "sad" — that doesn't exist anywhere in the dataset, paired with an energy level that no classical song actually has. Its top picks end up being the two classical songs (matched on genre only) followed by generically high-energy songs from other genres, purely on energy closeness. Compared to High-Energy Pop, which gets clean genre+mood+energy matches, this shows what happens when a user's stated preferences don't actually exist together in the catalog: the system doesn't fail, but it quietly falls back to whichever single feature it *can* match.

- **Negative Energy vs. Out-of-Range Energy:** Both push the `energy` value outside its valid 0–1 range, and both reveal the same underlying issue from the opposite direction — Negative Energy produces a negative "energy closeness" bonus (actually a penalty, mislabeled with a confusing `+-0.41`), while Out-of-Range Energy just shrinks every energy score toward zero. Comparing them side by side makes it obvious this is one bug (no input clamping) rather than two: valid energy values must stay in `[0, 1]`, and nothing in `score_song` currently enforces that.

- **Nonexistent Genre/Mood vs. Acoustic Lover Wanting Metal:** Nonexistent Genre/Mood (vaporwave/euphoric) has no matching genre or mood anywhere, so it falls back entirely to energy-closeness ranking. Acoustic Lover Wanting Metal *does* have a real genre/mood match (metal/intense) but adds a self-contradictory bonus preference (`likes_acoustic`) that metal songs don't satisfy. The difference makes sense: one profile fails to match *categorically* and falls back to energy; the other matches categorically just fine but its bonus feature simply never pays off, because no metal song in the catalog is acoustic. Both are "valid" outcomes — the system isn't confused, it's just accurately reporting that the combination of tastes doesn't exist in this catalog.

### System Evaluation: Adversarial / Edge Case Profiles

In addition to the three "normal" preference profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock), I asked my AI coding assistant to design adversarial user profiles meant to try to "trick" the scoring logic in `score_song`/`recommend_songs`, and ran each one through the CLI.

**Conflicting Preferences (high energy, sad mood: classical/sad/0.9)**
```
=== Conflicting Preferences (high energy, sad mood) ===
User profile: {'genre': 'classical', 'mood': 'sad', 'energy': 0.9}

Top recommendations:

1. Autumn Piano (by Elena Frost) - Score: 2.35
   Because: genre match (+2.0), energy closeness (+0.35)

2. Paper Moon (by Elena Frost) - Score: 2.30
   Because: genre match (+2.0), energy closeness (+0.30)

3. Storm Runner (by Voltline) - Score: 0.99
   Because: energy closeness (+0.99)

4. Gym Hero (by Max Pulse) - Score: 0.97
   Because: energy closeness (+0.97)

5. Iron Verdict (by Grave Hollow) - Score: 0.93
   Because: energy closeness (+0.93)
```
No "sad" mood exists in the dataset, so the mood match never fires for any song. The system still returns sensible results, ranking by genre match and energy closeness — it doesn't crash or return nonsense.

**Out-of-Range Energy (pop/happy/1.5)**
```
=== Out-of-Range Energy (> 1.0) ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 1.5}

Top recommendations:

1. Sunrise City (by Neon Echo) - Score: 3.32
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.32)

2. Gym Hero (by Max Pulse) - Score: 2.43
   Because: genre match (+2.0), energy closeness (+0.43)

3. Rooftop Lights (by Indigo Parade) - Score: 1.26
   Because: mood match (+1.0), energy closeness (+0.26)

4. Sunset Skank (by Copper Tide) - Score: 1.05
   Because: mood match (+1.0), energy closeness (+0.05)

5. Iron Verdict (by Grave Hollow) - Score: 0.47
   Because: energy closeness (+0.47)
```
Energy is on a 0–1 scale in the data, but nothing validates the input. A value of 1.5 doesn't error out — it just shrinks every energy-closeness score since `abs(song_energy - 1.5)` is always large. Ranking order still stays reasonable because genre/mood matches dominate.

**Negative Energy (rock/intense/-0.5)**
```
=== Negative Energy ===
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': -0.5}

Top recommendations:

1. Storm Runner (by Voltline) - Score: 2.59
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+-0.41)

2. Concrete Kings (by MC Ridgeline) - Score: 0.70
   Because: mood match (+1.0), energy closeness (+-0.30)

3. Gym Hero (by Max Pulse) - Score: 0.57
   Because: mood match (+1.0), energy closeness (+-0.43)

4. Iron Verdict (by Grave Hollow) - Score: 0.53
   Because: mood match (+1.0), energy closeness (+-0.47)

5. Paper Moon (by Elena Frost) - Score: 0.30
   Because: energy closeness (+0.30)
```
This is the clearest bug found: negative input energy pushes `abs(diff)` above 1, making `energy_points = 1 - abs(diff)` **negative**. The explanation string then prints a confusing double sign, e.g. `energy closeness (+-0.41)`, which actually *subtracts* from the score while being labeled a bonus. The scoring function has no input validation or clamping on `energy`.

**Nonexistent Genre/Mood (vaporwave/euphoric/0.5)**
```
=== Nonexistent Genre/Mood ===
User profile: {'genre': 'vaporwave', 'mood': 'euphoric', 'energy': 0.5}

Top recommendations:

1. Velvet Hours (by Marisol Vega) - Score: 1.00
   Because: energy closeness (+1.00)

2. Wildflower Road (by Sable & Wren) - Score: 0.95
   Because: energy closeness (+0.95)

3. Sunset Skank (by Copper Tide) - Score: 0.95
   Because: energy closeness (+0.95)

4. Midnight Coding (by LoRoom) - Score: 0.92
   Because: energy closeness (+0.92)

5. Focus Flow (by LoRoom) - Score: 0.90
   Because: energy closeness (+0.90)
```
Genre/mood values that don't exist anywhere in the catalog cause the system to fall back entirely to energy closeness. No error is raised, and the ranking still makes sense as a "closest energy" fallback — a reasonable degradation.

**Acoustic Lover Wanting Metal (metal/intense/0.95, likes_acoustic=True)**
```
=== Acoustic Lover Wanting Metal ===
User profile: {'genre': 'metal', 'mood': 'intense', 'energy': 0.95, 'likes_acoustic': True}

Top recommendations:

1. Iron Verdict (by Grave Hollow) - Score: 3.98
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98)

2. Gym Hero (by Max Pulse) - Score: 1.98
   Because: mood match (+1.0), energy closeness (+0.98)

3. Storm Runner (by Voltline) - Score: 1.96
   Because: mood match (+1.0), energy closeness (+0.96)

4. Concrete Kings (by MC Ridgeline) - Score: 1.85
   Because: mood match (+1.0), energy closeness (+0.85)

5. Wildflower Road (by Sable & Wren) - Score: 1.00
   Because: energy closeness (+0.50), acousticness bonus (+0.5)
```
This profile combines a preference contradiction on purpose (wants intense metal but also likes acoustic songs, which metal songs in this catalog are not). The system doesn't try to reconcile the contradiction — it simply scores each factor independently, so the top pick (Iron Verdict) satisfies genre/mood/energy but gets no acoustic bonus, while a completely different, low-energy acoustic folk song only surfaces at rank 5 via the bonus. This is expected additive-scoring behavior, not a bug.

**Takeaway:** the scoring logic never crashes on adversarial input, but it has no input validation — energy values outside `[0, 1]` are accepted silently and can produce a negative "bonus" term with a misleading explanation string (double sign). A future improvement would be to clamp `energy` to `[0, 1]` and validate `genre`/`mood` against the known catalog before scoring.

---

## 8. Future Work  

1. **Validate input.** Clamp `energy` to the 0-1 range and check that `genre`/`mood` are real values before scoring, so a typo or bad input can't produce a confusing negative score.
2. **Add more songs, especially in the missing energy range (0.55-0.75) and underrepresented genres.** This would fix the "energy gap" filter bubble and stop singleton genres from always returning the same one song.
3. **Add a diversity rule to the top 5**, like "don't show 2 songs by the same artist" or "don't show 5 songs from the exact same genre," so recommendations feel less repetitive even with a small catalog.

---

## 9. Personal Reflection  

My biggest learning moment was realizing how much a recommender's "personality" comes from the data, not just the math. The scoring formula is only a few lines long, but swapping weights or testing weird inputs (negative energy, made-up genres) showed me that most of the interesting behavior — and most of the bugs — come from edge cases in the data meeting simple arithmetic in ways nobody planned for.

Using an AI assistant helped me move fast: it wrote the edge-case profiles, ran experiments, and spotted the energy-gap and negative-score issues faster than I would have by manually scanning the CSV. But I had to double-check its claims against the actual data every time — for example, I re-ran the genre counts and energy value list myself before trusting the "filter bubble" claim, since it's easy for a plausible-sounding explanation to be wrong if it isn't checked against the real numbers.

What surprised me most is how convincing a dead-simple point system can feel. Just adding up "genre match + mood match + energy closeness" produces lists that feel personalized and reasonable — until you push on the edges (tiny catalog, contradictory preferences, out-of-range input) and see it's really just checking boxes, not understanding music. If I extended this project, I'd want to try weighting features based on how rare they are in the catalog, and add a real diversity constraint so the same 2-3 "extreme" songs stop dominating every high-energy profile's top 5.
