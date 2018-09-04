#!/usr/bin/env python

import subprocess
import sys
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Port:
	def __init__(self, attb):
		self.number = attb[0]
		self.stat = attb[1]
		self.tcp = attb[2]
		self.proto = attb[4]
		self.name = attb[5]

class Target:
	def __init__(self, address)
		self.address = address
		self.pListTCP = []
		self.pLIstUDP = []

	def getTCP:
		pList = []
		for p in self.pListTCP:
			pList.append(p.number)

		return pList

	def getUDP:
		pList = []
		for p in self.pListUDP:
			pList.append(p.number)

		return pList

OKPLUS = bcolors.OKBLUE + '[+]' + bcolors.ENDC + ' '
ERROR = bcolors.FAIL + '[-]' + bcolors.ENDC + ' '
WARNING = bcolors.WARNING + '[?]' + bcolors.ENDC + ' '
INFO = bcolors.WARNING + '[!]' + bcolors.ENDC + ' '
HEADER = bcolors.HEADER + '****' + bcolors.ENDC + ' '

PORT = 0
STAT = 1
TCP = 2
NULL = 3
PROTO = 4
NAME = 6

NMAPSCRIPTS = '/usr/share/nmap/scripts/'


# This creates directories for each of the IPs that it was given.
def setUp(ipList):
	print(OKPLUS + "Creating Directories")
	for ip in ipList:
		subprocess.call(["mkdir", "-p", ip + "/scans"])
		subprocess.call(["mkdir", "-p", ip + "/source"])
		subprocess.call(["mkdir", "-p", ip + "/lists"])
		subprocess.call(["touch", ip + "/notes.txt"])


# This will Run a basic nmap scan on the IPs 
def nmapScan(ipList):
	for ip in ipList:
		tList.append(Target(ip))
		print(OKPLUS + "Running Basic Nmap Scans on IP " + bcolors.OKGREEN + ip + bcolors.ENDC)
		output = subprocess.check_output(["nmap", "-sT", "-sC", '-sV', '-oA', ip + '/scans/nmap-scan-TCP', ip])
		output = subprocess.check_output(["nmap", "-sU" ,"-sC", '-sV', '-oA', ip + '/scans/nmap-scan-UDP', ip])


# This will parse the nmap scan output for each of the IPs and store the information.
# It will also look for relative nmap scripts and save a list of them in the IPs dir.
def parseNmap(ipList, proto):
	for ip in ipList:
		portInfo[ip] = []
		print(OKPLUS + "Gathering Port Information on IP " + bcolors.OKGREEN + ip + bcolors.ENDC)
		try:
			with open(ip+'/scans/nmap-scan-' + proto + '.gnmap', 'r') as fp:
				for line in fp:
					line = line.strip()
					if line.startswith('#'):
						continue

					if line.find('Ports') != -1:
						tempLine = line.split(':')[2].strip()
						tempPort = tempLine.strip().split(',')
						for p in tempPort:
							port = p.strip().split('/')
							if port[STAT] == 'open':
								portInfo[ip].append(port)

		except IOError as e:
			print(ERROR + str(e))

		output = subprocess.check_output(['ls', NMAPSCRIPTS])
		lines = output.split()
		
		fp = open(ip + '/scriptSuggestions.txt', 'w')
		protos = []
		scriptList = []
		for p in portInfo[ip]:
			if p[PROTO] not in protos:
				protos.append(p[PROTO])
				scriptList = scriptList + [s for s in lines if p[PROTO] in s]
		
		for item in scriptList:
			fp.write(item + '\n')

		fp.close()
		print(INFO + "Nmap Script suggestions for ip " + ip + " are stored in " + bcolors.OKGREEN + ip + '/scriptSuggestions.txt' + bcolors.ENDC)


# This will print out all the open ports that were found on each box.
for ip in ipAddresses:
	print(INFO + bcolors.OKGREEN + ip + bcolors.ENDC + ' has the open ports:')
	for i in portInfo[ip]:
		print('\t' + bcolors.OKBLUE + i[PORT] + bcolors.ENDC + "  " + i[PROTO] + "      " + i[NAME])


# This will check to see if there are any web servers running on the box
# and run dirb and nikto on them
for ip in ipAddresses:
	for i in portInfo[ip]:
		if i[PROTO] == 'http' or i[PROTO] == 'https':
			print(OKPLUS + "Running dirb on ip address " + ip + " port " + i[PORT])
			output = subprocess.check_output(["dirb", i[PROTO] + '://' + ip + ':' + i[PORT], '-r', '-o', ip + '/scans/dirb-scan-port-' + i[PORT] + '.txt'])
			print(INFO + "Results stored in " + ip + "/scans/dirb-scan.txt")
			print(OKPLUS + "Running nikto on ip address " + ip + " port " + i[PORT])
			output = subprocess.check_output(["nikto", "-h", i[PROTO] + '://' + ip + ':' + i[PORT], '-o', ip + '/scans/nikto-scan-port-' + i[PORT] + '.txt'])
			print(INFO + "Results stored in " + ip + "/scans/nikto-scan.txt")


# This will run a full port scan of each of the IP addresses and exit
for ip in ipAddresses:
	print(ip)
	print(OKPLUS + "Starting full port scan on ip " + ip)
	process[ip] = subprocess.Popen(['nmap', '-p-', '-oA', ip + '/scans/nmap-full-port-scan', '--max-retries=3', '--max-scan-delay=20ms', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	line = output.split()
	print(INFO + 'Process started with PID of ' + bcolors.OKBLUE + str(process[ip].pid) + bcolors.ENDC)

time.sleep(10)
subprocess.call(['stty','sane'])
exit()


if __name__ == '__main__':

	if len(sys.argv) != 2:
		print(ERROR + "Usage:   " + sys.argv[0] + " IPs.txt")
		exit()

	FILE = sys.argv[1]
	targets = []
	ipAddresses = []
	process = {}
	portInfo = {}

	with open(FILE, 'r') as fp:
		for ip in fp:
			ipAddresses.append(ip.strip())
			targets.append(Target(ip))
			

	setUp(ipAddresses)

