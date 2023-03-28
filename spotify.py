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

#Refresh token to get a new token
refreshToken = jsonSecrets["spotify"]["refreshToken"]
    
#Get PAT based on code
def getToken():
    headers = {
            "Authorization": "Basic " + base64.b64encode((clientID + ":" + clientSecret).encode("ascii")).decode("ascii"),
            "Content-Type": "application/x-www-form-urlencoded"
            }

    body = {
            "grant_type": "refresh_token",
            "refresh_token": refreshToken,
            "redirect_uri": "https://www.elliophill.com/"
            }

    print(headers)
    print(body)
    print(refreshToken)

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, params=body)
    print(response)
    print(response.json())
    
    #Check if new refresh token
    if "refresh_token" in response.json(): 
        #If so, add to the file
        jsonSecrets["refreshToken"] = response.json()["refresh_token"]

        with open("/home/ubuntu/planPlay/secrets.json", "w") as secrets:
            json.dump(jsonSecrets, secrets)
        
        print(response.json()["refresh_token"])

    return(response.json()["access_token"])
    
#Access token and auth header to use to access stuff
token = getToken()

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
