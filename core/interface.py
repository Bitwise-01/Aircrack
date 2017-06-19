# Date: 06/14/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Interface handler
#
# imports
import os
import subprocess

class Interface(object):
 def __init__(self):
  self.iface = None
  self.devnll = open(os.devnull,'w')

 def newMac(self):
  self.run(['macchanger','-r','-b',self.iface])

 def oldMac(self):
  self.run(['macchanger','-p',self.iface])

 def down(self):
  self.run(['ifconfig',self.iface,'down'])

 def up(self):
  self.run(['ifconfig',self.iface,'up'])

 def stopNetwork(self):
  self.run(['service','network-manager','stop'])

 def startNetwork(self):
  self.run(['service','network-manager','start'])

 def boost(self):
  self.setCntry()
  self.run(['iwconfig',self.iface,'txpower','30'])

 def setCntry(self):
  self.run(['iw','reg','set','BO'])

 def monitor(self):
  self.run(['iwconfig',self.iface,'mode','monitor'])

 def managed(self):
  self.run(['iwconfig',self.iface,'mode','managed'])

 def monitorMode(self,iface):
  self.iface = iface
  self.down()
  self.boost()
  self.newMac()
  self.monitor()
  self.stopNetwork()
  self.up()

 def managedMode(self,iface=None,rec=5):
  self.iface = iface if not self.iface else self.iface
  self.down()
  self.oldMac()
  self.managed()
  self.startNetwork()
  self.up()
  if rec:self.managedMode(rec=rec-1)

 def run(self,cmd):
  subprocess.Popen(cmd,stdout=self.devnll,stderr=self.devnll).wait()
