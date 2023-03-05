import smtplib
from email.message import EmailMessage
import random

def send_email(receivers_mail):
    port = 465  # For SSL
    password = 'akbytjsvqgcypzlw'
    sender_email = "appuninet@gmail.com"
    otp = ''.join([str(random.randint(0,9)) for i in range(6)])
    
    message = str(otp)
    newMessage = EmailMessage()
    
    newMessage['Subject'] = "UniNet Registration OTP" 
    newMessage['From'] = sender_email                 
    newMessage['To'] = receivers_mail   
    newMessage.set_content('''
<!DOCTYPE html>
<html>
    <body>
        <div style="background-color:#42817a;padding:10px 20px;">
            <h2 style="font:Gothic,'Times New Roman', Times, serif;color:#ffffff;">The OTP for registration in UniNet APP is {otp}</h2>
        </div>
    </body>
</html>
'''.format(otp = message), subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', port) as smtp:
        
        smtp.login(sender_email, password)              
        smtp.send_message(newMessage)
    
    return otp

