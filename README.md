# Reef Memory

A memory game with 246 marine animals photographed by divers and naturalists on iNaturalist. Each dive deals a random 8, 12 or 18 pairs, and every match shows a short fact about the animal.

Build it with `python3 build.py`, then open `site/index.html`. The only requirement is Python 3, and the output is one self-contained HTML file.

The game is in English, plus any language with a file in `i18n/` (Polish, German, French, Spanish and Italian to start). Translations load on demand, so serve `site/` over http to use them; `AGENTS.md` explains how to add one.

Add species to `species.json` and run `python3 fetch_taxa.py`, which looks up the new ones on the iNaturalist API with a one-second pause between species, then rebuild.

Photos come from iNaturalist open data and keep their own Creative Commons licenses. The game credits each photographer in the fact panel, the enlarged photo and "About the photos". The facts are written for this game and checked against sources such as FishBase, Wikipedia and the IUCN Red List. They live in `species.json`, so if you spot a wrong one, a fix is welcome.
