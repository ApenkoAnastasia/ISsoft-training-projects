USE stagingDB;
TRUNCATE TABLE stagingDB.movies_with_distinct_genres;
DROP PROCEDURE IF EXISTS split_genres;
DELIMITER //
CREATE PROCEDURE split_genres()
BEGIN
	INSERT INTO stagingDB.movies_with_distinct_genres (movieId, title, year, genre)
		WITH RECURSIVE cte(movieId, title, year, genre, tail) AS 
		(
			SELECT movieId, title, year, SUBSTRING_INDEX(genres, '|', 1) AS genre, SUBSTRING(genres, LENGTH(SUBSTRING_INDEX(genres, '|', 1)) + 2) AS tail
			FROM stagingdb.staging_movies
			UNION ALL
			SELECT movieId, title, year, SUBSTRING_INDEX(tail, '|', 1) AS genre, SUBSTRING(tail, LENGTH(SUBSTRING_INDEX(tail, '|', 1)) + 2) AS tail
			FROM cte
			WHERE tail <> ''
		)
		SELECT movieId, title, year, genre  
        FROM cte 
        ORDER BY movieId, genre;
END//
DELIMITER ;
CALL split_genres();