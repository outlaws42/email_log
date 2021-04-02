from tmod import open_yaml, open_file, open_log_file
# from email.message import EmailMessage
# from email.mime.text import MIMEText
# import base64
import schedule
import smtplib
import time

def login_info():
  ps = open_yaml('.cred.yaml', 'home')
  for key, value in ps.items():
    us = key
    psw = value
  return [us,psw]

def mail():
  us, psw = login_info()
  recipients = open_file('.rec', 'home').splitlines()

  # log_file = open('/home/troy/Logs/net_backup.log', 'r')
  # content = log_file.read()  # base64
  # content = MIMEText(log_file.read())
  # log_file.close()
  content = open_log_file('net_backup.log', 'home')
  print(content)

  subject = 'Backup Log'
  message = f'Subject: {subject}\n\n{content}'
  try:
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(us, psw)
    # mail.sendmail(us, recipients, content)
    mail.sendmail(us,recipients, message)
    mail.close()
    print('Successfully sent email')
  except Exception as e:
    print('Could not send email because')
    print(e)


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at("03:47").do(mail)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)