import os
import sys
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

def main():
    df = pd.read_csv('youtube/data/videos.csv')
    video_ids = df.id
    try:
        for video_id in video_ids:
            transcript = []
            line_list = YouTubeTranscriptApi.get_transcript(video_id)
            for line in line_list:
                transcript.append(line['text'])
            
            filename = 'youtube/data/transcripts/'+video_id+'.txt'
            with open(filename,'w') as f:
                f.write(' '.join(transcript))
    except TranscriptsDisabled as e:
        print("An error occurred:\n%s" % (e))

if __name__ == "__main__":
    main()