import matplotlib.pyplot as plt

# Plot dataset points
def plot(dataset, slope, intercept, regression):
    # For better experience in 42
    # plt.rcParams['font.size'] = 16
    # plt.figure(num='Linear Regression', figsize=(10.24, 7.68))
    plt.figure(num='Linear Regression')
    for point in dataset[1:]:
        plt.scatter(point[0], point[1], color='red')
    plt.xlabel(dataset[0][0])
    plt.ylabel(dataset[0][1])
    plt.title(f'{dataset[0][1]} = f({dataset[0][0]})')
    plt.grid(True)
    plot_line(dataset[1:], slope, intercept) if regression else None
    plt.show()

# Print regression line between two points [x1, y1],[x2, y2]
def plot_line(dataset, slope, intercept):
    x1 = min(point[0] for point in dataset)
    x2 = max(point[0] for point in dataset)
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept
    plt.plot([x1, x2], [y1, y2], color='blue', \
        label=f"y = {slope:.8f} * x + {intercept:.8f}")
    plt.legend()