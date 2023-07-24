import argparse
import mysql.connector as mc
from mysql.connector.constants import ClientFlag


Console_Output = 'console'
File_Output = 'file'
Delimiter = ', '


def modify_parser(parser):
    """Prepare arguments.  
    
    Function for preparation of Namespace arguments. 

    Keyword arguments:
    parser -- get an ArgumentParser object

    """
    parser.add_argument('--N', 
                        type=int,
                        help='set the number of top rated movies for each genre that are expected to be received.'
                        'syntax: [--N int]')

    parser.add_argument('--genres',
                        type=str,
                        help='set movies genres to choose.'
                        'syntax: [--genres "Comedy|Adventure|Action"]')

    parser.add_argument('--year_from',
                        type=int,
                        help='set a specific year from which the selection of movies will be started.'
                        'syntax: [--year_from int]')

    parser.add_argument('--year_to',
                        type=int,
                        help='set a specific year to which the selection of movies will be ended.'
                        'syntax: [--year_to int]')

    parser.add_argument('--regexp', 
                        type=str,
                        help='set regular expression for movies.'
                        'syntax: [--regexp yourRegEx]')

    parser.add_argument('--disp', 
                        choices=[Console_Output, File_Output],
                        default=Console_Output,  
                        type=str, 
                        help='set the way of displaying information.')

    return parser


def display_movies(cursor, delimiter):
    '''Display movie list.

    Function that display whole movie list or N-pieces of each genre if it were given.
    
    Keyword arguments:
    cursor -- cursor which store the connection object
    delimiter -- set delimiter for data which will be displayed
   
    '''
    columns = ['genre', 'title', 'year', 'rating']
    header = ', '.join(columns)
    print(header)
    
    for result in cursor.stored_results():
            data = result.fetchall()

    for column in range(0, len(data)):
        row = ''
        for value in range(0, len(data[column])):
            row += str(data[column][value]) + delimiter

        print(row[:-2])


def get_config():
    '''Get data to connection.

    Function that return dictionary of config data.
    
    return -- dictionary of config data
   
    '''
    config = {}
    with open('/Client/config.txt', 'r') as file:
        for line in file.readlines():
            data = line.strip().split(Delimiter)
            config[data[0]] = ''.join(data[1:])

    return config


def main():
    """Function that take and parse arguments, connect to MySQL database, call procedure for select movies and display result. """
    parser = argparse.ArgumentParser()

    parser = modify_parser(parser)

    args = parser.parse_args()

    config = get_config()

    cnx = mc.connect(**config, client_flags=[ClientFlag.LOCAL_FILES])
    
    cursor = cnx.cursor()

    args_for_sp = [args.N, args.regexp, args.year_from, args.year_to, args.genres]

    cursor.callproc('sp_find_top_rated_movies', args_for_sp)

    delimiter = ', '

    display_movies(cursor, delimiter)

    cursor.close()
    
    cnx.close()


if __name__ == "__main__":
    main()