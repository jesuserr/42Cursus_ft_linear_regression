import sys
import csv
import matplotlib.pyplot as plt

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
    try:
        dataset_file = parse_arguments()
        dataset = read_dataset(dataset_file)
        print(dataset)
        plot(dataset)
    except ValueError as error:
        print(error)
        sys.exit(1)