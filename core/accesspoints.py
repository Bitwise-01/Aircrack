# Date: 06/14/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Accesspoints handler
#
# imports
import csv
import time
import subprocess

class Accesspoints(object):
 def __init__(self):
  self.aps = {}
  self.mem = []
  self.map = []
  self.lst = []

 def open(self,csvfile):
  with open(csvfile,'r') as csvfile:
   self.csv = csv.reader(csvfile,delimiter = ',')
   self.organize()
   self.setMap()
   self.display()
   time.sleep(1)

 def organize(self):
  for line in self.csv:
   # where router info is displayed
   if len(line) == 15:
    self.updateInfo(line)

   # where clients are displayed
   if len(line) == 7:
    self.setClient(line)

 def setClient(self,data):
  # assign
  bssid = data[5].strip()

  # filter
  if len(bssid) != 17 or not bssid in self.aps:
   return

  # update
  self.aps[bssid]['client'] = True

 def updateInfo(self,data):
  # assign
  bssid = data[0]
  chann = data[3]
  power = data[8]
  essid = data[13]

  # reassign
  power = power.strip()
  chann = chann.strip()
  essid = essid.strip()

  # check for existence
  if not bssid in self.aps:
   self.aps[bssid] = {}
   self.aps[bssid]['client'] = None

  # filter
  if not chann.isdigit() or eval(chann.strip())==-1 or eval(power.strip())==-1:
   del self.aps[bssid]
   return

  # change essid of hidden ap
  essid = essid if not '\\x00' in essid else 'HIDDEN'
  essid = essid if essid else 'UNKNOWN'

  # update
  ap = self.aps[bssid]
  ap['essid'] = essid
  ap['chann'] = chann
  ap['power'] = power

 def sort(self):
  self.mem = self.aps.keys()
  for a,alpha in enumerate(self.mem):
   for b,beta in enumerate(self.mem):
    if a==b:continue

    # set aps
    ap1 = self.aps[alpha]
    ap2 = self.aps[beta]

    # set power levels
    pw1 = ap1['power']
    pw2 = ap2['power']

    # sort
    if a>b and pw1<pw2:
     self.mem[a],self.mem[b]=self.mem[b],self.mem[a]

 def setMap(self):
  if self.aps:
   self.sort()

  if self.mem:
   del self.map[:]

  for num,mac in enumerate(self.mem):
   # assign
   ap = self.aps[mac]
   num = '{}   '.format(num) if len(str(num)) == 1 else '{}  '.format(num) if len(str(num)) == 2 else '{} '.format(num) if len(str(num)) == 3 else num
   cnt = '*' if ap['client'] else '-'
   chann = '{} '.format(ap['chann']) if len(ap['chann'])==1 else ap['chann']

   # first ouput
   if not eval(num.strip()):
    self.map.append('------------------------------------------------------------------------')
    self.map.append('|| #    ||\t Bssid\t     || Channel ||  Power  || Client || Essid ||')
    self.map.append('------------------------------------------------------------------------')
    self.map.append('------------------------------------------------------------------------')
   self.map.append('|| {} || {} ||    {}   ||   {}   ||    {}   || {}'.format(num,mac,chann,ap['power'],cnt,ap['essid']))
  self.lst = [display for line in self.map for display in line]

 def display(self):
  if self.lst:
   subprocess.call(['clear'])
   for line in self.map:
    print line
