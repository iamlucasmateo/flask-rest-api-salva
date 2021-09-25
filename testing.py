import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# get items

# select_query = 'SELECT * FROM items'
# result = cursor.execute(select_query).fetchall()

# for item in result:
#     print(item)

# update items

# item ={"itemname": "test", "itemprice": 213.00}
# update_query = "UPDATE items SET itemprice=? WHERE itemname=?"
# cursor.execute(update_query, (item["itemprice"],item["itemname"]))

# result = cursor.execute(update_query).fetchall()

# for item in result:
#     print(item)

# get user

users = cursor.execute("SELECT * FROM items").fetchall()
for u in users:
    print(u)

conn.commit()
conn.close()
