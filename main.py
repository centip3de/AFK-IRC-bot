import socket
import re
import os
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

bot_owner = "centip3de"
nickname = "centip3de_away"
personNick = ""
authorized = ['mShred', 'Kage', 'limdis', 'LoGiCaL__', 'fas', 'NightQuest', 'weekend', 'spaux', 'ScrAm`', 'e3cb', 'wall', 'centip3de']
channel = "#bots"
sock = socket.socket()
server = "irc.hackthissite.org"
verified = [] 
port = 6667 

def sendEmail(text):
    infoFp = open("Info.txt", "r")
    sender = infoFp.readline().rstrip('\n')
    password = infoFp.readline().rstrip('\n')
    username = infoFp.readline().rstrip('\n')
    
    SMTPserver = "smtp.gmail.com"
    destination = sender
    text_subtype = "plain"

    if text == "":
        print "You must supply valid text!"
        return
    else:
        content = text

    msg = MIMEText(content)
    msg['Subject'] = "IRC ALERT"
    msg['From'] = sender

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(username, password)
    conn.sendmail(sender, destination, msg.as_string())
    conn.close()

def getName(data):
    colonIndex = data.find(":")
    colonIndex += 1
    exmarkIndex = data.find("!")
    name = data[colonIndex:exmarkIndex]
    return name

def isAuthorized():
    return personNick in authorized

def sendToPerson(msg):
    sock.send("PRIVMSG " + personNick + " :" + msg + "\r\n")

def sendToChan(msg):
    sock.send("PRIVMSG " + channel + " :" + msg + "\r\n")

def send(msg):
    sock.send(msg + "\r\n")

def isVerified(personNick):
    return personNick in verified

def verify(data, name):
    verifiyFp = open("pass.txt", "r")
    password = verifiyFp.readline().rstrip('\n')
    if(re.search(password, data)):
        print "Verified!"
        verified.append(name)
    else:
        print "Not verified!"
    
sock.connect((server, port))
send("USER " + nickname + " USING CUSTOM BOT")
send("NICK " + nickname)

while 1:
    data = sock.recv(512)
    print data
    if data[0:4] == "PING":
        send(data.replace("PING", "PONG"))
        send("MODE " + nickname + "+B")
        send("JOIN " + channel)
    elif re.search("PRIVMSG " + nickname + " :help", data):
        personNick = getName(data)
        sendToPerson("This is centip3de's AFK bot. If you need to leave him a message, just send it to me and I'll log it for him.")
        if isAuthorized():
            sendToPerson("If you really need to get in contact with him, you may use the 'alert' command to message him directly.")
            sendToPerson("The syntax for the command is: 'alert messageHere'.")
            sendToPerson("Remember, this is a direct line to him. Please do not use this unless absolutely necessary.")
    elif re.search("PRIVMSG " + nickname + " :alert", data):
        personNick = getName(data)
        if isAuthorized():
            sendEmail(data)
        else:
            sendToPerson("I'm sorry " + personNick + ", you must be authorized to complete this action.")
    elif re.search("PRIVMSG " + nickname + " :verify", data):
        verifyIndex = data.find(":verify")
        verifyIndex += 8
        verifyData = data[verifyIndex:].rstrip('\n')
        verify(verifyData, getName(data))
    elif re.search("PRIVMSG " + nickname + " :exit", data) and isVerified(getName(data)):
        print "HERE"
        exit()
    elif re.search("PRIVMSG " + nickname + " :", data):
        logFile = open("log.txt", "a")
        logFile.write(data)
