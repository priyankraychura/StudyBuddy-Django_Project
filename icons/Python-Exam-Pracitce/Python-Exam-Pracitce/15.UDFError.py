class NoName(Exception):
    pass

try:
    name = input("Enter a name: ")

    if name == "":
        raise NoName
    else:
        print("Your name is", name)
except:
    print("Name field cannot be empty")
    