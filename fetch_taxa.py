"""Fetch each species in species.json from iNaturalist and write taxa.json. Usage: python3 fetch_taxa.py [taxa.json] [species.json]"""
import json, sys, time, urllib.error, urllib.request, urllib.parse

OUT = sys.argv[1] if len(sys.argv) > 1 else "taxa.json"
SPECIES = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "species.json"))
PREF = ["cc0","cc-by","cc-by-sa","cc-by-nc","cc-by-nc-sa"]

def get(url, tries=6):
    req = urllib.request.Request(url, headers={"User-Agent": "reef-memory"})
    for attempt in range(tries):
        try:
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == tries - 1:
                raise
            time.sleep(30 * (attempt + 1))

# Resumable: species already in OUT are kept, and OUT is rewritten after each new one.
try:
    out = json.load(open(OUT))
except FileNotFoundError:
    out = []
done = {t["query"] for t in out}
for name in SPECIES:
    if name in done:
        continue
    res = get("https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode({"q": name, "rank": "species", "per_page": 30}))["results"]
    r = next((x for x in res if x["name"] == name or name in [n.get("name") for n in x.get("names", [])]), None) or next((x for x in res if x.get("matched_term") == name), res[0])
    t = get(f"https://api.inaturalist.org/v1/taxa/{r['id']}?locale=en")["results"][0]
    photos = [tp["photo"] for tp in t.get("taxon_photos", []) if "inaturalist-open-data" in (tp["photo"].get("medium_url") or tp["photo"].get("url") or "") and not (tp["photo"].get("attribution_name") or "").strip().isdigit()]
    photos.sort(key=lambda p: PREF.index(p["license_code"]) if p.get("license_code") in PREF else 99)
    p = photos[0] if photos else None
    if t["name"] != name:
        print("MISMATCH", name, "->", t["name"], file=sys.stderr)
    out.append({"query": name,
        "id": t["id"], "name": t["name"], "common": t.get("preferred_common_name"),
        "observations": t["observations_count"],
        "photo": p and (p.get("medium_url") or p["url"].replace("square", "medium")),
        "license": p and p.get("license_code"), "attribution": p and p.get("attribution"), "photo_id": p and p["id"], "photographer": p and (p.get("attribution_name") or "").strip(),
    })
    print(name, "->", out[-1]["common"], out[-1]["license"], file=sys.stderr)
    json.dump(out, open(OUT, "w"), indent=1)
    time.sleep(1)
