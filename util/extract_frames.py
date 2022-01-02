import argparse
import glob
import sys
from cv2 import cv2


# TODO: use absl? is it any better? need to explore
def main():
    parser = argparse.ArgumentParser(description='Extract frames from mp4 at set rate')

    parser.add_argument('-i', '--input',
        required=True, help='Input MP4 video path.'
    )
    parser.add_argument('-o', '--output',
        required=True, default='../output',
        help='Output folder for processed frames. default = \'../output\''
    )
    parser.add_argument('-r', '--rate', type=int,
        default=500, help='Millisecond interval at which to record frames. default = 500ms'
    )
    args = parser.parse_args()

    _process_image(args.input, args.output, args.rate)


# TODO: may want to consider a "smarter" form of choosing frames
def _process_image(input_video: str, output_folder: str, interval: int) -> None:
    video_capture = cv2.VideoCapture(input_video)
    frame_count = 0

    # Calculate total number of intervals that we will take a frame on
    total_frames = int(
        video_capture.get(cv2.CAP_PROP_FRAME_COUNT) // ( video_capture.get(cv2.CAP_PROP_FPS) * (interval / 1000) ) # pylint: disable=line-too-long
    )

    success = True
    while (success, image := video_capture.read()) and (frame_count <= total_frames):
        # Capture frames every `interval` milliseconds
        video_capture.set(cv2.CAP_PROP_POS_MSEC,
            (frame_count*interval)
        )
        success, image = video_capture.read()

        if cv2.imwrite(f"{output_folder}/frame{frame_count}.jpg", image):
            print(f"\r{frame_count}/{total_frames}", end=' ', flush=True)
            frame_count += 1
        else:
            print(f"Failed to save frame {frame_count}, exiting. " \
                "You may want to check if your output folder exists.")
            sys.exit(1)


if __name__ == "__main__":
    main()