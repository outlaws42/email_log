from tmod import open_yaml, open_file, check_file_age, last_n_lines
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser

version = '2021-04-03'
username = getuser()

def  call_funtion():
  print(username)
  if username == 'cara':
    mail('Logs/net_backup.log', 30)
    mail('Logs/backupUSB.log', 30)
  elif username == 'troy':
    mail('Logs/net_backup.log', 30)

def file_age(filename, lines):
  age =  check_file_age(filename)
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

def mail(filename, lines):
  us, psw = login_info()
  recipients = open_file('.rec', 'home').splitlines()
  content = file_age(filename, lines)
  print(content)

  subject = f'Backup Log: for {username} (Log file: {filename})'
  message = f'Subject: {subject}\n\n{content}'
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


every().day.at("07:41").do(call_funtion)

while True:
    run_pending()
    sleep(1)