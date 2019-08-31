class numstring:
    'This is my Class'
    def __init__(self,value, * args,**kwarg):
        self.value = str(value)

    def __str__(self):
        return self.value
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    def __add__(self,other):
        if '.' in self.value:
            return float(self)*other
        return int(self)+other
    




from ETC.A import numstring
me=numstring()
        
        
