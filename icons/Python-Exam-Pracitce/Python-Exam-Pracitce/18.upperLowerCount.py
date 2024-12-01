def caseCount(sentense):
    upper = 0
    lower = 0

    for i in sentense:
        if i.isupper():
            upper += 1
        elif i.islower():
            lower += 1
        else:
            pass

    print("UpperCount: ", upper)
    print("LowerCount: ", lower)

sent = input("Enter a sentense: ")
caseCount(sent)
