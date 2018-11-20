num = list(range(0,100))
def find(num):
    var = input("""Please enter a number: """)
    print("You entered " + var)
    for i in num:
        if i == i:
            print ("Is " + str(i) +" your number?")
        else:
            return str(42)
print (find(num))
