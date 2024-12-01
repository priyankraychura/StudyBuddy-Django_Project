f = open("number.txt")
even = open("even.txt", "a")
odd = open("odd.txt", "a")

for i in f:
    if int(i) % 2 == 0:
        even.write(i)
    else:
        odd.write(i)

even.close()
odd.close()
f.close()

numbers = open("number.txt")
even = open("even.txt")
odd = open("odd.txt")

print("Numbers: ", numbers.read())
print("Even numbers: ", even.read())
print("Odd number: ", odd.read())
