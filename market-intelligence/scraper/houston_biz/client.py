"""Socrata SODA API Client for Texas Open Data.

Provides reliable, paginated, and rate-limit-resilient data retrieval
from the Texas Comptroller datasets.
"""

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, Generator, List, Optional

SOCRATA_BASE_URL = "https://data.texas.gov/resource"

# Official Dataset Identifiers on data.texas.gov
DATASET_PERMITS = "jrea-zgmq"      # Active Sales Tax Permit Holders (Storefronts/Outlets/DBAs)
DATASET_FRANCHISE = "9cir-efmm"    # Active Franchise Taxpayers (LLCs, Corps, SOS filings)


class SocrataError(Exception):
    """Raised when an API error occurs from Socrata."""
    pass


class SocrataClient:
    """Client for pulling open public records from data.texas.gov."""

    def __init__(self, app_token: Optional[str] = None, user_agent: str = "HoustonBizScraper/1.0"):
        self.app_token = app_token
        self.user_agent = user_agent

    def _request_json(self, url: str, max_retries: int = 4) -> Any:
        """Execute HTTP request with exponential backoff for rate limits."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }
        if self.app_token:
            headers["X-App-Token"] = self.app_token

        req = urllib.request.Request(url, headers=headers)
        delay = 1.0

        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=45) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw)
            except urllib.error.HTTPError as e:
                if e.code == 429:  # Rate limited
                    time.sleep(delay)
                    delay *= 2
                    continue
                elif e.code in (500, 502, 503, 504):
                    time.sleep(delay)
                    delay *= 2
                    continue
                else:
                    err_msg = e.read().decode("utf-8", errors="replace")
                    raise SocrataError(f"HTTP {e.code} error: {err_msg}") from e
            except Exception as e:
                if attempt == max_retries - 1:
                    raise SocrataError(f"Network error after {max_retries} attempts: {e}") from e
                time.sleep(delay)
                delay *= 2

        raise SocrataError(f"Failed to fetch data from {url} after {max_retries} retries.")

    def get_count(self, dataset_id: str, where: str) -> int:
        """Get total number of records matching the WHERE filter."""
        params = {
            "$where": where,
            "$select": "count(*)",
        }
        query_str = urllib.parse.urlencode(params)
        url = f"{SOCRATA_BASE_URL}/{dataset_id}.json?{query_str}"
        data = self._request_json(url)
        if isinstance(data, list) and len(data) > 0 and "count" in data[0]:
            return int(data[0]["count"])
        return 0

    def fetch_records_stream(
        self,
        dataset_id: str,
        where: str,
        order_by: str,
        chunk_size: int = 10000,
        max_records: Optional[int] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """Stream paginated batches of records until all are retrieved."""
        total_available = self.get_count(dataset_id, where)
        target_records = min(total_available, max_records) if max_records else total_available

        offset = 0
        retrieved = 0

        while True:
            limit = min(chunk_size, target_records - retrieved) if target_records else chunk_size
            if limit <= 0:
                break

            params = {
                "$where": where,
                "$order": order_by,
                "$limit": str(limit),
                "$offset": str(offset),
            }
            query_str = urllib.parse.urlencode(params)
            url = f"{SOCRATA_BASE_URL}/{dataset_id}.json?{query_str}"

            batch = self._request_json(url)
            if not batch or not isinstance(batch, list):
                break

            yield batch

            batch_len = len(batch)
            retrieved += batch_len
            offset += batch_len

            if progress_callback:
                progress_callback(retrieved, target_records)

            if batch_len < limit:
                # Last page reached
                break
