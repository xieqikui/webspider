# -*- coding:utf-8 -*-
import sys
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
from email import encoders
import smtplib
import os, sys

class SendEmail():
	def __init__(self, senderaddr, senderpwd, receiveraddr, smtpserver, etext, efrom, eto, esubject, smptport, etype, filelist):
		self.senderaddr = senderaddr
		self.senderpwd = senderpwd
		self.receiveraddr = receiveraddr
		self.smtpserver = smtpserver
		self.etext = etext
		self.efrom = efrom
		self.eto = eto
		self.esubject = esubject
		self.smptport = int(smptport)
		self.etype = etype
		self.filelist =filelist
	def __formataddr__(self, s):
		name, addr = parseaddr(s)
		# print ('name:' ,name)
		# print ('addr:' ,addr)
		# print ('formataddr:' ,formataddr((Header(name, 'utf-8').encode(), addr)))
		return formataddr((Header(name, 'utf-8').encode(), addr))
	def __emailmsg__(self):
		msg = MIMEText(self.etext, self.etype, 'utf-8')
		msg['From'] = self.__formataddr__(self.efrom + '<' + self.senderaddr + '>') 
		msg['To'] = self.__formataddr__(self.eto + '<' + self.receiveraddr + '>')
		msg['Subject'] = Header(self.esubject, 'utf-8').encode()
		return msg
	# def __emailmsgwithattachment__(self):
	# 	msg = MIMEMultipart()
	# 	msg['From'] = self.__formataddr__(self.efrom + '<' +self.senderaddr + '>')
	# 	msg['To'] = self.__formataddr__(self.eto + '<' + self.receiveraddr + '>')
	# 	msg['Subject'] = Header(self.esubject, 'utf-8').encode()
	# 	# 邮件正文是MIMEText
	# 	msg.attach(MIMEText(self.etext, self.etype, 'utf-8'))
	# 	with open(self.filelist, 'rb') as f:
	# 		# 设置附件的MIME和文件名，这里是png类型
	# 		mime = MIMEBase('image', 'png', filename = os.path.basename(filelist))
	# 		# 加上必要的头信息
	# 		mime.add_header('Content-Disposition', 'attachment', filename = os.path.basename(filelist))
	# 		mime.add_header('Content-ID', '<0>')
	# 		mime.add_header('X-Attachment-Id', '0')
	# 		# 把附件的内容读进来：
	# 		mime.set_payload(f.read())
	# 		# 用Base64编码
	# 		encoders.encode_base64(mime)
	# 		# 将附件添加到MIMEMultipart
	# 		msg.attach(mime)
	# 		return msg
	def __emailmsgwithattachment__(self):
		msg = MIMEMultipart()
		msg['From'] = self.__formataddr__(self.efrom + '<' +self.senderaddr + '>')
		msg['To'] = self.__formataddr__(self.eto + '<' + self.receiveraddr + '>')
		msg['Subject'] = Header(self.esubject, 'utf-8').encode()
		# 邮件正文是MIMEText
		msg.attach(MIMEText(self.etext, self.etype, 'utf-8'))
		fid = 0
		for filepath in self.filelist:
			filename = os.path.basename(filepath)
			filetype = filename.split('.')[-1]
			with open(filepath, 'rb') as f:
				# 设置附件的MIME和文件名，这里是png/jpg类型
				mime = MIMEBase('image', filetype, filename = filename)
				# 加上必要的头信息
				mime.add_header('Content-Disposition', 'attachment', filename = filename)
				mime.add_header('Content-ID', '<' + str(fid) + '>')
				mime.add_header('X-Attachment-Id', str(fid))
				# 把附件的内容读进来：
				mime.set_payload(f.read())
				# 用Base64编码
				encoders.encode_base64(mime)
				# 将附件添加到MIMEMultipart
				msg.attach(mime)
			fid += 1
		return msg
	def __smptsendemail__(self, msg):
		try:
			# server = smtplib.SMTP_SSL()
			server = smtplib.SMTP_SSL(self.smtpserver, self.smptport)
			server.set_debuglevel(1)
			# server.connect(smtpserver, 465)
			server.login(self.senderaddr, self.senderpwd)
			server.sendmail(self.senderaddr, self.receiveraddr, msg.as_string())
			print ('Send successfully')
		except Exception as e:
			print ('Send fail')
		finally:
			server.quit()
if __name__ == '__main__':
	senderaddr = '525129486@qq.com'
	# senderpwd = 'qkxie00280873'
	senderpwd = 'fuqwtxndnevrcbbg'
	receiveraddr = 'zhiacting@163.com'
	# smtpserver = 'smtp.163.com'
	smtpserver = 'smtp.qq.com'
	# etext = '使用python编程语言中email模块和smtp模块实现发邮件功能！'
	etabletile = '<tr><th>序号</th><th>电影名</th><th>评分</th><th>海报</th></tr>'
	etablecontent = ''
	L1 = ['1', '2']
	L2 = ['电影1', '电影2']
	L3 = ['8.0', '8.1']
	L4 = ['电影1.jpg', '电影2.jpg']
	for i in range(2):
		etablecontent = etablecontent + '<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>'.format(L1[i], L2[i], L3[i], L4[i])
	etext = '<html><body><table>' + etabletile + etablecontent + '</table></body></html>'
	efrom = 'QQ邮箱'
	eto = '163邮箱'
	esubject = '邮件发送功能测试......'
	smptport = 465
	# etype = 'plain'
	etype = 'html'
	filelist = []
	filelist.append(os.path.join(os.getcwd(), '血观音.jpg'))
	filelist.append(os.path.join(os.getcwd(), '大佛普拉斯.jpg'))
	obj = SendEmail(senderaddr, senderpwd, receiveraddr, smtpserver, etext, efrom, eto, esubject, smptport, etype, filelist)
	obj.__smptsendemail__(obj.__emailmsgwithattachment__())


