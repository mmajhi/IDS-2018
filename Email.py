import smtplib,imaplib
import os,email,time,re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def sendMail(num):
    send_from = "arghaberry@gmail.com"
    send_to = "mayukhmajhi@gmail.com"
    text = "Intruder detected"
    subject = 'Home Surveillance'

    file1 = 'image' + str(num) + '.jpg'
    try:
        os.rename('video' + str(num) + '.h264', 'video' + str(num) + '.mp4')
    except:
        pass
    file2 = "video" + str(num) + ".mp4"
    file3 = 'image' + str(num) + '_2.jpg'


    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    #msg['Date'] = datetime.datetime.now()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    part1 = MIMEBase('application', "octet-stream")
    fo1 = open(file1, "rb")
    part1.set_payload(fo1.read())
    encoders.encode_base64(part1)
    part1.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file1))
    msg.attach(part1)

    part2 = MIMEBase('application', "octet-stream")
    fo2 = open(file2, "rb")
    part2.set_payload(fo2.read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file2))
    msg.attach(part2)

    part3 = MIMEBase('application', "octet-stream")
    fo3 = open(file3, "rb")
    part3.set_payload(fo3.read())
    encoders.encode_base64(part3)
    part3.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file3))
    msg.attach(part3)

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(send_from, 'nitd@12345')
    sent = smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    print('Mail Sent')

def read_email_from_gmail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('arghaberry@gmail.com', 'nitd@12345')

    mail.select('"[Gmail]/Sent Mail"')
    result, data = mail.uid('search', None, 'All')

    latest_sent_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_sent_email_uid, '(RFC822)')
    raw_email = data[0][1]

    sent_email_message = email.message_from_string(str(raw_email, 'utf-8'))
    sent_to = email.utils.parseaddr(sent_email_message['To'])
    sent_message_id = sent_email_message['Message-ID']

    while True:
        mail.select('inbox')
        result, data = mail.uid('search', None, "Unseen")

        try:
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]

            email_message = email.message_from_string(str(raw_email,'utf-8'))
            sender = email.utils.parseaddr(email_message['From'])
            in_reply_to = email_message['In-Reply-To']

            if sender[1] == sent_to[1] and sent_message_id==in_reply_to:
                print('Mail Received')
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = str(part.get_payload(decode=True), 'utf-8').lower()
                        if re.search('open', body):
                            print('Gate Opened')
                            return True
                        else:
                            print('Gate Closed')
                            return False

            print('Gate Closed')
            #mail.uid('STORE', latest_email_uid, '-FLAGS', '(\Seen)')
        except:
            pass

