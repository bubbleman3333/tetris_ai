n, m = list(map(int, input().split(" ")))

a = list(map(int, input().split(" ")))

b = list(range(n + 1))

base = b.copy()
for i in range(m):
    temp = a[i]
    base[temp], base[temp + 1] = base[temp + 1], base[temp]

pos = [0] * (n + 1)
for i in range(1, n + 1):
    pos[base[i]] = i

for i in a:
    if b[i] == 1:
        print(pos[b[i + 1]])
    elif b[i + 1] == 1:
        print(pos[b[i]])
    else:
        print(pos[1])
    b[i], b[i + 1] = b[i + 1], b[i]
