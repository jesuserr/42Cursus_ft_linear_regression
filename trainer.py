import sys
import csv
import argparse
from plot import plot

LEARNING_RATE = 0.001

# Parse command line arguments (another dataset can be provided)
def parse_arguments():
    msg = "python3 trainer.py [dataset_file] [-p] [-r]\n"
    msg += "dataset_file default name: 'data.csv'\n"
    msg += "[-p]: plot original dataset\n"
    msg += "[-n]: plot normalized dataset\n"
    msg += "[-r]: plot linear regression"
    arg_parser = argparse.ArgumentParser(add_help=False, usage=msg)
    arg_parser.add_argument('dataset_file', type=str, nargs='?', default='data.csv')
    arg_parser.add_argument("-p", '--plot', action='store_true')
    arg_parser.add_argument("-n", '--normalized', action='store_true')
    arg_parser.add_argument('-r', '--regression', action='store_true')
    args = arg_parser.parse_args()
    if any(arg.startswith('-') and len(arg) > 2 for arg in sys.argv[1:]):
        print("usage: " + msg)
        print("trainer.py: error: unrecognized arguments")
        sys.exit(1)
    return args

# Read dataset from .csv file and creates two lists of duples of floats,
# first list 'dataset' contains the original values and second list
# 'norm_dataset' contains the normalized values between 0 and 1
def read_dataset(dataset_file):
    try:
        with open(dataset_file, 'r') as file:
            reader = csv.reader(file)
            dataset = []
            for index, row in enumerate(reader):
                if len(row) != 2:
                    raise ValueError("Invalid dataset format")
                if index == 0:
                    dataset.append([row[0], row[1]])
                else:
                    dataset.append([float(row[0]), float(row[1])])
        norm_dataset = [[point[0], point[1]] for point in dataset]
        max_x = max(point[0] for point in norm_dataset[1:])
        min_x = min(point[0] for point in norm_dataset[1:])
        max_y = max(point[1] for point in norm_dataset[1:])
        min_y = min(point[1] for point in norm_dataset[1:])
        for point in norm_dataset[1:]:
            point[0] = (point[0] - min_x) / (max_x - min_x)
            point[1] = (point[1] - min_y) / (max_y - min_y)
        return dataset, norm_dataset
    except OSError as e:
        raise ValueError(f"Error: {e}")

# TIMEOUT needed
def gradient_descent(norm_dataset, dataset):
    m_norm = b_norm = 0
    while(True):
        m_gradient = b_gradient = 0
        for point in norm_dataset:
            x = point[0]
            y = point[1]
            m_gradient += ((m_norm * x + b_norm) - y) * x
            b_gradient += ((m_norm * x + b_norm) - y)
        previous_m = m_norm
        previous_b = b_norm
        m_norm -= m_gradient * LEARNING_RATE / len(norm_dataset)
        b_norm -= b_gradient * LEARNING_RATE / len(norm_dataset)
        if previous_m == m_norm and previous_b == b_norm:
            break
    max_x = max(point[0] for point in dataset)
    min_x = min(point[0] for point in dataset)
    max_y = max(point[1] for point in dataset)
    min_y = min(point[1] for point in dataset)
    m = m_norm * (max_y - min_y) / (max_x - min_x)
    b = b_norm * (max_y - min_y) + min_y - m * min_x
    return (m, b)

if __name__ == '__main__':
    args = parse_arguments()
    try:
        dataset, norm_dataset = read_dataset(args.dataset_file)
        #plot(dataset) if args.plot else None
        #plot(norm_dataset) if args.normalized else None
        m, b = gradient_descent(norm_dataset[1:], dataset[1:])
        print(f"y = {m} * x + {b}")
        #gradient_descent(dataset[1:])
        #print(dataset)
    except ValueError as error:
        print(error)
        sys.exit(1)