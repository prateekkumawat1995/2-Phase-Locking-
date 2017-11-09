#!usr/bin/env python
import sys
from __builtin__ import any

# Read schedule from file
file = open("schedule", "r")

# Store schedule in list s
s = file.readlines()
tno = s.count("new\n")
x = [[] for _ in xrange(tno)]
i = 2
j = 0

# stored transections in different nested lists
while i < len(s):
    if s[i] == "new\n":
        j = j + 1
        i = i + 2
    x[j].append(s[i])
    i = i + 1

print x
order=""
rollback=""
ins_exe=[]
locktable = []
point = [0] * tno
tstate = ["0"] * (tno)
while True:
    for p in range(tno):
        count=0
        while count < 3:
            if (tstate[p] == 'committed'):
                break
            if x[p][point[p]][0] == 'r' and any(x[p][point[p]][1] in c for c in locktable ) and not(str(p)+x[p][point[p]][1] in locktable):
                m=[m for m in locktable if x[p][point[p]][1] in m]
                rmlock=[]
                if p>int(m[0][0]):
                    for i in locktable:
                        if str(p)!=i[0] :
                            rmlock.append(i)
                    ins_exe.append("rollback" + str(p))
                    point[p]=0
                    locktable=rmlock
                    rollback = rollback + str(p)
                break
            if x[p][point[p]][0] == 'r' and any(x[p][point[p]][1] in c for c in locktable) and (str(p) + x[p][point[p]][1] in locktable):
                ins_exe.append(x[p][point[p]][0:2] + str(p))
                point[p] = point[p] + 1
                count = count + 1
                continue
            if x[p][point[p]][0] == 'c':
                order=order+str(p)
                rmlock = []
                tstate[p] = 'committed'
                for i in locktable:
                    if i[0] != str(p):
                        rmlock.append(i)
                ins_exe.append("commit" + str(p))
                locktable=rmlock
                break
            if x[p][point[p]][0] == 'w' and any(x[p][point[p]][1] in c for c in locktable) and not(str(p)+x[p][point[p]][1] in locktable):
                m = [m for m in locktable if x[p][point[p]][1] in m]
                rmlock = []
                if p > int(m[0][0]):
                    for i in locktable:
                        if str(p) != i[0]:
                            rmlock.append(i)
                    ins_exe.append("rollback" + str(p))
                    locktable=rmlock
                    point[p] = 0
                    rollback = rollback + str(p)
                break
            if x[p][point[p]][0] == 'w' and any(x[p][point[p]][1] in c for c in locktable) and (str(p) + x[p][point[p]][1] in locktable):
                ins_exe.append(x[p][point[p]][0:2] + str(p))
                point[p] = point[p] + 1
                count = count + 1
                continue
            if x[p][point[p]][0] == 'r' and not(any(x[p][point[p]][1] in c for c in locktable)):
                ins_exe.append(x[p][point[p]][0:2] + str(p))
                point[p] = point[p] + 1
                count = count + 1
                continue
            if x[p][point[p]][0] == 'w' and not(any(x[p][point[p]][1] in c for c in locktable)):
                locktable.append(str(p) + x[p][point[p]][1])
                ins_exe.append(x[p][point[p]][0:2]+str(p))
                point[p] = point[p] + 1
                count = count + 1
                continue
        if not ('0' in tstate):
            break
    if not ('0' in tstate):
        break
print "The order of execution is "+order
print "The order of rollback is  "+rollback
print "The order of instruction execution is :- \n"
for i in ins_exe :
    print i
