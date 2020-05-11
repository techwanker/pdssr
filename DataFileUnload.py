
from argparse import ArgumentParser


def main(args):

    record = {}

    if args.is_csv:
        print ('will emit CSV')
    if args.is_yaml or args.is_json:
        if args.is_json:
            print('will emit JSON')
        if args.is_yaml:
            print('will emit YAML')
        append_record_list(record)


def append_record_list(map):

    # add the map to the class list

    print ('map is ' + str(map))

if (__name__ == "__main__"):

    # TODO if no format is chosen use csv
    parser = ArgumentParser()
    parser.add_argument("-j", "--json", dest="is_json", default=False, help="export as JSON", action="store_true")
    parser.add_argument("-c", "--csv", dest="is_csv", default=False, help="export as CSV", action="store_true")
    parser.add_argument("-y", "--yaml", dest="is_yaml", default=False, help="export as CSV", action="store_true")

    args = parser.parse_args()

    main(args)
