from flask import Flask
import requests
from requests.auth import HTTPBasicAuth
import spotify 
import json

#Define the flask app
app = Flask(__name__)

#Route to this function
@app.route("/planCreate", methods=['POST'])
def getSongs():
    secretJson = {}

    #Open and read secret file to get stuff
    with open("/home/ubuntu/planPlay/secrets.json", "r") as secretFile:
        secretJson = json.load(secretFile)

    access = secretJson["plan"]["access"]
    secret = secretJson["plan"]["secret"]
    #URL for the gathering plans
    url = "https://api.planningcenteronline.com/services/v2/service_types/782403"

    serviceAuth = HTTPBasicAuth(access, secret)

    #Get all plans upcoming
    response = requests.get(url + "/plans?filter=future", auth=serviceAuth).json()
    
    #Make sure there are plans to get
    if response["data"]:
        plans = response["data"]
    else:
        return("no plans!")

    if not plans:
        return("no plans!")
    
    #For each plan, go through the songs
    for plan in plans:
        items = requests.get(url + "/plans/" + plan["id"] + "/items", auth=serviceAuth).json()["data"]
        
        songs = []

        #For each item, get its type, and if song, store its title
        for item in items:
            if item["attributes"]["item_type"] == "song":
                songs.append(item["attributes"]["title"])
        
        songDummy = []

        #Remove duplicates
        [songDummy.append(song) for song in songs if song not in songDummy]

        spotify.addSongs(songDummy)

        return("good!")

#Default, run on public ip port 5555
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
