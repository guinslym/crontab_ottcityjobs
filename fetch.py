#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os, io
from os import path
import json
from datetime import datetime
import socket
import logging
from logging.handlers import RotatingFileHandler

___author__= 'Guinsly Mondesir'
"""This script is inspired from https://github.com/toxtli/dailypush"""



def configuration_of_the_logs():
    """This will serve as a base for logs configuration

    Warning: make sure there is a filename 'logs.txt' inside of
    a folder named 'logs'

    Returns:
        Object -- a logging object
    """
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    #todo:#Check to see if the folder exist
    my_path = path.dirname(path.realpath(__file__))
    logFile = my_path + '/logs/logs.txt'

    #The logs.txt file can't be more than 5MB
    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    #app_log.setLevel(logging.INFO)
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)
    #app_log.info('configuraring the logs')

    return app_log

app_log = configuration_of_the_logs()

"""
######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
"""


def get_the_list_of_json_file():
    """
    get the list of the json file in the
    current directory
    """
    mypath = os.path.abspath(__file__)
    files = []
    for i in os.listdir('.'):
        if os.path.isfile(i):
            if i[0] != '.':
                if (i.split('.')[1] == 'json'):
                    files.append(i)
    return files

def open_json_file(file):
    """open a json file"""
    with open(file) as data_file:
        data = json.load(data_file)
    return (data['jobs'])

def create_a_json_file(data):
    """Create a json file """
    with io.open('full.json', 'w', encoding='utf-8') as f:
        f.write(str(json.dumps(data, sort_keys = True, indent = 4, ensure_ascii=False)))

def create_only_one_json_file(files):
    """
        Open the first file
        Loads it's content
        Open the second files loads it's content
        append Second file to the first file
        delete all the previous json file#
        Create a json file (full.json)
    """
    jobs_fr = open_json_file(files[0])
    jobs_en = open_json_file(files[1])
    data = jobs_en + jobs_fr
    #print(data)
    #delete json
    for i in files:
        os.remove(i)
    create_a_json_file(data)

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
    files = get_the_list_of_json_file()
    create_only_one_json_file(files)
    app_log.info('Today we fetch files {0} + {1}'.format(files[0], files[1]))

    #a = command_line('curl -s http://www.ottawacityjobs.ca/fr/data/'.split())
