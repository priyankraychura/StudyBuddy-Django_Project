f = open("demo.txt", "w")

f.write("This is demo file")
f.close()

f = open("demo.txt")
print(f.read())