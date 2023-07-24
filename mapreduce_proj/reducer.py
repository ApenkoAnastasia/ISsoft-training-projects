import sys
import argparse


def get_args():
    """Prepare and return arguments.

    Function for preparation of Namespace arguments.

    :return: list of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--N',
                        type=int,
                        help='set the number of top rated movies for each genre that are expected to be received.'
                             'syntax: [-N int]')
    args = parser.parse_args()

    return args


def reduce():
    """Reduce and print data.

    Reduce function that print results in necessary form.

    :return: genre and list of movies after catting them
    """
    reduced_items = []
    args = get_args()
    N = args.N

    for line in sys.stdin:
        key, values = line.split('\t')
        movies_of_each_genre = values.split("],")

        for movie in movies_of_each_genre:
            text = movie.split("',")
            title = text[0].replace('[', '').replace(']', '').replace("'", '').replace('"', '').rstrip('\r\n')
            year = text[1].replace('[', '').replace(']', '').replace(' ', '').replace("'", '').rstrip('\r\n')
            if N and len(reduced_items) >= N:
                continue
            else:
                reduced_items.append([title, year])

        for result_movie in reduced_items:
            yield key, ', '.join(result_movie)
        reduced_items = []


def main():

    field_names = 'genre, title, year'
    print(field_names)
    for key, values in reduce():
        print("{}, {}".format(key, str(values)))


if __name__ == "__main__":
    main()
