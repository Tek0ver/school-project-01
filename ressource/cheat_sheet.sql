-- select duplicates articles
SELECT link, count(*) 
FROM articles
GROUP BY link
HAVING count(*) > 1
;

-- select duplicates contents
SELECT MIN(id), MAX(article_id), count(*)
FROM contents
GROUP BY content
HAVING count(*) > 1
ORDER BY count(*) DESC
LIMIT 5
;

-- delete by id 
DELETE FROM articles WHERE id > 8200;

-- reset auto-increment
ALTER SEQUENCE articles_id_seq RESTART WITH 8201;

-- copy database
CREATE DATABASE targetdb 
WITH TEMPLATE sourcedb;


-- export table to csv
\copy articles TO '/home/tom/code/school-project-01/deployment/streamlit/streamlit/data-offline/articles.csv' DELIMITER ',' CSV HEADER;
\copy contents TO '/home/tom/code/school-project-01/deployment/streamlit/streamlit/data-offline/contents.csv' DELIMITER ',' CSV HEADER;
\copy content_cities TO '/home/tom/code/school-project-01/deployment/streamlit/streamlit/data-offline/content_cities.csv' DELIMITER ',' CSV HEADER;

-- didnt test but should work
\copy (SELECT * FROM articles) TO '/home/tom/code/school-project-01/deployment/streamlit/streamlit/data-offline/articles.csv' DELIMITER ',' CSV HEADER;
\copy (SELECT * FROM articles) to '/home/tom/code/school-project-01/deployment/streamlit/streamlit/data-offline/articles.csv' with csv


-- date, city, latitude, longitude
SELECT article_date, content_cities.city, latitude, longitude
FROM articles
JOIN contents ON articles.id = contents.article_id
JOIN content_cities ON contents.id = content_cities.content_id
JOIN geocity ON content_cities.city = geocity.city
WHERE '2022-01-01 06:44:00' < article_date AND article_date < '2024-01-01 06:44:00'
ORDER BY article_date
;