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