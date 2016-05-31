"""
 .o88b. d88888b d8888b.  .d8b.  d8888b. d8888b.  .d88b.  d888888b 
d8P  Y8 88'     88  `8D d8' `8b 88  `8D 88  `8D .8P  Y8. `~~88~~' 
8P      88ooooo 88   88 88ooo88 88oobY' 88oooY' 88    88    88    
8b      88~~~~~ 88   88 88~~~88 88`8b   88~~~b. 88    88    88    
Y8b  d8 88.     88  .8D 88   88 88 `88. 88   8D `8b  d8'    88    
 `Y88P' Y88888P Y8888D' YP   YP 88   YD Y8888P'  `Y88P'     YP    
                                                                                                                                

CedarBot -- the latest advancement on the H2Bot/RTLBot codebase, designed for use on the Pine64 network

CedarBot and H2Bot designed and built by fire219 (Matthew Petry)

LICENSE:

Copyright (c) 2014-2016 Matthew Petry (fire219)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
 
# librarieslibrarieslibraries.
import socket
import time
import random
import os
import thread 
import smtplib
import urllib2
import json
import datetime
import pickle

# variables you can touch      
server = "irc.freenode.net" # IRC network 
channel = "#CedarTest" # Channel
botnick = "CedarBot" # Bot's nick
curses = ['fuck', 'shit', 'damn', 'dammit', 'cunt', 'tits', 'bitch', ' cock ', 'dick', 'jizz', 'nigger', 'queer', 'slut', 'twat', 'whore', 'pussy', ' hell ', 'spick', 'wetback', 'dike', 'bastard', 'towelhead', 'clit', 'douche', 'bugger', ' fuk ', '$hit', 'godverdomme', 'miljaardeju', 'kut', 'klote', 'verdomme', 'godver', 'nondedju', 'mieljaar', 'tering', 'sodemieter', 'merde', 'conneries', 'branleur', 'connard', 'schwanz', 'arsch', 'hurensohn', 'verdammt', 'puta', 'foda', ] #Profanity list for swear filter (used on first run)
cursesns = ['fuck', 'shit', 'damn', 'dammit', 'cunt', 'tits', 'bitch', 'cock', 'dick', 'jizz', 'nigger', 'queer', 'slut', 'twat', 'whore', 'pussy', 'hell', 'spick', 'wetback', 'dike', 'bastard', 'towelhead', 'clit', 'douche', 'bugger', 'fuk', '$hit', 'godverdomme', 'miljaardeju', 'kut', 'klote', 'verdomme', 'godver', 'nondedju', 'mieljaar', 'tering', 'sodemieter', 'merde', 'conneries', 'branleur', 'connard', 'schwanz', 'arsch', 'hurensohn', 'verdammt', 'puta', 'foda',] #No-spaces profanity list for swear filter stage 2 (used on first run)  
selfref = ['h2bot', 'himself', 'hisself', 'itself', 'dick', 'cock', 'hydrobot', 'hydrogenbot', ' its ', 'thyself'] #Self (and bad thing) references for fun commands
log = 1 #create log file?
filelocation = "C:\\Users\\Matthew\\Documents\\hydrobot" #where to create bot files
password = "cedarbotexppass"
utc_datetime = datetime.datetime.utcnow()
#--------------DO NOT TOUCH----------------------------

swearfilter = 0
timelimit = 0 
funcommands = 1
ircmsg = ""
tbanned = dict()
seenlist = dict()
tbanned2 = []
mods = []
L1off = []
L2off = []
L3off = []
alloff= dict()
date = time.strftime("%m_%d_%Y")
swearcount = 0
chanready = 0
threadsrunning = 0
#------------END NO TOUCHIE AREA-----------------------
 
print("CedarBot is starting up!")
starttime=utc_datetime.strftime("%a, %d %b %Y %H:%M:%S") 
print("Startup time: "+starttime)
#log initialization
if log == 1: 
 if os.path.isfile(filelocation+'/log '+ date) == True:
   print("We already have a log for today -- appending messages to it.")	
   logw = open(filelocation+'/log '+ date, 'a')
   logw.write('---LOG CONTINUED---\n')

 else:
   print("We do not have a log for today. Creating a new one.") 
   logw = open(filelocation+'/log '+ date, 'w')
   logw.write('---LOG STARTED---\n')


#swear filter offenders file initialization

if os.path.isfile(os.path.normpath(filelocation+'/swfile')) == True:
	print("Swear filter file exists")
	pass
else:
 print("Creating swear filter file")
 swf = open(os.path.normpath(filelocation+'/swfile'), 'w')
 swf.write("{}")
 swf = open(os.path.normpath(filelocation+'/swfile'), 'w')
   
#tempban file initialization   
if os.path.isfile(os.path.normpath(filelocation+'/tbanned')) == True:
 print("Tempban file 1 exists. Trying to load contents.")
 tbf = open(os.path.normpath(filelocation+'/tbanned'), 'r+')
 tbanned = tbf.read()
 tbanned = tbanned.strip("[]")
 tbanned = eval(tbanned)
 print("Ban data loaded:"+str(tbanned))
 tbf.close()
else:
 print("Creating tempban file 1")
 tbf = open(os.path.normpath(filelocation+'/tbanned'), 'w')
 tbf.write("{}")
 tbf = open(os.path.normpath(filelocation+'/tbanned'), 'r+')
  
if os.path.isfile(os.path.normpath(filelocation+'/tbanned2')) == True:
 print("Tempban file 2 exists. Trying to load contents.")	
 tbf2 = open(os.path.normpath(filelocation+'/tbanned2'), 'r+')
 tbanned2 = tbf2.read()
 tbanned2 = tbanned2.strip("[]")
 tbanned2 = tbanned2.replace("'", " ") 
 tbanned2 = tbanned2.strip(",") 
 tbanned2 = tbanned2.split()
 print("Ban data loaded:"+str(tbanned2))
 tbf.close()
else:
 print("Creating tempban file 2")
 tbf2 = open(os.path.normpath(filelocation+'/tbanned2'), 'w') 
 tbf.write("[]")
 tbfw = open(os.path.normpath(filelocation+'/tbanned2'), 'r+') 
 


#--------------ABSOLUTELY NO TOUCHIE UNLESS YOU KNOW WHAT YOU'RE DOING-------------------

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) 
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Cousin of the Pine \n") # user authentication
time.sleep(2)
ircsock.send("NICK "+ botnick +"\n")
#--------------END NO TOUCHIE ZONE------------------------------------------------------- 
 
def sendmsg(chan, msg): # handler for channel and PM message sending
	ircsock.send("PRIVMSG "+ chan +" :"+ msg + "\n")
 
def stringdetect(string): #basic string detection
  if ircmsg.find(string) != -1:
    return True
  else:
    return False
 
def ping(): # IRC PING responder 
 
  ircsock.send("PONG :" + ircmsg.strip("PING :") + "/n")
  print("PONG :" + ircmsg.strip("PING :"))
  joinchan(channel)
 
 
def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")
 
def hello(): # This function responds to a user that inputs "Hello <botnick>"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")
 
def rand(number): #random number gen
 try:
  rand = random.randint(1, int(number))
  print(number) 
  ircsock.send("PRIVMSG "+ channel +" :Random Selection: " + str(rand) + "\n")
 except:
  pass
  ircsock.send("PRIVMSG "+ channel +" :Bad information given. \n")
 
def rand2(randstring): #random character chooser
 try:
  rand = random.choice(randstring)
  ircsock.send("PRIVMSG "+ channel +" :Random Selection: " + rand + "\n")
 except:
  pass
  ircsock.send("PRIVMSG "+ channel +" :Bad information given. \n")
 
def intro(): #introduction to H2
  ircsock.send("PRIVMSG "+ channel +" :Hello! I am CedarBot, a helper bot on the Pine64 IRC network. I was developed by fire219 (Matthew Petry), as an advancement of the previous RTLBot and H2Bot projects.\n")
 


def slapuser(user): #slap user
     ircsock.send("PRIVMSG "+ channel +" :\x01ACTION slaps " + user + " with a large robotic trout!\x01\n")
     
def ewuser(user): # ew user
     ircsock.send("PRIVMSG "+ channel +" :Ew, "+ user +"! \n")

def suckuser(user): #vacuum cleaner, hehe
     ircsock.send("PRIVMSG "+ channel +" :\x01ACTION sucks "+ user +" up with a vacuum cleaner!\x01\n")
 	 
	 
def opfindrun(): #find channel ops
    opfind = ircmsg 
    opfindr = opfind.index("353 "+botnick)
    opfind = opfind[opfindr:]
    opfindr = opfind.index(channel) 
    opfind = opfind[opfindr:]
    opfind2 = len(channel) + 1
    opfind = opfind[opfind2:]
    opfind = opfind[1:]
    #opfindr = opfind.index(":")
    #opfind = opfind[:opfindr]
    #opfind = opfind[:-2]
    opfind = opfind.split(' ')
    print(opfind)
    opparse = 0
    try:
     for x in range(0, len(opfind)):
        op1 = opfind[opparse].find("@")
        op2 = opfind[opparse].find("&")
        op3 = opfind[opparse].find("~")	
		
        if op1 == -1 and op2 == -1 and op3 == -1:
			opfind.pop(opparse)
			x = x + 1
			oparse = opparse + 1	
        else:
			tempop = opfind[opparse]            
			tempop = tempop.replace("@", "")
			mods.append(tempop)
			opfind.pop(opparse)
			x = x + 1
			oparse = opparse + 1	
    except IndexError:
        print()
    print(mods)
    mods.append("fire219")		
    chanready = "yes"
    seenlist = dict()
    seenlist.clear()
    print("Channel is ready!")
 
def help(ircmsg): #basic command help
    ircmsg = ircmsg[1:]
    ircmsgr = ircmsg.index("!")
    ircmsg = ircmsg[:ircmsgr]  
    ircsock.send("PRIVMSG "+ ircmsg +" :CedarBot Help\n")    
    ircsock.send("PRIVMSG "+ ircmsg +" :-----------\n")
    ircsock.send("PRIVMSG "+ ircmsg +" :'Hello CedarBot' - CedarBot says hello back \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB intro - Introduction \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB randomize <text> - selects a random character out of <text> \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB randomnum <end number> - Selects a random number from 1 to <end number> \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB slap <user> - slaps user with a fish \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB ew <user> - shows your disgust for a user \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB suck <user> - not quite what you think \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB curtime - shows the current time in the timezone H2 is running from (usually Central) \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :CB easy - Be a smartass and tell them how easy something was. \n")	
    ircsock.send("PRIVMSG "+ ircmsg +" :CB seen <user> - What was the most recent time this user was seen? \n")	
    ircsock.send("PRIVMSG "+ ircmsg +" :CB trivia <pack> - Run a game of trivia!\n")	

def adminhelp(ircmsg): #admin command help
    ircmsg = ircmsg[1:]
    ircmsgr = ircmsg.index("!")
    ircmsg = ircmsg[:ircmsgr]  
    ircsock.send("PRIVMSG "+ ircmsg +" :CedarBot Admin Help\n")    
    ircsock.send("PRIVMSG "+ ircmsg +" :-----------\n")
    ircsock.send("PRIVMSG "+ ircmsg +" :'CB sw on/off' - swearfilter toggle \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :'CB fun on/off' - FUNction toggle \n")
    ircsock.send("PRIVMSG "+ ircmsg +" :'CB shutdown' - shutdown H2Bot \n")	
    ircsock.send("PRIVMSG "+ ircmsg +" :'CB tban <user> M-D_h:m' - tempban \n")	
    ircsock.send("PRIVMSG "+ ircmsg +" :'CB tkban <user> M-D_h:m' - tempban + kick \n")		
	
def selfharmdetect(string, actionmsg1, actionmsg2, self=selfref): #detects if the user is trying to issue a command against the bot.
    if any(word in string.lower() for word in self):
        user = string[1:]
        print(user)
        ircmsgr = user.index("!")
        print(user)
        user = user[:ircmsgr]
        print(user)
        ircsock.send("PRIVMSG " + channel + actionmsg1 + user + actionmsg2)
	
        return False
    else:
        return True
 
def stringSplit(string, text, position): #gets the parameter the user passed and returns it
    stringreq = string
    stringreqr = stringreq.index(text)
    print(stringreqr)
    stringreq = stringreq[stringreqr:]
    print(stringreq)
    stringreq = stringreq[position:]
    print(stringreq)
    stringreq = stringreq.strip('\n\r')
    print(stringreq)
    return stringreq
   
def functionTimer(string, timelimit): #checks that the functions arent being used too often
    if timelimit > 0:
        string = string[1:]
        print(string)
        string = string.index("!")
        print(string)
        string = string[:ircmsgr]
        print(string)
        ircsock.send("NOTICE "+ string +" :A FUNction has been used recently. Please wait a while before trying again. " + str(timelimit) + " cycles left. \n")
        return False
    else:  
        timelimit = 10
        return True

def wrongarg(receive, expect): # wrong number of arguments handler
    ircsock.send("PRIVMSG "+channel+" :Error: Expected "+expect+" arguments, received "+receive+".\n")

def unbanloop(): #tempban parse 'n unban MULTITHREAD EDITION :O
  while True:
   try: 
	tbanparse = 0
	for x in xrange(0, len(tbanned2)):
	 #print("unban time "+tbanned[tbanned2[tbanparse]])
	 #print("current time "+time.strftime("%m-%d_%H:%M"))
	 curtime = time.strftime("%m-%d_%H:%M")
	 cmonth = time.strftime("%m")
	 if cmonth[0] == '0':
	  cmonth = cmonth[1:]
	 cday = time.strftime("%d")
	 if cday[0] == '0':
	  cday = cday[1:]	 
	 chour = time.strftime("%H") 
	 if chour[0] == '0':
	  chour = chour[1:]	 
	 cmin = time.strftime("%M")
	 if cmin[0] == '0':
	  cmin = cmin[1:]	
	 curtime = str(cmonth+"-"+cday+"_"+chour+":"+cmin) 
	 if tbanned[tbanned2[tbanparse]] == curtime:
			tbf2 = open(filelocation+'/tbanned2', 'w') 
			tbf = open(filelocation+'/tbanned', 'w') 
			ircsock.send("MODE "+ channel +" -b "+tbanned2[tbanparse]+"\n")
			temp=tbanned2[tbanparse]
			tbanned.pop(temp)
			ircsock.send("PRIVMSG "+ channel +" :User "+tbanned2[tbanparse]+" is unbanned.\n")
			tbanned2.pop(tbanparse)
			tbf.write(str(tbanned))	
			tbf2.write(str(tbanned2))
			tbf.close()
			tbf2.close()		
	 tbanparse = tbanparse + 1	

   except KeyError:
		tbf2 = open(filelocation+'/tbanned2', 'w')
		tbanned2.pop(tbanparse)
		tbf2.write(str(tbanned2))
		tbf2.close()
		tbanparse = tbanparse + 1
		print("We hit an error, but we're still purring along!")

def swtimeout(name): #swearfilter timeout
	time.sleep(600)	
	alloff.pop(name)
	swf = open(filelocation+'swfile', 'w')
	swf.write(str(alloff))
	swf.close()		
"""
def seenlistloader(): #load seenlist from file
	if os.path.isfile(os.path.normpath(filelocation+'/seenlist')) == True:
		print("Last seen dictionary exists. Trying to load contents.")
		seenlistf = open(os.path.normpath(filelocation+'/seenlist'), 'CB+')
		if (seenlistf.read() == ""):
			print("Dictionary is empty. Continuing with blank list.")
		else:	
			seenlist = pickle.load(seenlistf)
			print("Dictionary loaded:"+str(seenlist))
	else:
			print("Creating last seen dictionary")
			seenlistf = open(os.path.normpath(filelocation+'/seenlist'), 'wb')
			seenlist = dict()
"""
	
while True: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server
  '''if not "PING :" in ircmsg and threadsrunning == 1:
	curchan = ircmsg
	curchanr = curchan.index("PRIVMSG")+8
	curchan = curchan[curchanr:]
	curchan = curchan.split(":")[0]
	print("Channel is: "+curchan+".")
	if curchan == botnick:
		curchan = ircmsg[1:]
		curchan = curchan.split("!")[0]
		print("PM from "+curchan)
	'''
  if log == 1:
	if not "PING :" in ircmsg:
		logw = open(filelocation+'/log '+ date, 'a')
		logw.write(utc_datetime.strftime("%d %b %Y %H:%M:%S")+":  "+ircmsg+'\n')
		logw.close()	
 
 
  if stringdetect("353 "+botnick):
    opfindrun()
 
  if stringdetect("This nickname is registered"):
    ircsock.send("PRIVMSG NickServ :identify "+password+"\n")
	
  if stringdetect(":"+botnick+" MODE "+botnick+" :+i"):
    joinchan(channel)	
	

	
  if stringdetect(":Hello "+ botnick): # If we can find "Hello Mybot" it will call the function hello()
    hello()
 
  if stringdetect("PING :"): # if the server pings us then we've got to respond!
    ping()
 
  if stringdetect(":CB intro"):
    intro()  
 
  if stringdetect(":CB locate"):
    locateuser(stringSplit(ircmsg, "locate", 7))
 
  if funcommands == 1:    
    if stringdetect("CB randomize"): #checks if this command was used
      if functionTimer(ircmsg, timelimit): #checks if the time limit is up
       rand2(stringSplit(ircmsg, "randomize", 10)) #runs the function rand2 with the players parameter
    if stringdetect("CB randomnum"):
      if functionTimer(ircmsg, timelimit):
       rand(stringSplit(ircmsg, "randomnum", 10))
    if stringdetect(":CB slap"):
      if functionTimer(ircmsg, timelimit):
        if selfharmdetect(ircmsg, " :\x01ACTION slaps ", " with a large robotic trout for thinking I am dumb! \x01\n"):
         slapuser(stringSplit(ircmsg, "slap", 5))

    if stringdetect(":CB ew"):
      if functionTimer(ircmsg, timelimit):
        if selfharmdetect(ircmsg, " :Ew, ", ". I'm not that stupid! :P \n"):
         ewuser(stringSplit(ircmsg, "ew ", 3))
    if stringdetect(":CB suck"):
      if functionTimer(ircmsg, timelimit):
        if selfharmdetect(ircmsg, " :Um no ", ". I'm not that stupid! :P \n"):
         suckuser(stringSplit(ircmsg, "suck", 5))
  
  if stringdetect(":is this the real life"):
    ircsock.send("PRIVMSG "+ channel +" :Is this just fantasy?\n") 
	
  if stringdetect(":CB easy"):
	ircsock.send("PRIVMSG "+ channel +" :That was easy. http://goo.gl/bnUZS7 \n") 
	
  if stringdetect(":CB help"):
    help(ircmsg)
	
  if stringdetect(":CB make me a sandwich"):
	sandwich = random.randint(1,10)
	if sandwich <= 5:
		ircsock.send("PRIVMSG "+ channel +" :Make the damn sandwich yourself. \n") 	
	if sandwich > 5:
		ircsock.send("PRIVMSG "+ channel +" :Poof, you're a sandwich. \n") 
		
  if stringdetect(":CB sudo make me a sandwich"):
	ircsock.send("PRIVMSG "+ channel +" :Making sandwich. \n")
		
  if stringdetect(":CB curtime"):
    ircsock.send("PRIVMSG "+ channel +" :"+time.strftime("%m-%d_%H:%M")+"\n")
	
  if swearfilter == 1:
   
   if any(word in ircmsg.lower() for word in curses):
	swearmessage = ircmsg.lower()
	swearmessage = swearmessage[1:]
	swearmessager = swearmessage.index(":")
	swearmessage = swearmessage[swearmessager:]
	swearmessage = swearmessage[1:]
	
	ircmsg = ircmsg[1:]
	print(ircmsg)
	ircmsgr = ircmsg.index("!")
	print(ircmsg)
	ircmsg = ircmsg[:ircmsgr]
	print(ircmsg)
	try:
		sweartally = alloff[ircmsg]
	except KeyError:
		sweartally = 0
		thread.start_new_thread(swtimeout, (ircmsg,))
		print("New Timeout thread started.")
	swearmessage = swearmessage.split(" ")
	print(swearmessage)
	swearparse = 0

	for word in swearmessage:
		if any(word in swearmessage[swearparse] for word in curses):
			sweartally = sweartally + 1
			swearparse = swearparse + 1
		else:
			swearparse = swearparse + 1
	

	alloff[ircmsg] = sweartally
	swf = open(filelocation+'swfile', 'w')
	swf.write(str(alloff))
	swf.close()	
	if sweartally > 6:
		opparse = 0
		for x in xrange(0, len(mods)):
			ircsock.send("NOTICE "+mods[opparse]+" :Hey "+mods[opparse]+", "+ircmsg+" has continued using profanity.\n")
			opparse = opparse + 1		
		ircsock.send("NOTICE "+ ircmsg +" :"+ircmsg+", the chat mods have been alerted again.\n")	
	elif sweartally == 6:
		opparse = 0
		for x in xrange(0, len(mods)):
			ircsock.send("NOTICE "+mods[opparse]+" :Hey "+mods[opparse]+", "+ircmsg+" has reached the profanity limit.\n")
			opparse = opparse + 1	
		ircsock.send("NOTICE "+ ircmsg +" :"+ircmsg+", the chat mods have been alerted. Action will be taken as deemed necessary.\n")		
	elif sweartally == 5:
		ircsock.send("NOTICE "+ ircmsg +" :"+ircmsg+", stop cursing immediately. You have cursed "+str(sweartally)+" times in the last hour. Further offenses will be immediately brought to the attention of a moderator.\n")
	elif sweartally >= 3:	
		ircsock.send("NOTICE "+ ircmsg +" :"+ircmsg+", please do not curse. You have cursed "+str(sweartally)+" times in the last hour. \n")

   
  if stringdetect(":CB sw on"):
   secr = ircmsg.index("PRIVMSG")
   ircmsg = ircmsg[:secr]
   if any(word in ircmsg for word in mods):  
    swearfilter = 1  
    ircsock.send("PRIVMSG "+ channel +" :Swear warning on. Current setting: six strikes every 10 minutes.\n")
 
  if stringdetect(":CB sw off"):
   secr = ircmsg.index("PRIVMSG")
   ircmsg = ircmsg[:secr]
   if any(word in ircmsg for word in mods):
    swearfilter = 0  
    ircsock.send("PRIVMSG "+ channel +" :Swear warning off. Someone complained enough to make fire219 turn it off. \n")
   
  if stringdetect(":CB fun on"):
   secr = ircmsg.index("PRIVMSG")
   ircmsg = ircmsg[:secr]
   if any(word in ircmsg for word in mods):  
    funcommands = 1  
    ircsock.send("PRIVMSG "+ channel +" :FUNctions on.\n")

	
  if stringdetect(":ping"):
	ircsock.send("PRIVMSG "+ channel +" :Shut the fuck up.\n")
	
  if stringdetect(":CB shutdown"):
   secr = ircmsg.index("PRIVMSG")
   ircmsg = ircmsg[:secr]
   secret = ['Doctor']
   if any(word in ircmsg for word in mods): 
		ircsock.send("PRIVMSG "+ channel +" :'Good night', says the moon.\n")
		ircsock.send("QUIT :CedarBot -- Entering sleep mode.\n")
		print("Bot is shutting down. ZZZZZZZzzzzzz..... ")
		time.sleep(1)
		os._exit(1)
   else:
		ircsock.send("PRIVMSG "+ channel +" :You are not authorized to shut me down. You must be a channel operator.\n")
   
  if stringdetect(":CB fun off"):
   secr = ircmsg.index("PRIVMSG")
   ircmsg = ircmsg[:secr]
   if any(word in ircmsg for word in mods):
    funcommands = 0
    ircsock.send("PRIVMSG "+ channel +" :FUNctions off.\n")    
   
  if stringdetect(":CB tban"):
   sec = ircmsg
   secr = ircmsg.index("PRIVMSG")
   sec = sec[:secr]
   if any(word in sec for word in mods):   
	tban = ircmsg
	tbanr = tban.index("tban")
	print(tbanr)
	tban = tban[tbanr:]
	tban = tban[5:]
	tban = tban.strip('\n\r')
	tban = tban.split(" ")
	if len(tban) == 1:
	  wrongarg(1 , 2)
	tbanned[tban[0]] = tban[1]
	tbanned2.append(tban[0])    
	ircsock.send("PRIVMSG "+ channel +" :User "+tban[0]+" banned until "+tban[1]+"\n")
	ircsock.send("MODE "+ channel +" +b "+tban[0]+"\n")	
	print(tbanned)
	print(tbanned2)
	tbf2 = open(filelocation+'tbanned2', 'w') 
	tbf = open(filelocation+'tbanned', 'w') 
	tbf.write(str(tbanned))
	tbf2.write(str(tbanned2))
	tbf.close()
	tbf2.close()	
	tban = []
 
  if stringdetect(":CB tkban"):
   sec = ircmsg
   secr = ircmsg.index("PRIVMSG")
   sec = sec[:secr]
   if any(word in sec for word in mods):   
	tban = ircmsg
	tbanr = tban.index("tkban")
	print(tbanr)
	tban = tban[tbanr:]
	tban = tban[6:]
	tban = tban.strip('\n\r')
	tban = tban.split(" ")
	if len(tban) == 1:
	  wrongarg(1 , 2)
	tbanned[tban[0]] = tban[1]
	tbanned2.append(tban[0])    
	ircsock.send("PRIVMSG "+ channel +" :User "+tban[0]+" banned until "+tban[1]+"\n")
	ircsock.send("MODE "+ channel +" +b "+tban[0]+"\n")
	ircsock.send("KICK "+ channel +" "+tban[0]+"\n")	
	print(tbanned)
	print(tbanned2)
	tbf2 = open(filelocation+'tbanned2', 'w') 
	tbf = open(filelocation+'tbanned', 'w') 
	tbf.write(str(tbanned))
	tbf2.write(str(tbanned2))
	tbf.close()
	tbf2.close()	
	tban = []
 
  if stringdetect("slaps "+botnick):
    ircmsg = ircmsg[1:]
    print(ircmsg)
    ircmsgr = ircmsg.index("!")
    print(ircmsg)
    ircmsg = ircmsg[:ircmsgr]
    print(ircmsg)
    ircsock.send("PRIVMSG "+ channel +" :\x01ACTION returns " + ircmsg + " the favor with a large robotic trout!\x01\n")
 
  if stringdetect("slapped "+botnick):
    ircmsg = ircmsg[1:]
    print(ircmsg)
    ircmsgr = ircmsg.index("!")
    print(ircmsg)
    ircmsg = ircmsg[:ircmsgr]
    print(ircmsg)
    ircsock.send("PRIVMSG "+ channel +" :\x01ACTION returns " + ircmsg + " the favor with a large robotic trout!\x01\n")      
 
  if timelimit > 0:
   timelimit = timelimit - 1
   
  if stringdetect(":CB adminhelp"):
   secr = ircmsg.index("PRIVMSG")
   ircmsg = ircmsg[:secr]
   if any(word in ircmsg for word in mods):
     adminhelp(ircmsg)
	 
  if stringdetect(":CB weather"):
	wloc = stringSplit(ircmsg, "weather", 8)
	if (wloc == "" or wloc == "\n"):
		ircsock.send("PRIVMSG "+ channel +" :Usage -- CB weather <location> \n")
		ircsock.send("PRIVMSG "+ channel +" :<location> can be a US zip code, IATA airport code, city (format 'FL/Orlando' or 'France/Paris') or lat/long coordinates. \n")
	else:	
		wreq = urllib2.urlopen('http://api.wunderground.com/api/561a25f41f6ebf72/geolookup/conditions/q/'+wloc+'.json')
		json_string = wreq.read()
		parsed_json = json.loads(json_string)
		city = parsed_json['location']['city']
		temperature = parsed_json['current_observation']['temperature_string']
		wind = parsed_json['current_observation']['wind_string']
		weather = parsed_json['current_observation']['weather']	
		ircsock.send("PRIVMSG "+ channel +" :Weather in "+city+" is "+weather+ " with a temperature of "+temperature+" and wind is "+wind+". (CedarBot weather is powered by Weather Underground)\n")

  if stringdetect(":CB seen"):
	seensubj = stringSplit(ircmsg, "seen", 5)
	print(seenlist)
	if (seensubj == "" or seensubj == "\n"):
		ircsock.send("PRIVMSG "+ channel +" :Usage -- CB seen <user> \n")
		ircsock.send("PRIVMSG "+ channel +" :Find the last time that <user> was seen (since CedarBot's last startup) \n")
	else:	
		try:
			ircsock.send("PRIVMSG "+ channel +" :User "+seensubj+" was last seen at "+seenlist[seensubj]+" UTC \n")
		except:	
			ircsock.send("PRIVMSG "+ channel +" :User "+seensubj+" has not been seen since CedarBot's last startup ("+starttime+")\n")
	
  if stringdetect(":CB trivia"):
	triviakill = 0
	badfile = 0
	scores = dict()
	triviatype = stringSplit(ircmsg, "trivia", 7)
	print("Trivia type:"+triviatype)
	if os.path.isfile(os.path.normpath(filelocation+'/trivia-'+triviatype)) == True:
		ircsock.send("PRIVMSG "+ channel +" :Loading trivia pack "+triviatype+"!\n")
		print("Loading trivia")	
		time.sleep(1)	
		with open(os.path.normpath(filelocation+'/trivia-'+triviatype)) as triviafile:
			try:
				triviapack = triviafile.read()
				print(triviapack)
				triviapack = eval(triviapack)
				trivq = triviapack.keys()
				triva = triviapack.values()
				print(trivq)
				print(triva)
			except:
				ircsock.send("PRIVMSG "+ channel +" :Bad trivia file.\n")
				badfile = 1
				ircmsg = ""
		if badfile == 0:		
			ircsock.send("PRIVMSG "+ channel +" :Trivia mode is activated. All other bot functions will not work. Type 'CB trivia stop' to stop the game.\n")
			trivcounter = 0
			trivanswered = 0
			
			for x in trivq:
				trivcounter = trivcounter + 1
				ircsock.send("PRIVMSG "+ channel +" :\x0304Question "+str(trivcounter)+": "+trivq[trivcounter - 1]+"\x03\n")
				timer = time.time()
				while trivanswered == 0 and (time.time() < timer + 30):
					try:
						ircmsg = ircsock.recv(2048) # receive data from the server
					except:
						pass
					ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
					print(ircmsg) # Here we print what's coming from the server
					if stringdetect(":CB trivia stop"):
						if any(word in ircmsg for word in mods):
							ircsock.send("PRIVMSG "+ channel +" :Stopping trivia game immediately.\n")
							triviakill = 1
							break
						else:
							ircsock.send("PRIVMSG "+ channel +" :You are not authorized to stop the game!\n")
					if str(triva[trivcounter - 1]).lower()	in ircmsg.lower():
						trivanswered = 1		
				if triviakill == 1:
					break
				if trivanswered == 0:
					ircsock.send("PRIVMSG "+ channel +" :No one answered in time! The answer is: "+triva[trivcounter - 1]+"\n")
				if trivanswered == 1:	
					user = ircmsg[1:]
					ircmsgr = user.index("!")
					user = user[:ircmsgr]
					ircsock.send("PRIVMSG "+ channel +" :"+user+" got it right! The answer is: "+triva[trivcounter - 1]+"\n")
					try:
						scores[user] = scores[user] + 1
					except:
						scores[user] = 1
					ircmsg = ""	
					trivanswered = 0
			ircsock.send("PRIVMSG "+ channel +" :Game over! :) \n")
			ircsock.send("PRIVMSG "+ channel +" :Scores:\n")
			scoresstr = str(scores)
			scoresstr = scoresstr.strip("{")
			scoresstr = scoresstr.strip("}")
			ircsock.send("PRIVMSG "+ channel +" :"+scoresstr+"\n")
				
	else:
		ircsock.send("PRIVMSG "+ channel +" :Trivia pack not found!\n")	

  try:	
		newmsg = ircmsg
		newmsgr = newmsg.index("!")
		newmsg = newmsg[:newmsgr]
		newmsg = newmsg[1:]
		utc_datetime = datetime.datetime.utcnow()
		seenlist[newmsg] = utc_datetime.strftime("%a, %d %b %Y %H:%M:%S")	

  except:
		continue 
		

  
  if threadsrunning == 0:
   if mods != []: #activate tempban threads and do final var cleanup
	thread.start_new_thread(unbanloop,())
	print("Tempban thread running!")
	#seenlistloader()
	threadsrunning = 1
	

"""	
  if (mods != []):
	seenlistf = open(os.path.normpath(filelocation+'/seenlist'), 'wb')
	pickle.dump(seenlist, seenlistf)  
	seenlistf.close()
"""