def reverseStr(name):
    reverseName = ""

    for i in range(len(name) - 1, 0 - 1, -1):
        reverseName += name[i]

    return reverseName

print(reverseStr("Priyank"))