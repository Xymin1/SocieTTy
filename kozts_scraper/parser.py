from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

from bs4 import BeautifulSoup

from kozts_scraper.models import Match, PlayerRanking, TeamRanking

DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%Y-%m-%d %H:%M", "%d.%m.%Y %H:%M"]


def _parse_date(value: str) -> Optional[datetime]:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    return None


def _extract_headers(table) -> List[str]:
    headers = [th.get_text(strip=True) for th in table.select("thead th")]
    if headers:
        return headers

    first_row = table.find("tr")
    if first_row:
        headers = [cell.get_text(strip=True) for cell in first_row.find_all(["td", "th"])]
    return headers


def _find_table_by_headers(soup: BeautifulSoup, header_keywords: Iterable[str]):
    best_table = None
    best_score = 0

    for table in soup.find_all("table"):
        headers = _extract_headers(table)
        normalized = [h.lower() for h in headers]

        score = 0
        for keyword in header_keywords:
            if any(keyword in header for header in normalized):
                score += 1

        if score > best_score:
            best_table = table
            best_score = score

    return best_table


def parse_table_rows(table) -> List[dict]:
    if table is None:
        return []

    headers = _extract_headers(table)
    body_rows = table.select("tbody tr")

    if not headers and body_rows:
        headers = [cell.get_text(strip=True) for cell in body_rows[0].find_all(["td", "th"])]
        body_rows = body_rows[1:]

    parsed_rows = []
    for tr in body_rows:
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all("td")]
        if not cells:
            continue
        parsed_rows.append(dict(zip(headers, cells)))
    return parsed_rows


def parse_matches(html: str, phase_id: int) -> List[Match]:
    soup = BeautifulSoup(html, "html.parser")
    matches_table = _find_table_by_headers(
        soup,
        header_keywords=(
            "gosp",
            "goś",
            "gość",
            "away",
            "home",
            "wynik",
            "result",
            "kolej",
            "termin",
            "data",
        ),
    )
    rows = parse_table_rows(matches_table)

    parsed: List[Match] = []
    for row in rows:
        home = row.get("Gospodarz") or row.get("Home") or row.get("Drużyna gospodarzy")
        away = row.get("Gość") or row.get("Away") or row.get("Drużyna gości")
        score = row.get("Wynik") or row.get("Result")
        round_label = row.get("Kolejka") or row.get("Round")
        date_value = row.get("Data") or row.get("Date") or row.get("Termin")

        parsed.append(
            Match(
                phase_id=phase_id,
                round=round_label,
                home_team=home or "?",
                away_team=away or "?",
                score=score,
                match_date=_parse_date(date_value) if date_value else None,
            )
        )
    return parsed


def parse_teams(html: str, phase_id: int) -> List[TeamRanking]:
    soup = BeautifulSoup(html, "html.parser")
    table = _find_table_by_headers(
        soup,
        header_keywords=(
            "dru",
            "team",
            "pkt",
            "punk",
            "małe",
            "set",
            "m ",
            "mp",
        ),
    )
    rows = parse_table_rows(table)

    parsed: List[TeamRanking] = []
    for row in rows:
        try:
            position = int(row.get("Lp.") or row.get("#") or row.get("Poz") or row.get("Position"))
        except (TypeError, ValueError):
            position = len(parsed) + 1

        name = row.get("Drużyna") or row.get("Team") or row.get("Nazwa") or "?"
        matches_played = row.get("M") or row.get("MP") or row.get("Rozegrane")
        points = row.get("Punkty") or row.get("Pkt") or row.get("Pts")
        sets_balance = row.get("Sety") or row.get("Sety +/−") or row.get("Set balance")
        games_balance = row.get("Małe punkty") or row.get("Punkty") or row.get("Points")

        parsed.append(
            TeamRanking(
                phase_id=phase_id,
                position=position,
                name=name,
                matches_played=int(matches_played) if matches_played and str(matches_played).isdigit() else None,
                points=int(points) if points and str(points).replace("+", "").replace("-", "").isdigit() else None,
                sets_balance=sets_balance,
                games_balance=games_balance,
            )
        )
    return parsed


def parse_players(html: str, phase_id: int) -> List[PlayerRanking]:
    soup = BeautifulSoup(html, "html.parser")
    table = _find_table_by_headers(
        soup,
        header_keywords=(
            "nazw",
            "zaw",
            "player",
            "klub",
            "bilans",
            "punk",
        ),
    )
    rows = parse_table_rows(table)

    parsed: List[PlayerRanking] = []
    for row in rows:
        try:
            position = int(row.get("Lp.") or row.get("#") or row.get("Poz") or row.get("Position"))
        except (TypeError, ValueError):
            position = len(parsed) + 1

        name = row.get("Nazwisko i imię") or row.get("Zawodnik") or row.get("Player") or row.get("Name") or "?"
        club = row.get("Klub") or row.get("Drużyna") or row.get("Club")
        balance = row.get("Bilans") or row.get("Balance") or row.get("W/L")
        points = row.get("Punkty") or row.get("Pts") or row.get("Points")

        parsed.append(
            PlayerRanking(
                phase_id=phase_id,
                position=position,
                name=name,
                club=club,
                balance=balance,
                points=float(points.replace(",", ".")) if points and str(points).replace(",", ".").replace(".", "").isdigit() else None,
            )
        )
    return parsed
