# -*- coding: utf-8 -*-

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "youtube_cred.json"
    next_page_token = ''

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    while True:
        request = youtube.videos().list(
            part="snippet",
            myRating="like",
            maxResults=50,
            pageToken=next_page_token
        )

        response = request.execute()

        # print(response)
        with open(f'videos_set/liked_videos_{next_page_token}.json', mode='w') as fd:
            json.dump(response, fd)

        # Take the token for the next page
        try:
            if response['nextPageToken']:
                next_page_token = response['nextPageToken']
        except Exception:
            break


if __name__ == "__main__":
    main()
