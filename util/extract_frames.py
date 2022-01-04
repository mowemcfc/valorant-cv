import argparse
from glob import glob
from typing import List
import sys
from cv2 import cv2


# TODO: use absl? is it any better? need to explore
def main():
    parser = argparse.ArgumentParser(description='Extract frames from mp4 at set rate')

    parser.add_argument('-i', '--inputs',
        required=True, nargs='+',
        help='Space-delimited list of input MP4 files.'
    )
    parser.add_argument('-o', '--output',
        default='../output', help='Output folder for processed frames. default = ../output'
    )
    parser.add_argument('-r', '--rate', type=int,
        default=500, help='Millisecond interval at which to record frames. default = 500ms'
    )
    args = parser.parse_args()

    _process_input_videos(args.inputs, args.output, args.rate)


def _process_input_videos(input_list: List[str], output_folder: str, interval: int) -> None:
    for video in input_list:
        _split_video_into_frames(video, output_folder, interval)


# TODO: may want to consider a "smarter" form of choosing frames. maybe some form
#       of 'dumb' classifier for a brief run-through.
def _split_video_into_frames(input_video: str, output_folder: str, interval: int) -> None:
    video_capture = cv2.VideoCapture(input_video)
    frame_count = 0

    # frame count / fps * (interval / 1000) = total # of video frames
    total_frames = int(
        video_capture.get(cv2.CAP_PROP_FRAME_COUNT) // (video_capture.get(cv2.CAP_PROP_FPS) * (interval / 1000) ) # pylint: disable=line-too-long
    )

    success = True
    while (success, image := video_capture.read()) and (frame_count <= total_frames):
        # skip ahead by 1 interval and take a snapshot of frames 
        video_capture.set(cv2.CAP_PROP_POS_MSEC,
            (frame_count*interval)
        )
        success, image = video_capture.read()

        # Truncate extension and save frame as jpg image
        output_filename = input_video.split('/')[-1].split('.')[0] # "folder1/folder2/video.mp4" -> "video"
        output_path = f"{output_folder}{output_filename}{frame_count}.jpg" # "output_folder/video123.jpg"
        if cv2.imwrite(output_path, image):
            print(f"\r{input_video}: {frame_count}/{total_frames}", end=' ', flush=True) # "video.mp4: 12/245"
            frame_count += 1
        else:
            print(f"Failed to save frame {frame_count}, exiting. " \
                "You may want to check if your output folder exists.")
            sys.exit(1)


if __name__ == "__main__":
    main()
