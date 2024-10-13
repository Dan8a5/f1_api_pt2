-- Insert Teams
INSERT INTO teams (name, country) VALUES
('Mercedes', 'Germany'),
('Red Bull Racing', 'Austria'),
('Ferrari', 'Italy'),
('McLaren', 'United Kingdom'),
('Aston Martin', 'United Kingdom'),
('Alpine', 'France'),
('Williams', 'United Kingdom'),
('AlphaTauri', 'Italy'),
('Alfa Romeo', 'Switzerland'),
('Haas F1 Team', 'United States');

-- Insert Drivers (with corresponding team_id)
INSERT INTO drivers (first_name, last_name, country, date_of_birth, team_id) VALUES
('Lewis', 'Hamilton', 'United Kingdom', '1985-01-07'::date, 1),
('George', 'Russell', 'United Kingdom', '1998-02-15'::date, 1),
('Max', 'Verstappen', 'Netherlands', '1997-09-30'::date, 2),
('Sergio', 'Perez', 'Mexico', '1990-01-26'::date, 2),
('Charles', 'Leclerc', 'Monaco', '1997-10-16'::date, 3),
('Carlos', 'Sainz', 'Spain', '1994-09-01'::date, 3),
('Lando', 'Norris', 'United Kingdom', '1999-11-13'::date, 4),
('Oscar', 'Piastri', 'Australia', '2001-04-06'::date, 4),
('Fernando', 'Alonso', 'Spain', '1981-07-29'::date, 5),
('Lance', 'Stroll', 'Canada', '1998-10-29'::date, 5),
('Esteban', 'Ocon', 'France', '1996-09-17'::date, 6),
('Pierre', 'Gasly', 'France', '1996-02-07'::date, 6),
('Alexander', 'Albon', 'Thailand', '1996-03-23'::date, 7),
('Logan', 'Sargeant', 'United States', '2000-12-31'::date, 7),
('Daniel', 'Ricciardo', 'Australia', '1989-07-01'::date, 8),
('Yuki', 'Tsunoda', 'Japan', '2000-05-11'::date, 8),
('Valtteri', 'Bottas', 'Finland', '1989-08-28'::date, 9),
('Zhou', 'Guanyu', 'China', '1999-05-30'::date, 9),
('Nico', 'Hulkenberg', 'Germany', '1987-08-19'::date, 10),
('Kevin', 'Magnussen', 'Denmark', '1992-10-05'::date, 10);

-- Insert Driver Rankings (example data; update with actual 2023 standings)
INSERT INTO driver_rankings (driver_id, points, position, wins) VALUES
(1, 306, 1, 3),
(2, 290, 2, 2),
(3, 210, 3, 1),
(4, 190, 4, 0),
(5, 180, 5, 0),
(6, 170, 6, 0),
(7, 160, 7, 0),
(8, 150, 8, 0),
(9, 140, 9, 0),
(10, 130, 10, 0),
(11, 120, 11, 0),
(12, 110, 12, 0),
(13, 100, 13, 0),
(14, 90, 14, 0),
(15, 80, 15, 0),
(16, 70, 16, 0),
(17, 60, 17, 0),
(18, 50, 18, 0),
(19, 40, 19, 0),
(20, 30, 20, 0);

-- Insert Constructor Standings (example data; update with actual 2023 standings)
INSERT INTO constructor_standings (team_id, points, position) VALUES
(1, 550, 1),
(2, 490, 2),
(3, 340, 3),
(4, 290, 4),
(5, 260, 5),
(6, 240, 6),
(7, 210, 7),
(8, 200, 8),
(9, 150, 9),
(10, 100, 10);
