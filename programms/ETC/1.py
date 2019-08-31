import random
print("You have to insert lower and upper bound of a Scope then we choos a random value between and help you guess ")
result = 'y'
while result=='y' :
   lower = int(input("Please enter the lower bound  >"))
   upper = int(input("Please enter the upper bound  >"))
   Times = int(input("Let me know how many times do you want to guess!? >"))
   secret_number=random.randint(lower,upper)
   times_1=Times
   while Times:
          print ("Enter The Number",times_1-Times+1 ,"between ",lower," - ",upper,":")
          num = int(input())
          if num == secret_number :
                print ("Congratulations! \nYou Won The Game ! ")
                break
          Times-=1
   print("Unfortunately You Loosed The Game!")
   print("-- The Number Was", secret_number," --")
   print("------------------------------------------------------------")
   result = input("Do You Want to Try New Game(Y/n)?")
    # if not(num<=upper)and(num>= lower):