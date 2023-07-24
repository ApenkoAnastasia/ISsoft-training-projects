USE stagingDB;
TRUNCATE TABLE stagingdb.staging_ratings;
SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'D:/Python_labs/lab_3/Admin/data/ratings.csv'
INTO TABLE stagingdb.staging_ratings
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(@ignored, movieId, rating, @ignored);