USE moviesDB;
CREATE TABLE IF NOT EXISTS movies AS 
SELECT m.movieId, m.title, m.year, m.genre, ROUND(AVG(r.rating), 3) AS rating
FROM stagingDB.movies_with_distinct_genres AS m 
LEFT JOIN stagingDB.staging_ratings AS r
ON m.movieId = r.movieId
GROUP BY m.movieId, m.title, m.year, m.genre;