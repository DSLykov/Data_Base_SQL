-- Исполнитель
CREATE TABLE Artist (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Жанр
CREATE TABLE Genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Связь Исполнитель и Жанр
CREATE TABLE ArtistGenre (
    artist_id INT REFERENCES Artist(artist_id) ON DELETE CASCADE,
    genre_id INT REFERENCES Genre(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)
);

-- Альбом
CREATE TABLE Album (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT
);

-- Связь Исполнитель и Альбом
CREATE TABLE ArtistAlbum (
    artist_id INT REFERENCES Artist(artist_id) ON DELETE CASCADE,
    album_id INT REFERENCES Album(album_id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, album_id)
);

-- Трек
CREATE TABLE Track (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    album_id INT REFERENCES Album(album_id) ON DELETE CASCADE
);

-- Сборник
CREATE TABLE Compilation (
    compilation_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT
);

-- Связь Сборник и Трек
CREATE TABLE CompilationTrack (
    compilation_id INT REFERENCES Compilation(compilation_id) ON DELETE CASCADE,
    track_id INT REFERENCES Track(track_id) ON DELETE CASCADE,
    PRIMARY KEY (compilation_id, track_id)
);

-- Добавляем исполнителей
INSERT INTO Artist (name) VALUES
    ('Queen'),
    ('The Beatles'),
    ('Michael Jackson'),
    ('Led Zeppelin');

-- Добавляем жанры
INSERT INTO Genre (name) VALUES
    ('Rock'),
    ('Pop'),
    ('Metal');

-- Связываем исполнителей и жанры
INSERT INTO ArtistGenre (artist_id, genre_id) VALUES
    (1, 1), -- Queen -> Rock
    (2, 1), -- The Beatles -> Rock
    (2, 2), -- The Beatles -> Pop
    (3, 2), -- Michael Jackson -> Pop
    (4, 1), -- Led Zeppelin -> Rock
    (4, 3); -- Led Zeppelin -> Metal

-- Добавляем альбомы
INSERT INTO Album (title, release_year) VALUES
    ('A Night at the Opera', 1975),
    ('Abbey Road', 1969),
    ('Thriller', 1982);

-- Связываем исполнителей и альбомы
INSERT INTO ArtistAlbum (artist_id, album_id) VALUES
    (1, 1), -- Queen -> A Night at the Opera
    (2, 2), -- The Beatles -> Abbey Road
    (3, 3); -- Michael Jackson -> Thriller

-- Добавляем треки
INSERT INTO Track (title, duration, album_id) VALUES
    ('Bohemian Rhapsody', 355, 1), -- A Night at the Opera
    ('Love of My Life', 219, 1),   -- A Night at the Opera
    ('Come Together', 259, 2),     -- Abbey Road
    ('Here Comes the Sun', 185, 2),-- Abbey Road
    ('Thriller', 357, 3),          -- Thriller
    ('Beat It', 258, 3);           -- Thriller

-- Добавляем сборники
INSERT INTO Compilation (title, release_year) VALUES
    ('Best of Rock', 2020),
    ('Pop Hits', 2019),
    ('Classic Rock', 2018),
    ('80s Music', 2021);

-- Связываем сборники и треки
INSERT INTO CompilationTrack (compilation_id, track_id) VALUES
    (1, 1), -- Best of Rock -> Bohemian Rhapsody
    (1, 3), -- Best of Rock -> Come Together
    (2, 5), -- Pop Hits -> Thriller
    (2, 6), -- Pop Hits -> Beat It
    (3, 1), -- Classic Rock -> Bohemian Rhapsody
    (3, 4), -- Classic Rock -> Here Comes the Sun
    (4, 5), -- 80s Music -> Thriller
    (4, 6); -- 80s Music -> Beat It

-- Количество исполнителей в каждом жанре
SELECT g.name AS genre, COUNT(ag.artist_id) AS artist_count
FROM Genre g
LEFT JOIN ArtistGenre ag ON g.genre_id = ag.genre_id
GROUP BY g.name;

-- Количество треков, вошедших в альбомы 2019–2020 годов
SELECT COUNT(t.track_id) AS track_count
FROM Track t
JOIN Album a ON t.album_id = a.album_id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- Средняя продолжительность треков по каждому альбому
SELECT a.title AS album, AVG(t.duration) AS avg_duration
FROM Track t
JOIN Album a ON t.album_id = a.album_id
GROUP BY a.title;

-- Все исполнители, которые не выпустили альбомы в 2020 году
SELECT ar.name AS artist
FROM Artist ar
WHERE ar.artist_id NOT IN (
    SELECT aa.artist_id
    FROM ArtistAlbum aa
    JOIN Album a ON aa.album_id = a.album_id
    WHERE a.release_year = 2020
);

-- Названия сборников, в которых присутствует конкретный исполнитель
SELECT DISTINCT c.title AS compilation
FROM Compilation c
JOIN CompilationTrack ct ON c.compilation_id = ct.compilation_id
JOIN Track t ON ct.track_id = t.track_id
JOIN Album a ON t.album_id = a.album_id
JOIN ArtistAlbum aa ON a.album_id = aa.album_id
JOIN Artist ar ON aa.artist_id = ar.artist_id
WHERE ar.name = 'Queen';