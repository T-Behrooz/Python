myset={0,}
y=1
i=0
print("Your numbers must be greater than Zero!")
while (y!=0):
   i+=1
   y=int(input("Number {}:".format(i)))
   myset.add(y)
myset.remove(0)
print("your set has {} elements and is : \n{}".format(myset.__len__(),myset))
