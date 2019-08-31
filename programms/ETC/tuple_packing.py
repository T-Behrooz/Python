def tuplepacking(first,* args):
    total =0
    for num in args :
        total+=num
    return first,total,"Done"

print (tuplepacking('ali',))