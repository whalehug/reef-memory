# Reef Memory

A memory game with reef animals from iNaturalist, served as one static HTML page.

## Commands

- `python3 build.py`: builds `site/index.html` from the template and the four JSON files, plus `site/i18n/<code>.json` for each translated language. It prints each language's coverage and stops on a UI file with an unknown key or a missing or extra placeholder. Run it after every change. `site/` is gitignored, so never edit it by hand.
- `python3 fetch_taxa.py`: looks up every species in `species.json` that isn't in `taxa.json` yet and saves after each one, pausing a second between species and backing off on HTTP 429. To refresh a species, delete its entry from `taxa.json` first. Read its `MISMATCH` lines: a renamed genus is fine, a different animal is not (the search once returned a tree for `Mola mola`).
- `python3 -m http.server --directory site`: serves the built page for checking. Languages other than English load with `fetch`, so they only work over http, not from `file://`.

## Map

- `index.template.html`: the whole game (HTML, CSS and JS). `build.py` fills in `__TAXA__`, `__UI__`, `__LANGS__`, `__TITLE__` and `__COUNT__`.
- `species.json`: the species list and the fact for each one, keyed by the scientific name we search iNaturalist for.
- `display.json`: common-name overrides for when iNaturalist's name isn't the one divers use ("Gigas Giant Clam" becomes "Giant Clam").
- `taxa.json`: written by `fetch_taxa.py`. Taxon id, names, observation count, and the default photo with its license and photographer.
- `photos.json`: hand-picked photos that replace the default one (empty shells, beach-cast or aquarium shots, wrong colour forms). `build.py` applies them, so a refetch doesn't undo them.
- `i18n/languages.json`: every language with its code, its name in that language, `dir` (`ltr` or `rtl`) and `reviewed` (false until a native speaker has checked it). English comes first.
- `i18n/ui/<code>.json`: the interface text. `en.json` is the source, with a `_comment` on keys a translator needs context for. A language appears in the picker only once it has this file.
- `i18n/names/<code>.json` and `i18n/facts/<code>.json`: common names and facts, keyed by the same scientific name as `species.json`. English stays in `display.json`, `taxa.json` and `species.json`. Anything missing shows in English.

## Rules

- One self-contained page. No dependencies, no frameworks, and no build tooling beyond Python's standard library.
- Photos only from `inaturalist-open-data.s3.amazonaws.com`, which holds Creative Commons photos. Skip photos credited to a bare numeric account. The fact panel, the enlarged photo and "About the photos" credit the photographer and license, linked to the iNaturalist photo page.
- Cards and the fact panel use the `medium` photo. The enlarged view loads `large` only when someone opens it.
- Facts are one or two sentences (60 to 160 characters) of well-established natural history, written so a curious nine-year-old and an experienced diver both enjoy them. Each new fact is checked against a source other than the one it came from. Hedge anything contested ("is still debated"), keep numbers to what sources agree on, say "Like all pufferfish" when something is true of the family rather than the species, and only mention a conservation status that matches the current IUCN global listing. British spelling, no em dashes, no exclamation marks.
- Photos show the living animal in the wild, big enough to recognise in a square crop. No dead, caught, held or aquarium shots.
- On phones the board is full width. At 760px and wider in a landscape window the fact panel docks beside the board; otherwise it slides up from the bottom. No horizontal scroll at 375px.
- No `alert()`, `confirm()` or `prompt()`, since sandboxed hosts block them. Abandoning a dive mid-round takes a second press instead.
- The `role="status"` line announces every flip, match and miss. Matched cards stay focusable and reopen their fact, arrow keys move between cards, and `prefers-reduced-motion` turns off every effect.
- `localStorage` holds only the chosen level, the chosen language and the best move count per level, and every access is wrapped in try/catch.
- Every visible string, `aria-label` and status announcement comes from `i18n/ui`, never from the template. Use named placeholders (`{name}`, `{count}`) instead of joining sentence parts, `**` around text the status line shows bold, and an object keyed by `Intl.PluralRules` category (`one`, `few`, `many`, `other`) for anything with a count, where `{count}` picks the form. Numbers go through `Intl.NumberFormat`.
- The page picks `?lang=`, then the saved choice, then the browser's languages, then English. Switching language re-renders text only and never reshuffles or resets the board.
- A translation whose `reviewed` is false shows the `machine_note` line under the title. Set it to true only after a native speaker has read the UI, names and facts.

## Workflow

- No test suite. Check changes in a browser at 390×700, 807×1030 and 1280×800, and play at least one round to the win screen. For interface changes, also switch language mid-dive.
- New interface text: add the key to `i18n/ui/en.json`, use it in the template, and rebuild. Other languages show English for that key until they add it.
- New language: add it to `i18n/languages.json` with `reviewed: false`, copy `i18n/ui/en.json` to `i18n/ui/<code>.json` and translate it (keep placeholders and `**`, give each plural key the forms the language needs), then add `i18n/names/<code>.json` and `i18n/facts/<code>.json` and rebuild. Facts follow the same rules as the English ones.
- Commits carry no Co-Authored-By trailer.
- Publishing needs credentials from the site owner. Never commit keys, tokens or deploy links. Publish the built `site/` folder, then open the live URL signed out to check it is still public.
