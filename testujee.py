import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage


def run():
    smtp_port = 587
    smtp_server = "smtp.gmail.com"


    email_from ='belocarrent@gmail.com'
    emial_to = "beluskostefan@gmail.com"
    pswd = "lhhoqqwekekeoxhz"

    simple_email_context = ssl.create_default_context()

    try:
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        print("Conected")
        message = MIMEMultipart("alternatives")
        message["Subject"] = "Dakujeme za objednavku"
        message["from"] = email_from

        message["to"] = emial_to
        text = "Toto je kod ktory generuje program\n a totot "

        html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
hello

</body>
</html>
        """
        text = MIMEText(text, "plain")
        html = MIMEMultipart(html,"html")
        #print(text,html)
        message.attach(text)

        message.attach(html)
        TIE_server.sendmail(email_from, emial_to, message.as_string())
        print("Send")
    except Exception as e:
        print(e)
    finally:
        TIE_server.quit()


if __name__ == '__main__':
    run()
