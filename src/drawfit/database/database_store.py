from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional
from psycopg2 import connect
from psycopg2.errors import UniqueViolation, ForeignKeyViolation, RaiseException
from datetime import datetime

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
import drawfit.domain.followables as f
from drawfit.dtos import LeagueDto, DomainDto
from drawfit.database.drawfit_error import DrawfitError
from drawfit.database.db_messages import *

from drawfit.utils import Sites, OddSample, LeagueCode, LeagueCodesFactory, str_dates, tz_aware, to_utc

class DatabaseStore:
    
    def __init__(self) -> NoReturn:
        # No caching
        self._db_connection = None
    
    def __enter__(self) -> DatabaseStore:
        self._db_connection = connect(dbname='drawfit_mock', user='drawfit_bot', host='localhost', password='McMahaeWsNoBeat')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> NoReturn:
        if exc_type is None:
            self._db_connection.commit()
        else:
            self._db_connection.rollback()
            
        self._db_connection.close()
        self._db_connection = None
    
    @property
    def db_connection(self):
        return self._db_connection

    def getAllSites(self) -> List[str]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch all sites
            cursor.execute("SELECT * FROM site;")
            stored_sites = cursor.fetchall()
        
        return [site for site in Sites if (site.value,) in stored_sites]


    def getAllColors(self) -> Tuple[Tuple[str, int]]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch all colors
            cursor.execute("SELECT * FROM color;")
            stored_colors = cursor.fetchall()
        
        return tuple(color_tuple for color_tuple in stored_colors)
    
    def getColor(self, color_name: str) -> int:
        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT hex_code FROM color WHERE name=(%s)", (color_name,))
            result = cursor.fetchall()
        
            if len(result) != 1:
                raise DrawfitError(ColorNotFound(color_name))
            
        return result[0][0]

    def getLeague(self, league_name: str) -> l.League:
        with self.db_connection.cursor() as cursor:

            # Fetch league and color
            cursor.execute("SELECT * FROM league WHERE name=(%s);", (league_name, ))
            result = cursor.fetchall()
            
            if len(result) != 1:
                raise DrawfitError(LeagueNotFound(league_name))
            
            league = l.League(result[0][0], color=result[0][1])
            
            # Fetch league codes
            cursor.execute("SELECT site_name, code FROM league_code WHERE league_name = (%s);", (league_name,))
            result = cursor.fetchall()
            
            for site_name, raw_code in result:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    league.codes[site] = LeagueCodesFactory(site, raw_code)
        
        return league
    
    def getAllLeagues(self) -> List[l.League]:
        with self.db_connection.cursor() as cursor:
            
            cursor.execute("SELECT name FROM league;")
            result = cursor.fetchall()
        
        all_leagues = []
        
        for (league_name,) in result:
            all_leagues.append(self.getLeague(league_name))
        
        return all_leagues
        
    
    def getTeamNamesFromLeague(self, league_name: str) -> List[str]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch team names
            cursor.execute("SELECT team_name FROM plays_in WHERE league_name=(%s);", (league_name,))
            result = cursor.fetchall()
            
        return [team_name for (team_name,) in result]
    
    def getLeagueNamesFromTeam(self, team_name: str) -> List[str]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch league names
            cursor.execute("SELECT league_name FROM plays_in WHERE team_name=(%s);", (team_name,))
            result = cursor.fetchall()
            
        return [league_name for (league_name,) in result]
            
            
    def getTeam(self, team_name: str) -> f.Team:
        with self.db_connection.cursor() as cursor:
            
            # Fetch team and active status
            cursor.execute("SELECT * FROM team WHERE name=(%s);", (team_name,))
            result = cursor.fetchall()
            
            if len(result) != 1:
                raise DrawfitError(TeamNotFound(team_name))
            
            team = f.Team(team_name)
            team.active = result[0][1]
            
            # Fetch team's site ids
            cursor.execute("SELECT site_name, id FROM team_id WHERE team_name = (%s);", (team_name,))
            result = cursor.fetchall()
            
            for site_name, team_id in result:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    team.setId(site, (team_id,))
            
        return team

    def getCurrentGame(self, team: f.Team, leagues: Dict[str, l.League]) -> Optional[f.Game]:
        with self.db_connection.cursor() as cursor:
            
            # Fetch team and active status
            cursor.execute("SELECT name, date, league_name FROM game WHERE team_name = (%s) AND date > (%s);", (team.name, datetime.utcnow()))
            result = cursor.fetchall()
            
            if len(result) != 1:
                return None
            
            game = f.Game(result[0][0], tz_aware(result[0][1]), team, leagues[result[0][2]])
            
            # Fetch all odds from game
            cursor.execute("SELECT site_name, value, date FROM odd WHERE game_name = (%s) AND game_date = (%s);", (game.name, to_utc(game.date)))
            results = cursor.fetchall()
            
            # sort by date
            results.sort(key=lambda x: x[2])
            
            for site_name, odd_value, odd_datetime in results:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    game.addOdd(float(odd_value), tz_aware(odd_datetime), site)
            
            # Fetch game's ids
            cursor.execute("SELECT site_name, id0, id1 FROM game_id WHERE game_name = (%s) AND game_date = (%s);", (game.name, to_utc(game.date)))
            results = cursor.fetchall()
            for site_name, game_id0, game_id1 in results:
                site = Sites.SiteFromName(site_name)
                if not site is None:
                    game.setId(site, (game_id0, game_id1))            
            
        return game
    
    def getAllTeams(self) -> List[f.Team]:
        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT name FROM team;")
            result = cursor.fetchall()
        
        all_teams = []
        
        for (team_name,) in result:
            all_teams.append(self.getTeam(team_name))
        
        return all_teams
    
    def registerLeague(self, league_name: str, league_color: int) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO league VALUES ((%s), (%s))", (league_name, league_color))
        
        except UniqueViolation:
            raise DrawfitError(DuplicateLeague(league_name))
        except ForeignKeyViolation:
            raise DrawfitError(InvalidColor(league_color))
    
    def registerTeam(self, team_name: str) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO team VALUES ((%s), true);", (team_name,))
        except UniqueViolation:
            raise DrawfitError(DuplicateTeam(team_name))
    
    def registerGame(self, team_name: str, game_name: str, game_date: datetime, league_name: str) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO game VALUES ((%s), (%s), (%s), (%s));", (team_name, game_name, game_date, league_name))
                
        except UniqueViolation as e:
            if game_name in e.pgerror:
                raise DrawfitError(GameAlreadyRegistered(game_name, str_dates(game_date)))
            else:
                raise DrawfitError(TeamAlreadyHasGame(team_name, str_dates(game_date)))
            
        except ForeignKeyViolation as e:
            if team_name in e.pgerror and league_name in e.pgerror:
                raise DrawfitError(TeamNotInLeague(team_name, league_name))
            elif team_name in e.pgerror:
                raise DrawfitError(TeamNotFound(team_name))
            else:
                raise DrawfitError(LeagueNotFound(league_name))
        
        except RaiseException as e:
            raise DrawfitError(e.pgerror)
    
    def registerOdd(self, game_name: str, game_date: datetime, site: Site, value: float, date: datetime):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO odd VALUES ((%s), (%s), (%s), (%s), (%s));", \
                    (game_name, game_date, site.value, value, date))
                
        except UniqueViolation:
            raise DrawfitError(DuplicateOdd(game_name, site.value, str_dates(date)))
        
        except ForeignKeyViolation as e:
            if game_name in e.pgerror:
                raise DrawfitError(GameNotFound(game_name, str_dates(game_date)))
            else:
                raise DrawfitError(SiteNotFound(site.value))
        
        except RaiseException as e:
            raise DrawfitError(e.pgerror)
    
    def addTeamToLeague(self, team_name: str, league_name: str) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO plays_in VALUES ((%s), (%s));", (team_name, league_name))
        
        except UniqueViolation:
            pass
        
        except ForeignKeyViolation as e:
            if team_name in e.pgerror:
                raise DrawfitError(TeamNotFound(team_name))
            else:
                raise DrawfitError(LeagueNotFound(league_name))
    
    def addLeagueCode(self, league_name: str, site: Site, code: str) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO league_code VALUES ((%s), (%s), (%s));", \
                        (league_name, site.value, code))
        
        except UniqueViolation as e:
            if league_name in e.pgerror:
                raise DrawfitError(DuplicateLeagueCode(league_name, site.value))
            else:
                raise DrawfitError(RepeatedSiteCode(site.value, code))
        
        except ForeignKeyViolation as e:
            if league_name in e.pgerror:
                raise DrawfitError(LeagueNotFound(league_name))
            else:
                raise DrawfitError(SiteNotFound(site.value))
    
    def updateLeagueColor(self, league_name: str, color: int) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("UPDATE league SET color=(%s) WHERE name=(%s)", (color, league_name))
    
    def updateLeagueCode(self, league_name: str, site: Site, code: str) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("UPDATE league_code SET code=(%s) WHERE league_name=(%s) AND site_name=(%s)", (code, league_name, site.value))
    
    def addTeamId(self, team_name: str, site: Site, id: str) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO team_id VALUES ((%s), (%s), (%s));", (team_name, site.value, id[0]))
        
        except UniqueViolation:
            raise DrawfitError(DuplicateTeamId(team_name, site.value))
        
        except ForeignKeyViolation as e:
            if team_name in e.pgerror:
                raise DrawfitError(TeamNotFound(team_name))
            else:
                raise DrawfitError(SiteNotFound(site.value))
    
    def addGameId(self, game_name: str, game_date: datetime, site: Site, id: Tuple[str, str]) -> NoReturn:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("INSERT INTO game_id VALUES ((%s), (%s), (%s), (%s), (%s));",\
                        (game_name, game_date, site.value, id[0], id[1]))
            
        except UniqueViolation:
            raise DrawfitError(DuplicateGameId(game_name, str_dates(game_date), site.value))
        
        except ForeignKeyViolation as e:
            if game_name in e.pgerror:
                raise DrawfitError(GameNotFound(game_name, str_dates(game_date)))
            else:
                raise DrawfitError(SiteNotFound(site.value))

    def updateGameDate(self, game: f.Game, new_date: datetime):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("UPDATE game SET date=(%s) WHERE name=(%s) AND date=(%s)", (new_date, game.name, to_utc(game.date)))
        
        except UniqueViolation as e:
            if game.name in e.pgerror:
                raise DrawfitError(GameAlreadyRegistered(game.name, str_dates(new_date)))
            else:
                raise DrawfitError(TeamAlreadyHasGame(game.team.name, str_dates(new_date)))
    
    def activateTeam(self, team_name: str) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("UPDATE team SET active=true WHERE name=(%s)", team_name)
    
    def deactivateTeam(self, team_name: str) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("UPDATE team SET active=false WHERE name=(%s)", team_name)
    
    def deleteGameIds(self, game: f.Game) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM game_id WHERE game_name=(%s) AND game_date=(%s)", (game.name, to_utc(game.date)))
    
    def deleteGameOdds(self, game: f.Game) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM odd WHERE game_name=(%s) AND game_date=(%s)", (game.name, to_utc(game.date)))
    
    def updateGameDate(self, game: f.Game, new_date: datetime) -> NoReturn:
        with self.db_connection.cursor() as cursor:
            cursor.execute("UPDATE game SET date=(%s) WHERE name=(%s) AND date=(%s)", (new_date, game.name, to_utc(game.date)))
