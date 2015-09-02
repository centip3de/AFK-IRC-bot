
class Parser():

    def __init__(self, filename):
        self.filename   = filename 
        self.text       = "" 
        self.TOKENS = {
                "password"  : "",
                "authorized": "",
                "channel"   : "",
                "bot_owner" : "",
                "nickname"  : "",
                "server"    : "",
                "port"      : ""} 


    def parse(self):
        fd = open(self.filename, 'r')
        lines = fd.read().split('\n')
        fd.close()

        for line in lines:
            if(line == ""):
                continue

            tokens = line.split('=')
            tokens[0] = tokens[0].strip()
            tokens[1] = tokens[1].strip()
            if(tokens[0] in self.TOKENS):
                self.TOKENS[tokens[0]] = tokens[1]
        
        return self.TOKENS
