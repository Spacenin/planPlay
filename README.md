# planPlay
This is a backend application that runs on an EC2 instance owned by me. The application awaits until a Planning Center Plan is created or updated,
thus sending a POST request to the Flask server. The server then performs a GET to get the plan and its songs, and passes them along to the Spotify section
of the application. This portion deletes all songs currently in the chosen playlist, and adds the songs in the plan instead. All of this is implemented in Python with 
access tokens and authentication provided in a local JSON file.
