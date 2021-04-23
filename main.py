# -*- coding: utf-8 -*-
version = '2021-04-23'

from tmod import (
  check_dir, encrypt, open_file, open_yaml, check_file_age, last_n_lines,
   decrypt_login, mail, gen_key, save_yaml, remove_file, make_dir)
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser
# from icecream import ic

username = getuser()

def settings():
  settings = open_yaml(
  fname = ".config/email-log/emailog_set.yaml",
  fdest = "home",
  )
  return settings['runtime']

def file_not_found(conf_dir: str):
  make_dir(conf_dir)
  gen_key(f'{conf_dir}/.info.key')
  # gen_key('.info.key')
  key = open_file(
      fname = f'{conf_dir}/.info.key', 
      fdest = "home",
      mode ="rb"
      )

  # Email Login info
  print("We could not find the conf ")
  email = input("Enter your email(example@gmail.com): ") 
  pas = input("Enter your password(examplepassword): ")
  lo = {email:pas}
  open_yaml(
    fname = f'{conf_dir}/.cred.yaml',
    fdest = 'home',
    def_content = lo
    )
  
  encrypt(
    key = key,
    fname = f'{conf_dir}/.cred.yaml',
    e_fname = '.config/email-log/.cred_en.yaml',
    fdest = 'home'
    )
  remove_file(f'{conf_dir}/.cred.yaml')

  run: str = str(input("Enter time to run script daily(default: 05:00): ") or '05:00')
  numb_lines: int = int(input("Enter the number of lines of the log file to send(default: 30): ") or 30)
  print('You can add more Email adresses later in the config file')
  send: str = input("Enter email address to send to(example@gmail.com): ")
  logf: str = input("Enter the log file to check(Default: Logs/net_backup.log): ") or 'Logs/net_backup.log'
  load = {
    'runtime': str(run),
    'lines': numb_lines,
    'sendto': [send],
    'logs': [logf]
    }
  save_yaml(
    fname =f'{conf_dir}/emailog_set.yaml',
    fdest = 'home',
    content = load)


def  call_funtion():  
  settings = open_yaml(
  fname = ".config/email-log/emailog_set.yaml",
  fdest = "home",
  )
  kf = ".config/email-log/.info.key"
  ef = ".config/email-log/.cred_en.yaml"
  st = settings['sendto']
  log = settings['logs']
  lines = settings['lines']
  for i in range(len(log)):
    body = mail_body(log[i], lines)
    sub = f'Backup Log: for {username} (Log file: {log})'
    key = open_file(
      fname = kf, 
      fdest = "home",
      mode ="rb"
      )
    login = decrypt_login(
      key = key, 
      e_fname = ef, 
      fdest = "home"
      )
    mail(
      body = body, 
      subject = sub, 
      send_to = st,
      login = login
        )

def mail_body(filename, lines):
  age =  check_file_age(filename, 'home')
  if age >= 24:
    con = f"The log file {filename} for {username} is {age} hours old check backup"
  else:
    con = last_n_lines(filename, lines,'home')
  return con

conf_dir = '.config/email-log'
dir_exist = check_dir(conf_dir)
if dir_exist == False:
  file_not_found(conf_dir)
every().day.at(str(settings())).do(call_funtion)

if __name__ == "__main__":
  try:
    print('waiting on timer')
    while True:
      run_pending() # every().day.at(settings()).do(call_funtion)
      sleep(1)
  except KeyboardInterrupt as e:
    print(e)
    print('Interrupted')