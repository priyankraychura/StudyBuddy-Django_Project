numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
odd = []
even = []

for i in numbers:
    if i % 2 == 0:
        even.append(i)
    else:
        odd.append(i)
    
print(odd)
print(even)