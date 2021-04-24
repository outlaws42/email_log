# -*- coding: utf-8 -*-
version = '2021-04-24'

from tmod import (
  check_dir, encrypt, open_file, open_yaml, check_file_age, last_n_lines,
   decrypt_login, mail, gen_key, prGreenBold, save_yaml, input_loop,
   remove_file, make_dir,prYellowBold, prRedMulti, prGreen, prCyan)
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser
from icecream import ic

username = getuser()
conf_dir = ".config/email-log"

def settings():
  settings = open_yaml(
  fname = f"{conf_dir}/emailog_set.yaml",
  fdest = "home",
  )
  return settings['runtime']

def config_setup_email(conf_dir: str):
  make_dir(conf_dir)
  gen_key(f'{conf_dir}/.info.key')
  key = open_file(
      fname = f'{conf_dir}/.info.key', 
      fdest = "home",
      mode ="rb"
      )
  prYellowBold("\nWe could not find any configuration folder ")
  prGreen('This Wizard will ask some question to setup the configuration needed for the script to function.')
  prGreenBold('This configuration wizard will only run once.')
  prGreen(
    '\nThe first 2 questions are going to be about your email and password you are using\n to send')
  prGreen('this email will be stored on your local computer encrypted seperate from ')
  prGreen('from the rest of the configuration')
  email = input("\nEnter your email(example@gmail.com): " )
  prCyan(email)
  pas = input("\nEnter your password(examplepassword): ")
  prCyan("*******")
  lo = {email:pas}
  save_yaml(
    fname = f'{conf_dir}/.cred.yaml',
    fdest = 'home',
    content = lo
    )
  encrypt(
    key = key,
    fname = f'{conf_dir}/.cred.yaml',
    e_fname = f'{conf_dir}/.cred_en.yaml',
    fdest = 'home'
    )
  remove_file(f'{conf_dir}/.cred.yaml')

  run: str = str(input(
    "\nEnter the time to run the script daily(default: 05:00): ") or '05:00')
  prCyan(run)
  numb_lines: int = int(input(
    "\nEnter the number of lines from the end of log file to send(default: 30): ") or 30)
  prCyan(numb_lines)
  
  send_list = input_loop(
    subject= "email address",
    description = 'to send to (example@gmail.com)')

  logf = input_loop(
    subject= "log file",
    description = 'to check relative to your home dir (Example: Logs/net_backup.log)')
  load = {
    'runtime': run,
    'lines': numb_lines,
    'sendto': send_list,
    'logs': logf
    }
  save_yaml(
    fname =f'{conf_dir}/emailog_set.yaml',
    fdest = 'home',
    content = load)
  prYellowBold('\nThis completes the wizard')
  print('The configuration file has been written to disk')
  prRedMulti('If you change the settings you can edit', f'{conf_dir}/emailog_set.yaml')
  print('in your home dir.')
  prGreenBold("This wizard won't run any more, So the script can now be run automatically\n")


def  call_funtion():  
  settings = open_yaml(
  fname = f"{conf_dir}/emailog_set.yaml",
  fdest = "home",
  )
  kf = f"{conf_dir}/.info.key"
  ef = f"{conf_dir}/.cred_en.yaml"
  st = settings['sendto']
  log = settings['logs']
  lines = settings['lines']
  for i in range(len(log)):
    body = mail_body(log[i], lines)
    sub = f'Backup Log: for {username} (Log file: {log[i]})'
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

dir_exist = check_dir(conf_dir)
if dir_exist == False:
  config_setup_email(conf_dir)
every().day.at(str(settings())).do(call_funtion)

if __name__ == "__main__":
  try:
    print('waiting on timer')
    while True:
      run_pending()
      sleep(1)
  except KeyboardInterrupt as e:
    print(e)
    print('Interrupted')
