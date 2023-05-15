import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendEmail(message, to):
    #Writing Email details
    msg = MIMEMultipart('alternative')
    msg[ 'Subject'] = "PizSub"
    msg['From' ] = 'belocarrent@gmail.com'
    msg[ 'To'] = "beluskostefan@gmail.com"
    msg. attach(MIMEText (message, 'html'))
    img_o = open("Images/Belo_logo.jpg","rb").read()
    img = MIMEImage(img_o,"jpg",name ="logi.jpg")
    msg.attach(img)
    #Writing Server Details
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server. ehlo()
    server.starttls()
    server. login(email_from, password)
    print( "Connected To Server")
    server. sendmail(email_from, emial_to, msg.as_string())
    print("Email sent")

email_from ='belocarrent@gmail.com'
emial_to = "beluskostefan@gmail.com"
password = "lhhoqqwekekeoxhz"
message =f"""
<body>
<h1> Ďakujeme za objednávku</h1>
<table>
  <tr>
    <th>meno</th>
    <td>{0}</td>
  </tr>
  <tr>
    <th>adresa</th>
    <td>{0}</td>
  </tr>
  <tr>
    <th>auto</th>
    <td>{0}</td>
  </tr>
  <tr>
    <th>datum od</th>
    <td>{0}</td>
  </tr>
  <tr>
    <th>datum do</th>
    <td>{0}</td>
  </tr>
  <tr>
    <th>cena</th>
    <td>{0}</td>
  </tr>
</table>

</body>
</html>
"""
sendEmail(message,emial_to)