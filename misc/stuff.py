# First parser
def parse_arguments():
    msg = "python3 trainer.py [dataset_file]\n"
    msg += "dataset_file default name: data.csv\n"
    arg_parser = argparse.ArgumentParser(add_help=False, usage=msg)
    arg_parser.add_argument('dataset_file', type=str, nargs='?', default='data.csv')
    args = arg_parser.parse_args()
    return args

# Second parser (options for bonus where not taken into account)
# Parse command line arguments in case another dataset file is provided
def parse_arguments():
    if len(sys.argv) > 2:
        raise ValueError("Invalid number of arguments\n" +
        "usage: python3 trainer.py [dataset_file]\n" +
        "dataset_file default name: 'data.csv'")
    elif len(sys.argv) == 2:
        return sys.argv[1]
    return 'data.csv'


def gradient_descent_2(m_now, b_now, dataset, L):
    m_gradient = 0
    b_gradient = 0    
    for i in dataset:
        x = i[0]
        y = i[1]
        m_gradient += -(2/len(dataset)) * x * (y - (m_now * x + b_now))
        b_gradient += -(2/len(dataset)) * (y - (m_now * x + b_now))
    m = m_now - L * m_gradient
    b = b_now - L * b_gradient
    return m, b

#m = b = 0
#L = 0.0001
#epochs = 1000
#for i in range(epochs):
#    m, b = gradient_descent_2(m, b, dataset[1:], L)
#    print(f"y = {m} * x + {b}")

def mean_squared_error(dataset, m, b):
    error = 0
    for point in dataset:
        x = point[0]
        y = point[1]
        error += (y - (m * x + b)) ** 2
    return (error / len(dataset))

def gradient_descent(m_now, b_now, dataset):
    L = 0.01
    m_gradient = 0
    b_gradient = 0
    n = float(len(dataset))
    for i in dataset:
        x = i[0]
        y = i[1]
        m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
        b_gradient += -(2/n) * (y - (m_now * x + b_now))
    m = m_now - L * m_gradient
    b = b_now - L * b_gradient
    return [m, b]

def init_values(dataset, m, b):    
    x_max = x_min = dataset[0][0]
    y_for_x_max = y_for_x_min = dataset[0][1]
    for point in dataset:
        if point[0] > x_max:
            x_max = point[0]
            y_for_x_max = point[1]
        if point[0] < x_min:
            x_min = point[0]
            y_for_x_min = point[1]
    m = (y_for_x_max - y_for_x_min) / (x_max - x_min)
    b = y_for_x_max - m * x_max
    return m, b

def gradient_descent(dataset):
    m = b = 0
    for i in range(EPOCHS):
        m_gradient = b_gradient = 0
        for point in dataset:
            x = point[0]
            y = point[1]
            m_gradient += ((m * x + b) - y) * x
            b_gradient += ((m * x + b) - y)
        m -= m_gradient * LEARNING_RATE / len(dataset)
        b -= b_gradient * LEARNING_RATE / len(dataset)
    return (m, b)

def gradient_descent_2(dataset):
    m = b = 0
    i = 0
    while(True):    
        m_gradient = b_gradient = 0
        for point in dataset:
            x = point[0]
            y = point[1]
            m_gradient += ((m * x + b) - y) * x
            b_gradient += ((m * x + b) - y)
        previous_m = m
        previous_b = b
        m -= m_gradient * LEARNING_RATE / len(dataset)
        b -= b_gradient * LEARNING_RATE / len(dataset)
        if previous_m == m or previous_b == b:
            break
        i += 1
        print(f"i: {i} -> m: {m}, b: {b}")
    return (m, b)

# Normalize dataset to values between 0 and 1 for both x and y
def normalize_dataset(dataset):
    norm_dataset = [[point[0], point[1]] for point in dataset]
    max_x = max(point[0] for point in norm_dataset[1:])
    min_x = min(point[0] for point in norm_dataset[1:])
    max_y = max(point[1] for point in norm_dataset[1:])
    min_y = min(point[1] for point in norm_dataset[1:])
    for point in norm_dataset[1:]:
        point[0] = (point[0] - min_x) / (max_x - min_x)
        point[1] = (point[1] - min_y) / (max_y - min_y)
    return norm_dataset

# Denormalize thetas to dataset original values
def denormalize_thetas(dataset, m, b):
    max_x = max(point[0] for point in dataset)
    min_x = min(point[0] for point in dataset)
    max_y = max(point[1] for point in dataset)
    min_y = min(point[1] for point in dataset)
    m = m * (max_y - min_y) / (max_x - min_x)
    b = b * (max_y - min_y) + min_y - m * min_x
    return (m, b)    

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

def calculate_model_rmse(dataset, slope, intercept):
    print(f"Calculating RMSE... ", end="", flush=True)
    error = 0
    for point in dataset[1:]:
        x = point[0]
        y = point[1]
        error += (y - (slope * x + intercept)) ** 2
    rmse = (error / len(dataset)) ** 0.5
    print(f"{GREEN}OK{DEF}", flush=True)
    print(rmse)

print(f"{GREEN}OK\t\t R² = {r_squared:.4f}\t RMSE = {rmse:.4f}\t MAE = {mae:.4f}{DEF}", flush=True)
RED = '\033[91m'
print(f"{RED}KO\t{DEF}", end="")