def parse_arguments():
    msg = "python3 trainer.py [dataset_file]\n"
    msg += "dataset_file default name: data.csv\n"
    arg_parser = argparse.ArgumentParser(add_help=False, usage=msg)
    arg_parser.add_argument('dataset_file', type=str, nargs='?', default='data.csv')
    args = arg_parser.parse_args()
    return args