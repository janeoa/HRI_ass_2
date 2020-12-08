# HRI Codign Assignment 2
## Example video
https://youtu.be/rB4InQveUiE
## The code
The code comes in two parts:
* Python server
* HTML5 website
Both of which use https as a main communication protocol

### Python server
Python server is used to control the robot and to reciev control data from the website.
#### TCP server
The code begins by creating a Threaded TCP server that has SSL encrypytion and listens on port 8001.
```Python
PORT = 8001
httpd = SocketServer.TCPServer(("", PORT), MyTCPHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
```
The handler of a server just need to catch new speed and direction
```Python
current_speed = float(urlparse.parse_qs(parsed.query)['speed'][0])

current_direc = float(urlparse.parse_qs(parsed.query)['rot'][0].split(" ")[0])
```
#### Choreograph connection
Then it connects to choreograph and executes the Hello World sequence
```Python
tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559) 
motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)

names = list()
times = list()
keys = list()
```
#### Main loop
After that the program loops forever and sends new speed and direction
```Python
while(1):
    ...
	motionProxy.move(speed, 0, direction*0.1) 
```

### Website
Website uses PoseNet library to track a person and sends the tracking data to the Python server. The code stores positions of main three feature.
```Javascript
var elbowPos = {x:0, y:0};
var wristPos = {x:0, y:0};
var Shoulder = {x:0, y:0};
```
Positional data is then used to draw points on the scree
```Javascript
ellipse(keypoint.position.x, keypoint.position.y, 20, 20);
```
With a simple math code calculates relative positions of the joins to get direction and speed
```Javascript
var dist_se = Math.sqrt(Math.pow(elbowPos.x-Shoulder.x,2) + Math.pow(elbowPos.y-Shoulder.y,2));
var dist_at = Math.sqrt(Math.pow(elbowPos.x-wristPos.x,2) + Math.pow(elbowPos.y-wristPos.y,2));
$("#distance").html('distance: {'+ round(dist_at) +'}');

var angle = 90-Math.acos((elbowPos.x- wristPos.x)/dist_at)*180/Math.PI;
$("#angle").html('angle: {'+ round(angle) +'}');
```
Obtained data is then transported to the Python server via this simple line. (This is a local address of the Virtual Machine that hosted the Python Code and Nao simulation)
```Javascript
$.get("https://10.211.55.11:8001",{"speed": speed_t, "rot" : rotation});```
