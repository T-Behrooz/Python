string='d:\myfile.txt'
f= open (string,'r')
firstline=f.readline()
secondline=f.readline()
third=f.readline()
print(firstline)
print(secondline)
print(third)
f.close()
