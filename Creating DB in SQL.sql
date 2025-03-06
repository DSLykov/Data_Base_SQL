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