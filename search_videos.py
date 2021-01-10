import json
import os

# Initialiaze
filtered_videos = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, 'videos_set')
BASE_URI = 'https://www.youtube.com/watch?v='
FLTR = 'python'


def retrieve_videos(file_name):
    with open(file_name, mode='r') as fd:
        videos = json.load(fd)
        for video in videos['items']:
            if FLTR in video['snippet']['title'].lower():
                filtered_videos.append(
                    (video['snippet']['title'], BASE_URI + video['id']))


def retrieve_files():
    return os.listdir(f'{BASE_DIR}/videos_set')


def main():
    for item in retrieve_files():
        retrieve_videos(os.path.join(VIDEOS_DIR, item))


if __name__ == "__main__":

    # Get all the videos from all the json files
    main()

    # Write all the videos in a txt file
    with open('videos.txt', mode='w') as fd:
        for video in filtered_videos:
            fd.write(f"{' -> '.join(video)}\n")
