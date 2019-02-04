import csv

def write_full_data(csv_as_dict, path):

    with open(path, 'w') as f:
        w = csv.DictWriter(f, csv_as_dict[0].keys())
        w.writeheader()
        for row in csv_as_dict:
            w.writerow(row)