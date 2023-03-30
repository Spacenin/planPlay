import json
import base64
import requests

#Get PAT based on code
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
    
#Setup headers and stuff to get the token
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
    
#Get the actual thing
response = requests.post("https://accounts.spotify.com/api/token", headers=headers, params=body)
print(response)
print(response.json())
    
#Check if new refresh token
if "refresh_token" in response.json(): 
    #If so, add to the file
    jsonSecrets["spotify"]["refreshToken"] = response.json()["refresh_token"]

    print(response.json()["refreshToken"])

#Put new access token in
jsonSecrets["spotify"]["accessToken"] = response.json()["access_token"]
    
#Write back to file
with open("/home/ubuntu/planPlay/secrets.json", "w") as secrets:
    json.dump(jsonSecrets, secrets)
        
print(response.json()["access_token"])
