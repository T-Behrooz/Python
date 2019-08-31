import random
print("You have to insert lower and upper bound of a Scope then we choose a random value between and help you guess ")
result = 'y'
r = True
while result=='y' :# This loop repeats the game!
    lower = int(input("Please enter the lower bound  :\>"))
    upper = int(input("Please enter the upper bound  :\>"))
    Times = int(input("Let me know how many times do you want to guess!? :\>"))
    secret_number=random.randint(lower,upper)
    times_1=Times
    while Times:
       while r:# This Loops checks and gets the numbers

            if (times_1-Times+1)==times_1:
               print(" \n +++++ Be Carfule! This is your last Chance +++++ \n")
            print ("Enter The Number",times_1-Times+1 ,"between ",lower," - ",upper,":")
            num = int(input())
           #Here I check if if the entered value is between lower and upper bounds
            if (num > upper) or (num < lower) :
               r = True
            else:
               break
       if num == secret_number :
           print (" ******* Congratulations! ******* \nYou Won The Game ! ")
           break
       elif num>secret_number:
           print( "========== The Chosen number is LOWER than yours! ========== \n")
       else :
           print( "========== The Chosen number is GREATER than yours! ==========\n")
       Times-=1
    else :
        print("Unfortunately You Loosed The Game!")
        print("==============================================================================")
        print("-- The Number Was", secret_number," --")
        print("==============================================================================")
    result = input("Do You Want to Try New Game(Y/n)?")
