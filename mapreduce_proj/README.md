# Bash script to get top N most rated movies with MapReduce features

## Description

Launch.sh is a bash script which supports arguments from command line and automatically starts mapper.py, shuffler.py and reducer.py with them. 
It represent MapReduce concept on single machine.

## Installation
#### Requirements 
Launch.sh requires [Python](https://www.python.org/downloads/)  v3+ to run and Bash.

## Usage

In command line interpreter start programm.
Usage examples:

1)To get all movies sorted by genre and rating

```sh
$ /launch.sh 
```  

It returns:
   
```sh
    genre, title, year
    (no genres listed), ..., ...
    ...
    Action, ..., ...
    ...
    Adventure, ..., ...
    ...
```
    
2)To get N most rated movies sorted by genre and rating
   
```sh
$ /launch.sh --N 3
```
    
It returns:
    
```sh
    genre, title, year
    (no genres listed), ..., ...
    (no genres listed), ..., ...
    (no genres listed), ..., ...
    Action, ..., ...
    Action, ..., ...
    Action, ..., ...
    Adventure, ..., ...
    Adventure, ..., ...
    Adventure, ..., ...
    ...
```

3)To get movies satisfying a certain regular expression
    
```sh
$ /launch.sh --regexp Kingdom
```
    
It returns:
    
```sh
    genre, title, year
    Action , Jurassic World: Fallen Kingdom  , 2018 
    Action , Forbidden Kingdom The  , 2008 
    Action , Kingdom The  , 2007 
    Action , Indiana Jones and the Kingdom of the Crystal Skull  , 2008 
    Action , Kingdom of Heaven  , 2005 
    Action , Wizards of the Lost Kingdom II  , 1989 
    Adventure , Jurassic World: Fallen Kingdom  , 2018 
    Adventure , Forbidden Kingdom The  , 2008 
    Adventure , Vovka in the Kingdom of Far Far Away  , 1965 
    Adventure , Indiana Jones and the Kingdom of the Crystal Skull  , 2008 
    Adventure , 10th Kingdom The  , 2000 
    ...
```
    
4)To get certain genre or genres

```sh
$ /launch.sh --genres 'Animation|Romance'
```
    
It returns:

```sh
    genre, title, year
    Animation, ..., ...
    Animation, ..., ...
    ...
    Romance, ..., ...
    Romance, ..., ...
    Romance, ..., ...
    ...
``` 
    
5)To get movies by setting a specific year from which the selection of movies will be started

```sh
$ /launch.sh --year_from 2005
```
    
It returns:

```sh
    genre, title, year
    Animation, ..., 2018
    ...
    Animation, ..., 2006
    ..., ..., 2005
    Romance, ..., 2020
    ...
``` 

6)To get movies by setting a specific year to which the selection of movies will be ended

```sh
$ /launch.sh--year_to 2005
```
    
It returns:

```sh
    genre, title, year
    Animation, ..., 2005
    ...
    Animation, ..., 1995
    ..., ..., 1941
    Romance, ..., 2003
    ...
``` 
    
7)To get help message:

```sh
$ /launch.sh  --help
```

Utility also allows to combine this filters in different ways. For example:
```sh
$ /launch.sh --N 2 --regexp Beauty --genres 'Animation|Romance' --year_from 1993 --year_to 2002
```
It returns:
```sh
genre, title, year
Animation , Beauty and the Beast: The Enchanted Christmas  , 1997 
Romance , American Beauty  , 1999 
```