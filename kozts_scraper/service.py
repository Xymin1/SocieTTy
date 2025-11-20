from __future__ import annotations

import asyncio
from datetime import datetime
from typing import List, Optional

import httpx
from fastapi import HTTPException

from kozts_scraper import parser
from kozts_scraper.models import Match, PhaseSummary, PlayerRanking, TeamRanking
from kozts_scraper.sample_data import SAMPLE_MATCHES, SAMPLE_PHASE_ID, SAMPLE_PLAYERS, SAMPLE_TEAMS, SAMPLE_TITLE

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
BASE_URL = "https://liga.kozts.pl"
PHASE_PATH = "/index.php?action=phase&id={phase_id}"


class KoztsScraper:
    def __init__(self, client: Optional[httpx.AsyncClient] = None) -> None:
        self.client = client or httpx.AsyncClient(headers={"User-Agent": USER_AGENT}, timeout=20)

    async def fetch_phase_html(self, phase_id: int) -> str:
        url = BASE_URL + PHASE_PATH.format(phase_id=phase_id)
        response = await self.client.get(url)
        response.raise_for_status()
        return response.text

    async def extract_matches(self, html: str, phase_id: int) -> List[Match]:
        return parser.parse_matches(html, phase_id)

    async def extract_teams(self, html: str, phase_id: int) -> List[TeamRanking]:
        return parser.parse_teams(html, phase_id)

    async def extract_players(self, html: str, phase_id: int) -> List[PlayerRanking]:
        return parser.parse_players(html, phase_id)

    async def hydrate_phase(self, phase_id: int) -> PhaseSummary:
        try:
            html = await self.fetch_phase_html(phase_id)
            matches, teams, players = await asyncio.gather(
                self.extract_matches(html, phase_id),
                self.extract_teams(html, phase_id),
                self.extract_players(html, phase_id),
            )
            title = f"Faza {phase_id}"
        except httpx.HTTPError as exc:  # pragma: no cover - network dependent
            # Fall back to bundled demo data if the live source is unavailable.
            if phase_id != SAMPLE_PHASE_ID:
                raise HTTPException(status_code=502, detail=f"Błąd pobierania danych z KOZTS: {exc}")
            matches, teams, players = SAMPLE_MATCHES, SAMPLE_TEAMS, SAMPLE_PLAYERS
            title = SAMPLE_TITLE

        return PhaseSummary(
            phase_id=phase_id,
            title=title,
            updated_at=datetime.utcnow(),
            matches=matches,
            teams=teams,
            players=players,
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> "KoztsScraper":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
