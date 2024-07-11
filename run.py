from cg2real import upscale
import argparse

def read_arguments():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('path_in', type=str, help='Input path')
    parser.add_argument('path_out', type=str, help='Output path')

    args = parser.parse_args()
    return args.path_in, args.path_out

if __name__ == "__main__":
    path_in, path_out = read_arguments()
    upscale(path_in, path_out)