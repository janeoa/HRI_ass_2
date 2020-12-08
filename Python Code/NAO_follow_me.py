from naoqi import ALProxy
import time

import SimpleHTTPServer
import SocketServer
from threading import Thread
import sys
import signal
import urlparse
import ssl

current_speed = 0
current_direc = 0

class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		# self.request is the TCP socket connected to the clientglobal a
		global current_speed
		global current_direc
		
		self.data = self.request.recv(1024).strip()
		# print "{} wrote:".format(self.client_address[0])
		result = [x.strip() for x in self.data.split('\n')]
		parsed = urlparse.urlparse(result[0])
		current_speed = float(urlparse.parse_qs(parsed.query)['speed'][0])
		current_direc = float(urlparse.parse_qs(parsed.query)['rot'][0].split(" ")[0])
		# print current_speed
		# just send back the same data, but upper-cased
		# self.request.sendall(self.data.upper())


PORT = 8001
httpd = SocketServer.TCPServer(("", PORT), MyTCPHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)

def start_server():
	
	print "serving at port", PORT
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("interupted")
		sys.exit(0)
	httpd.server_close()

serverThread = Thread(target=start_server)

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	httpd.server_close()
	sys.exit(0)

serverThread.daemon = True
serverThread.start()

counter = 1

# write your port name here
tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559) 
motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)

names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.36, 3.16])
keys.append([[-0.17, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.160616, [3, -0.933333, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.36, 3.16])
keys.append([[0, [3, -0.133333, 0], [3, 0.933333, 0]], [0, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LAnklePitch")
times.append([0.36, 3.16])
keys.append([[0.0701587, [3, -0.133333, 0], [3, 0.933333, 0]], [0.0835226, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.36, 3.16])
keys.append([[-0.10313, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.107048, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[-0.559927, [3, -0.133333, 0], [3, 0.266667, 0]], [-0.417833, [3, -0.266667, 0], [3, 0.133333, 0]], [-0.417833, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.417833, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.417833, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.431954, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.42194, [3, -0.133333, 0], [3, 0.266667, 0]], [-0.433729, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[-1.21406, [3, -0.133333, 0], [3, 0.266667, 0]], [-1.20195, [3, -0.266667, 0], [3, 0.133333, 0]], [-1.20195, [3, -0.133333, 0], [3, 0.133333, 0]], [-1.20195, [3, -0.133333, 0], [3, 0.133333, 0]], [-1.20195, [3, -0.133333, 0], [3, 0.133333, 0]], [-1.21452, [3, -0.133333, 0], [3, 0.133333, 0]], [-1.2043, [3, -0.133333, -0.00226095], [3, 0.266667, 0.0045219]], [-1.19418, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[0.296379, [3, -0.133333, 0], [3, 0.266667, 0]], [0.296585, [3, -0.266667, 0], [3, 0.133333, 0]], [0.296585, [3, -0.133333, 0], [3, 0.133333, 0]], [0.296585, [3, -0.133333, 0], [3, 0.133333, 0]], [0.296585, [3, -0.133333, 0], [3, 0.133333, 0]], [0.296585, [3, -0.133333, 0], [3, 0.133333, 0]], [0.296585, [3, -0.133333, 0], [3, 0.266667, 0]], [1, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.36, 3.16])
keys.append([[0.182419, [3, -0.133333, 0], [3, 0.933333, 0]], [0.129447, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.36, 3.16])
keys.append([[0.107335, [3, -0.133333, 0], [3, 0.933333, 0]], [0.109498, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.36, 3.16])
keys.append([[-0.159691, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.160193, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.36, 3.16])
keys.append([[-0.089004, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.0872552, [3, -0.933333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[1.50585, [3, -0.133333, 0], [3, 0.266667, 0]], [1.43857, [3, -0.266667, 0], [3, 0.133333, 0]], [1.43857, [3, -0.133333, 0], [3, 0.133333, 0]], [1.43857, [3, -0.133333, 0], [3, 0.133333, 0]], [1.43857, [3, -0.133333, 0], [3, 0.133333, 0]], [1.42951, [3, -0.133333, 0], [3, 0.133333, 0]], [1.44055, [3, -0.133333, 0], [3, 0.266667, 0]], [-0.0760369, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[0.198813, [3, -0.133333, 0], [3, 0.266667, 0]], [0.223846, [3, -0.266667, 0], [3, 0.133333, 0]], [0.223846, [3, -0.133333, 0], [3, 0.133333, 0]], [0.223846, [3, -0.133333, 0], [3, 0.133333, 0]], [0.223846, [3, -0.133333, 0], [3, 0.133333, 0]], [0.244349, [3, -0.133333, 0], [3, 0.133333, 0]], [0.232997, [3, -0.133333, 0.0113521], [3, 0.266667, -0.0227043]], [-0.0111126, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[0.105004, [3, -0.133333, 0], [3, 0.266667, 0]], [0.106233, [3, -0.266667, 0], [3, 0.133333, 0]], [0.106233, [3, -0.133333, 0], [3, 0.133333, 0]], [0.106233, [3, -0.133333, 0], [3, 0.133333, 0]], [0.106233, [3, -0.133333, 0], [3, 0.133333, 0]], [0.106233, [3, -0.133333, 0], [3, 0.133333, 0]], [0.106233, [3, -0.133333, 0], [3, 0.266667, 0]], [1.30923, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.36, 3.16])
keys.append([[0.0768804, [3, -0.133333, 0], [3, 0.933333, 0]], [0.0845, [3, -0.933333, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.36, 3.16])
keys.append([[0.0765043, [3, -0.133333, 0], [3, 0.933333, 0]], [0.110751, [3, -0.933333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[0.484128, [3, -0.133333, 0], [3, 0.266667, 0]], [0.375623, [3, -0.266667, 0], [3, 0.133333, 0]], [1.03947, [3, -0.133333, 0], [3, 0.133333, 0]], [0.0438527, [3, -0.133333, 0], [3, 0.133333, 0]], [0.994733, [3, -0.133333, 0], [3, 0.133333, 0]], [0.48733, [3, -0.133333, 0.0642016], [3, 0.133333, -0.0642016]], [0.423128, [3, -0.133333, 0], [3, 0.266667, 0]], [0.423128, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[1.30761, [3, -0.133333, 0], [3, 0.266667, 0]], [0.366358, [3, -0.266667, 0], [3, 0.133333, 0]], [0.376446, [3, -0.133333, 0], [3, 0.133333, 0]], [0.376067, [3, -0.133333, 0.000378768], [3, 0.133333, -0.000378768]], [-0.168076, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.165247, [3, -0.133333, -0.00282886], [3, 0.133333, 0.00282886]], [1.2011, [3, -0.133333, 0], [3, 0.266667, 0]], [1.2011, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[0.328184, [3, -0.133333, 0], [3, 0.266667, 0]], [0.991115, [3, -0.266667, 0], [3, 0.133333, 0]], [0.991115, [3, -0.133333, 0], [3, 0.133333, 0]], [0.991115, [3, -0.133333, 0], [3, 0.133333, 0]], [0.991115, [3, -0.133333, 0], [3, 0.133333, 0]], [0.737048, [3, -0.133333, 0.115107], [3, 0.133333, -0.115107]], [0.300471, [3, -0.133333, 0], [3, 0.266667, 0]], [0.300471, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.36, 3.16])
keys.append([[0.167127, [3, -0.133333, 0], [3, 0.933333, 0]], [0.128883, [3, -0.933333, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.36, 3.16])
keys.append([[-0.0841869, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.112873, [3, -0.933333, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.36, 3.16])
keys.append([[-0.159691, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.160193, [3, -0.933333, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.36, 3.16])
keys.append([[-0.089004, [3, -0.133333, 0], [3, 0.933333, 0]], [-0.0872552, [3, -0.933333, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[1.47626, [3, -0.133333, 0], [3, 0.266667, 0]], [-1.38566, [3, -0.266667, 0], [3, 0.133333, 0]], [-1.38566, [3, -0.133333, 0], [3, 0.133333, 0]], [-1.38542, [3, -0.133333, -0.000243147], [3, 0.133333, 0.000243147]], [-1.36684, [3, -0.133333, -0.0185802], [3, 0.133333, 0.0185802]], [-0.854466, [3, -0.133333, -0.46695], [3, 0.133333, 0.46695]], [1.43486, [3, -0.133333, 0], [3, 0.266667, 0]], [1.43486, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[-0.173455, [3, -0.133333, 0], [3, 0.266667, 0]], [-0.275038, [3, -0.266667, 0.020659], [3, 0.133333, -0.0103295]], [-0.285367, [3, -0.133333, 0.0103295], [3, 0.133333, -0.0103295]], [-0.961101, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.0591022, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.411081, [3, -0.133333, 0], [3, 0.133333, 0]], [-0.219411, [3, -0.133333, 0], [3, 0.266667, 0]], [-0.219411, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.36, 1.16, 1.56, 1.96, 2.36, 2.76, 3.16, 3.96])
keys.append([[0.141651, [3, -0.133333, 0], [3, 0.266667, 0]], [0.00489187, [3, -0.266667, 0], [3, 0.133333, 0]], [0.00489187, [3, -0.133333, 0], [3, 0.133333, 0]], [0.00489187, [3, -0.133333, 0], [3, 0.133333, 0]], [0.00489187, [3, -0.133333, 0], [3, 0.133333, 0]], [0.0137151, [3, -0.133333, -0.00882327], [3, 0.133333, 0.00882327]], [0.0980686, [3, -0.133333, 0], [3, 0.266667, 0]], [0.0980686, [3, -0.266667, 0], [3, 0, 0]]])

motionProxy.angleInterpolationBezier(names, times, keys) # waving
tts.say("Hi, human! I want to come with you.") # tts

useSensors = 0

#motionProxy.setStiffnesses('LShoulderPitch', 1)

leftArmEnable = False
rightArmEnable = True
motionProxy.setMoveArmsEnabled(leftArmEnable, rightArmEnable)

motionProxy.setAngles('LShoulderPitch', 0.0, 0.01)
motionProxy.setAngles('LWristYaw', 0.0, 0.05)

iter = 1
while(1):
	print("iter", iter)
	iter = iter+1
	# x = motionProxy.getAngles('LShoulderPitch', useSensors) # get shoulder pitch
	# if (x[0] > 1.57):
	# 	motionProxy.stopMove()
	# 	break

	# direction = motionProxy.getAngles('LWristYaw', useSensors) # get wrist yaw
	direction = current_direc

	# speed = (-x[0]*2.23+3.5)/(3.5) # map speed between 0 and 2
	speed = current_speed
	if speed > 2:
		speed = 2
	if speed < 0:
		speed = 0 

	print ""
	print "speed is: ", speed, ""

	# if (direction[0] > 0):
	# 	print "direction is: ", direction[0]*0.1*180/3.14, "degrees/s to the left", ""
	# else:
	# 	print "direction is: ", direction[0]*0.1*180/3.14, "degrees/s to the right", ""
	if direction > 2:
		direction =2
	if direction < -2:
		direction = -2

	motionProxy.move(speed, 0, direction*0.1) 

	time.sleep(0.800)


	
