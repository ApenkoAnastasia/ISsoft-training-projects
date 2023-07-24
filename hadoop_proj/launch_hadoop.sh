#!/bin/bash

if [ -e /tmp/Datasets/ml-latest-small/movies.csv ]; then 
	echo "File csv exists."
elif [ -e /tmp/ml-latest-small.zip ]; then 
	unzip /tmp/ml-latest-small.zip \ml-latest-small/movies.csv -d /tmp/Datasets 
	rm /tmp/ml-latest-small.zip
else 
	wget -P /tmp https://files.grouplens.org/datasets/movielens/ml-latest-small.zip 
	unzip /tmp/ml-latest-small.zip \ml-latest-small/movies.csv -d /tmp/Datasets 
	rm /tmp/ml-latest-small.zip
fi 

hdfs dfs -mkdir /tmp/Input
hdfs dfs -put /tmp/Datasets/ml-latest-small/movies.csv /tmp/Input

$HADOOP_HOME/bin/hadoop jar/usr/hdp/2.6.5.0-292/hadoop-mapreduce/hadoop-streaming.jar \
-D mapred.map.tasks=3 \
-D mapred.reduce.tasks=2 \
-input /tmp/Input/movies.csv \
-output /tmp/Output \
-file ~/tmp/mapper.py ~/tmp/reducer.py \
-mapper "python3 mapper.py --regexp Kingdom --genres 'Children|Animation|Fantasy' --year_from 1996 --year_to 2005 " -reducer "python3 reducer.py --N 4"

hdfs dfs -cat /tmp/Output/*

hdfs dfs -rm /tmp/Output/*
hdfs dfs -rmdir /tmp/Output