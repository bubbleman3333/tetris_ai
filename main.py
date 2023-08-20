class a:
    def __init__(self,name):
        self.name = name


x = a("aaa")
y = a("yyy")

x = y

y=a("new")

print(x.name)
print(y.name)