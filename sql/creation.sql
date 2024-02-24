-- Crear tabla Titles
CREATE TABLE Titles (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    type VARCHAR(50),
    description TEXT,
    release_year INT,
    age_certification VARCHAR(50),
    runtime INT,
    seasons INT,
    imdb_id VARCHAR(50),
    imdb_score FLOAT,
    imdb_votes INT,
    tmdb_popularity FLOAT,
    tmdb_score FLOAT
);

-- Crear tabla Genres
CREATE TABLE Genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- Crear tabla TitleGenres
CREATE TABLE TitleGenres (
    title_id VARCHAR(255),
    genre_id INT,
    PRIMARY KEY (title_id, genre_id),
    FOREIGN KEY (title_id) REFERENCES Titles (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres (id) ON DELETE CASCADE
);

-- Crear tabla ProductionCountries
CREATE TABLE ProductionCountries (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(10)
);

-- Crear tabla TitleCountries
CREATE TABLE TitleCountries (
    title_id VARCHAR(255),
    country_id INT,
    PRIMARY KEY (title_id, country_id),
    FOREIGN KEY (title_id) REFERENCES Titles (id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES ProductionCountries (id) ON DELETE CASCADE
);

-- Crear tabla Credits
CREATE TABLE Credits (
    person_id INT,
    title_id VARCHAR(255),
    name VARCHAR(255),
    character VARCHAR(255),
    role VARCHAR(50),
    PRIMARY KEY (person_id, title_id, role),
    FOREIGN KEY (title_id) REFERENCES Titles (id) ON DELETE CASCADE
);
