from googleapiclient.discovery import build


# You must replace DEVELOPER_KEY with your own API key for this to work.
DEVELOPER_KEY = 'AIzaSyDo_fBwT1xBQLcsOFznE-pMvbuxMNVZNLQ'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(q=query, part='id,snippet', maxResults=5).execute()

    videos = []

    for search_result in search_response['items']:
        if search_result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': search_result['snippet']['title'],
                'video_id': search_result['id']['videoId']
            })

    if videos:
        return videos

    return search_multiple_vegan_recipes(query)

def search_multiple_vegan_recipes(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(q=query, part='id,snippet', maxResults=5).execute()

    videos = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': search_result['snippet']['title'],
                'video_id': search_result['id']['videoId']
            })

    return videos
