#  coding: utf-8 
import socketserver
import inspect
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

# Assignment 1 for CMPUT 404
# Additional code by Ivan Ma

OS_PATH = os.path.dirname(os.path.abspath(__file__))
class MyWebServer(socketserver.BaseRequestHandler):

    HTML_DIR = ""
    def handle(self):
        global HTML_DIR
        allowedRequests = ['GET']
        full_payload = ""
        payload = ""
        header = ""
        webpageFile = None
        requestFile = ""
        requestPath = ""
        self.data = self.request.recv(1024).strip()
        requestList = str(self.data).split(" ")
        #print("requestList: "+str(requestList))
        absPath = os.getcwd()
        requestPath = absPath+"/www"+requestList[1]
        requestType = requestList[0][2:]
        requestFile = requestList[1]
        requestFileType = ""
        #print("abs path: "+str(requestPath))
        #print("current WD: "+str(absPath))
        if(requestType in allowedRequests):
            try:
                if(requestPath[-1:] == "/"):
                    header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
                    webpageFile = open(requestPath+"index.html")
                else:
                    header = "HTTP/1.1 301 Moved Permanently\nContent-Type: text/html\nLocation: "+requestFile+"/\n\n"
                    webpageFile = open(requestPath+"/index.html")
                    HTML_DIR = requestFile
            except:
                try:
                    try:
                        webpageFile = open(requestPath)
                        HTML_DIR = ""
                        #print("RESET GLOBAL HTML VAR")
                    except:
                        requestPath = absPath+"/www"+HTML_DIR+requestList[1]
                        #print("Tried to open: /"+requestPath)
                        webpageFile = open("/"+requestPath)
                    absPathConcat = os.path.dirname(os.path.realpath(webpageFile.name))
                    if(absPath in absPathConcat):
                        requestFileType = requestFile.split(".")[1]
                    else:
                        raise Exception("Detected insecure file access!")

                    if("html" == requestFileType):
                        HTML_DIR = requestFile
                        header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"

                    if("css" == requestFileType):
                        header = "HTTP/1.1 200 OK\nContent-Type: text/css\n\n"
                    
                except:
                    #print("File: "+str(requestFile)+" not found!")
                    header = 'HTTP/1.1 404 Not Found\r\n'
                    webpageFile = open("www/notFound.html") 
            #print("HTML_DIR: "+str(HTML_DIR))
            try:
                payload = webpageFile.read()      
            except:
                payload = webpageFile                                             
            full_payload = header + payload

        else:
            header = '405 Method Not Allowed\r\nContent-Type: text/html\n\n'
            webpageFile = open(requestPath+"/notAllowed.html")
            full_payload = header

        self.request.sendall(full_payload.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
