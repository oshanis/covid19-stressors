# Sample Python code for youtube.comments.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import sys
import csv
import pandas as pd
import googleapiclient.discovery
import youtube_init
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_comment_threads(youtube, video_id, comments=[], token=""):
    results = youtube.commentThreads().list(
        part="snippet",
        pageToken=token,
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    if "nextPageToken" in results:
        return get_comment_threads(youtube, video_id, comments, results["nextPageToken"])
    else:
        return comments

def get_comment_count_threads(youtube, video_id, comments_count=[], token=""):
    results = youtube.commentThreads().list(
        part="snippet",
        pageToken=token,
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        comment_count = item["snippet"]["topLevelComment"]
        like_count = comment_count["snippet"]["likeCount"]
        comments_count.append(like_count)

    if "nextPageToken" in results:
        return get_comment_count_threads(youtube, video_id, comments_count, results["nextPageToken"])
    else:
        return comments_count


# Call the API's comments.list method to list the existing comment replies.
# Not used - test method
def get_comments(youtube, parent_id):
  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  for item in results["items"]:
    author = item["snippet"]["authorDisplayName"]
    text = item["snippet"]["textDisplay"]
    print("Comment by %s: %s" % (author, text))

  return results["items"]

def get_statistics_views(youtube,video_id,token=""):
    response = youtube.videos().list(
    part='statistics, snippet',
    id=video_id).execute()

    view_count = response['items'][0]['statistics']['viewCount']
    like_count = response['items'][0]['statistics']['likeCount']
    dislike_count = response['items'][0]['statistics']['dislikeCount']
    return view_count,like_count,dislike_count

def main():
    youtube = youtube_init.init()

    df = pd.read_csv('youtube/data/videos.csv')
    video_ids = df.id
    
    for videoid in video_ids:
        video_comment_threads = get_comment_threads(youtube, videoid)
        video_comment_count_threads = get_comment_count_threads(youtube, videoid)
        a,b,c = get_statistics_views(youtube, videoid)
        sia = SentimentIntensityAnalyzer()
        filename = 'youtube/data/comments/'+videoid+'_data.csv'
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            #view counts , likes ,dislikes
            writer.writerow([a,b,c])
            for i in range(0,len(video_comment_threads)):
                comment = video_comment_threads[i]
                score = sia.polarity_scores(comment)
                comment_count = video_comment_count_threads[i]
                writer.writerow([comment,score["compound"],comment_count])

        print('Logged the sentiments of {0} comments to '+'youtube/data/comments/'+videoid+'_data.csv'.format(len(video_comment_threads)))

if __name__ == "__main__":
    main()