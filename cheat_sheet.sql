-- select duplicates articles
SELECT link, count(*) 
FROM articles
GROUP BY link
HAVING count(*) > 1
;

-- select duplicates contents
SELECT content, count(*) 
FROM contents
GROUP BY content
HAVING count(*) > 1
;


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