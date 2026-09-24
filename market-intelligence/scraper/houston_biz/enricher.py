"""Contact & Geolocation Enrichment Module.

Provides enrichment capabilities using public APIs (OpenStreetMap Nominatim
and Overpass API) to add coordinates, phone numbers, and websites to business listings.
"""

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class BusinessEnricher:
    """Enriches Houston business listings with external web and map metadata."""

    def __init__(self, user_agent: str = "HoustonBizScraper/1.0"):
        self.user_agent = user_agent

    def geocode_address(self, street: str, city: str = "Houston", state: str = "TX", zip_code: str = "") -> Optional[Dict[str, Any]]:
        """Geocode a business address using OpenStreetMap Nominatim."""
        query = f"{street}, {city}, {state} {zip_code}".strip()
        encoded = urllib.parse.quote(query)
        url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={encoded}"

        headers = {"User-Agent": self.user_agent}
        req = urllib.request.Request(url, headers=headers)

        try:
            # Respect OpenStreetMap 1 request/second usage policy
            time.sleep(1.0)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data and isinstance(data, list) and len(data) > 0:
                    item = data[0]
                    return {
                        "lat": item.get("lat"),
                        "lon": item.get("lon"),
                        "display_name": item.get("display_name"),
                        "osm_type": item.get("osm_type"),
                    }
        except Exception:
            return None
        return None

    def generate_google_search_url(self, business_name: str, street: str, zip_code: str) -> str:
        """Generate a direct query URL for finding phone number and website."""
        query = f'"{business_name}" "{street}" Houston TX {zip_code}'
        return f"https://www.google.com/search?q={urllib.parse.quote(query)}"
