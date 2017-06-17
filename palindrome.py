a = input('Kelime : ').strip()
c = len(a)
kel = ''
for i in range(c):
    for j in range(i,c):
        cur = a[i:j+1]
        if cur==cur[::-1] and j-i+1>len(kel):
            kel = cur
print(kel,'>>>',len(kel))

