import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Column, Sequence
from sqlalchemy.ext.declarative import declarative_base

# Database Initialization
engine = create_engine('sqlite:///videos.sqlite', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Initialiaze
filtered_videos = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, 'videos_set')
BASE_URI = 'https://www.youtube.com/watch?v='
FLTR = 'python'


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(256))
    uri = Column(String(256))

    def __repr__(self):
        return f"<Video(name={self.name}, uri={self.uri})>"


# Utility functions
def create_table():
    try:
        Base.metadata.create_all(engine)
    except Exception:
        print("Table already exists!")


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
        create_table()
        retrieve_videos(os.path.join(VIDEOS_DIR, item))


if __name__ == "__main__":

    # Get all the videos from all the json files
    main()

    # Get old videos from database
    videos = [video[0] for video in session.query(Video.uri).all()]

    # Write all the videos in a txt file
    with open('videos.txt', mode='a') as fd:
        for video in filtered_videos:
            if video[1] not in videos:
                session.add(Video(name=video[0], uri=video[1]))
                fd.write(f"{' -> '.join(video)}\n")

    session.commit()
