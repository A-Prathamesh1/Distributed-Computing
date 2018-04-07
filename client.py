#!/usr/bin/env python
"""client.py : This file allows client to enter numbers in order to perform add, subtract, multiply, division"""
__author__ = "Priyanka Nalawade Net Id: vu2628 & Prathamesh Ausekar Net ID:eq7948"


import socket
import json
import re

with open('main_configuration.json') as configuration_file:
    config = json.load(configuration_file)

HOST = config.get('main').get('host')
PORT = config.get('main').get('port')
NUMBER_ONE = 0
NUMBER_TWO = 0
MODE= ''

print 'Welcome to CS 6580 Distributed System Group Project'
print 'Please enter expression 1+2 6-2 2*5 8/2 to get calculation back'
while True:
    try:
        input_data = raw_input("Enter expression you need to perform : \n")
        exp = re.split("([+-/*])", input_data.strip().replace(" ", ""))
        NUMBER_ONE = int(exp[0])
        NUMBER_TWO = int(exp[2])
        MODE = ''
        if exp[1] == '/':
            MODE = 'division'
        elif exp[1] == '+':
            MODE = 'addition'
        elif exp[1] == '*':
            MODE = 'multiplication'
        elif exp[1] == '-':
            MODE = 'subtraction'
        else:
            raise Exception('Error in the expression')
        break
    except ValueError:
        print 'Please enter numbers: '
        continue
    except Exception as err:
        print 'there is an error'
        continue

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1000)

# connecting to server
client_socket.connect((HOST, PORT))

try:
    print 'Connected to server at', HOST, 'and port number', PORT
    client_socket.send(MODE)
    response = client_socket.recv(1024)# buffer size
    print 'Received a response from the server...'
    print 'Response:', response
finally:
    client_socket.close()

print
print
if not response:
    print 'Invalid response'
    quit()

response = json.loads(response)

if 'port' and 'host' not in response.keys():
    print 'Invalid response.'
    quit()

# connection to operation server
print
print

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1000)
client_socket.connect((response.get('host'), response.get('port')))
try:
    print 'Connected to Mode: ', MODE, '\n server is', response.get('host'), '\n Port Number is: ', response.get('port')
    obj = {'x': NUMBER_ONE, 'y': NUMBER_TWO}
    message = json.dumps(obj)
    client_socket.send(message)
    # buffer size
    data = client_socket.recv(1024)
    data = json.loads(data)
    print "Operation result is ", data.get('result')
finally:
    client_socket.close()
