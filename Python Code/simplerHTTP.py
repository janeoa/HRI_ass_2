import SimpleHTTPServer
import SocketServer
import time
import sys
import signal
import urlparse
import ssl
from threading import Thread

current_speed = 0

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the clientglobal a
        global current_speed
        self.data = self.request.recv(1024).strip()
        # print "{} wrote:".format(self.client_address[0])
        result = [x.strip() for x in self.data.split('\n')]
        parsed = urlparse.urlparse(result[0])
        current_speed = float(urlparse.parse_qs(parsed.query)['speed'][0])
        print current_speed
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



while 1: 
    print counter, " ", current_speed
    counter = counter +1
    time.sleep(1)