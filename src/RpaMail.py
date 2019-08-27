import env
import smtplib
from email.mime.text import MIMEText


class mail_msg:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('sub0713@gmail.com', env.mail_password)

    def __init__(self, mail):
        self.mail = mail

    def msg(self, err):
        msg = MIMEText("Error occurred during check : {err}".format(err=err))
        msg['Subject'] = '[KTing]Error occurred during check'
        mail_msg.s.sendmail("sub0713@gmail.com", self.mail, msg.as_string())
        mail_msg.s.quit()