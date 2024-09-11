import sys
import csv
import argparse
import time
import json
from plot import plot

LEARNING_RATE = 0.001
GREEN = '\033[92m'
DEF = '\033[0m'

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
    print(f"Parsing data... ", end="", flush=True)
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
        print(f"{GREEN}OK{DEF}", flush=True)
        return dataset, norm_dataset
    except OSError as e:
        raise ValueError(f"Error: {e}")

# Calculates linear regression using gradient descent on normalized
# dataset and returns denormalized slope 'm' and intercept 'b'
def gradient_descent(norm_dataset, dataset, timeout = 30):
    print(f"Calculating Linear Regression... ", end="", flush=True)
    timeout_start_time = time.time()
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
        if abs(previous_m - m_norm) < 1e-20 and abs(previous_b - b_norm) < 1e-20:
            break
        if (time.time() - timeout_start_time) > timeout:
            raise ValueError(f"Error: Maximum calculation time exceeded")
    max_x = max(point[0] for point in dataset)
    min_x = min(point[0] for point in dataset)
    max_y = max(point[1] for point in dataset)
    min_y = min(point[1] for point in dataset)
    slope = m_norm * (max_y - min_y) / (max_x - min_x)
    intercept = b_norm * (max_y - min_y) + min_y - slope * min_x
    print(f"{GREEN}OK{DEF}", flush=True)
    write_json_data(slope, intercept)
    return (slope, intercept)

def write_json_data(slope, intercept):
    data = {"theta1": slope, "theta0": intercept}
    filename = args.dataset_file.split('.')[0]
    print(f"Exporting thetas to '{filename}.json'... ", end="", flush=True)
    try:
        with open(f"{filename}.json", 'w') as file:
            json.dump(data, file)
    except OSError as e:
            raise ValueError(f"Error: {e}")
    print(f"{GREEN}OK{DEF}", flush=True)

if __name__ == '__main__':
    args = parse_arguments()
    try:
        dataset, norm_dataset = read_dataset(args.dataset_file)
        slope, intercept = gradient_descent(norm_dataset[1:], dataset[1:])
        plot(dataset, slope, intercept, args.regression) if args.plot else None
    except ValueError as error:
        print(error)
        sys.exit(1)

    #TODO: plot cost function