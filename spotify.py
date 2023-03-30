import requests
import json
import base64

jsonSecrets = {}

#Get secret stuff
with open("/home/ubuntu/planPlay/secrets.json", "r") as secrets:
    jsonSecrets = json.load(secrets)

#Playlist id for the setlist
playlistID = jsonSecrets["spotify"]["playlistID"]
#Base url for the api
url = "https://api.spotify.com/v1"
#Client id and secret
clientID = jsonSecrets["spotify"]["clientID"]
clientSecret = jsonSecrets["spotify"]["clientSecret"]
 
#Access token and auth header to use to access stuff
token = jsonSecrets["spotify"]["accessToken"]

authHeader = {
        "Authorization": "Bearer " + token
        }

#Clear the playlist of all current songs
def clearPlaylist():
    #Get all current songs
    #print(requests.get(url + "/playlists/" + playlistID + "/tracks", headers=authHeader))
    currentSongs = requests.get(url + "/playlists/" + playlistID + "/tracks", headers=authHeader).json()["items"]
    
    #Setup json to send
    currentJson = {
            "tracks": []
            }

    #Remove this song from playlist
    for currentSong in currentSongs:
        currentJson["tracks"].append({"uri":currentSong["track"]["uri"]})

    #Delete from the playlist (send delete request)
    requests.delete(url + "/playlists/" + playlistID + "/tracks", headers=authHeader, data=json.dumps(currentJson)).json()

#Add songs in the list to the playlist
def addSongs(songs):
    clearPlaylist()
    
    #Get each song by title
    for song in songs:
        print(song)
        
        #Get the uri to send to create
        response = requests.get(url + "/search?q=" + song + "%20genre=gospel&type=track&market=US", headers=authHeader).json()["tracks"]["items"][0]
        print(response["name"])
        uri = response["uri"]
        
        requests.post(url + "/playlists/" + playlistID + "/tracks?uris=" + uri, headers=authHeader).json()
