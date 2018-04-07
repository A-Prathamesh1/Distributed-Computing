#!/usr/bin/env python
"""Subtract_Server.py : This file performs subtraction"""
__author__ = "Priyanka Nalawade Net Id: vu2628 & Prathamesh Ausekar Net ID:eq7948"

import socket
import json
import sys

 # maximum connection number
MAX_CON = 5

with open('main_configuration.json') as configuration_file:
    config = json.load(configuration_file)

#get host and port for subtract server from config 
HOST = config.get('subtraction').get('host')
PORT = config.get('subtraction').get('port')


# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(MAX_CON)  # become a server socket
print

while True:
    # receiving connections from outside
    print >> sys.stderr, 'Waiting for connection on port', PORT
    (connection, address) = sock.accept()
    try:
        print 'Connection accepted from ' + repr(address[1])

        while 1:
            data = connection.recv(1024)
            print 'received "%s"' % data
            if data:
                try:
                    data = json.loads(data)
                except:
                    print 'Cannot decode json'
                    connection.send('error')
                    break
                # Perform subtraction of two given numbers
                if 'x' in data.keys() and 'y' in data.keys():
                    res = json.dumps({'result' : int(data.get('x')) - int(data.get('y'))})
                    connection.send(res)
                    print 'Sending', res, 'response to client'
                else:
                    break
            else:
                break
    finally:
        print 'Shutting down the connection with', repr(address[1])
        connection.close()
