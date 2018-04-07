#!/usr/bin/env python
"""Main_Server.py : This file displays all details about each activities in this application"""
__author__ = "Priyanka Nalawade Net Id: vu2628 & Prathamesh Ausekar Net ID:eq7948"

import socket
import json
import sys
# maximum connection number
MAX_CON = 5

with open('main_configuration.json') as configuration_file:
    config = json.load(configuration_file)

#get host and port for main server from config
HOST = config.get('main').get('host')
PORT = config.get('main').get('port')
# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CON)
print

while True:
    # receive connections from outside
    print >> sys.stderr, 'Waiting for connection at port', PORT
    (connection, address) = server_socket.accept()
    try:
        print 'Connection accepted from ' + repr(address[1])

        while 1:
            data = connection.recv(1024)
            print 'received "%s"' % data
            if data:
                connection.send(json.dumps(config.get(data)))
            else:
                break
    finally:
        connection.close()
