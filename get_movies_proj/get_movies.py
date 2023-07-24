import argparse
import csv
import re
import operator as opr
from sorted_movies import Movies as sm


Console_Output = 'console'
File_Output = 'file'
Ratings_Path = 'Datasets/ratings.csv'
Movies_Path = 'Datasets/movies.csv'


def modify_parser(parser):
    """Prepare arguments.  
    
    Function for preparation of Namespace arguments. 

    Keyword arguments:
    parser -- get an ArgumentParser object

    """
    parser.add_argument('--N', 
                        type=int,
                        help='set the number of top rated movies for each genre that are expected to be received.'
                        'syntax: [-N int]')

    parser.add_argument('--genres',
                        type=str,
                        help='set movies genres to choose.'
                        'syntax: [-genres "Comedy|Adventure|Action"]')

    parser.add_argument('--year_from',
                        type=int,
                        help='set a specific year from which the selection of movies will be started.'
                        'syntax: [-year_from int]')

    parser.add_argument('--year_to',
                        type=int,
                        help='set a specific year to which the selection of movies will be ended.'
                        'syntax: [-year_to int]')

    parser.add_argument('--regexp', 
                        type=str,
                        help='set regular expression for movies.'
                        'syntax: [-regexp yourRegEx]')

    parser.add_argument('--disp', 
                        choices=[Console_Output, File_Output],
                        default=Console_Output,  
                        type=str, 
                        help='set the way of displaying information.')

    return parser


def get_title_year(original_title):
    '''Form title and year.

    Function that return title and year from not parsed string.
    
    Keyword arguments:
    original_title -- string from args

    return -- title and year if they were set or None in other case
    
    '''
    original_title = original_title.replace('"', '').split('(')

    try:
        year = int(original_title[-1].replace(')',''))
    except:
        year = None

    if year is None:
        title = ''.join(original_title[:])
    else:
        title = ''.join(original_title[:-1]).replace(')', '').replace(',', '')

    return title, year


def get_genres(all_genres):
    '''Form list of distinct genres. 

    Function that return distinct genres from not parsed string of genres.
    
    Keyword arguments:
    all_genres -- list of all genres
  
    return -- list of distinct genres if they were set or None in other case.  

    '''
    if all_genres:
        distinct_genres = all_genres.split('|')
    else:
        distinct_genres = None

    return distinct_genres


def display_movies(arr_of_movies, arr_of_none, N):
    '''Display movie list.

    Function that display whole movie list or N-pieces of each genre if it were given.
    
    Keyword arguments:
    movies_arr -- array of movies which doesn't contain None in args
    none_arr -- array of movies which contain None in args
    N -- quantity of movies which will be displayed
    
    '''
    field_names = 'genre, title, year, rating'
    counter = 0

    sorted_movies = sorted(arr_of_movies, 
                    key=lambda x: (opr.attrgetter('genre')(x), -opr.attrgetter('rating')(x) 
                    if opr.attrgetter('rating')(x) is not None else opr.attrgetter('genre')(x)))
    if not N:
        N = len(sorted_movies) + len(arr_of_none)
 
    print(field_names)
    for movie in sorted_movies:
        if counter == 0:
           previous_genre = movie.genre
  
        if movie.genre != previous_genre:
            counter = 0
            previous_genre = movie.genre

        if counter < N and movie.genre == previous_genre:
            movie.show_all()
            counter += 1
        else:
            counter += 1
            continue

    for movie in arr_of_none:
        movie.show_all()


def get_dict_movie(args_genres, args):
    '''Form dictionary of movies.

    Function that return dictionary of movies with all requirements in args if they were given.
    
    Keyword arguments:
    args_genres -- list of parsed genres
    args -- arguments from Namespace

    return -- dictionary of movies
    
    '''
    dict_movie = dict()

    with open(Movies_Path, encoding="utf8") as csv_file:
        parsed_data = csv.DictReader(csv_file, delimiter=',')
        for row in parsed_data:
            movie_id = row.get('movieId') 
            title, year = get_title_year(row.get('title')) 

            if args.regexp and not (re.search(args.regexp, title)):
                continue

            if year is None:
                pass
            else:
                if args.year_from and not (year >= args.year_from):
                    continue

                if args.year_to and not (year <= args.year_to):
                    continue

            genres = get_genres(row.get('genres')) 
            if args_genres:
                if genres:
                    flags_genres = []
                    for genre in args_genres:
                        if (genre in genres):
                            flags_genres.append(True)
                        else:
                            flags_genres.append(False)
                
                    if not (any(flags_genres)):
                        continue
                
            if genres:
                dict_movie[movie_id] = {'genre' : sorted(genres)}
            else:
                dict_movie[movie_id] = {'genre' : None}
            dict_movie[movie_id]['title'] = title
            dict_movie[movie_id]['year'] = year

    return dict_movie


def get_average_ratings(dict_movie):
    '''Form dictionary of average ratings.

    Function that return dictionary of average ratings for movies which in dict_movie.
    
    Keyword arguments:
    dict_movie -- dictionary of movies with all args requirements

    return -- dictionary of average ratings
    
    '''
    movie_ratings = dict()
    with open(Ratings_Path, encoding="utf8") as csv_file:
        parsed_data = csv.DictReader(csv_file, delimiter=',')
        for row in parsed_data:
            movie_id = row.get('movieId') 
            rating = row.get('rating')
            
            if movie_id in dict_movie.keys():
                if movie_id in movie_ratings.keys():
                    arr_ratings = movie_ratings[movie_id]
                    arr_ratings[0] += 1                     
                    arr_ratings[1] += float(rating)          
                else:
                    movie_ratings[movie_id] = [1, float(rating)]

    average_ratings = dict()
    for movie_key in movie_ratings.keys():
        arr_ratings = movie_ratings.get(movie_key)
        average_ratings[movie_key] = round(arr_ratings[1] / arr_ratings[0], 2)

    return average_ratings


def get_joined_arr(dict_movie, average_ratings, args):
    '''Form array of joined dictionaries.

    Function that join dict_movie and average_ratings together on key-field 'movie_id'.
    This function create objects of certain strusture, make arrays of them and return arrays of movies and movies with None fields.
    
    Keyword arguments: 
    dict_movie -- dictionary of movies with all args requirements
    average_ratings -- dictionary of average ratings
    args -- arguments from Namespace

    return -- arrays of movies and movies with None fields
    
    '''
    for movie_id in dict_movie.keys():
        if movie_id not in average_ratings.keys():
            dict_movie[movie_id]['rating'] = None
        else:
            dict_movie[movie_id]['rating'] = average_ratings[movie_id]

    arr_of_movies = []
    arr_of_none = []

    for key in dict_movie.keys():
        genres = dict_movie[key]['genre']
        title = dict_movie[key]['title']
        year = dict_movie[key]['year']
        rating = dict_movie[key]['rating']

        if genres is None:
            genre = None
            movie = sm(genre, title, year, rating)
            arr_of_none.append(movie)
        else:
            for genre in genres:
                if not (args.genres) or (genre in (args.genres)):
                    movie = sm(genre, title, year, rating)
                    if (movie.genre and movie.rating and movie.title and movie.year) is None:
                        arr_of_none.append(movie)
                        continue
                    arr_of_movies.append(movie)

    return arr_of_movies, arr_of_none


def main():
    """Function that make dictionaries of movies, ratings, join them and display. """
    parser = argparse.ArgumentParser()

    parser = modify_parser(parser)

    args = parser.parse_args()

    args_genres = get_genres(args.genres)

    dict_movie = get_dict_movie(args_genres, args)
 
    average_ratings = get_average_ratings(dict_movie)
 
    arr_of_movies, arr_of_none = get_joined_arr(dict_movie, average_ratings, args)

    N = args.N

    display_movies(arr_of_movies, arr_of_none, N)


if __name__ == "__main__":
    main()