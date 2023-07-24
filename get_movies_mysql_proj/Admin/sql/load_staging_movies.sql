USE stagingDB;
TRUNCATE TABLE stagingdb.staging_movies;
SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'D:/Python_labs/lab_3/Admin/data/movies.csv'
INTO TABLE stagingdb.staging_movies
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(movieId, @title, genres)
SET title = SUBSTRING_INDEX(@title, '(', 1),
	year = SUBSTRING(@title FROM -5 FOR 4);