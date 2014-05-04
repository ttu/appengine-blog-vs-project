import json

class UserProfile():
 
    def __init__(self, data = None):	
        self.id = ''
        self.name = ''
        if data:
            self.parse(data)

    def parse(self, data):
       j = json.loads(data)
       self.id = j['id']
       self.name = j['name']