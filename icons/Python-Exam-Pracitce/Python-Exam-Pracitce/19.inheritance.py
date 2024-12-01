class Parent():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def view(self):
        print("This is parent class view")
        print(self.name, self.age)
    
class Child(Parent):
    def __init__(self, name, age, college):
        super().__init__(name, age)
        self.college = college

    def view(self):
        print("This is child class view")
        print(self.name)
        print(self.age)
        print(self.college)

p1 = Parent("Priyank", 22)
p1.view()

c1 = Child("Chaman", 19, "Christ")
c1.view()

