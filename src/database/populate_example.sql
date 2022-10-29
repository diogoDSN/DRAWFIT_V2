INSERT INTO league VALUES ('PT', 4379892);
INSERT INTO league VALUES ('BR',     117);

INSERT INTO team VALUES ('Benfica',  true);
INSERT INTO team VALUES ('Porto',   false);
INSERT INTO team VALUES ('Sporting', true);

INSERT INTO plays_in VALUES ('Benfica',  'PT');
INSERT INTO plays_in VALUES ('Porto',    'PT');
INSERT INTO plays_in VALUES ('Sporting', 'PT');

INSERT INTO game VALUES ('Benfica',   'my_game', '2023-01-01T00:00:00Z', 'PT');
INSERT INTO game VALUES ('Benfica', 'your_game', '2022-09-01T12:30:20Z', 'PT');

INSERT INTO odd VALUES ('my_game', '2023-01-01T00:00:00Z', 'Bwin', 3.5, '2022-12-15T00:00:00Z');
INSERT INTO odd VALUES ('my_game', '2023-01-01T00:00:00Z', 'Bwin', 3.5, '2022-12-14T00:00:00Z');