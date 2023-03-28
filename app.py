from flask import Flask
import requests
from requests.auth import HTTPBasicAuth
import spotify 

access = "0e7728b3e5b83ae6fa2f0bb10f67d00ec69f2aa30c45b441fe698cb5aaa043c6"
secret = "f145339246b3dbde38ecd813b4711ccd385ac8e9a6727cf393cf33d81e702280"
#URL for the gathering plans
url = "https://api.planningcenteronline.com/services/v2/service_types/782403"

serviceAuth = HTTPBasicAuth(access, secret)

#Define the flask app
app = Flask(__name__)

#Route to this function
@app.route("/planCreate", methods=['POST'])
def getSongs():
    #Get all plans upcoming
    plans = requests.get(url + "/plans?filter=future", auth=serviceAuth).json()["data"]
    
    #For each plan, go through the songs
    for plan in plans:
        print(plan["id"])
        items = requests.get(url + "/plans/" + plan["id"] + "/items", auth=serviceAuth).json()["data"]
        
        songs = []

        #For each item, get its type, and if song, store it
        for item in items:
            if item["attributes"]["item_type"] == "song":
                songs.append(item)
        
        songDummy = []

        #Remove duplicates
        [songDummy.append(song) for song in songs if song not in songDummy]
        
        #Make the list just song titles
        songTitles = []

        for song in songDummy:
            songTitles.append(song["attributes"]["title"])

        spotify.addSongs(songTitles)

        return("good!")

#Default, run on public ip port 5555
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
