#!/bin/bash
function check_connection {

	if mysql -u $USER -p$PASSWORD -e 'USE $DATABASE';then 
		return 0
	else 
		return 1
	fi
	
}

function setup_db {
	
	if check_connection $CHECK_CONNECTION -eq 0 ;
	then 
		echo "Connected succesfully."
	else 
		if [ -e ~/Datasets/ml-latest-small/ratings.csv -a -e ~/Datasets/ml-latest-small/movies.csv ]; then 
			echo "Files csv exists."
		elif [ -e /tmp/ml-latest-small.zip ]; then 
			unzip /tmp/ml-latest-small.zip \ml-latest-small/ratings.csv \ml-latest-small/movies.csv -d /tmp/Admin/Datasets 
			rm /tmp/ml-latest-small.zip
		else 
			wget -P /tmp https://files.grouplens.org/datasets/movielens/ml-latest-small.zip 
			unzip /tmp/ml-latest-small.zip \ml-latest-small/ratings.csv \ml-latest-small/movies.csv -d /tmp/Admin/Datasets 
			rm /tmp/ml-latest-small.zip
		fi 
		
		while read line 
		do
			mysql --local-infile=1 -u $USER -p$PASSWORD < "/tmp/Admin/SQL_queries/$line"
		done < /tmp/Admin/call_sql.txt
	fi 
	
}

while (($#)); do

	case "$1" in 
		--setupdb)
			setup_db 
			shift
			;;
			
		-h|--help)
			h_param=$1
			python3 /tmp/Client/get_movies.py $h_param
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
			
		--regex)
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

python3 /tmp/Client/get_movies.py $n_param $n_value $rx_param $rx_value $gs_param $gs_value $yf_param $yf_value $yt_param $yt_value