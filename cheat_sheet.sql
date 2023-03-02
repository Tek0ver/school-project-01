-- select duplicates
SELECT title, article_date, link, count(*) 
FROM articles
GROUP BY title, article_date, link
HAVING count(*) > 1
;


-- delete by id 
DELETE FROM articles WHERE id > 8200;

-- reset auto-increment
ALTER SEQUENCE articles_id_seq RESTART WITH 8201;