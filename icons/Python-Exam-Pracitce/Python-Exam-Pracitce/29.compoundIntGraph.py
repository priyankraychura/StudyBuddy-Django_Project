principal = 10000
interestRate = 0.05
years = 20
values = []

for i in range(years + 1):
    values.append(principal)
    principal += principal * interestRate

print(values)