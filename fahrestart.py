# Folding@Home Restart Script for Windows (BaH)
# Command-line arguments: number of gpus to restart (min 1)


# Customize paths etc.
hostname="localhost"
FAHPath ="C:\Program Files (x86)\FAHClient\FAHClient.exe"
port="36330"


# Begin

import sys
import telnetlib
import win32api, win32con
import wmi
from time import sleep

gpuSlots = list(range(1,1+int(sys.argv[1])))

# pauses folding via remote and closes telnet session
tnbot=telnetlib.Telnet(hostname, port)
tnbot.read_until(b"> ")
tnbot.write(b"pause\n")
tnbot.write(b"exit\n")

# finds and terminates the folding process on windows

wmibot = wmi.WMI()

for process in wmibot.Win32_Process(name="FAHClient.exe"):
  process.Terminate()

# creates new folding process
wmibot.Win32_Process.Create(CommandLine="C:\Program Files (x86)\FAHClient\FAHClient.exe")

# wait for startup

sleep(15)

# pauses CPU folding
tnbot=telnetlib.Telnet(hostname, port)
tnbot.read_until(b"> ")

#for number of gpus, restart them

for slotNum in gpuSlots:
  tnbot.write(b"run "+ str(slotNum)+"\n")
tnbot.write(b"exit\n")





