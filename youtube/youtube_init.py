import os
import sys
import googleapiclient.discovery

def init():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = ""
    with open("youtube/youtube.credentials", "r") as credentials_file:
        DEVELOPER_KEY = credentials_file.readline()
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    return youtube
