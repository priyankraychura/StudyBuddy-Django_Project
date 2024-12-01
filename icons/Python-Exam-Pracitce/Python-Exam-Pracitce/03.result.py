name = input("Enter name: ")
sem = input("Input semester: ")
college = input("Enter college name: ")

print("Enter marks: ")
j2ee = int(input("Enter j2ee  marks: "))
python = int(input("Enter python marks: "))
cs = int(input("Enter cyber security marks: "))

print("---------------------------------------------")
print("Nmae:", name)
print("Semester: ", sem)
print("College: ", college)
print("J2EE marks: ", j2ee)
print("Python marks: ", python)
print("Cyber Security marks: ", cs)

total = j2ee + python + cs
percentage = (total/300) * 100

if percentage > 80:
    Class = "Dist"
elif percentage > 70:
    Class = "First"
elif percentage > 60:
    Class = "Second"
elif percentage > 50:
    Class = "Third"
else:
    Class = "Fail"

print("Total marks: ", total)
print("Percentage: ", percentage)
print("Class: ", Class)


