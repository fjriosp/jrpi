#!/usr/bin/python

import subprocess
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from config.youtube import *

def search(query):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=20,
    type='video'
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      video = {
        'id':    search_result['id']['videoId'],
        'title': search_result['snippet']['title'],
        'frame': search_result['snippet']['thumbnails']['default']['url'],
        'description': search_result['snippet']['description'],
      }
      videos.append(video)

  return videos

def getYoutubeUrl(video_id):
  return YOUTUBE_BASE_URL+video_id

def getStream(video_id):
  url = getYoutubeUrl(video_id)
  p = subprocess.Popen(['youtube-dl','-g',url], stdout=subprocess.PIPE, close_fds=True)
  stream = p.communicate()[0].split('\n',1)[0]
  stream = stream.replace("https://","http://")
  return stream
