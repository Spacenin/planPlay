import requests
import json

#Playlist id for the setlist
playlistID = "4HlwjvadjOSoUwTil1hIFX"
#Base url for the api
url = "https://api.spotify.com/v1"

#Access token and auth header to use to access stuff
token = "BQC3mIpntt5LcDTvJmSyUvcm2yo01_J9O2HX-krshGkaQ4dk-AlL7A55m1PIQ8a1yKVDWIP8euHRFNM4ezzoJv7YhtPLe08O9Bfl2a4E00wJmred9ZYEgyvkCerxApW_VXKRR5LGUvrH4NAgaSlvA0B16OKkw4RUFygVlKwkJtMy8q5rYyZGuP4hxA6koh_dLw1LeWKYVu3t1TZH8w"

authHeader = {
        "Authorization": "Bearer " + token
        }

#Clear the playlist of all current songs
def clearPlaylist():
    #Get all current songs
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

    print(songs)

