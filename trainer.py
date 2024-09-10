import sys
import csv
import argparse
import matplotlib.pyplot as plt

# Parse command line arguments (another dataset can be provided)
def parse_arguments():
    msg = "python3 trainer.py [dataset_file] [-p] [-r]\n"
    msg += "dataset_file default name: 'data.csv'\n"
    msg += "[-p]: plot dataset\n"
    msg += "[-r]: plot linear regression"
    arg_parser = argparse.ArgumentParser(add_help=False, usage=msg)
    arg_parser.add_argument('dataset_file', type=str, nargs='?', default='data.csv')
    arg_parser.add_argument("-p", '--plot', action='store_true')
    arg_parser.add_argument('-r', '--regression', action='store_true')
    args = arg_parser.parse_args()
    if any(arg.startswith('-') and len(arg) > 2 for arg in sys.argv[1:]):
        print("usage: " + msg)
        print("trainer.py: error: unrecognized arguments")
        sys.exit(1)
    return args

# Read dataset from file and convert it to a list of duples of floats
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
        return dataset
    except OSError as e:
        raise ValueError(f"Error: {e}")

# Plot dataset points
def plot(dataset):
    plt.figure(num='Linear Regression')
    for point in dataset[1:]:
        plt.scatter(point[0], point[1], color='red')
    plt.xlabel(dataset[0][0])
    plt.ylabel(dataset[0][1])
    plt.title(f'{dataset[0][1]} = f({dataset[0][0]})')
    plt.grid(True)
    #plot_regression_line(dataset)
    plt.show()

# Plot regression line using numpy (testing purposes)
def plot_regression_line(dataset):
    import numpy as np
    x_values = [point[0] for point in dataset[1:]]
    y_values = [point[1] for point in dataset[1:]]
    slope, intercept = np.polyfit(x_values, y_values, 1)
    x_line = np.linspace(min(x_values), max(x_values), 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, color='blue', label='Regression Line')
    print(f"y = {slope} * x + {intercept}")

if __name__ == '__main__':
    args = parse_arguments()
    try:
        dataset = read_dataset(args.dataset_file)
        plot(dataset) if args.plot else None
    except ValueError as error:
        print(error)
        sys.exit(1)