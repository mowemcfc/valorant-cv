import glob, os
import argparse
import errno

def main():
    parser = argparse.ArgumentParser(description='Splits dataset into test/train sets according to given ratio.')

    parser.add_argument('-i', '--input',
        required=True,
        default='../data/img/', help='Folder containing labelled JPEG images. default = ../data/img/'
    )
    parser.add_argument('-o', '--output',
        default='../data/', help='Output folder for test, train text files. default = ../data/'
    )
    parser.add_argument('-r', '--ratio', type=int,
        default=10, help='Percentage of dataset to be used as test data. default = 10 percent (ratio of test set)'
    )
    args = parser.parse_args()


    _split_dataset(args.input, args.output, args.ratio)


def _split_dataset(input_folder: str, output_folder: str, ratio: int) -> None:
    if not os.path.exists(os.path.dirname(output_folder)):
        try:
            os.makedirs(os.path.dirname(output_folder))
            print(os.path.dirname(output_folder))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
        
    __, _, files = next(os.walk(input_folder))
    input_count = len(files)
    test_boundary = input_count // ratio # start adding images to train set instead after this number

    train_filename = f"{output_folder}train.txt"
    test_filename = f"{output_folder}test.txt"
    with open(train_filename, 'w') as train_file, \
         open(test_filename, 'w') as test_file:

        for (i, input_file) in enumerate(glob.iglob(os.path.join(input_folder, '*.jpg'))):
            if i < test_boundary:
                test_file.write(input_file + '\n')
            else:
                train_file.write(input_file + '\n')


    

    



if __name__ == "__main__":

    main()