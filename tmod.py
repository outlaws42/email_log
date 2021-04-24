#! /usr/bin/env python3

# -*- coding: utf-8 -*-
version = '2021-04-24'

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

def save_file(
    fname: str,
    content: str,
    fdest: str ='relative', 
    mode: str = 'w'):
    """
    fname = filename, content = what to save to the file, 
    fdest = where to save file, mode = w for write or a for append
    import os
    """
    home = os.path.expanduser("~")
    if fdest == 'home' or fdest == 'Home':
        with open(f'{home}/{fname}', mode) as output:
            output.write(content)
    else:
        with open(get_resource_path(fname), mode) as output:
            output.write(content)

def save_yaml(
    fname: str,
    content: dict,
    fdest: str ='relative',
    mode: str = 'w'
    ):
    """
    fname = filename, content = data to save, fdest = file destination,
    mode = 'w' for overwrite file or 'a' to append to the file
    Takes a dictionary and writes it to file specified. it will either
    write or append to the file depending on the mode method
    requires: import os, yaml
    """
    home = os.path.expanduser("~")
    if fdest == 'home' or fdest == 'Home':
        with open(f'{home}/{fname}', mode) as output:
            yaml.safe_dump(content,output, sort_keys=True)
    else:
        with open(get_resource_path(fname), mode) as output:
            yaml.safe_dump(content,output, sort_keys=True)

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
              
def check_dir(dname: str):
  home = os.path.expanduser("~")
  dpath = f'{home}/{dname}'
  dir_exist = os.path.isdir(dpath)
  return dir_exist

def make_dir(fname:str):
  home = os.path.expanduser("~")
  os.mkdir(f'{home}/{fname}')

def remove_file(fname:str):
  home = os.path.expanduser("~")
  os.remove(f'{home}/{fname}')

# Encryption

def gen_key(fname: str,):
  home = os.path.expanduser("~")
  key = Fernet.generate_key()
  with open(f'{home}/{fname}', 'wb')as fkey:
    fkey.write(key)

def encrypt(
  key: str, 
  fname: str, 
  e_fname: str, 
  fdest='relative', 
  ):
  """
  key = key file used to encrypt file,
  fname = file to encrypt,
  e_fname = name of the encrypted file,
  fdest = file destination relative too,
  Takes a input file and encrypts output file
  requires tmod open_file and save_file functions
  requires from cryptography.fernet import Fernet
  """
  keyf = Fernet(key)
  e_file = open_file(
    fname = fname,
    fdest = fdest,
    mode = "rb"
    )
  encrypted_file = keyf.encrypt(e_file)
  save_file(
    fname = e_fname,
    content = encrypted_file,
    fdest = fdest,
    mode = "wb"
  )

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

# colors 
def prRedMulti(ntext,text): print(f"{ntext}\033[91m \033[1m{text}\033[00m")
def prRedBold(text): print(f"\033[91m \033[1m{text}\033[00m")
def prGreenBold(text): print(f"\033[92m \033[1m{text}\033[00m")
def prYellowBold(text): print(f"\033[93m \033[1m{text}\033[00m")
def prLightPurpleBold(text): print(f"\033[94m \033[1m{text}\033[00m")
def prPurpleBold(text): print(f"\033[95m \033[1m{text}\033[00m")
def prCyanBold(text): print(f"\033[96m \033[1m{text}\033[00m")
def prLightGrayBold(text): print(f"\033[97m \033[1m{text}\033[00m")
def prBlackBold(text): print(f"\033[98m \033[1m{text}\033[00m")

def prRed(text): print(f"\033[91m {text}\033[00m")
def prGreen(text): print(f"\033[92m {text}\033[00m")
def prYellow(text): print(f"\033[93m {text}\033[00m")
def prLightPurple(text): print(f"\033[94m {text}\033[00m")
def prPurple(text): print(f"\033[95m {text}\033[00m")
def prCyan(text): print(f"\033[96m {text}\033[00m")
def prLightGray(text): print(f"\033[97m {text}\033[00m")
def prBlack(text): print(f"\033[98m {text}\033[00m")

# Input Loop
def input_loop(
  subject: str, 
  description: str
  ):
  """
  subject = The subject of the input item,
  description = the description of the input item,
  This would be use for a input item that you would
  want to add to a list.
  Requires: doesn't require any special imports
  """
  print(f'\nYou can add as many items as you like.')
  prRedMulti('When your done adding, Type', 'NA')
  item_list = []
  item = ''
  while True:
    item: str = input(
      f"Enter the {subject} {description}: ")
    if (item == 'na') or (item == 'NA'):
      length = len(item_list)
      prRedMulti(f'\nYou have added {length} item(s), Because you typed', item)
      print(f'That will complete your selection for {subject}.')
      break
    else:
      prCyan(f'You added {item} to the list')
      item_list.append(item)
    prCyan(item_list)
  return item_list
