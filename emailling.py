import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD= 'jdbdhdbvdhdh'
EMAIL = 'dmgikman1994@gmail.com'
RECIEVER_EMAIL = 'dmgikman1994@gmail.com'


def send_email(image_path):
    email_msg = EmailMessage()
    email_msg['Subject'] = "New Object found"
    email_msg.set_content("Hey we're going to")

    with open(image_path,"rb") as image_file:
        content = image_file.read()
    email_msg.add_attachment(content,maintype='image',subtype=imghdr.what(None,content))

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL,PASSWORD)
    gmail.send_message(EMAIL,RECIEVER_EMAIL,email_msg.as_string())
    gmail.quit()

if __name__ == '__main__':
    send_email('images')