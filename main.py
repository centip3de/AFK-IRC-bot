import socket
import re
import os
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from Parser import Parser

class Bot():
    def __init__(self):
        self.bot_owner      = ""
        self.nickname       = ""
        self.personNick     = ""
        self.authorized     = ['mShred', 'Kage', 'limdis', 'LoGiCaL__', 'fas', 'NightQuest', 'weekend', 'spaux', 'case', 'apples', 'e3cb', 'wall', 'centip3de']
        self.channel        = ""
        self.sock           = socket.socket()
        self.server         = ""
        self.verified       = [] 
        self.port           = 0
        self.initial_ping   = True 

        self.setVariables()

    def setVariables(self):
        parser          = Parser("bot.config")
        tokens          = parser.parse()

        self.bot_owner  = tokens["bot_owner"]
        self.nickname   = tokens["nickname"]
        self.channel    = tokens["channel"]
        self.server     = tokens["server"]
        self.port       = int(tokens["port"])

    def start(self):
        self.sock.connect((self.server, self.port))
        self.send("USER " + self.nickname + " USING CUSTOM BOT")
        self.send("NICK " + self.nickname)
        
        while 1:
            data = self.sock.recv(512).decode('UTF-8')
            lines = data.split("\r\n")
            self.personNick = self.getName(data)

            for line in lines:
                print(line) 

            if(data[0:4] == "PING"):
                self.send(data.replace("PING", "PONG"))

                if(self.initial_ping):
                    self.send("MODE " + self.nickname + "+B")
                    self.send("JOIN " + self.channel)

            elif(re.search("PRIVMSG " + self.nickname + " :help", data)):
                self.sendToPerson("This is centip3de's AFK bot. If you need to leave him a message, just send it to me and I'll log it for him.")

            elif(re.search("PRIVMSG " + self.nickname + " :verify", data)):
                verifyIndex = data.find(":verify")
                verifyIndex += 8
                verifyData = data[verifyIndex:].rstrip('\n')
                self.verify(verifyData, self.getName(data))

            elif(re.search("PRIVMSG " + self.nickname + " :exit", data)):
                self.runVerifiedCommand(exit) 

            elif(re.search("PRIVMSG " + self.nickname + " :", data)):
                logFile = open("log.txt", "a")
                logFile.write(data)

    def runVerifiedCommand(self, command):
        if(self.isVerified()):
            command()
        else:
            self.sendToPerson("I'm sorry" + self.personNick + ", you must be verified to complete this action.") 

    def runAuthorizedCommand(self, command):
        if(self.isAuthorized()):
            command()
        else:
            self.sendToPerson("I'm sorry" + self.personNick + ", you must be authorized to complete this action.")

    def getName(self, data):
        colonIndex = data.find(":")
        colonIndex += 1
        exmarkIndex = data.find("!")
        name = data[colonIndex:exmarkIndex]
        return name

    def isAuthorized(self):
        return self.personNick in self.authorized

    def sendToPerson(self, msg):
        #print("MSG: ", msg)
        self.sock.send(bytes("PRIVMSG " + self.personNick + " :" + msg + "\r\n", 'UTF-8'))

    def sendToChan(self, msg):
        self.sock.send(bytes("PRIVMSG " + self.channel + " :" + msg + "\r\n", 'UTF-8'))

    def send(self, msg):
        self.sock.send(bytes(msg + "\n", 'UTF-8'))

    def isVerified(self):
        return self.personNick in self.verified

    def verify(self, data, name):
        verifiyFp = open("pass.txt", "r")
        password = verifiyFp.readline().rstrip('\n')
        if(re.search(password, data)):
            self.sendToPerson("Verified!")
            self.verified.append(name)
        else:
            self.sendToPerson("Incorrect password for verification.")

def main():
    bot = Bot()
    bot.start()

if __name__ == "__main__":
    main()
