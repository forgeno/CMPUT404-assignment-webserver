#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

OS_PATH = os.path.dirname(os.path.abspath(__file__))
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        allowedRequests = ['GET']
        full_payload = ""
        payload = ""
        header = ""
        webpageFile = None
        requestFile = ""
        self.data = self.request.recv(1024).strip()
        requestList = str(self.data).split(" ")
        requestPath = "./www"+requestList[1]
        requestType = requestList[0][2:]
        requestFile = requestList[1]
        requestFileType = ""
        # print("File: "+requestFile+" Filetype: "+requestFileType+"")
        # print("requestFile: %s requestPath: %s",requestFile, requestPath)
        # print(requestList)
        # try:
        if(requestType in allowedRequests):
            try:
                header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
                webpageFile = open(requestPath+"index.html")
            except:
                try:
                    requestFileType = requestFile.split(".")[1]
                    webpageFile = open(requestPath)
                    if("css" == requestFileType):
                        header = "HTTP/1.1 200 OK\nContent-Type: text/css\n\n"
                        
                    if("html" == requestFileType):
                        header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
                    
                except:
                    print("File: "+str(self.data)+" not found!")
                    header = 'HTTP/1.1 404 Not Found\r\n'
                    webpageFile = open("www/notFound.html") 

            try:
                payload = webpageFile.read()      
            except:
                payload = webpageFile                                             
            full_payload = header + payload

        else:
            header = '405 Method Not Allowed\r\nContent-Type: text/html\n\n'
            webpageFile = open(requestPath+"/notAllowed.html")
            full_payload = header

        #  Exception as e: 
        #     print(e)
        #     print("file not found: "+requestFile[0]+"."+requestFile[1])
        #     header = 'HTTP/1.1 404 Not Found\r\n'
        #     webpageFile = open(requestFile+"/notFound.html")
        #     payload = webpageFile.read()
        #     payload = "<h1>File: {}.{} does exisexceptt! </h2>".format(requestFile[0],requestFile[1])
        #     full_payload = header + payload #test

            
        #print ("Got a request of: %s\n" % self.data)
        self.request.sendall(full_payload.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
