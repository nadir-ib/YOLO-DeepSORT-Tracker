import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailAlert:
    def __init__(self, config):
        self.sender = config['email']['sender']
        self.password = config['email']['password']
        self.recipients = config['email']['recipients']
        self.smtp_server = config['email']['smtp_server']
        self.smtp_port = config['email']['smtp_port']

    def send_alert(self, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.recipients)
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'html'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.recipients, msg.as_string())
            server.quit()
        except Exception as e:
            print("Error sending email:", e)
