#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import json
from datetime import datetime
import socket

___author__= 'Guinsly Mondesir'
"""This script is inspired from https://github.com/toxtli/dailypush"""

#Change to the current directory
def cd_to_this_file_directory():
    """Change to this file directory
    
    While the crontab will run your command
    it needs to change to this directory in 
    order to do a 'git add .'
    """
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def command_line(cmd):
    """[summary]
    
    Process a command
    
    Arguments:
        cmd {[list]} -- a list that represent the command that 
        we will pass to the shell (Terminal)
    
    Execption:
        [ERROR] -- raise a ValueError if an error occurs while executing
                  the commands on the terminal,
                  meaning that the EXIT STATUS is 1
    """
    try:
        s = subprocess.check_output(cmd)
        return s.split()
    except subprocess.CalledProcessError:
        raise ValueError('An error occurs with the command that you passed.')


def execute_this_command_in_the_terminal(sentences):
    """execute this command in your Terminal
    
    It will receive the command and the necessary parameters
    to execute on your terminal
    
    Arguments:
        sentences {[list]} -- the command line that you want
        to execute
    
    Helper: This script will need the function command_line(cmd)
    """
    for cmd in sentences:
        command_line(cmd.split())

def ping_this_server():
	  """Ping the server
	  
	  this script will ping the server
	  """
	  try:
	  	  socket.gethostbyname('www.ottawacityjobs.ca')
	  except socket.gaierror as ex:
	      # url cannot be reached
	      print("Error:")

#curl -s http://www.ottawacityjobs.ca/fr/data/ > fr.json
#wget http://www.ottawacityjobs.ca/en/data/ -O hello2.json
#
if __name__ == '__main__':
    cd_to_this_file_directory()
    ping_this_server()
    today = datetime.now()
    today = str(today).split()[0] + '-Ottawacityjobs.json'
    sentences = [
    'wget http://www.ottawacityjobs.ca/en/data/ -O '+ 'EN-' + today,
    'wget http://www.ottawacityjobs.ca/fr/data/ -O '+ 'FR-' + today,
      ]
    execute_this_command_in_the_terminal(sentences)
    #a = command_line('curl -s http://www.ottawacityjobs.ca/fr/data/'.split())