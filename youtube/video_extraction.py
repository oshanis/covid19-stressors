import argparse
import csv
import youtube_init

def get_video_ids(youtube, options):
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  videos = [('id','title')]
  channels = [('id','title')]
  playlists = [('id','title')]

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append((search_result['id']['videoId'],search_result['snippet']['title']))
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append((search_result['id']['channelId'],search_result['snippet']['title']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append((search_result['id']['playlistId'],search_result['snippet']['title']))

  write_to_file("videos", videos)
  write_to_file("channels", channels)
  write_to_file("playlists", playlists)

def write_to_file(type_of_data, data):
    with open('youtube/data/'+type_of_data+'.csv', 'w') as f:
        csv.writer(f).writerows(data)

def main():
    youtube = youtube_init.init()
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='coronavirus unemployment')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()
    get_video_ids(youtube, args)


if __name__ == "__main__":
    main()