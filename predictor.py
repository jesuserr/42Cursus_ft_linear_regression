import sys
import argparse
import json
from trainer import read_dataset
from utils import predictor_plot, GREEN, BLUE, RED, DEF

# Parse command line arguments (any thetas file name can be provided)
# Default thetas file name is 'data.json'
def parse_arguments():
    msg = "python3 predictor.py [thetas_file.json] [-p]\n"
    msg += "thetas_file default name: 'data.json'\n"
    msg += "[-p]: plot estimated value over linear regression\n"
    arg_parser = argparse.ArgumentParser(add_help=False, usage=msg)
    arg_parser.add_argument('thetas_file', type=str, nargs='?', \
        default='data.json')
    arg_parser.add_argument("-p", '--plot', action='store_true')
    args = arg_parser.parse_args()
    if any(arg.startswith('-') and len(arg) > 2 for arg in sys.argv[1:]):
        print("usage: " + msg)
        print("predictor.py: error: unrecognized arguments")
        sys.exit(1)
    return args

# Read thetas and labels from .json and return them
def read_thetas(thetas_file):
    print(f"Reading thetas from '{thetas_file}'... ", end="")
    try:
        with open(thetas_file, 'r') as file:
            values = json.load(file)
            theta0 = values.get('theta0')
            theta1 = values.get('theta1')
            labels = values.get('labels')
            if theta0 is None or theta1 is None:
                raise ValueError("Missing thetas in JSON file")
            if labels is None:
                raise ValueError("Missing labels in JSON file")
            theta0 = float(theta0)
            theta1 = float(theta1)
            labels = [str(label) for label in labels]
    except OSError as e:
        if e.errno == 2:
            print(f"\n'{thetas_file}' {RED}not found{DEF}, setting ", end="")
            print(f"default values {BLUE}\ntheta0 = 0\ntheta1 = 0{DEF}")
            return 0, 0, ["km","price"]
        else:
            raise ValueError(f"Error: {e}")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Invalid JSON format")
    except ValueError as e:
        raise ValueError(f"Error: {e}")
    print(f"{GREEN}OK{BLUE}")
    print(f"theta0 = {theta0:,.5f}\ntheta1 = {theta1:,.5f}{DEF}")
    return theta0, theta1, labels

# Calculate and print car price for a given mileage (subject mandatory part)
def calculate_price(theta0, theta1):
    while True:
        try:
            mileage = input("Please enter car mileage: ")
            mileage = float(mileage)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user")
            sys.exit(0)
    price = theta0 + theta1 * mileage
    print(f"Estimated price for a car with a mileage of ", end="")
    print(f"{BLUE}{mileage:,.2f}{DEF} km = {BLUE}{price:,.2f}{DEF} Euros")
    return mileage

# Calculate and print y for a given x (subject bonus part)
def calculate_custom(theta0, theta1, labels):
    while True:
        try:
            x = input(f"Please enter value of [{labels[0]}]: ")
            x = float(x)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user")
            sys.exit(0)
    y = theta0 + theta1 * x
    print(f"Estimated value of [{labels[1]}] for {BLUE}{x:,.2f}{DEF}", end="")
    print(f" [{labels[0]}] = {BLUE}{y:,.2f}{DEF} [{labels[1]}]")
    return x

if __name__ == '__main__':
    args = parse_arguments()
    try:
        theta0, theta1, labels = read_thetas(args.thetas_file)
        if labels[0] == 'km' and labels[1] == 'price':
            input_value = calculate_price(theta0, theta1)
        else:
            input_value = calculate_custom(theta0, theta1, labels)
        if args.plot and theta0 != 0 and theta1 != 0:
            filename = f"{args.thetas_file.split('.')[0]}.csv"
            dataset, norm_dataset = read_dataset(filename)
            estimation = theta0 + theta1 * input_value
            predictor_plot(dataset, theta1, theta0, input_value, estimation)
    except ValueError as error:
        print(error)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        sys.exit(0)