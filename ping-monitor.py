#!/bin/env python
import os, re, time
print "Ventrilo Ping Analyzer by Josh Rendek Copyright 2009"
hostname=raw_input("What is the hostname/ip? ")
port=raw_input("What is the port? ")
times_to_test=raw_input("How many samples? ")
seconds_between=raw_input("How many seconds between tests? ")
users_avg = {}
users_max = {}
users_min = {}
counter = 0
while counter < int(times_to_test):
	stdout_handle = os.popen("./ventrilo_status-Linux -c2 -t" + hostname + ":" + port, "r")
	output = stdout_handle.read().split('\n')
	for x in output:
		line = re.finditer("CLIENT: (.*)", x) 
		for match in line:
			l = match.group()
			name = re.finditer("NAME=[A-Za-z0-9]+", l)
			for n in name:
				user_name = n.group().split("=")[1]
				ping = l.split(',')[3].split('=')[1]
				#print user_name + " Ping: " + ping
				if counter == 0:
					users_avg[user_name] = int(ping)
					users_max[user_name] = int(ping)
					users_min[user_name] = int(ping)
				else:
					#print "Previous value was: " + ping
					users_avg[user_name] = (int(ping)+int(users_avg[user_name]))/2
					if int(ping) > users_max[user_name]:
						users_max[user_name] = int(ping)
					if int(ping) < users_min[user_name]:
						users_min[user_name] = int(ping)
				
	counter+=1	
	print "Done test " + str(counter)
	time.sleep(int(seconds_between))
print "Average ping for users: "
print users_avg
print "Max ping for users: "
print users_max
print "Min ping for users: "
print users_min