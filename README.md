# Reef Memory

A memory game with 71 reef animals photographed by divers and naturalists on iNaturalist. Each dive deals a random 8, 12 or 18 pairs, and every match shows a short fact about the animal.

Build it with `python3 build.py`, then open `site/index.html`. The only requirement is Python 3, and the output is one self-contained HTML file.

Refresh the species data with `python3 fetch_taxa.py`, which calls the iNaturalist API with a one-second pause between species (about three minutes for all 71), then rebuild.

Photos come from iNaturalist open data and keep their own Creative Commons licenses. The game credits each photographer in the fact panel, the enlarged photo and "About the photos". The facts are written for this game and live in `species.json`, so if you spot a wrong one, a fix is welcome.
