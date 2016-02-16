import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
import os

def mailer():

	emailfrom = "Megatron.matvik@gmail.com"
	password = "rquqozfpharupslf"
	emailto = "peter.borovykh@gmail.com"

	file1 = "result1.csv"
	file2 = "result2.csv"
	file3 = "result3.csv"


	msg = MIMEMultipart()
	msg["From"] = emailfrom
	msg["To"] = emailto
	msg["Subject"] = "This is a Subject of Email"
	msg.preamble = "Tis is a preamble of Email"

	ctype, encoding = mimetypes.guess_type(file1)
	if ctype is None or encoding is not None:
		ctype = "application/octet-stream"


	maintype, subtype = ctype.split("/", 1)

	for fl in [file1,file2,file3]:
		fp = open(fl, "rb")
		attachment = MIMEBase(maintype, subtype)
		attachment.set_payload(fp.read())
		fp.close()
		encoders.encode_base64(attachment)
		attachment.add_header("Content-Disposition", "attachment", filename=fl)
		msg.attach(attachment)

	server = smtplib.SMTP("smtp.gmail.com:587")
	server.starttls()
	server.login(emailfrom,password)
	server.sendmail(emailfrom, emailto, msg.as_string())
	server.quit()

	print "Email sent"

def main():
	os.system('python dayX/dayX.py')
	os.system('python week52/test_week.py')
	os.system('python golden_cross/test_cross.py')
	os.system('clear')
	print 'Sending results...'
	mailer()

main()
