#!/bin/bash

while (($#)); do

	case "$1" in 
		-h|--help)
			h_param=$1
			python3 ~/get_movies.py $h_param
			exit 1
			;;
		
		--N)
			if [ -n "$2" ]  && ! grep -q "^--" <<<  "$2" ; then 
				n_param=$1
				n_value=$2
				shift 2
			else 
				echo "Value for parameter $1 is missed. Enter get_movies.sh -h to get more information."
				exit 1
			fi 
			;;
			
		--regexp)
			if [ -n "$2" ]  && ! grep -q "^--" <<<  "$2" ; then 
				rx_param=$1
				rx_value=$2
				shift 2
			else 
				echo "Value for parameter $1 is missed. Enter get_movies.sh -h to get more information."
				exit 1
			fi 
			;;
			
		--genres)
			if [ -n "$2" ]  && ! grep -q "^--" <<<  "$2" ; then 
				gs_param=$1
				gs_value=$2
				shift 2
			else 
				echo "Value for parameter $1 is missed. Enter get_movies.sh -h to get more information."
				exit 1
			fi 
			;;
			
		--year_from)
			if [ -n "$2" ]  && ! grep -q "^--" <<<  "$2" ; then  
				yf_param=$1
				yf_value=$2
				shift 2
			else 
				echo "Value for parameter $1 is missed. Enter get_movies.sh -h to get more information."
				exit 1
			fi 
			;;
			
		--year_to)
			if [ -n "$2" ]  && ! grep -q "^--" <<<  "$2" ; then  
				yt_param=$1
				yt_value=$2
				shift 2
			else 
				echo "Value for parameter $1 is missed. Enter get_movies.sh -h to get more information."
				exit 1
			fi 
			;;
		
		*)
			echo "No reasonable parameters found. Error $OPTERR"
			echo "Enter get_movies.sh -h to get help information."
			exit 1
			;;
	esac
	
done 

cat ~/movies.csv \
| python3 ~/mapper.py $rx_param $rx_value \
					  $gs_param $gs_value \
					  $yf_param $yf_value \
					  $yt_param $yt_value \
| sort \
| python3 ~/shuffler_and_sorter.py \
| python3 ~/reducer.py $n_param $n_value