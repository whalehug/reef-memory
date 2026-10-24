"""Build site/index.html from the template, taxa.json (iNaturalist), species.json (facts) and display.json (name overrides)."""
import html, json, os

taxa = json.load(open("taxa.json"))
facts = json.load(open("species.json"))
display = json.load(open("display.json"))

data = [{
    "id": t["id"], "name": t["name"], "common": display.get(t["query"]) or t["common"],
    "observations": t["observations"], "photo": t["photo"], "photo_id": t["photo_id"],
    "license": t["license"], "photographer": " ".join(html.unescape(t["photographer"]).split()),
    "fact": facts[t["query"]],
} for t in taxa]

page = open("index.template.html").read()
page = page.replace("__TAXA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")).replace("__COUNT__", str(len(data)))
os.makedirs("site", exist_ok=True)
open("site/index.html", "w").write(page)
print(f"built site/index.html with {len(data)} species")
