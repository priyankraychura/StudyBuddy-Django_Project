start = int(input("Enter starting point: "))
end = int(input("Enter ending point: "))
order = input("Enter asc or des: ")

if order == "asc":
    for i in range(start, end + 1):
        print(i)
elif order == "des":
    for i in range(end, start -1, -1):
        print(i)