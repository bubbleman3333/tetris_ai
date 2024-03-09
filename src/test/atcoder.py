n,x = list(map(int,input().split(" ")))

a = list(map(int,input().split(" ")))
for i in range(101):
    temp = a.copy()
    temp.append(i)
    temp.sort()
    if sum(temp[1:-1])>=x:
        print(i)
        exit()
print(-1)