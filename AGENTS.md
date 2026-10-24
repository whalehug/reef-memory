# Reef Memory

A memory game with reef animals from iNaturalist, served as one static HTML page.

## Commands

- `python3 build.py`: builds `site/index.html` from the template and the three JSON files. Run it after every change. `site/` is gitignored, so never edit `site/index.html` by hand.
- `python3 fetch_taxa.py`: refetches every species in `species.json` from the iNaturalist API into `taxa.json`, pausing a second between species. Read its `MISMATCH` lines: a renamed genus is fine, a different animal is not (the search once returned a tree for `Mola mola`).
- `python3 -m http.server --directory site`: serves the built page for checking.

## Map

- `index.template.html`: the whole game (HTML, CSS and JS). `build.py` fills in `__TAXA__` and `__COUNT__`.
- `species.json`: the species list and the fact for each one, keyed by the scientific name we search iNaturalist for.
- `display.json`: common-name overrides for when iNaturalist's name isn't the one divers use ("Gigas Giant Clam" becomes "Giant Clam").
- `taxa.json`: written by `fetch_taxa.py`. Taxon id, names, observation count, and the chosen photo with its license and photographer.

## Rules

- One self-contained page. No dependencies, no frameworks, and no build tooling beyond Python's standard library.
- Photos only from `inaturalist-open-data.s3.amazonaws.com`, which holds Creative Commons photos. Skip photos credited to a bare numeric account. The fact panel, the enlarged photo and "About the photos" credit the photographer and license, linked to the iNaturalist photo page.
- Cards and the fact panel use the `medium` photo. The enlarged view loads `large` only when someone opens it.
- Facts are one or two sentences of well-established natural history. Hedge anything contested ("is still debated"), and only mention a conservation status that matches the current IUCN listing.
- On phones the board is full width. At 760px and wider in a landscape window the fact panel docks beside the board; otherwise it slides up from the bottom. No horizontal scroll at 375px.
- No `alert()`, `confirm()` or `prompt()`, since sandboxed hosts block them. Abandoning a dive mid-round takes a second press instead.
- The `role="status"` line announces every flip, match and miss. Matched cards stay focusable and reopen their fact, arrow keys move between cards, and `prefers-reduced-motion` turns off every effect.
- `localStorage` holds only the chosen level and the best move count per level, and every access is wrapped in try/catch.

## Workflow

- No test suite. Check changes in a browser at 390×700, 807×1030 and 1280×800, and play at least one round to the win screen.
- Commits carry no Co-Authored-By trailer.
- Publishing needs credentials from the site owner. Never commit keys, tokens or deploy links. Publish the built `site/` folder, then open the live URL signed out to check it is still public.
