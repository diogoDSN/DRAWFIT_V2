from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional
from psycopg2 import connect, connection
from datetime import datetime

if TYPE_CHECKING:
    from drawfit.domain.league import League

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
import drawfit.domain.followables as f
from drawfit.dtos import LeagueDto, DomainDto
from drawfit.database.drawfit_database_error import DrawfitDatabaseError
from drawfit.database.db_messages import *

from drawfit.utils import Sites, OddSample, LeagueCode, LeagueCodesFactory

class DatabaseStore:
    
    def __init__(self) -> NoReturn:
        # No caching
        self._db_connection = None
    
    def __enter__(self) -> DatabaseStore:
        self._db_connection = connect(dbname='drawfit_mock', user='drawfit_bot', host='localhost', password='McMahaeWsNoBeat')
        return self

    def __exit__(self) -> NoReturn:
        self._db_connection.rollback()
        self._db_connection.close()
        self._db_connection = None
    
    @property
    def db_connection() -> Optional[connection]:
        return _db_connection

    def GetAllSites() -> List[str]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch all sites
            cursor.execute("SELECT * FROM site;")
            stored_sites = cursor.fetchall()
        
        return [site for site in Sites if (site.value,) in stored_sites]


    def GetAllColors() -> Tuple[Tuple[str, int]]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch all colors
            cursor.execute("SELECT * FROM color;")
            stored_colors = cursor.fetchall()
        
        return tuple(color_tuple for color_tuple in stored_colors)

    def GetLeague(self, league_name: str) -> Optional[l.League]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch league and color
            cursor.execute("SELECT * FROM league WHERE name=(%s);", (league_name))
            result = cursor.fetchall()
            
            if len(result) != 1:
                raise DrawfitDatabaseError(LeagueNotFound(league_name))
            
            league = l.League(result[0][0], color=result[0][1])
            
            # Fetch league codes
            cursor.execute("SELECT site_name, code FROM league_code WHERE league_name = (%s);", (league_name))
            result = cursor.fetchall()
            
            for site_name, raw_code in result:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    league.codes[site] = LeagueCodesFactory(site, raw_code)
        
        return league
            
    def GetTeam(self, team_name: str) -> Optional[f.Team]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch team and active status
            cursor.execute("SELECT * FROM team WHERE name=(%s);", (team_name))
            if len(result) != 1:
                raise DrawfitDatabaseError(TeamNotFound(team_name))
            
            team = f.Team(team_name)
            team.active = result[0][1]
            
            # Fetch team's site ids
            cursor.execute("SELECT site_name, id FROM team_id WHERE team_name = (%s);", (team_name))
            result = cursor.fetchall()
            
            for site_name, team_id in result:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    team.setId(site, team_id)
            
            # Fetch team's current game if any
            cursor.execute("SELECT site_name, id FROM game WHERE team_name = (%s);", (team_name))
            result = cursor.fetchall()
            
        return team

    def GetCurrentGame(self, team_name: str) -> Optional[f.Game]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch team and active status
            cursor.execute("SELECT name, date FROM game WHERE team_name = (%s) and date > (%s);", (team_name, datetime.utcnow()))
            result = cursor.fetchall()
            
            if len(result) != 1:
                return None
            
            game = f.Game(result[0][0])
            game.date = result[0][1]
            
            # Fetch all odds from game
            cursor.execute("SELECT site_name, value, date FROM odd WHERE game_name = (%s) AND game_date = (%s);", (game.name, game.date))
            results = cursor.fetchall()
            
            # sort by date
            results.sort(key=lambda x: x[2])
            
            for site_name, odd_value, odd_datetime in results:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    game.addOdd(odd_value, odd_datetime, site)
            
            # Fetch game's ids
            cursor.execute("SELECT site_name, id FROM odd WHERE game_name = (%s) AND game_date = (%s);", (game.name, game.date))
            results = cursor.fetchall()
            
            for site_name, game_id in results:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    game.setId(site, game_id)            
            
        return game
                    
                
            
            
            
            
            
            
            
            
            
            