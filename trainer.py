import sys

def parse_arguments():
    if (len(sys.argv) > 2):
        raise ValueError("Invalid number of arguments\n" +
        "usage: python3 trainer.py [dataset_file]\n" +
        "dataset_file default name: 'data.csv'")
    elif (len(sys.argv) == 2):
        return sys.argv[1]
    return ('data.csv')

if __name__ == '__main__':
    try:
        dataset_file = parse_arguments()
        print(dataset_file)
        print('I am the trainer')
    except ValueError as error:
        print(error)
        sys.exit(1)