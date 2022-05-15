import requests

class Spotify:
    def __init__(self, OAuth_Token):
        self.__auth = OAuth_Token
    
    def get_artist(self, artist_id):
        url = "https://api.spotify.com/v1/artists/{}".format(artist_id)
        headers = {"Authorization": "Bearer {}".format(self.__auth)}
        response = requests.get(url, headers=headers)
        response = response.json()
        return response['name']
    
    def get_track(self, music_id):
        url = "https://api.spotify.com/v1/tracks/{}".format(music_id)
        headers = {"Authorization": "Bearer {}".format(self.__auth)}
        response_get = requests.get(url, headers=headers)
        response = response_get.json()
        return {'name': response['name'], 'artist_id': response['artists'][0]['id'], 'artist_name': response['artists'][0]['name']}
