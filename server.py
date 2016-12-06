#!/usr/bin/env python
#
#
#******************************************
#******************************************
# Cornell University
# ECE 5725: Web-App based Robot Control(Webo-Pi)
# Authors: Mahantesh Salimath, Rahul Sharma
#
#******************************************
#******************************************
#
#

#import the required headers.
import os
import sys 
import urlparse
import time
import subprocess
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import argparse
from requests import *

#Class to handle the HTTP Requests like POST
class HTTP_handler(BaseHTTPRequestHandler):
	def do_POST(self):
		#Extract the form data.
		length =int(self.headers.getheader('content-length'))
		form_data =self.rfile.read(length)
		query_dict =urlparse.parse_qs(form_data)
		#Write the data to a file.
		try :
			subprocess.check_output("echo "+query_dict['username'][0] + ",action : " + query_dict['action'][0] +" time: " + \
			query_dict['time'][0] + " >> log_backup.txt",shell=True)
			#Send the OK response.
			self.send_response(200)
		except subprocess.CalledProcessError:
			#Send the error response.
			self.send_response(400)
		self.end_headers()
		
#function to start the server.
def start_server(args):
	http_server =(args.ipaddress, args.port)
	httpd =HTTPServer(http_server, HTTP_handler)
	httpd.serve_forever()

#main function to parse the arguments.
if __name__ == '__main__':
	parser =argparse.ArgumentParser()
	#parse the ip address if passed as an argument.
	parser.add_argument(	'-ip',
			        '--ipaddress',
			        dest='ipaddress',
			        default='0.0.0.0',
			        required=False,
			        type=str,
			        help="The ip-address of the host from where to start the http server")
	#Parse the port number if passed, 8082 by default.
	parser.add_argument(	'-p',
			    	'--port',
				dest ='port',
				default =8082,
				required =False,
				help ="The port where the http server will listen for request",
				type =int)
	args =parser.parse_args()
	#Start the server.
	start_server(args)
	


