hw=('Hello World!')
HW = hw.lower()
for i in HW:
    if i == 'h':
        print (HW.replace ('h','H'))
    elif i == 'l':
        HW = HW.upper()
        print (HW)
