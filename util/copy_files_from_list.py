import argparse
import subprocess
import sys

# TODO: use absl? is it any better? need to explore
def main():
    parser = argparse.ArgumentParser(description='Copies files specified by text file from one folder into a separate folder')

    parser.add_argument('-i', '--input_folder',
        default = './media/extracted_frames',
        help='Folder containing files to be copied.'
    )
    parser.add_argument('-l', '--list',
        required=True,
        help='Text file containing newline-delimited filenames to be copied.'
    )
    parser.add_argument('-o', '--output_folder',
        default='../media/selected_frames',
        help='Output folder for selected files. default = ../media/selected_frames'
    )
    args = parser.parse_args()

    _move_selected_files(args.input_folder, args.list, args.output_folder)


def _move_selected_files(input_folder: str, list_path: str, output_folder: str) -> None:
    for file in open(list_path).read().split():
        input_path = f'{input_folder}/{file}'
        output_path = f'{output_folder}/{file}'
        try:
            subprocess.run(['cp', input_path, output_path], check=True)
        except subprocess.CalledProcessError:
            print(f"Error occured while attempting to copy {input_path} to {output_path}.\n" \
                "Exiting.")
            sys.exit(1)



if __name__ == "__main__":
    main()