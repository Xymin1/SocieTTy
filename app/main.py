from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from kozts_scraper.models import PhaseSummary
from kozts_scraper.service import KoztsScraper

app = FastAPI(title="KOZTS Hyper League", version="1.0.0")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_scraper() -> KoztsScraper:
    scraper = KoztsScraper()
    try:
        yield scraper
    finally:
        await scraper.close()


@app.get("/", response_class=HTMLResponse)
async def landing_page() -> HTMLResponse:
    index_path = STATIC_DIR / "index.html"
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/favicon.ico")
async def favicon() -> FileResponse:
    icon = STATIC_DIR / "favicon.ico"
    if icon.exists():
        return FileResponse(icon)
    raise HTTPException(status_code=404, detail="favicon not found")


@app.get("/api/phase/{phase_id}", response_model=PhaseSummary)
async def get_phase(phase_id: int, scraper: KoztsScraper = Depends(get_scraper)) -> PhaseSummary:
    return await scraper.hydrate_phase(phase_id)


@app.get("/api/phase/{phase_id}/matches")
async def get_phase_matches(phase_id: int, scraper: KoztsScraper = Depends(get_scraper)):
    phase = await scraper.hydrate_phase(phase_id)
    return phase.matches


@app.get("/api/phase/{phase_id}/teams")
async def get_phase_teams(phase_id: int, scraper: KoztsScraper = Depends(get_scraper)):
    phase = await scraper.hydrate_phase(phase_id)
    return phase.teams


@app.get("/api/phase/{phase_id}/players")
async def get_phase_players(phase_id: int, scraper: KoztsScraper = Depends(get_scraper)):
    phase = await scraper.hydrate_phase(phase_id)
    return phase.players


app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="static")
