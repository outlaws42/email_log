#! /usr/bin/env python3

# -*- coding: utf-8 -*-
version = '2021-04-21'

# Imports included with python
import os
import os.path
import sys
from datetime import datetime
from smtplib import SMTP

# Imports installed through pip
try:
  # pip install pyyaml if needed
  import yaml
except:
  pass

try:
  # pip install cryptography if needed
  from cryptography.fernet import Fernet
except:
  pass

# File I/O /////////////////////////////////////////
def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(sys.argv[0])
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource

def open_file(
    fname: str,
    fdest: str = 'relative', 
    def_content: str = '0',
    mode: str = 'r'
    ):
    """
    fname = filename, fdest = file destination, 
    def_content = default value if the file doesn't exist,
    mode = defines read mode 'r' or 'rb'
    Opens the file if it exists and returns the contents.
    If it doesn't exitst it creates it. Writes 
    the def_content value to it and returns the def_content value
    import os
    """
    home = os.path.expanduser("~")
    try:
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', mode) as path_text:
                content=path_text.read()
        else:
            with open(get_resource_path(fname), mode) as text:
                content=text.read()
        return content
    except(FileNotFoundError) as e:
        print(e)
        print('It is reading here')
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', 'w') as output:
                output.write(def_content)
        else:
            with open(get_resource_path(fname), 'w') as output:
                output.write(def_content)
        return def_content

def open_yaml(
    fname: str,
    fdest: str ='relative',
    def_content: dict = {'key': 'value'}
    ):
    """
    fname = filename, fdest = file destination, 
    def_content = default value if the file doesn't exist
    opens the file if it exists and returns the contents
    if it doesn't exitst it creates it writes 
    the def_content value to it and returns the def_content value
    import os, yaml(pip install pyyaml)
    """
    home = os.path.expanduser("~")
    try:
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', 'r') as fle:
                    content = yaml.full_load(fle)
            return content
        else:
            with open(get_resource_path(fname), 'r') as fle:
                    content = yaml.full_load(fle)
            return content
    except(FileNotFoundError, EOFError) as e:
        print(e)
        if fdest == 'home' or fdest == 'Home':
            with open(f'{home}/{fname}', 'w') as output:
                yaml.dump(def_content,output, sort_keys=True)
        else:
            with open(get_resource_path(fname), 'w') as output:
                yaml.dump(def_content,output, sort_keys=True)
        return def_content
              


def decrypt_login(
  key: str, 
  e_fname: str,
  fdest: str = 'relative'
  ):
  keyf = Fernet(key)
  encrypted = open_file(
    fname = e_fname,
    fdest = fdest,
    mode = "rb"
    )
  decrypt_file = keyf.decrypt(encrypted)
  usr = decrypt_file.decode().split(':')
  return [usr[0],usr[1]]



# Gleen info ////////////////////////////////////////////////////

def last_n_lines(fname, lines, fdest='relative'):
  """
  Gets the last so many lines of a file 
  and returns those lines in text.
  Arguments = filename, number of lines
  """
  home = os.path.expanduser("~")
  try:
    file_lines = []
    if fdest == 'home' or fdest == 'Home':
      with open(f'{home}/{fname}') as file:
        for line in (file.readlines() [-lines:]):
          file_lines.append(line)
    else:
      with open(get_resource_path(fname), 'r') as file:
        for line in (file.readlines() [-lines:]):
          file_lines.append(line)
    file_lines_text = (''.join(file_lines))
    return file_lines_text
  except(FileNotFoundError) as e:
    print(e)
    return 'file not found'


# file information
def check_file_age(fname, fdest='relative'):
  """
  Returns the difference of the current timestamp and the
  timestamp of a file last write in hours 
  Arguments = filename from home dir
  Requires import os
  """
  home = os.path.expanduser("~")
  if fdest == 'home' or fdest == 'Home':
    file_info= os.stat(f'{home}/{fname}')
  else:
    file_info= os.stat(get_resource_path(fname))
  now = datetime.now().timestamp()
  modified = int(file_info.st_mtime)
  difference_hour = int(((now - modified)/60)/60)
  return difference_hour

# Send/Receive

def mail(
  body: str, 
  subject: str,
  send_to: list,
  login: list
  ):
  """
  body = Body of the message, subject = The subject,
  send_to = Who you want to send the message to,
  login = The login information for email.
  Requires from smtplib import SMTP
  """
  us, psw = login
  message = f'Subject: {subject}\n\n{body}'
  print(message)
  try:
    mail = SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(us, psw)
    mail.sendmail(us,send_to, message)
    mail.close()
    print('Successfully sent email')
  except Exception as e:
    print('Could not send email because')
    print(e)