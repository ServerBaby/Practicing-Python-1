#!/usr/bin/env python3

# Welcome to my test server
# Comments are just to explain (to myself mainly) how each of the commands work

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import logging
from datetime import datetime


port = 8000


class SimpleRequestHandler(BaseHTTPRequestHandler):
# This class is called into existence when the HTTPD server gets a request on the above port
# It currently only handles GET and POST actions


    def do_GET(self):
        if self.path == '/':
            self.path = '/serverbaby_test.html'
            # if this is a directory [ends in /], use file called serverbaby_test.html

        try:
            file_to_open = open(self.path[1:]).read()
            # open serverbaby_test.html
            server_time_local = self.log_date_time_string()
            # take the current LOCAL time from the server 
            date_obj = datetime.strptime(server_time_local, '%d/%b/%Y %H:%M:%S')
            # identify the components that make up the server time
            served_on_time = datetime.strftime(date_obj, '%d-%m-%Y %I:%M:%S %p')
            # Turn those components into a string in the desired format to display the time
            amended_file = file_to_open.replace("XXXXXXXXXX", str(served_on_time))
            # XXXXXXXXXX is a a placeholder in the serverbaby_test.html file to insert the time
            # replace the placeholder with the actual time from the server
            self.send_response(200)
            # send an "OK" response from the server

        except:
            # this is a bare except, which means it will catch any and all exceptions.
            # Bare excepts are not usually recommended but desired for this example.
            amended_file = "404 Not Found - Whoops! You broke the Interwebz"
            # if for any reason the file serverbaby_test.html can't be located opened, read, amended etc
            # This error message will display on the browser instead
            self.send_response(404)
            # 404 Not Found - Requested resource could not be found. 
            # Subsequent requests by the client permissible.
        self.end_headers()
        # tells the program this line is the end of what to display as html 
        self.wfile.write(bytes(amended_file, 'utf-8'))
        # take the text contents of whatever is currently saved in "amended_file",
        # either the amended version of serverbaby_test.html or the error message,
        # and display it in the browser window


def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, variable_port=port):
    logging.basicConfig(level=logging.INFO)
    # info(msg, *args, **kwargs)  Logs a message with level INFO on this logger.
    server_address = ('', port)
    # any IP address for server, port == the port listed above [8000]
    httpd = server_class(server_address, handler_class)
    local_path = os.getcwd()
    # os.getcwd() == absolute path of the current working directory
    message = 'serving from {0} at port {1}'
    print(message.format(local_path, variable_port))
    # print the welcome message with the following details:
    # format:   0 == local_path, 1 == variable_port  
    logging.info('Starting server, use <Ctrl-C> to stop...\n')
    # this message is displayed, and the logging info is displayed after this message
    try:
        # This is where the listener is set up
        httpd.serve_forever()
        # if the code works, and there is no Keyboard Interrupt, it leaves the server running
    except KeyboardInterrupt:
        # KeyboardInterrupt - Raised when the user presses Ctrl+c, Ctrl+z or Delete
        httpd.server_close()
        # if a KeyboardInterrupt is entered, close the server and print the below message
        logging.info('<Ctrl-C> entered, shutting down server\n')


if __name__ == '__main__':
    run()
    # this makes it all run....

