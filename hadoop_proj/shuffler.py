import sys
from operator import itemgetter


def sorting(shuffled_items):
    """Sort by year, title.

    Function that sort movies by year firstly, and then by title.

    :param shuffled_items: list of movies
    """
    for i in range(0, len(shuffled_items)):
        shuffled_items[i][1] = sorted(shuffled_items[i][1], key=itemgetter(1), reverse=True)


def shuffle(num_reducers=5):
    """Shuffle to join on genres.

    Shuffle function which get each key and join to them movies. Also it split data into chunks for further algorithms..

    :param num_reducers: number of reducers
    :return: chunks of shuffled data
    """
    shuffled_items = []
    prev_key = None
    values = []

    try:
        for line in sys.stdin:
            key, value = line.split("\t")
            if key != prev_key and prev_key != None:
                shuffled_items.append([prev_key, values])
                values = []
            prev_key = key
            text = value.split(", '")
            title = text[0].replace('[', '').replace(']', '').replace("'", '').replace('"', '').replace('\r\n', '')
            year = int(text[1].replace('[', '').replace(']', '').replace("'", '').replace('\r\n', ''))
            values.append([title, year])
    except:
        pass
    finally:
        if prev_key != None:
            shuffled_items.append([key, values])

    sorting(shuffled_items)

    result = []
    num_items_per_reducer = len(shuffled_items) // num_reducers

    if len(shuffled_items) / num_reducers != num_items_per_reducer:
        num_items_per_reducer += 1
    for i in range(num_reducers):
        result.append(shuffled_items[num_items_per_reducer * i:num_items_per_reducer * (i + 1)])

    return result


def main():

    for group in shuffle():
        for key, values in group:
            print("{}\t{}".format(key, str(values)))


if __name__ == "__main__":
    main()
