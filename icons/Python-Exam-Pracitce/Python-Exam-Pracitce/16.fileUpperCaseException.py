try:
    file = open("demo.txt")
except FileNotFoundError:
    print("File does not exists")
else:
    def convertToUpper():
        for i in file:
            print(i.upper())

convertToUpper()