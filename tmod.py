#! /usr/bin/env python3

# -*- coding: utf-8 -*-
version = '2021-04-13'

# Imports included with python
import os
import os.path
import sys
from datetime import datetime

# Imports installed through pip
try:
  # pip install pyyaml if needed
  import yaml
except:
  pass

# File I/O /////////////////////////////////////////
def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(sys.argv[0])
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource

def open_file(file_,type_='relative', variable = '0'):
    home = os.path.expanduser("~")
    try:
        if type_ == 'home' or type_ == 'Home':
            with open(f'{home}/{file_}', 'r') as path_text:
                variable=path_text.read()
        else:
            with open(get_resource_path(file_), 'r') as text:
                variable=text.read()
        return variable
    except(FileNotFoundError) as e:
        print(e)
        print('It is reading here')
        if type_ == 'home' or type_ == 'Home':
            with open(f'{home}/{file_}', 'w') as output:
                output.write(variable)
        else:
            with open(get_resource_path(file_), 'w') as output:
                output.write(variable)
        return variable

def open_yaml(file_,type_='relative'):
    home = os.path.expanduser("~")
    try:
        if type_ == 'home' or type_ == 'Home':
            with open(f'{home}/{file_}', 'r') as fle:
                    variable = yaml.full_load(fle)
            return variable
        else:
            with open(get_resource_path(file_), 'r') as fle:
                    variable = yaml.full_load(fle)
            return variable
    except(FileNotFoundError, EOFError) as e:
        print(e)
        variable = 0
        if type_ == 'home' or type_ == 'Home':
            with open(f'{home}/{file_}', 'w') as fle:
                yaml.dump(variable, fle)
        else:
            with open(get_resource_path(file_), 'w') as fle:
                yaml.dump(variable, fle)
        return variable
              
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
