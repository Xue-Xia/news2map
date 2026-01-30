# news2map

Convert news article text into GIS-ready spatial data.

## Features
- Input: news article text (German supported)
- Extract spatial events and places via ChatGPT
- Geocode places
- Produce GeoJSON and Shapefile outputs

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set environment variables:

```bash
export OPENAI_API_KEY="..."
export NEWS2MAP_LLM_MODEL="gpt-4o-mini"
export NOMINATIM_USER_AGENT="news2map/0.1 (your_email@example.com)"
export NOMINATIM_EMAIL="your_email@example.com"
```

## Usage

```bash
python test.py "URL"
```

## Project layout
- `news2map/` core package
- `tests/` minimal tests
- `data/outputs/` generated outputs (gitignored)


