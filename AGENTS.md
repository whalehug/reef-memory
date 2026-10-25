# Reef Memory

A memory game with reef animals from iNaturalist, served as one static HTML page.

## Commands

- `python3 build.py`: builds `site/index.html` from the template and the four JSON files. Run it after every change. `site/` is gitignored, so never edit `site/index.html` by hand.
- `python3 fetch_taxa.py`: looks up every species in `species.json` that isn't in `taxa.json` yet and saves after each one, pausing a second between species and backing off on HTTP 429. To refresh a species, delete its entry from `taxa.json` first. Read its `MISMATCH` lines: a renamed genus is fine, a different animal is not (the search once returned a tree for `Mola mola`).
- `python3 -m http.server --directory site`: serves the built page for checking.

## Map

- `index.template.html`: the whole game (HTML, CSS and JS). `build.py` fills in `__TAXA__` and `__COUNT__`.
- `species.json`: the species list and the fact for each one, keyed by the scientific name we search iNaturalist for.
- `display.json`: common-name overrides for when iNaturalist's name isn't the one divers use ("Gigas Giant Clam" becomes "Giant Clam").
- `taxa.json`: written by `fetch_taxa.py`. Taxon id, names, observation count, and the default photo with its license and photographer.
- `photos.json`: hand-picked photos that replace the default one (empty shells, beach-cast or aquarium shots, wrong colour forms). `build.py` applies them, so a refetch doesn't undo them.

## Rules

- One self-contained page. No dependencies, no frameworks, and no build tooling beyond Python's standard library.
- Photos only from `inaturalist-open-data.s3.amazonaws.com`, which holds Creative Commons photos. Skip photos credited to a bare numeric account. The fact panel, the enlarged photo and "About the photos" credit the photographer and license, linked to the iNaturalist photo page.
- Cards and the fact panel use the `medium` photo. The enlarged view loads `large` only when someone opens it.
- Facts are one or two sentences (60 to 160 characters) of well-established natural history, written so a curious nine-year-old and an experienced diver both enjoy them. Each new fact is checked against a source other than the one it came from. Hedge anything contested ("is still debated"), keep numbers to what sources agree on, say "Like all pufferfish" when something is true of the family rather than the species, and only mention a conservation status that matches the current IUCN global listing. British spelling, no em dashes, no exclamation marks.
- Photos show the living animal in the wild, big enough to recognise in a square crop. No dead, caught, held or aquarium shots.
- On phones the board is full width. At 760px and wider in a landscape window the fact panel docks beside the board; otherwise it slides up from the bottom. No horizontal scroll at 375px.
- No `alert()`, `confirm()` or `prompt()`, since sandboxed hosts block them. Abandoning a dive mid-round takes a second press instead.
- The `role="status"` line announces every flip, match and miss. Matched cards stay focusable and reopen their fact, arrow keys move between cards, and `prefers-reduced-motion` turns off every effect.
- `localStorage` holds only the chosen level and the best move count per level, and every access is wrapped in try/catch.

## Workflow

- No test suite. Check changes in a browser at 390×700, 807×1030 and 1280×800, and play at least one round to the win screen.
- Commits carry no Co-Authored-By trailer.
- Publishing needs credentials from the site owner. Never commit keys, tokens or deploy links. Publish the built `site/` folder, then open the live URL signed out to check it is still public.
