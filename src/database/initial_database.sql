DROP TABLE IF EXISTS site cascade;
DROP TABLE IF EXISTS team cascade;
DROP TABLE IF EXISTS team_id cascade;
DROP TABLE IF EXISTS color cascade;
DROP TABLE IF EXISTS league cascade;
DROP TABLE IF EXISTS league_code cascade;
DROP TABLE IF EXISTS plays_in cascade;
DROP TABLE IF EXISTS game cascade;
DROP TABLE IF EXISTS odd cascade;


----------------------------------------
-- Table Creation
----------------------------------------

CREATE TABLE site(
    name        VARCHAR(80)     NOT NULL UNIQUE,

    CONSTRAINT  pk_website PRIMARY KEY(name)
);

CREATE TABLE team(
    name        VARCHAR(80)     NOT NULL UNIQUE,

    CONSTRAINT  pk_team PRIMARY KEY(name)
);

CREATE TABLE team_id(
    team_name   VARCHAR(80)     NOT NULL UNIQUE,
    site_name   VARCHAR(80)     NOT NULL UNIQUE,
    id          VARCHAR(80)     NOT NULL,

    CONSTRAINT pk_team_id       PRIMARY KEY(team_name, site_name),
    CONSTRAINT fk_team_id_team  FOREIGN KEY(team_name) REFERENCES team(name),
    CONSTRAINT fk_team_id_site  FOREIGN KEY(site_name) REFERENCES site(name)
);

CREATE TABLE color(
    name        VARCHAR(80)             NOT NULL UNIQUE,
    hex_code    INTEGER                 NOT NULL UNIQUE,

    CONSTRAINT pk_color PRIMARY KEY(name)
);

CREATE TABLE league(
    name            VARCHAR(80)     NOT NULL UNIQUE,
    color_name      VARCHAR(80)     NOT NULL,

    CONSTRAINT pk_league PRIMARY KEY(name),
    CONSTRAINT fk_league_color FOREIGN KEY(color_name) REFERENCES color(name)
);

CREATE TABLE league_code(
    league_name         VARCHAR(80)             NOT NULL UNIQUE,
    site_name           VARCHAR(80)             NOT NULL UNIQUE,
    code                VARCHAR(80)             NOT NULL,

    CONSTRAINT pk_league_code           PRIMARY KEY(league_name, site_name),
    CONSTRAINT fk_league_code_league    FOREIGN KEY(league_name) REFERENCES league(name),
    CONSTRAINT fk_league_code_site      FOREIGN KEY(site_name) REFERENCES site(name),
    CONSTRAINT u_league_code_site_code  UNIQUE (site_name, code)
);

CREATE TABLE plays_in(
    team_name           VARCHAR(80)             NOT NULL,
    league_name         VARCHAR(80)             NOT NULL,

    CONSTRAINT pk_plays_in          PRIMARY KEY(team_name, league_name),
    CONSTRAINT fk_plays_in_team     FOREIGN KEY(team_name) REFERENCES team(name),
    CONSTRAINT fk_plays_in_league   FOREIGN KEY(league_name) REFERENCES league(name)
);

CREATE TABLE game(
    name            VARCHAR(80)             NOT NULL,
    date            TIMESTAMPTZ             NOT NULL,
    team1_name      VARCHAR(80)             NOT NULL,
    team2_name      VARCHAR(80)             ,
    league_name     VARCHAR(80)             NOT NULL,

    CONSTRAINT pk_game          PRIMARY KEY(name, date),
    CONSTRAINT fk_game_team1    FOREIGN KEY(team1_name) REFERENCES team(name),
    CONSTRAINT fk_game_team2    FOREIGN KEY(team2_name) REFERENCES team(name),
    CONSTRAINT fk_game_league   FOREIGN KEY(league_name) REFERENCES league(name)
);

CREATE TABLE odd(
    game_name       VARCHAR(80)             NOT NULL,
    game_date       TIMESTAMPTZ             NOT NULL,
    site_name       VARCHAR(80)             NOT NULL,
    value           NUMERIC(4, 2)  NOT NULL,
    date            TIMESTAMPTZ             NOT NULL,

    CONSTRAINT pk_odd           PRIMARY KEY(game_name, game_date, site_name),
    CONSTRAINT fk_odd_game      FOREIGN KEY(game_name, game_date) REFERENCES game(name, date),
    CONSTRAINT fk_odd_site      FOREIGN KEY(site_name) REFERENCES site(name)
);


----------------------------------------
-- Integrity Constraints
----------------------------------------

DROP TRIGGER IF EXISTS check_odd_sampled_before_game_update_trigger ON odd;
DROP TRIGGER IF EXISTS check_odd_sampled_before_game_insert_trigger ON odd;

--(IC-1) An odd's datetime must be before the game's start datetime
CREATE OR REPLACE FUNCTION check_odd_sampled_before_game() 
RETURNS TRIGGER AS
$$
DECLARE unidades_var INTEGER;

BEGIN
    IF NEW.date >= NEW.game_date THEN
        RAISE EXCEPTION 'Tried adding/changing odd on game %.  The new (game_date, odd_date) pair is invalid: (%, %)',
                        NEW.game_name, NEW.game_date, New.date;
    END IF;

    RETURN new;
END
$$
LANGUAGE plpgsql;

CREATE TRIGGER check_odd_sampled_before_game_update_trigger 
BEFORE UPDATE OF game_date, date ON odd
FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE PROCEDURE check_odd_sampled_before_game();

CREATE TRIGGER check_odd_sampled_before_game_insert_trigger 
BEFORE INSERT ON odd
FOR EACH ROW
EXECUTE PROCEDURE check_odd_sampled_before_game();
