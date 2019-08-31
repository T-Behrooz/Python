try:
    x=int(input("please Enter your number::"))
    print(x/0)
except Exception as e:
    print("An Error occured!\n",e)
