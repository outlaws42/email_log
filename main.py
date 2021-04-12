# -*- coding: utf-8 -*-
version = '2021-04-12'

from tmod import open_file, open_yaml, check_file_age, last_n_lines
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser
from os import environ


username = getuser()
timer = open_file('.logtimer', 'home', '13:15')
print(timer)

def  call_funtion():
  print(username)
  if username == 'cara':
    log = ['Logs/net_backup.log', 'Logs/backupUSB.log']
    for i in len(log):
      body = mail_body(log[i], 30)
      sub = f'Backup Log: for {username} (Log file: {log[i]})'
      mail(body, sub)

  elif username == 'troy':
    log = 'Logs/net_backup.log'
    body = mail_body(log, 30)
    sub = f'Backup Log: for {username} (Log file: {log})'
    mail(body, sub)
  else:
    print('Unknown log file')

def mail_body(filename, lines):
  age =  check_file_age(filename, 'home')
  print(f'file age {age} hours')
  if age >= 24:
    con = f"The log file {filename} for {username} is {age} hours old check backup"
  else:
    con = last_n_lines(filename, lines)
  return con

def login_info():
  ps = open_yaml('.cred.yaml', 'home')
  for key, value in ps.items():
    us = key
    psw = value
  return [us,psw]

def mail(body, subject):
  us, psw = login_info()
  recipients = open_file('.rec', 'home').splitlines()
  message = f'Subject: {subject}\n\n{body}'
  print(message)
  try:
    mail = SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(us, psw)
    mail.sendmail(us,recipients, message)
    mail.close()
    print('Successfully sent email')
  except Exception as e:
    print('Could not send email because')
    print(e)


every().day.at(timer).do(call_funtion)

while True:
    run_pending()
    sleep(1)