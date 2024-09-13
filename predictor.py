import sys
import argparse
import json

# Constants for color codes
GREEN = '\033[92m'
DEF = '\033[0m'

# Parse command line arguments (any thetas file name can be provided)
# Default thetas file name is 'data.json'
def parse_arguments():
    msg = "python3 predictor.py [thetas_file.json] [-p]\n"
    msg += "thetas_file default name: 'data.json'\n"
    msg += "[-p]: plot point into original dataset\n"
    arg_parser = argparse.ArgumentParser(add_help=False, usage=msg)
    arg_parser.add_argument('thetas_file', type=str, nargs='?', default='data.json')
    arg_parser.add_argument("-p", '--plot', action='store_true')
    args = arg_parser.parse_args()
    if any(arg.startswith('-') and len(arg) > 2 for arg in sys.argv[1:]):
        print("usage: " + msg)
        print("predictor.py: error: unrecognized arguments")
        sys.exit(1)
    return args

def read_thetas(thetas_file):
    print(f"Reading thetas from '{thetas_file}'... ", end="")
    try:
        with open(thetas_file, 'r') as file:
            thetas = json.load(file)
            theta0 = thetas.get('theta0')
            theta1 = thetas.get('theta1')
            if theta0 is None or theta1 is None:
                raise ValueError("Missing thetas in JSON file")
            theta0 = float(theta0)
            theta1 = float(theta1)
    except OSError as e:
        if e.errno == 2:
            print(f"\n'{thetas_file}' not found, setting default values", end="")
            print(f"{GREEN}\ttheta0 = 0\t\ttheta1 = 0{DEF}")
            return 0, 0
        else:
            raise ValueError(f"Error: {e}")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Invalid JSON format")
    except ValueError as e:
        raise ValueError(f"Error: {e}")
    print(f"{GREEN}OK\t", end="")
    print(f"\ttheta0 = {theta0:.5f}\ttheta1 = {theta1:.5f}{DEF}")
    return theta0, theta1

if __name__ == '__main__':
    args = parse_arguments()
    try:
        theta0, theta1 = read_thetas(args.thetas_file)
    except ValueError as error:
        print(error)
        sys.exit(1)