from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Match(BaseModel):
    phase_id: int
    round: Optional[str] = Field(None, description="Round label or phase name")
    home_team: str
    away_team: str
    score: Optional[str]
    match_date: Optional[datetime]


class TeamRanking(BaseModel):
    phase_id: int
    position: int
    name: str
    matches_played: Optional[int]
    points: Optional[int]
    sets_balance: Optional[str] = Field(None, description="Sets won/lost or ratio")
    games_balance: Optional[str] = Field(None, description="Games or points ratio")


class PlayerRanking(BaseModel):
    phase_id: int
    position: int
    name: str
    club: Optional[str]
    balance: Optional[str]
    points: Optional[float]


class PhaseSummary(BaseModel):
    phase_id: int
    title: str
    updated_at: datetime
    matches: List[Match]
    teams: List[TeamRanking]
    players: List[PlayerRanking]
