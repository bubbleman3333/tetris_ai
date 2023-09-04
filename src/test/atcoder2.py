from collections import defaultdict

dic = defaultdict(dict)
n = int(input())
for i in range(1, n):
    for idx, d in enumerate(list(map(int, input().split(" ")))):
        opp = i + idx + 1
        dic[i][opp] = d
        dic[opp][i] = d

remain = [False] * (1 + n)
remain[0] = True
now_max = 0

t = 0


def read(number, score, odd):
    global t
    t += 1
    global now_max
    remain[number] = True
    rem = [idx for idx, v in enumerate(remain) if not v]
    if len(rem) == 0:
        now_max = max(now_max, score)
        remain[number] = False
        return
    for i in rem:
        if odd:
            c = dic[number][i]
            temp_score = score + c
        else:
            temp_score = score
        read(i, temp_score, not odd)
    remain[number] = False


import time

start = time.time()
read(1,0,0)
print(now_max)
print(time.time() - start)
print(t)
