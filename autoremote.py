from __future__ import print_function
import re 
import os
import requests
import subprocess
import hexchat
__module_name__ = 'Hexchat Alerts to Autoremote'
__module_author__ = 'Pip'
__module_version__ = '1'
__module_description__ = 'Hexchat Alerts to Autoremote'

class autoremote:
	def __init__(self):
		#self.name=raw_input("Enter the name of THIS device:")
		#self.url=raw_input("Enter YOUR Autoremote URL:")
		self.name="Home-Hexchat"
		self.url="Enter YOUR Autoremote URL"
		self.key_url=requests.get(self.url,allow_redirects=True)
		if self.key_url.status_code==200:
			self.url=self.key_url.url
			self.key=re.search(r'key\=(.*)',self.url,re.DOTALL)
			self.key=self.key.group(1)
		else:
			raise 		
		print ('device name:',self.name)
		print ('fetching global ip')
		self.publicip = requests.get("http://ipecho.net/plain")
		if self.publicip.status_code==200:
			self.publicip=self.publicip.text
			print ('global IP:',self.publicip)
		print ('fetching local ip')
		self.localip=os.popen("ifconfig|grep inet|head -1|sed 's/\:/ /'|awk '{print $3}'").read()
		print ('local IP:',self.localip)
	
	def register(self):
		self.reg_url="http://autoremotejoaomgcd.appspot.com/registerpc?key={0}&name={1}&id=3&type=linux&publicip={2}&localip={3}".format(self.key,self.name,self.publicip,self.localip)
		self.reg_req=requests.get(self.reg_url)
		if self.reg_req.status_code==200:
			print ('Registered successfully')
	def send(self, word, word_eol, userdata):
		self.message='HexchatData=:=' + word_eol[0]
		print ('Alert sent to device successfully')
		self.send_url="http://autoremotejoaomgcd.appspot.com/sendmessage?key={0}&message={1}".format(self.key,self.message)
		self.send_req=requests.get(self.send_url)

if __name__ == "__main__":
	pc=autoremote()
	pc.register()
	#pc.send("hello Jarvis")

hexchat.hook_print('Channel Msg Hilight', pc.send)
