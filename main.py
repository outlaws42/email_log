# -*- coding: utf-8 -*-
version = '2021-04-21'

from tmod import (
  open_file, open_yaml, check_file_age, last_n_lines,
   decrypt_login, mail)
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser
from icecream import ic

ic.configureOutput(includeContext=True)

default: dict = open_yaml(
  fname = 'default.yaml',
  fdest = 'relative',
  )

username = getuser()
# timer = open_file('.logtimer', 'home', '13:15')
# print(timer)
settings = open_yaml(
  fname = '.config/emailog_set.yaml',
  fdest = 'home',
  def_content = default,
  )
ic(settings['runtime'])

def  call_funtion():
  print(username)
  if username == 'cara':
    log = ['Logs/net_backup.log', 'Logs/backupUSB.log']
    for i in range(len(log)):
      body = mail_body(log[i], 30)
      sub = f'Backup Log: for {username} (Log file: {log[i]})'
      key = open_file(
        fname = ".config/info.key", 
        fdest = "home",
        mode ="rb")
      login = decrypt_login(key = key, 
      e_fname = ".config/.cred_en.yaml", 
      fdest = "home"
      )
      mail(
        body = body, 
        subject = sub, 
        send_to = settings['sendto'],
        login = login
        )

  elif username == 'troy':
    log = 'Logs/net_backup.log'
    body = mail_body(log, 30)
    sub = f'Backup Log: for {username} (Log file: {log})'
    key = open_file(
           fname = ".config/info.key", 
           fdest = "home",
           mode ="rb"
           )
    login = decrypt_login(key = key, 
      e_fname = ".config/.cred_en.yaml", 
      fdest = "home"
      )
    mail(
      body = body, 
      subject = sub, 
      send_to = settings['sendto'],
      login = login
        )
  else:
    print('Unknown log file')

def mail_body(filename, lines):
  age =  check_file_age(filename, 'home')
  print(f'file age {age} hours')
  if age >= 24:
    con = f"The log file {filename} for {username} is {age} hours old check backup"
  else:
    con = last_n_lines(filename, lines,'home')
  return con

def login_info():
  ps = open_yaml('.cred.yaml', 'home')
  for key, value in ps.items():
    us = key
    psw = value
  return [us,psw]

# def mail(body, subject):
#   us, psw = login_info()
#   recipients = settings['sendto'] #open_file('.rec', 'home').splitlines()
#   message = f'Subject: {subject}\n\n{body}'
#   print(message)
#   try:
#     mail = SMTP('smtp.gmail.com', 587)
#     mail.ehlo()
#     mail.starttls()
#     mail.ehlo()
#     mail.login(us, psw)
#     mail.sendmail(us,recipients, message)
#     mail.close()
#     print('Successfully sent email')
#   except Exception as e:
#     print('Could not send email because')
#     print(e)


every().day.at(settings['runtime']).do(call_funtion)

while True:
    run_pending()
    sleep(1)