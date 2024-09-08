import sys
import csv

# Parse command line arguments in case another dataset file is provided
def parse_arguments():
    if len(sys.argv) > 2:
        raise ValueError("Invalid number of arguments\n" +
        "usage: python3 trainer.py [dataset_file]\n" +
        "dataset_file default name: 'data.csv'")
    elif len(sys.argv) == 2:
        return sys.argv[1]
    return 'data.csv'

# Read dataset from file and convert it to a list of duples of floats
def read_dataset(dataset_file):
    try:
        with open(dataset_file, 'r') as file:
            reader = csv.reader(file)
            header_row = next(reader)
            dataset = []
            for row in reader:
                if len(row) != 2:
                    raise ValueError("Invalid dataset format")
                dataset.append([float(row[0]), float(row[1])])
        return dataset
    except OSError as e:
        raise ValueError(f"Error: {e}")

if __name__ == '__main__':
    try:
        dataset_file = parse_arguments()
        dataset = read_dataset(dataset_file)
        print(dataset)
    except ValueError as error:
        print(error)
        sys.exit(1)