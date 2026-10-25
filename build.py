"""Build site/index.html (English embedded) and site/i18n/<code>.json for each translated language."""
import glob, html, json, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def to_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


taxa = load("taxa.json")
facts = load("species.json")
display = load("display.json")
photos = load("photos.json")
taxa = [{**t, **photos.get(t["query"], {})} for t in taxa]
queries = {t["query"] for t in taxa}

data = [{
    "q": t["query"], "id": t["id"], "name": t["name"], "common": display.get(t["query"]) or t["common"],
    "observations": t["observations"], "photo": t["photo"], "photo_id": t["photo_id"],
    "license": t["license"], "photographer": " ".join(html.unescape(t["photographer"]).split()),
    "fact": facts[t["query"]],
} for t in taxa]

# A UI string is a plain string, {"text": ...}, or an object keyed by Intl.PluralRules category; any may carry "_comment".
PLURAL = {"zero", "one", "two", "few", "many", "other"}
errors = []


def clean(value):
    if isinstance(value, str):
        return value
    value = {k: v for k, v in value.items() if k != "_comment"}
    return value["text"] if set(value) == {"text"} else value


def placeholders(s):
    return set(re.findall(r"\{(\w+)\}", s))


def check_ui(code, ui, en=None):
    out = {}
    for key, raw in ui.items():
        if key == "_comment":
            continue
        if en is not None and key not in en:
            errors.append(f"{code}: unknown key {key!r}")
            continue
        value = clean(raw)
        if isinstance(value, dict):
            if "other" not in value or not set(value) <= PLURAL or not all(isinstance(v, str) for v in value.values()):
                errors.append(f"{code}: {key!r} plural needs string forms keyed by {sorted(PLURAL)}, including 'other'")
                continue
        elif not isinstance(value, str):
            errors.append(f"{code}: {key!r} must be a string or a plural object")
            continue
        if en is not None:
            ref = en[key]
            if isinstance(ref, dict) != isinstance(value, dict):
                errors.append(f"{code}: {key!r} must be {'a plural object' if isinstance(ref, dict) else 'a string'}, like English")
                continue
            ref = ref["other"] if isinstance(ref, dict) else ref
            for form, s in (value.items() if isinstance(value, dict) else [("other", value)]):
                # Only the "other" form must show {count}; "one" may spell the number out.
                missing = placeholders(ref) - placeholders(s) - ({"count"} if form != "other" else set())
                unknown = placeholders(s) - placeholders(ref)
                if missing:
                    errors.append(f"{code}: {key!r} ({form}) is missing " + ", ".join("{%s}" % p for p in sorted(missing)))
                if unknown:
                    errors.append(f"{code}: {key!r} ({form}) has unknown " + ", ".join("{%s}" % p for p in sorted(unknown)))
                if s.count("**") != ref.count("**"):
                    errors.append(f"{code}: {key!r} ({form}) needs {ref.count('**')} ** bold markers, like English")
        out[key] = value
    return out


def species_map(code, kind):
    path = f"i18n/{kind}/{code}.json"
    if not os.path.exists(path):
        return {}
    found = {q: s.strip() for q, s in load(path).items() if isinstance(s, str) and s.strip()}
    unknown = sorted(set(found) - queries)
    if unknown:
        print(f"  warning: {path} has {len(unknown)} unknown species, ignored: {', '.join(unknown[:5])}{' ...' if len(unknown) > 5 else ''}")
    return {q: s for q, s in found.items() if q in queries}


languages = load("i18n/languages.json")
codes = [l.get("code") for l in languages]
for l in languages:
    if not re.fullmatch(r"[a-z]{2,3}(-[A-Za-z0-9]{2,8})*", l.get("code") or "") or l.get("dir") not in ("ltr", "rtl") \
            or not l.get("name") or not isinstance(l.get("reviewed"), bool):
        errors.append(f"i18n/languages.json: bad entry {l}")
if codes[:1] != ["en"] or len(set(codes)) != len(codes):
    errors.append("i18n/languages.json: English must come first and codes must be unique")
for path in glob.glob("i18n/ui/*.json"):
    if os.path.basename(path)[:-5] not in codes:
        errors.append(f"{path}: language missing from i18n/languages.json")

en_ui = check_ui("en", load("i18n/ui/en.json"))
built, packs = [languages[0]], {}
for l in languages[1:]:
    code = l["code"]
    if not os.path.exists(f"i18n/ui/{code}.json"):
        print(f"{code}: no i18n/ui/{code}.json, skipped")
        continue
    pack = {"ui": check_ui(code, load(f"i18n/ui/{code}.json"), en_ui),
            "names": species_map(code, "names"), "facts": species_map(code, "facts")}
    print(f"{code}: ui {len(pack['ui'])}/{len(en_ui)}, names {len(pack['names'])}/{len(data)}, "
          f"facts {len(pack['facts'])}/{len(data)}{'' if l['reviewed'] else ', not reviewed'}")
    packs[code] = pack
    built.append(l)

if errors:
    sys.stdout.flush()
    print("\n".join(f"error: {e}" for e in errors), file=sys.stderr)
    sys.exit(1)

script = lambda value: to_json(value).replace("</", "<\\/")
page = open("index.template.html", encoding="utf-8").read()
page = (page.replace("__TAXA__", script(data)).replace("__UI__", script(en_ui)).replace("__LANGS__", script(built))
        .replace("__TITLE__", html.escape(en_ui["title"])).replace("__COUNT__", str(len(data))))
os.makedirs("site/i18n", exist_ok=True)
write("site/index.html", page)
for path in glob.glob("site/i18n/*.json"):
    if os.path.basename(path)[:-5] not in packs:
        os.remove(path)
for code, pack in packs.items():
    write(f"site/i18n/{code}.json", to_json(pack))
print(f"built site/index.html with {len(data)} species, plus {len(packs)} translation file{'' if len(packs) == 1 else 's'} in site/i18n/")
