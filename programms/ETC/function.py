def isSquare(n):
    i = 1
while i * i <= n:
    if (i * i == n):
        return True
        i = i + 1
    return False

n = int(input("Enter n:"))
for i in range(1, n + 1):
    if isSquare(i) == True:
       print(i, end = '\t')
