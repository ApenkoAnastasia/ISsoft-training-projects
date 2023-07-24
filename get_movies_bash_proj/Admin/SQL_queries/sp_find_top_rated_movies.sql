USE moviesDB;
DROP PROCEDURE IF EXISTS sp_find_top_rated_movies;
DELIMITER //
CREATE PROCEDURE sp_find_top_rated_movies(
IN n SMALLINT,
IN `regexp` VARCHAR(250),
IN year_from SMALLINT,
IN year_to SMALLINT,
IN genres VARCHAR(250)
)
BEGIN
	WITH rowed_movies AS (
	SELECT *, ROW_NUMBER() OVER(PARTITION BY moviesDB.movies.genre ORDER BY moviesDB.movies.rating DESC, moviesDB.movies.year DESC, moviesDB.movies.title) rn
	FROM moviesDB.movies
    WHERE 
		((year_from IS NULL) OR (moviesDB.movies.year >= year_from))
	AND ((year_to IS NULL) OR (moviesDB.movies.year <= year_to))
    AND ((`regexp` = '') OR (`regexp` IS NULL) OR (REGEXP_SUBSTR(moviesDB.movies.title, `regexp`) <> ''))
    AND ((genres IS NULL) OR (REGEXP_SUBSTR(moviesDB.movies.genre, genres) <> ''))
    )
    
    SELECT genre, title, year, rating
    FROM rowed_movies
    WHERE (n IS NULL) OR (rn <= n);
END//
DELIMITER ;
