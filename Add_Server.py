#!/usr/bin/env python
"""Add_Server.py : This file performs addition"""
__author__ = "Prathamesh Ausekar Net ID:eq7948"

import socket
import json
import sys

# maximum connection number
MAX_CON = 5

with open('main_configuration.json') as configuration_file:
    config = json.load(configuration_file)
# get host and port for add server from config 
HOST = config.get('addition').get('host')
PORT = config.get('addition').get('port')


# creating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(MAX_CON)
print

while True:
    # to receive connections from outside network
    print >> sys.stderr, 'Waiting for connection on port', PORT
    (connection, address) = sock.accept()
    try:
        print 'Connection accepted from ' + repr(address[1])

        while 1:
            # buffer size
            data = connection.recv(1024)
            print 'Data received is :"%s"' % data
            if data:
                try:
                    data = json.loads(data)
                except:
                    print 'Error in JSON'
                    connection.send('error')
                    break
                # get data from JSON and perform addition
                if 'x' in data.keys() and 'y' in data.keys():
                    res = json.dumps({'result' : int(data.get('x')) + int(data.get('y'))})
                    connection.send(res)
                    print 'Sending', res, 'response to client'
                else:
                    break
            else:
                break
    finally:
        print 'Closing down the connection with', repr(address[1])
        connection.close()
