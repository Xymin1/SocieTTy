from datetime import datetime

from kozts_scraper.models import Match, PlayerRanking, TeamRanking


SAMPLE_PHASE_ID = 364
SAMPLE_TITLE = "Przykładowa faza KOZTS"

SAMPLE_MATCHES = [
    Match(
        phase_id=SAMPLE_PHASE_ID,
        round="Kolejka 1",
        home_team="TS Velo",
        away_team="UKS 911",
        score="7:3",
        match_date=datetime(2024, 10, 1, 18, 0),
    ),
    Match(
        phase_id=SAMPLE_PHASE_ID,
        round="Kolejka 1",
        home_team="ZKS Galaxy",
        away_team="KS Pogoń",
        score="5:5",
        match_date=datetime(2024, 10, 2, 18, 30),
    ),
    Match(
        phase_id=SAMPLE_PHASE_ID,
        round="Kolejka 2",
        home_team="TS Velo",
        away_team="ZKS Galaxy",
        score="6:4",
        match_date=datetime(2024, 10, 9, 18, 0),
    ),
]

SAMPLE_TEAMS = [
    TeamRanking(
        phase_id=SAMPLE_PHASE_ID,
        position=1,
        name="TS Velo",
        matches_played=2,
        points=6,
        sets_balance="13:7",
        games_balance="467:430",
    ),
    TeamRanking(
        phase_id=SAMPLE_PHASE_ID,
        position=2,
        name="ZKS Galaxy",
        matches_played=2,
        points=4,
        sets_balance="9:11",
        games_balance="451:455",
    ),
    TeamRanking(
        phase_id=SAMPLE_PHASE_ID,
        position=3,
        name="KS Pogoń",
        matches_played=1,
        points=1,
        sets_balance="5:5",
        games_balance="230:230",
    ),
]

SAMPLE_PLAYERS = [
    PlayerRanking(
        phase_id=SAMPLE_PHASE_ID,
        position=1,
        name="Marek Kowalski",
        club="TS Velo",
        balance="6:1",
        points=6.0,
    ),
    PlayerRanking(
        phase_id=SAMPLE_PHASE_ID,
        position=2,
        name="Anna Nowak",
        club="ZKS Galaxy",
        balance="5:2",
        points=5.0,
    ),
    PlayerRanking(
        phase_id=SAMPLE_PHASE_ID,
        position=3,
        name="Piotr Zieliński",
        club="KS Pogoń",
        balance="3:2",
        points=3.0,
    ),
]
