import sqlite3 as sl

sqlite = sl.connect('old.db')
cursor = sqlite.cursor()

a = cursor.execute('SELECT * FROM items WHERE itemstatus = 1').fetchall()

t = 0
for i in a:
    t += i[4]

print("Total unclaimed payout: ",t*0.7)
print("Total unclaimed items: ", len(a))

sellers = {}

for i in a:
    try:
        sellers[i[1]] +=1
    except:
        sellers[i[1]] = 1


b = cursor.execute('SELECT * FROM items WHERE itemstatus = 2').fetchall()
tt = 0
for i in b:
    tt += i[4]

print("Total payed out: ",tt*0.7)

print("Total profit: ", tt*0.3 + t)

cursor.close()
sqlite.close()