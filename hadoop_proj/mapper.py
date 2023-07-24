import sys
import argparse
import re

Console_Output = 'console'
File_Output = 'file'


def modify_parser(parser):
    """Prepare arguments.

    Function for preparation of Namespace arguments.

    :param parser: get an ArgumentParser object
    :return: parser object
    """
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
    """Form title and year.

    Function that return title and year from not parsed string.

    :param original_title: string from args
    :return: title and year if they were set or None in other case
    """
    year = None

    for i in range(0, len(original_title)):
        original_title[i] = original_title[i].replace('"', '').replace('(', '').replace(')', '').replace('\r\n', '')
        digits = re.findall(r'\d\d\d\d+', original_title[i])

        if digits:
            year = str(digits[-1])
            original_title[i] = original_title[i].replace(year, '')

    title = ''.join(original_title[:])

    return title, year


def get_genres(all_genres):
    """Form list of distinct genres.

    Function that return distinct genres from not parsed string of genres.

    :param all_genres: list of all genres
    :return: list of distinct genres if they were set or None in other case.
    """
    if all_genres:
        distinct_genres = all_genres.split('|')
    else:
        distinct_genres = None

    return distinct_genres


def get_args():
    """Form list of arguments and genres.

    Function that return list of arguments, which where taken from command line, and list of splitted genres.

    :return: list of arguments, list of genres
    """
    parser = argparse.ArgumentParser()
    parser = modify_parser(parser)
    args = parser.parse_args()
    args_genres = get_genres(args.genres)

    return args, args_genres


def map(line_number, line):
    """Map for parse.

    Map function for parse part of dataset, which return key and value from movies dataset.

    :param line_number: part of block
    :param line: data for parsing
    :return: key which is string, value which is list
    """
    original_title = []
    parts = line.split(',')
    all_genres = get_genres(parts[-1])

    for word in parts[:-1]:
        if word.isdigit():
            continue
        original_title.append(word)

    title, year = get_title_year(original_title)
    args, args_genres = get_args()

    for genre in all_genres:
        genre = genre.replace('\r\n', '')
        if args.regexp and not (re.search(args.regexp, title)):
            continue
        if year is None:
            continue
        else:
            if args.year_from and not (int(year) >= args.year_from):
                continue

            if args.year_to and not (int(year) <= args.year_to):
                continue
        if args_genres and not (genre in args_genres):
            continue
        yield genre.rstrip("\r\n"), [title, year]


def main():

    for line_number, line in enumerate(sys.stdin):
        if line_number != 0:
            for key, value in map(line_number, line):
                print("{}\t{}".format(key, value))


if __name__ == "__main__":
    main()
