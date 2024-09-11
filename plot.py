import matplotlib.pyplot as plt

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