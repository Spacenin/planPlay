import requests
import json

#Playlist id for the setlist
playlistID = "4HlwjvadjOSoUwTil1hIFX"
#Base url for the api
url = "https://api.spotify.com/v1"

#Access token and auth header to use to access stuff
token = "BQALUD_BWxvVppQwyOHVVh3VkSlP_YQ1algj8EoKvtO6qtBDrbjkVuqtF7WRzldH21VuEaG85yGVAMalj0TkRoSBieI7zTSUheopuSz3Kx5XIOfCcJHVlRk12whrVZ938wvES8zCyy39a3RjAtccRchXi0TGE96SvDjnYUIi95DSgLBFPPDjNbQGJTTSzgW2WsgNXsxToe1oaprSHA"

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
        response = requests.get(url + "/search?q=" + song + "&type=track&market=US", headers=authHeader).json()["tracks"]["items"][0]
        print(response["name"])
        uri = response["uri"]
        
        requests.post(url + "/playlists/" + playlistID + "/tracks?uris=" + uri, headers=authHeader).json()
