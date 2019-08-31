import random


class Father :
    def __init__(self,name ,**kwargs):
        self.name = name
        for key , value in kwargs .items():
            setattr(self,key,value)
            
class soldier(Father):
    name = 'guest'
    def  __init__(self, name,type1 = 'x25', **kwargs):
        self.name  = name
        self.color = 'white'
        self.alive = True
        self.Death = False
        self.type = type1
        for key , value in kwargs .items():
            setattr(self,key,value)


    def myprint(self,text):
        return text
    
    def takecare(self):
        print("{} Called Me!".format(self))
        return bool(random.randint(0,1))
