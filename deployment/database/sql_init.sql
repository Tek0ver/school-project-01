CREATE DATABASE vinci;

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    journal VARCHAR(50),
    title VARCHAR(255),
    article_date TIMESTAMP,
    link VARCHAR(255)
);

CREATE TABLE contents (
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL,
    content TEXT,
    nb_words INTEGER,
    FOREIGN KEY (article_id)
    REFERENCES articles (id)
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city VARCHAR (50),
    population_2022 INTEGER
);

CREATE TABLE content_cities (
    id SERIAL PRIMARY KEY,
    content_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    nb_occurence INTEGER,
    FOREIGN KEY (content_id)
    REFERENCES contents (id),
    FOREIGN KEY (city_id)
    REFERENCES cities (id)
);
