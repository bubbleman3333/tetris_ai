from collections import defaultdict

dic = defaultdict(list)
n, m = list(map(int, input().split(" ")))

for i in range(m):
    a, b = list(map(int, input().split(" ")))
    dic[a].append(b)

for i in dic:
    dic[i].sort()
seen = [True] * n


def read(v):
    seen[v] = False
    for v2 in dic[v]:
        if not seen[v2]:
            continue
        read(v2)


read(0)
print(sum(seen))
