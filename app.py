import socket
import thread
import os

gmsgs = dict()
dict = {}
username = ""
check = True
groupcheck = True

def GMSG(string, i):

	name = ""
	user = ""
	message = ""
	newmsg = ""

	while string[i] != "/":
		name = name + string[i]
		i = i+1

	i = i + 1
	while string[i] != "/":
		user = user + string[i]
		i = i+1

	i = i + 1

	while string[i] != "/":
		message = message + string[i]
		i = i + 1
		newmsg = {user: message}
	if(gmsgs.has_key(name) == True):
		gmsgs[name].append(newmsg)
	else:
		newgrp = [newmsg]
		gmsgs.update({name: newgrp})

	i = i + 1
	return string[i:]

def mesg(string, i):
	username = ""
	message = ""

	while string[i] != "/":
		username = username + string[i]
		i = i + 1

	i = i + 1
	while string[i] != "/":
		message = message + string[i]
		i = i + 1

	if(dict.has_key(username) == True):
		dict[username].append(message)
	else:
		newstring = [message]
		dict.update({username: newstring})

	i = i + 1	
	return string[i:] 

def keys(string, s):
	print "You have messages from: " 
	print "users:"  
	print dict.keys()
	print "groups:" 
	print gmsgs.keys()
	print "(note you can only view group messages from option 4)"
	global username

	username = raw_input("Who's messages do you want to see? enter \"**\" to go back: ")
	while not (username in dict):
		if(username == "**"):
			break;
		else:
	 		print "invalid username, try again: "
	 		print dict.keys()
	 		print gmsgs.keys()
	 		username = raw_input("Who's messages do you want to see? enter \"**\" to go back: ")			

	s.send(username)
	return ""

def keyreader(string, s):
	while string != "":
		keyword = string[0:4]
		i = 0
		if(keyword == "mesg"):
			string = mesg(string[5:], i)

		elif(keyword == "keys"):
			string = keys(string, s)

		elif(keyword == "GMSG"):
			string = GMSG(string[5:], i)

def recv(username, s):
	while check:
		if username in dict:
			for i in dict.get(username):
				print username + ": " + i
			dict.pop(username, None)

def chat(username, s):
	chatmessage = ""
	global check
	check = True
	thread.start_new_thread(recv,(username, s))

	while chatmessage != "**":
		chatmessage = raw_input()
		s.send(chatmessage)

	check = False

def grouprecv(group, s):
	while groupcheck:
		if group in gmsgs:
			for mesg in gmsgs.get(group):
				print (mesg.keys())[0] + ": " + (mesg.values())[0]
			gmsgs.pop(group, None)

def groupchat(group, s):
	chatmessage = ""
	global groupcheck
	groupcheck = True
	thread.start_new_thread(grouprecv,(group, s))


	while chatmessage != "*?":
		chatmessage = raw_input()
		s.send(chatmessage)
	groupcheck = False

def Main():
	ip = '127.0.0.1'
	port = 50000
	s = socket.socket()
	s.connect((ip,port))
	path = ""
	name = ""
	print("connected \n")
	global username
	while True:
		string = s.recv(1024)
		if(string[0:4] in ("mesg", "keys", "GMSG")):	
			keyreader(string, s)
		elif(string[0:5] == "list/"):
			print string[5:]
			s.send('ok')
		elif(string == "Who do you want to send a message to? Enter Username."):
		 	username = raw_input(string + '\n' + "Enter name: ")
			s.send(username);
		elif(string == "Username does not exist, Please re-enter Username or enter \"**\" to go back to the Main Menu"):
		 	username = raw_input(string + '\n' + "Enter name or **: ")
			s.send(username);
		elif(string == string == "What message do you want to send?Enter \"**\" to stop sending message and go back to the Main menu."):
			print string + ": "
			thread.start_new_thread(chat,(username, s))
		elif(string == "What message do you want to send in the group? or enter \"*?\" for options" or string == "What message do you want to send in the group? or enter *? to go back" or string == "You're not an admin, send a message" or string == "returning to chat" or string == "No command recieved, Send a message."):
			print string + '\n'
			thread.start_new_thread(groupchat,(name, s))	
		elif(string == "What do you want to name the group?"):
			name = raw_input(string + '\n' + "name: ")
			s.send(name)
		elif(string == "Group already exists, please re-enter name or enter \"**\" to go back to the main menu"):
			name = raw_input(string + '\n' + "Enter name or **: ")
			s.send(name)
		elif(string == "Which group do you want to send a message in?" or string == "Group does not exist, please enter name again. To go back enter \"**\" " or string == "Sorry but you are not added in this group, please try again.  To go back enter \"**\""):
			name = raw_input(string + '\n' + "Enter name or **: ")
			s.send(name)
		else:
			resp = raw_input(string + '\n')
			s.send(resp)
	s.close()

if __name__ == "__main__":
	Main()
