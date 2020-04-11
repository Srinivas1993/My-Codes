import os
from apiclient.discovery import build 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re


os.environ['SPOTIPY_CLIENT_ID'] = '2feeff36bc3d4f57b2aa7961fa0d9b72'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'fa87923cb14747e1914016b3c7a6d2d5'
DEVELOPER_KEY = "AIzaSyDWGX6x3m8SBuSpLGXJAtpMcq1x0z-VyGo" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)
search_keyword = youtube_object.search().list(q = "Taylor Swift", part = "id, snippet", maxResults = 5,order="relevance").execute()
results = search_keyword.get("items", [])
response=[]
for search_result in results:
    if search_result["id"]["kind"]=="youtube#video":
        response.append(youtube_object.videos().list(part='statistics, snippet', id=search_result['id']['videoId']).execute()) 
youtube_Count=[]
for d in response:
    dict_Count={}
    for search in d['items']:
        if int(search['statistics']['viewCount']) >100000000:
            dict_Count['Video Title']=search['snippet']['title']
            dict_Count['No of Views']=int(search['statistics']['viewCount'])
            youtube_Count.append(dict_Count)
print("Youtube Search \n",youtube_Count)
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
spotify_search=[]
for video_name in youtube_Count:
    v_name = video_name['Video Title'].split('(')[0].strip()
    Spa_Name=re.sub('[^A-Za-z0-9 ]','',v_name)
    S_Name=Spa_Name.split()
    if len(S_Name) > 4:
        Orginal_Name=S_Name[:2]
        Orginal_Name=" ".join(Orginal_Name)
    else:
        Orginal_Name=' '.join(S_Name)
    Spotify_Results = sp.search(q=Orginal_Name, limit=20)
    for idx, track in enumerate(Spotify_Results['tracks']['items']):
        spotify_search.append((idx,track['name']))
print("Spotify Result \n",spotify_search)