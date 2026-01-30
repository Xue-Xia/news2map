import os

# LLM
LLM_MODEL = os.getenv("NEWS2MAP_LLM_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Geocoding
NOMINATIM_BASE_URL = os.getenv("NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org")
NOMINATIM_USER_AGENT = os.getenv("NOMINATIM_USER_AGENT", "news2map/0.1 (contact@example.com)")
NOMINATIM_EMAIL = os.getenv("NOMINATIM_EMAIL", "")
NOMINATIM_COUNTRYCODES = os.getenv("NOMINATIM_COUNTRYCODES", "de")

# Output
OUTPUT_DIR = os.getenv("NEWS2MAP_OUTPUT_DIR", "data/outputs")
