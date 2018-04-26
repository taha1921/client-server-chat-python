import socket 
import thread
import os
offline = dict()
online = dict()
groups = dict()
admins = dict()
def func(client, addr):
	print "connected to:  ", addr 
	while True:
		accountDet(client)

def onlineStat(check, userName):
	if not check:
		del online[userName]

def accountDet(client):
	client.send("Do you have an account?")
	exist = client.recv(1024)
	if exist in ("No","n","no","N"):
		newAccount(client)
	else:
		existAccount(client)

def existAccount(client):
	userName = ""
	client.send("Please enter your Username.")
	while not(userName in offline):
		userName = client.recv(1024)
		if userName == "**":
			accountDet(client)
			return
		if userName in offline:
			if userName in online:
				client.send("Sorry user is already online, you can't sign in from different devices. Enter any key to go back.")
				userName = client.recv(1024)
				accountDet(client)
				return
			else:
				online[userName]=client	
				mainMenu(client,userName)
		else:
			client.send("Username does not exist please try again with another userName, if you want to go back enter \"**\"")			

def newAccount(client):
	client.send("Please Choose Your Username.")
	userName = client.recv(1024)
	while userName in offline:
		client.send("Username already exists, Please try again. If you want to go back enter \"**\".")
		userName = client.recv(1024)
		if userName=="**":
			accountDet(client)
			return
	offline[userName]=client
	online[userName]=client
	mainMenu(client,userName)
	
def mainMenu (client,userName):
	msg= """Welcome to the main menu, please select the appropriate option or input \"0\" at any time to go back to the previous menu.
	1)Open chat with a user.
	2)View recieved messages.
	3)Create a group.
	4)Send message in a group.
	5)Display all online users"""
	client.send(msg)
	option=client.recv(1024)
	onlineStat(option,userName)
	if option == "1":
		client.send("Who do you want to send a message to? Enter Username.")
		reciever = client.recv(1024)
		onlineStat(reciever,userName)
		interact(client,userName, reciever)
	elif option == "2":
		client.send("keys/")
		reciever = client.recv(1024)
		onlineStat(reciever,userName)
		interact(client,userName, reciever)

	elif option == "3":
		group(client,userName)
	elif option == "4":
		client.send("Which group do you want to send a message in?")
		name = client.recv(1024)
		onlineStat(name,userName)
		while True:
			if name == "**":
				mainMenu(client, userName)
				return
			elif not(name in groups):
				client.send("Group does not exist, please enter name again. To go back enter \"**\" ")
				name = client.recv(1024)
				onlineStat(name,userName)

			elif not (userName in groups[name]):
				client.send("Sorry but you are not added in this group, please try again.  To go back enter \"**\"")
				name = client.recv(1024)
				onlineStat(name,userName)	
			else:
				client.send("What message do you want to send in the group? or enter *? to go back")
				groupMsg(client,userName,groups[name], name)
				return
	elif option=="5":
		listofnames = userName
		for names in online:
			if not(names== userName):
				listofnames = listofnames +"," + names
		client.send("list/" + listofnames)
		client.recv(1024)
		mainMenu(client,userName)


	elif option == "0":
		accountDet(client)
		
def group(client,userName):
	client.send("What do you want to name the group?")
	name = client.recv(1024)
	onlineStat(name,userName)
	while name in groups:
		client.send("Group already exists, please re-enter name or enter \"**\" to go back to the main menu")
		name = client.recv(1024)
		onlineStat(name,userName)
		if name == "**":
			mainMenu(client,userName)
	client.send("Who do you want to add in the group?")
	member = ""
	while not(member in offline) :
		member = client.recv(1024)
		onlineStat(member,userName)
		if member=="**":
			mainMenu(client,userName)
			return
		if member in offline:
			break
		else:
			client.send("The Username does not exist, please re-enter Username or enter \"**\" to go back to main menu.")
			
	adminList = []
	adminList.append(userName)
	members = []
	members.append(userName)
	admins[name] = adminList 
	addMem(client, userName, members, member ,name)
	client.send("What message do you want to send in the group? or enter \"*?\" for options")
	groupMsg(client,userName,members, name)

def addMem(client, userName, members, member,name):
	while member != "**":
		if member in members:
			client.send("The Username already in group, please re-enter Username or enter \"**\" to get done.")
			member = client.recv(1024)
			onlineStat(member,userName)
			if member=="**":
				return
			addMem(client, userName, members, member,name)
		elif not(member in offline):
			client.send("The Username does not exist, please re-enter Username or enter \"**\" to get done.")
			member = client.recv(1024)
			onlineStat(member,userName)
			if member=="**":
				return
			addMem(client, userName, members, member,name)

		members.append(member)
		client.send("Do you want to add anyone else? If not enter \"**\".")
		member = client.recv(1024)
		onlineStat(member,userName)
		if member=="**":
			break
		while True:
			if member in members:
				client.send("The Username already in group, please re-enter Username or enter \"**\" to get done.")
				member = client.recv(1024)
				onlineStat(member,userName)
				if member=="**":
					return
			elif member in offline:
				break
			else:
				client.send("The Username does not exist, please re-enter Username or enter \"**\" to get done.")
				member = client.recv(1024)
				onlineStat(member,userName)
				if member=="**":
					return

	groups[name]= members

def groupMsg(client,userName, members , name):
	gmsg = client.recv(1024)
	onlineStat(gmsg, userName)
	while True:
		for friend in members:
			if friend == userName:
				x=0
			elif not(friend in online):
				message = "GMSG/" + name +"/" + userName + "/" + gmsg +"/"
				thread.start_new_thread(offlineC,(friend, message))
			else:
				reciever = online[friend]
				try:
					reciever.send("GMSG/" + name +"/" + userName + "/" + gmsg +"/")
				except:
					del online[friend]
					message = "GMSG/" + name +"/" + userName + "/" + gmsg +"/"
					thread.start_new_thread(offlineC,(friend, message))

				
		gmsg = client.recv(1024)
		onlineStat(gmsg, userName)

		if gmsg == "*?":
			client.send("""Enter \"*!\" to add more members 
	or \"*@\" to make other people admin
	or \"**\" to go back to main menu
	or \"*x\" to go leave group
	or just send a message.""" )
			gmsg = client.recv(1024)
			onlineStat(gmsg, userName)
			if gmsg == "*!":
				if (userName in admins[name]):
					client.send("Who do you want to add?")
					member = client.recv(1024)
					onlineStat(gmsg, userName)
					addMem(client, userName, members, member , name)
					client.send("returning to chat")
					gmsg = client.recv(1024)

				else:
					client.send("You're not an admin, Send a message")
					gmsg = client.recv(1024)
					onlineStat(gmsg, userName)
			elif gmsg == "*@":
				if (userName in admins[name]):
					adAdmin(client, userName, members, name)
					client.send("returning to chat")
					gmsg = client.recv(1024)
				else:
					client.send("You're not an admin, send a message")
					gmsg = client.recv(1024)
					onlineStat(gmsg, userName)

			elif gmsg == "**":
				mainMenu(client, userName)
			elif gmsg == "*x":
				i = members.index(userName)
				del members[i]
				mainMenu(client, userName)
			else:
				client.send("No command recieved, Send a message.")
				gmsg = client.recv(1024)
				onlineStat(gmsg, userName)

def adAdmin (client, userName, members, name):
	client.send("Who do you want to make admin?")
	admin = client.recv(1024)
	onlineStat(admin, userName)
	currentList = admins[name]
	while not(admin == "**"):
		if admin not in members:
			client.send("Username not in group, please enter another username or enter \"**\" to get done")
			admin = client.recv(1024)
			onlineStat(admin, userName)
			if admin == "**":
				admins[name] = currentList
				return
		else:
			currentList.append(admin)
			client.send("Admin added, please enter another username or enter \"**\" to get done")
			admin = client.recv(1024)
			onlineStat(admin, userName)

	admins[name] = currentList
	
def interact(client, userName, reciever):
	if reciever in offline:
		client.send("What message do you want to send?Enter \"**\" to stop sending message and go back to the Main menu.")
		mesg =client.recv(1024)
		onlineStat(mesg,userName)
		while mesg != "**":
			if reciever in online:
				friend = online[reciever]
				try:
					friend.send("mesg/" + userName +"/"+mesg + "/")
				except:
					del online[reciever]
					message = "mesg/" + userName +"/"+mesg + "/"
					thread.start_new_thread(offlineC,(reciever, message))



			else:
				message = "mesg/" + userName +"/"+mesg + "/"
				thread.start_new_thread(offlineC,(reciever, message))
			mesg =client.recv(1024)
			onlineStat(mesg,userName)
		mainMenu(client, userName)
	else:
		client.send("Username does not exist, Please re-enter Username or enter \"**\" to go back to the Main Menu")
		reciever = client.recv(1024)
		if reciever == "**":
			mainMenu(client, userName)
		onlineStat(reciever,userName)
		interact(client,userName, reciever)

def offlineC (reciever, message):
	while True:
		if reciever in online:

			friend = online[reciever]
			try:
				friend.send(message)
			except:
				del online[reciever]
				thread.start_new_thread(offlineC,(reciever, message))
			friend.send(message)
			break

def Main():
	host='127.0.0.1'
	port=50000
	s = socket.socket()
	s.bind((host,port))
	s.listen(10) # max number of connections

	print "Waiting for new connections"
	while True:
		client, addr = s.accept()
		thread.start_new_thread(func,(client,addr))

		
if __name__=="__main__":
	Main()