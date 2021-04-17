#! /usr/bin/env python3

# -*- coding: utf-8 -*-
version = '2021-04-17'

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
