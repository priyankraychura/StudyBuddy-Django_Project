start = int(input("Enter starint point: "))
end = int(input("Enter ending point: "))

for i in range(start, end + 1):
    if i % 2 != 0:
        print(i)