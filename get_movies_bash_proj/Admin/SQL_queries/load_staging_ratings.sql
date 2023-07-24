USE stagingDB;
TRUNCATE TABLE stagingDB.staging_ratings;
SET GLOBAL local_infile = 'ON';
LOAD DATA LOCAL INFILE '/home/apenko/Labs/lab4/Admin/Datasets/ratings.csv'
INTO TABLE stagingDB.staging_ratings
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(@ignored, movieId, rating, @ignored);
