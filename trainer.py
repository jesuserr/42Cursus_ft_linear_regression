import sys

if __name__ == '__main__':
    try:
        print('I am the trainer')
    except ValueError as error:
        print(error)
        sys.exit(1)