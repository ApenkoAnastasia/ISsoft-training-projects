USE stagingDB;
CREATE TABLE IF NOT EXISTS movies_with_distinct_genres (
	movieId INT NOT NULL,
	title VARCHAR(255) NOT NULL,
	year SMALLINT DEFAULT NULL,
	genre VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB, DEFAULT CHARSET=utf8mb4;