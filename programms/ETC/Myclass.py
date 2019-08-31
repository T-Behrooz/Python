import random

class soldier:
    name = True
    def __init__(self,type = 'x25',color,alive,death ,**kwargs):
        self.color = 'white'
        self.alive = True
        self.Death = False
        for key , value in kwargs .items():
            setattr(self,key,value)


    def myprint(self,text):
        return text
    def takecare(self):
        print("{} Called Me!".format(self))
        return bool(random.randint(0,1))
