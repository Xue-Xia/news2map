import re
import sys

import requests

from news2map.pipeline import run_pipeline


def html_to_text(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html).strip()
    return html


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python test.py <url>")
        return 2

    url = sys.argv[1]
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    text = html_to_text(resp.text)
    result = run_pipeline(text)

    print("Events:", len(result.events))
    print("Features:", len(result.features))
    print("GeoJSON:", result.geojson_path)
    print("Shapefile:", result.shapefile_path)

    for i, e in enumerate(result.events[:5], 1):
        places = ", ".join(p.name for p in e.places)
        print(f"{i}. {e.title} | {places}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
