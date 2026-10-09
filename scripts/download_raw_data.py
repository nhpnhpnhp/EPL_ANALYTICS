"""Download raw EPL datasets used by the project.

Examples:
    python scripts/download_raw_data.py
    python scripts/download_raw_data.py --start-season 2015-2016 --end-season 2024-2025
    python scripts/download_raw_data.py --force
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MATCHES_DIR = PROJECT_ROOT / "data" / "raw" / "matches"
PLAYERS_DIR = PROJECT_ROOT / "data" / "raw" / "players"
FOOTBALL_DATA_URL = "https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
UNDERSTAT_URL = "https://understat.com/getLeagueData/EPL/{year}"
DEFAULT_START_SEASON = "2014-2015"
DEFAULT_END_SEASON = "2024-2025"
DEFAULT_PLAYERS_START_SEASON = "2014-2015"
DEFAULT_PLAYERS_END_SEASON = "2024-2025"
SEASON_PATTERN = re.compile(r"^(19|20)\d{2}-(19|20)\d{2}$")


def parse_season(value: str) -> tuple[int, int]:
    """Convert YYYY-YYYY into two seasons and reject malformed ranges."""
    if not SEASON_PATTERN.fullmatch(value):
        raise argparse.ArgumentTypeError("season must use YYYY-YYYY, for example 2024-2025")

    start, end = (int(part) for part in value.split("-"))
    if end != start + 1:
        raise argparse.ArgumentTypeError("season must contain consecutive years")
    return start, end


def season_values(start: str, end: str) -> Iterable[tuple[int, int]]:
    start_year, _ = parse_season(start)
    end_year, _ = parse_season(end)
    if start_year > end_year:
        raise ValueError("start season must not be after end season")
    for year in range(start_year, end_year + 1):
        yield year, year + 1


def make_session() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    session = requests.Session()
    session.headers.update({"User-Agent": "EPL-Analytics-data-downloader/1.0"})
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def download_file(
    session: requests.Session,
    url: str,
    destination: Path,
    force: bool,
    timeout: int,
) -> str:
    if destination.exists() and not force:
        return f"SKIP  {destination.relative_to(PROJECT_ROOT)} (already exists)"

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = session.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destination.parent, prefix=f".{destination.name}.", delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    temporary_file.write(chunk)
        temporary_path.replace(destination)
    except (requests.RequestException, OSError):
        if "temporary_path" in locals() and temporary_path.exists():
            temporary_path.unlink()
        raise

    return f"OK    {destination.relative_to(PROJECT_ROOT)}"


def download_matches(
    session: requests.Session,
    start_season: str,
    end_season: str,
    force: bool,
    timeout: int,
) -> int:
    downloaded = 0
    for start_year, end_year in season_values(start_season, end_season):
        season = f"{start_year}-{end_year}"
        code = f"{str(start_year)[-2:]}{str(end_year)[-2:]}"
        destination = MATCHES_DIR / f"EPL_{season}.csv"
        url = FOOTBALL_DATA_URL.format(code=code)
        try:
            print(download_file(session, url, destination, force, timeout))
            if force or destination.exists():
                downloaded += 1
        except requests.RequestException as error:
            print(f"ERROR {season}: {error}", file=sys.stderr)
    return downloaded


def download_understat_players(
    session: requests.Session,
    start_season: str,
    end_season: str,
    force: bool,
    timeout: int,
) -> int:
    """Fetch and save Understat's EPL player table for each season as a separate CSV."""
    downloaded = 0
    scraped_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for start_year, end_year in season_values(start_season, end_season):
        season_str = f"{start_year}-{end_year}"
        destination = PLAYERS_DIR / f"understat_players_{season_str}.csv"
        
        if destination.exists() and not force:
            print(f"SKIP  {destination.relative_to(PROJECT_ROOT)} (already exists)")
            downloaded += 1
            continue

        season = f"{start_year}/{str(end_year)[-2:]}"
        page_url = f"https://understat.com/league/EPL/{start_year}"
        url = UNDERSTAT_URL.format(year=start_year)
        
        try:
            page_response = session.get(page_url, timeout=timeout)
            page_response.raise_for_status()
            response = session.get(
                url,
                headers={"Referer": page_url, "X-Requested-With": "XMLHttpRequest"},
                timeout=timeout,
            )
            response.raise_for_status()
            payload = response.json()
            players = payload.get("players") if isinstance(payload, dict) else None
            if not isinstance(players, list) or not players:
                raise ValueError(f"Understat returned no player data for season {season}")
    
            rows = []
            for player in players:
                record = dict(player)
                record["league"] = "EPL"
                record["year"] = start_year
                record["season"] = season
                record["scrape_timestamp"] = scraped_at
                if record.get("primary_position") is None and record.get("position"):
                    record["primary_position"] = str(record["position"]).split()[0]
                rows.append(record)
                
            df = pd.DataFrame(rows)
            save_dataframe(df, destination)
            print(f"OK    {destination.relative_to(PROJECT_ROOT)}: {len(players):,} players")
            downloaded += 1
        except (requests.RequestException, ValueError) as error:
            print(f"ERROR {season_str}: {error}", file=sys.stderr)
            
    return downloaded


def save_dataframe(dataframe: pd.DataFrame, destination: Path) -> None:
    """Write a CSV through a temporary file so partial downloads are not kept."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=destination.parent,
        prefix=f".{destination.name}.", suffix=".tmp", delete=False
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
        dataframe.to_csv(temporary_file, index=False)
    temporary_path.replace(destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download raw EPL match and Understat player data.")
    parser.add_argument("--start-season", default=DEFAULT_START_SEASON, type=parse_season)
    parser.add_argument("--end-season", default=DEFAULT_END_SEASON, type=parse_season)
    parser.add_argument("--players-start-season", default=DEFAULT_PLAYERS_START_SEASON, type=parse_season)
    parser.add_argument("--players-end-season", default=DEFAULT_PLAYERS_END_SEASON, type=parse_season)
    parser.add_argument("--force", action="store_true", help="Overwrite files that already exist.")
    parser.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds (default: 60).")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    start_season = f"{args.start_season[0]}-{args.start_season[1]}"
    end_season = f"{args.end_season[0]}-{args.end_season[1]}"
    players_start_season = f"{args.players_start_season[0]}-{args.players_start_season[1]}"
    players_end_season = f"{args.players_end_season[0]}-{args.players_end_season[1]}"
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    try:
        with make_session() as session:
            print(f"Downloading matches: {start_season} -> {end_season}")
            match_count = download_matches(
                session, start_season, end_season, args.force, args.timeout
            )
            
            print(f"Downloading Understat players: {players_start_season} -> {players_end_season}")
            player_count = download_understat_players(
                session, players_start_season, players_end_season, args.force, args.timeout
            )

    except (requests.RequestException, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Finished: {match_count} match file(s), {player_count} player file(s) downloaded or present.")
    return 0 if match_count else 1


if __name__ == "__main__":
    raise SystemExit(main())
