import csv
import json


def to_aggregate(
        path='./data.csv',
        *,
        newline='',
        dialect='excel'
):
    data_dict = {}
    with open(path, 'r', newline=newline) as file:
        next(csv.reader(file, dialect=dialect))
        for line in csv.reader(file, dialect=dialect):
            country = data_dict.setdefault(
                line[0],
                {"people": [], "count": 0}
            )
            country['people'].append(line[1])
            country['count'] += 1

    return data_dict


def main():
    aggregated_data = to_aggregate()
    print(json.dumps(aggregated_data, indent=4))


if __name__ == '__main__':
    main()
