import requests as rq
artist = str(input('Please enter the artists name --> '))
song_title = str(input('Please enter the song title --> '))
print(rq.get(f'https://api.lyrics.ovh/v1/{artist}/{song_title}').json()['lyrics']) if 'error' not in rq.get(f'https://api.lyrics.ovh/v1/{artist}/{song_title}').json() else print("Song could not be found.")