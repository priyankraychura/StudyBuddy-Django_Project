class Bank:
    def __init__(self, accountType, balance):
        self.accountType = accountType
        self.__balance = balance

    def showBalance(self):
        print(self.__balance)

acc = Bank("Saving", 2000)
print(acc.accountType)
acc.showBalance()