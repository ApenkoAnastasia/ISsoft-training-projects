USE stagingDB;
TRUNCATE TABLE stagingDB.staging_movies;
SET GLOBAL local_infile = 'ON';
LOAD DATA LOCAL INFILE '/home/apenko/Labs/lab4/Admin/Datasets/movies.csv'
INTO TABLE stagingDB.staging_movies
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(movieId, @title, genres)
SET title = SUBSTRING_INDEX(@title, '(', 1),
    year = SUBSTRING(@title FROM -5 FOR 4);
