import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv('EMAIL_HOST')
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')

    def send_email(self, address_list, subject, body):
        problems = []
        try:
            with smtplib.SMTP(self.smtp_server, port=587) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                
                for address in address_list:
                    # Criar mensagem com codificação UTF-8 adequada
                    msg = MIMEMultipart('alternative')
                    msg['From'] = f"Representa <noreply@representa.com>"
                    msg['To'] = address
                    msg['Subject'] = subject
                    
                    # Anexar corpo com codificação UTF-8
                    part = MIMEText(body, 'plain', 'utf-8')
                    msg.attach(part)
                    
                    # Enviar com formato de mensagem adequado
                    if server.sendmail(from_addr=self.email_user, to_addrs=address, msg=msg.as_string()) != {}:
                        problems.append(address)
            
            if problems:
                print(f"Failed to send email to the following addresses: {problems}")
                return False
            else:
                print("Email sent successfully")
                return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
        

if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.send_email(['fernandorldf@gmail.com'], 'Test Subject', 'This is a test email.')