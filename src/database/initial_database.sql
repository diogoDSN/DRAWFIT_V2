----------------------------------------
-- Database Setup
----------------------------------------

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

----------------------------------------
-- Create Database and Connect
----------------------------------------

CREATE DATABASE drawfit WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';
\connect drawfit

----------------------------------------
-- Table Creation
----------------------------------------

CREATE TABLE site(
    name        VARCHAR(80)     NOT NULL UNIQUE,

    CONSTRAINT  pk_website PRIMARY KEY(name)
);

CREATE TABLE team(
    name        VARCHAR(80)     NOT NULL UNIQUE,
    active      BOOLEAN         NOT NULL,

    CONSTRAINT  pk_team PRIMARY KEY(name)
);

CREATE TABLE team_id(
    team_name   VARCHAR(80)     NOT NULL,
    site_name   VARCHAR(80)     NOT NULL,
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
    color_code      INTEGER         NOT NULL,

    CONSTRAINT pk_league PRIMARY KEY(name),
    CONSTRAINT fk_league_color FOREIGN KEY(color_code) REFERENCES color(hex_code)
);

CREATE TABLE league_code(
    league_name         VARCHAR(80)             NOT NULL,
    site_name           VARCHAR(80)             NOT NULL,
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
    team_name       VARCHAR(80)             NOT NULL,
    name            VARCHAR(80)             NOT NULL,
    date            TIMESTAMP               NOT NULL,
    league_name     VARCHAR(80)             NOT NULL,

    CONSTRAINT pk_game          PRIMARY KEY (team_name, date),
    CONSTRAINT game_name_date   UNIQUE (name, date),
    CONSTRAINT fk_game_team1    FOREIGN KEY(team_name) REFERENCES team(name),
    CONSTRAINT fk_game_league   FOREIGN KEY(league_name) REFERENCES league(name),
    CONSTRAINT fk_plays_in      FOREIGN KEY(team_name, league_name) REFERENCES plays_in(team_name, league_name)
);

CREATE TABLE game_id(
    game_name   VARCHAR(80)     NOT NULL,
    game_date   TIMESTAMP       NOT NULL,
    site_name   VARCHAR(80)     NOT NULL,
    id0         VARCHAR(80)     NOT NULL,
    id1         VARCHAR(80)     NOT NULL,

    CONSTRAINT pk_game_id       PRIMARY KEY(game_name, game_date, site_name),
    CONSTRAINT fk_game_id_game  FOREIGN KEY(game_name, game_date) REFERENCES game(name, date),
    CONSTRAINT fk_game_id_site  FOREIGN KEY(site_name) REFERENCES site(name)
);

CREATE TABLE odd(
    game_name       VARCHAR(80)             NOT NULL,
    game_date       TIMESTAMP               NOT NULL,
    site_name       VARCHAR(80)             NOT NULL,
    value           NUMERIC(4, 2)           NOT NULL,
    date            TIMESTAMP               NOT NULL,

    CONSTRAINT pk_odd           PRIMARY KEY(game_name, game_date, site_name, date),
    CONSTRAINT fk_odd_game      FOREIGN KEY(game_name, game_date) REFERENCES game(name, date),
    CONSTRAINT fk_odd_site      FOREIGN KEY(site_name) REFERENCES site(name)
);


----------------------------------------
-- Integrity Constraints
----------------------------------------

DROP TRIGGER IF EXISTS check_odd_sampled_before_game_update_trigger ON odd;
DROP TRIGGER IF EXISTS check_odd_sampled_before_game_insert_trigger ON odd;

--(IC-1) An odd's datetime must be before the game's start datetime--
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


DROP TRIGGER IF EXISTS check_only_current_game_update_trigger ON game;
DROP TRIGGER IF EXISTS check_only_current_game_insert_trigger ON game;

--(IC-2) Each team can only have one game registered in the future-- (update)
CREATE OR REPLACE FUNCTION check_only_current_game_update() 
RETURNS TRIGGER AS
$$
DECLARE unidades_var INTEGER;

BEGIN
    -- Checks if the inserted/updated game is in the future and if there exists another game in the future for the same team
    IF NEW.date > current_timestamp and 
       EXISTS(SELECT * FROM game WHERE team_name = NEW.team_name AND name != NEW.name AND date > current_timestamp) 
    THEN
        RAISE EXCEPTION 'Tried insertign/updating game %. The new games date is invalid: %. There is another current game for the same team.',
                        NEW.name, NEW.date;
    END IF;

    RETURN new;
END
$$
LANGUAGE plpgsql;


CREATE TRIGGER check_only_current_game_update_trigger 
BEFORE UPDATE OF date ON game
FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE PROCEDURE check_only_current_game_update();

--(IC-3) Each team can only have one game registered in the future-- (insert)
CREATE OR REPLACE FUNCTION check_only_current_game_insert() 
RETURNS TRIGGER AS
$$
DECLARE unidades_var INTEGER;

BEGIN
    -- Checks if the inserted/updated game is in the future and if there exists another game in the future for the same team
    IF NEW.date > current_timestamp and 
       EXISTS(SELECT * FROM game WHERE team_name = NEW.team_name AND date > current_timestamp) 
    THEN
        RAISE EXCEPTION 'Tried insertign/updating game %. The new games date is invalid: %. There is another current game for the same team.',
                        NEW.name, NEW.date;
    END IF;

    RETURN new;
END
$$
LANGUAGE plpgsql;

CREATE TRIGGER check_only_current_game_insert_trigger 
BEFORE INSERT ON game
FOR EACH ROW
EXECUTE PROCEDURE check_only_current_game_insert();

----------------------------------------
-- Role Creation
----------------------------------------

DROP ROLE IF EXISTS drawfit_bot;
CREATE ROLE drawfit_bot WITH LOGIN PASSWORD :drawfit_bot_pass;

GRANT SELECT                         ON color       TO drawfit_bot;
GRANT SELECT                         ON site        TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON game        TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON league      TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON league_code TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON odd         TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON plays_in    TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON team        TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON team_id     TO drawfit_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON game_id     TO drawfit_bot;

DROP ROLE IF EXISTS drawfit_read_only;
CREATE ROLE drawfit_read_only;

GRANT SELECT ON color       TO drawfit_read_only;
GRANT SELECT ON site        TO drawfit_read_only;
GRANT SELECT ON game        TO drawfit_read_only;
GRANT SELECT ON league      TO drawfit_read_only;
GRANT SELECT ON league_code TO drawfit_read_only;
GRANT SELECT ON odd         TO drawfit_read_only;
GRANT SELECT ON plays_in    TO drawfit_read_only;
GRANT SELECT ON team        TO drawfit_read_only;
GRANT SELECT ON team_id     TO drawfit_read_only;
GRANT SELECT ON game_id     TO drawfit_read_only;

-------------------------------
---- Sites
-------------------------------

INSERT INTO site VALUES ('Bwin')     ON CONFLICT DO NOTHING;
INSERT INTO site VALUES ('Betano')   ON CONFLICT DO NOTHING;
INSERT INTO site VALUES ('Betclic')  ON CONFLICT DO NOTHING;
INSERT INTO site VALUES ('Solverde') ON CONFLICT DO NOTHING;
INSERT INTO site VALUES ('Moosh')    ON CONFLICT DO NOTHING;
INSERT INTO site VALUES ('Betway')   ON CONFLICT DO NOTHING;


-------------------------------
---- Colors
-------------------------------

INSERT INTO color VALUES ('White',    16777215) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Red',      16711680) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Orange',   16740352) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Yellow',   16776960) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Cyan',      4379892) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Blue',      4416472) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Navy',          117) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Green',     3978315) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Lime',     12578629) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Mint',     11206595) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Pink',     15741670) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Purple',    8388736) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Lavender', 14466815) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Maroon',    8388608) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Olive',     8421376) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Apricot',  16767153) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Brown',    10117924) ON CONFLICT DO NOTHING;
INSERT INTO color VALUES ('Gray',      8421504) ON CONFLICT DO NOTHING;
