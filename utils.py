import matplotlib.pyplot as plt

GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
DEF = '\033[0m'

# Plot dataset points and regression line (trainer program)
def plot(dataset, slope, intercept, regression, norm_set):
    # For better experience in 42 School's Macs
    # plt.rcParams['font.size'] = 16
    # plt.figure(num='Linear Regression', figsize=(10.24, 7.68))
    plt.figure(num='Linear Regression')
    for point in dataset[1:]:
        plt.scatter(point[0], point[1], color='red')
    plt.xlabel(dataset[0][0])
    plt.ylabel(dataset[0][1])
    if norm_set:
        plt.title(f'{dataset[0][1]} = f({dataset[0][0]})\n[Normalized Values]')
    else:
        plt.title(f'{dataset[0][1]} = f({dataset[0][0]})\n[Original Values]')
    plt.grid(True)
    plot_line(dataset[1:], slope, intercept) if regression else None
    plt.show()

# Plot dataset points, regression line and estimated point (predictor program)
def predictor_plot(dataset, slope, intercept, x, y):
    # For better experience in 42 School's Macs
    # plt.rcParams['font.size'] = 16
    # plt.figure(num='Linear Regression', figsize=(10.24, 7.68))
    plt.figure(num='Linear Regression')
    for point in dataset[1:]:
        plt.scatter(point[0], point[1], color='red')
    plt.xlabel(dataset[0][0])
    plt.ylabel(dataset[0][1])
    plt.title(f'{dataset[0][1]} = f({dataset[0][0]})\n[Original Values]')
    plt.grid(True)
    plot_line(dataset[1:], slope, intercept)
    plt.scatter(x, y, color='green', label=f"x = {x:.2f}, y = {y:.2f}", \
        marker='*', s=150)
    plt.legend()
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

# Calculates four metrics to have an overall view of the model accuracy
# R²: Coefficient of determination, RMSE: Root Mean Squared Error,
# MAE: Mean Absolute Error, RSE: Residual Standard Error
def model_metrics(dataset, slope, intercept):
    print(f"Calculating model metrics... ", end="")
    if slope == 0:
        print(f"{GREEN}OK{BLUE}\nR² = N/A\nRMSE = 0\nMAE = 0\nRSE = 0{DEF}")
        return
    y_mean = sum(point[1] for point in dataset) / len(dataset)
    residual_sum_of_squares = total_sum_of_squares = abs_error = 0
    for point in dataset:
        x = point[0]
        y = point[1]
        residual_sum_of_squares += (y - (slope * x + intercept)) ** 2
        total_sum_of_squares += (y - y_mean) ** 2
        abs_error += abs(y - (slope * x + intercept))
    r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares)
    rmse = (residual_sum_of_squares / len(dataset)) ** 0.5
    mae = abs_error / len(dataset)
    rse = (residual_sum_of_squares / (len(dataset) - 2)) ** 0.5
    print(f"{GREEN}OK{BLUE}\nR² = {r_squared:.4f}\nRMSE = {rmse:,.4f}")
    print(f"MAE = {mae:,.4f}\nRSE = {rse:,.4f}{DEF}")