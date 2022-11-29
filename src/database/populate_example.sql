INSERT INTO league VALUES ('League1', 14466815);
INSERT INTO league VALUES ('League2', 8421504);
INSERT INTO league VALUES ('League3', 16711680);

INSERT INTO league_code VALUES ('League1', 'Bwin', '20,102848');
INSERT INTO league_code VALUES ('League1', 'Betano', '10210');
INSERT INTO league_code VALUES ('League1', 'Betclic', '30');
INSERT INTO league_code VALUES ('League1', 'Solverde', 'le,30000');
INSERT INTO league_code VALUES ('League1', 'Moosh', 'League');
INSERT INTO league_code VALUES ('League1', 'Betway', 'League');

INSERT INTO team VALUES ('Team1', true);
INSERT INTO team VALUES ('Team2', true);
INSERT INTO team VALUES ('Team3', false);

INSERT INTO team_id VALUES ('Team2', 'Bwin',     'Team Two');
INSERT INTO team_id VALUES ('Team2', 'Betano',   'Second Team');
INSERT INTO team_id VALUES ('Team2', 'Betclic',  'Team 2');
INSERT INTO team_id VALUES ('Team2', 'Solverde', 'Team 2');
INSERT INTO team_id VALUES ('Team2', 'Moosh',    'Team Two');
INSERT INTO team_id VALUES ('Team2', 'Betway',   'Team Two');

INSERT INTO plays_in VALUES ('Team1', 'League1');
INSERT INTO plays_in VALUES ('Team2', 'League1');
INSERT INTO plays_in VALUES ('Team2', 'League2');

INSERT INTO game VALUES ('Team2', 'Team2 vs Team4', '2022/12/31 12:00:00', 'League1');

INSERT INTO game_id VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Bwin',     'Team Two',    'Team4');
INSERT INTO game_id VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betano',   'Second Team', 'Team4');
INSERT INTO game_id VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betclic',  'Team 2',      'Team4');
INSERT INTO game_id VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Solverde', 'Team 2',      'Team4');
INSERT INTO game_id VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Moosh',    'Team Two',    'Team4');
INSERT INTO game_id VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betway',   'Team Two',    'Team4');

INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Bwin', 3.2, '2022/11/27 12:01:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Bwin', 2.8, '2022/11/27 12:03:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Bwin', 3.3, '2022/11/27 12:10:00');

INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betano', 1.5, '2022/11/27 12:00:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betano', 1.6, '2022/11/27 12:02:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betano', 1.5, '2022/11/27 12:04:00');

INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Moosh', 0.5, '2022/11/27 12:00:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Moosh', 1,   '2022/11/27 12:10:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Moosh', 1.5, '2022/11/27 12:20:00');

INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betclic',  1,   '2022/11/27 12:00:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Solverde', 1.3, '2022/11/27 12:00:00');
INSERT INTO odd VALUES ('Team2 vs Team4', '2022/12/31 12:00:00', 'Betway',   2.5, '2022/11/27 12:00:00');


