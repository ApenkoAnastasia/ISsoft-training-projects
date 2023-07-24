# Bash script to get top N most rated movies

## Description

Get_movies.sh is a bash script which automatically deploy the database, create tables with movies and ratings in them, load the corresponding data from csv-files, transform and load them into the final table. The utility also creates procedures for client requests and processing of original data.
Also this script allows to determine the top N most rated movies (by average rating) for each specified genre. It allows to set filters for the search: genres, regular expression, years from and to, as well as a number, showing how many movies of each genre to display.
At the same time, it sorts movies by genre and average ratings; in case of the same rating then sort by year and title. This utility connects to the MySQL database with movies ang display the necessary information.
## Installation
#### Requirements 
Get_movies.sh requires [Python](https://www.python.org/downloads/)  v3+ to run and MySQL on your computer.
Install MySQL Installer (recommended): When executing [MySQL Installer](https://dev.mysql.com/doc/refman/8.0/en/mysql-installer.html), choose MySQL Connector/Python as one of the products to install.

## Usage

In command line interpreter start programm.
Usage examples:

1)To get all movies sorted by genre and rating

```sh
$ /Client/get_movies.sh 
```  

It returns:
   
```sh
    genre, title, year, rating
    (no genres listed), ..., ..., ...
    ...
    Action, ..., ..., ...
    ...
    Adventure, ..., ..., ...
    ...
```
    
2)To get N most rated movies sorted by genre and rating
   
```sh
$ /Client/get_movies.sh --N 3
```
    
It returns:
    
```sh
    genre, title, year, rating
    (no genres listed), ..., ..., ...
    (no genres listed), ..., ..., ...
    (no genres listed), ..., ..., ...
    Action, ..., ..., ...
    Action, ..., ..., ...
    Action, ..., ..., ...
    Adventure, ..., ..., ...
    Adventure, ..., ..., ...
    Adventure, ..., ..., ...
    ...
```

3)To get movies satisfying a certain regular expression
    
```sh
$ /Client/get_movies.sh --regexp Kingdom
```
    
It returns:
    
```sh
    genre, title, year, rating
    Action , Forbidden Kingdom The  , 2008 , 3.83
    Action , Kingdom The  , 2007 , 3.81
    Action , Kingdom of Heaven  , 2005 , 3.5
    Action , Jurassic World: Fallen Kingdom  , 2018 , 3.25
    Action , Indiana Jones and the Kingdom of the Crystal Skull  , 2008 , 2.83
    Action , Wizards of the Lost Kingdom II  , 1989 , 0.5
    Adventure , Vovka in the Kingdom of Far Far Away  , 1965 , 5.0
    Adventure , Forbidden Kingdom The  , 2008 , 3.83
    Adventure , Jurassic World: Fallen Kingdom  , 2018 , 3.25
    Adventure , Indiana Jones and the Kingdom of the Crystal Skull  , 2008 , 2.83
    Adventure , 10th Kingdom The  , 2000 , 2.75
    ...
```
    
4)To get certain genre or genres

```sh
$ /Client/get_movies.sh --genres 'Animation|Romance'
```
    
It returns:

```sh
    genre, title, year, rating
    Animation, ..., ..., ...
    Animation, ..., ..., ...
    ...
    Romance, ..., ..., ...
    Romance, ..., ..., ...
    Romance, ..., ..., ...
    ...
``` 
    
5)To get movies by setting a specific year from which the selection of movies will be started

```sh
$ /Client/get_movies.sh --year_from 2005
```
    
It returns:

```sh
    genre, title, year, rating
    Animation, ..., 2005, ...
    ...
    Animation, ..., 2018, ...
    ..., ..., 2006, ...
    Romance, ..., 2020, ...
    ...
``` 

6)To get movies by setting a specific year to which the selection of movies will be ended

```sh
$ /Client/get_movies.sh --year_to 2005
```
    
It returns:

```sh
    genre, title, year, rating
    Animation, ..., 2005, ...
    ...
    Animation, ..., 1995, ...
    ..., ..., 1941, ...
    Romance, ..., 2003, ...
    ...
``` 
    
7)To get help message:

```sh
$ /Client/get_movies.sh  --help
```

Utility also allows to combine this filters in different ways. For example:
```sh
$ /Client/get_movies.sh --N 2 --regexp Beauty --genres 'Animation|Romance' --year_from 1993 --year_to 2002
```
It returns:
```sh
genre, title, year, rating
Animation , Beauty and the Beast: The Enchanted Christmas  , 1997 , 4.0
Romance , American Beauty  , 1999 , 4.06
```

If you want setup all necessary databases and tables, and download all csv-files then use ```--setupdb``` parameter:
```sh
$ /Client/get_movies.sh  --setupdb
```