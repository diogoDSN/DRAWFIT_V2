SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS websites;
DROP TABLE IF EXISTS leagues;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS listed_games;
DROP TABLE IF EXISTS game_participants;
DROP TABLE IF EXISTS league_variants;
DROP TABLE IF EXISTS team_variants;
DROP TABLE IF EXISTS odds;
SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE websites (
	name_website VARCHAR(20),
    PRIMARY KEY (name_website)
);

CREATE TABLE leagues (
	name_league VARCHAR(20),
    PRIMARY KEY (name_league)
);

CREATE TABLE games (
	id_game INTEGER,
    name_league VARCHAR(20) NOT NULL,
    game_date DATETIME NOT NULL,
    PRIMARY KEY (id_game),
    FOREIGN KEY (name_league) REFERENCES leagues(name_league)
);

CREATE TABLE teams (
	name_team VARCHAR(20),
    PRIMARY KEY (name_team)
);

CREATE TABLE  listed_games (
	id_game INTEGER,
    name_website VARCHAR(20),
    PRIMARY KEY (id_game, name_website),
    FOREIGN KEY (id_game) REFERENCES games(id_game),
    FOREIGN KEY (name_website) REFERENCES websites(name_website)
);

CREATE TABLE game_participants (
	id_game INTEGER,
    name_team VARCHAR(20),
    PRIMARY KEY (id_game, name_team),
    FOREIGN KEY (id_game) REFERENCES games(id_game),
    FOREIGN KEY (name_team) REFERENCES teams(name_team)
);

CREATE TABLE league_variants (
	name_league VARCHAR(20),
    name_website VARCHAR(20),
    cod_league VARCHAR(50) NOT NULL,
    cod_region VARCHAR(50),
    alt_league_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (name_league, name_website),
    FOREIGN KEY (name_league) REFERENCES leagues(name_league),
    FOREIGN KEY (name_website) REFERENCES websites(name_website)
);

CREATE TABLE team_variants (
	name_team VARCHAR(20),
    name_website VARCHAR(20),
    alt_team_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (name_team, name_website),
    FOREIGN KEY (name_team) REFERENCES teams(name_team),
    FOREIGN KEY (name_website) references websites(name_website)
);

CREATE TABLE odds (
	id_game INTEGER,
    name_website VARCHAR(20),
    date_odd DATETIME NOT NULL,
    val DECIMAL(4,2) NOT NULL,
    PRIMARY KEY (id_game, name_website, date_odd),
    FOREIGN KEY (id_game, name_website) REFERENCES listed_games(id_game, name_website)
);



