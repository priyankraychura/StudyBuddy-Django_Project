num1  = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print("--------------------------------------")
print("Choice: ")
print("1. Addition")
print("2. Substration")
print("3. Multiplication")
print("4. Divison")

choice = input("Enter choice: ")

if choice == "1":
    print("Addition is: ", num1 + num2)
elif choice == "2":
    print("Subsctraction is: ", num1 - num2)
elif choice == "3":
    print("Multiplication is: ", num1 * num2)
elif choice == "4":
    print("Division is: ", num1 / num2)
else:
    print("Invalid choice")