import sys

if __name__ == '__main__':
    try:
        print('I am the predictor')
    except ValueError as error:
        print(error)
        sys.exit(1)