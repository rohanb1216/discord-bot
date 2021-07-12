import sqlite3

def create_connection(db_file):
	conn = None
	conn = sqlite3.connect(db_file)
	return conn

def create_table(conn):
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS user_info (
										discord_id varchar(100) PRIMARY KEY,
										d2_name varchar(100),
										d2_member_id varchar(100)
									);""")

def add_user(conn, discord_id, d2_name, d2_member_id):
	cur = conn.cursor()
	users = cur.execute("SELECT * from user_info WHERE discord_id=?",(discord_id,))
	if(len(list(users)) != 0):
		return False
	else:
		cur.execute("INSERT INTO user_info VALUES(?,?,?)",(discord_id, d2_name, d2_member_id))
		conn.commit()
		return True

def get_d2_member_id(conn, discord_id):
	cur = conn.cursor()
	users = cur.execute("SELECT * from user_info WHERE discord_id=?",(discord_id,))
	users = list(users)
	if(len(users) == 0):
		return ()
	else:
		return (users[0][1], users[0][2])

def disp_db(conn):
	cur = conn.cursor()
	users = cur.execute("SELECT * from user_info")
	users = list(users)
	for i in users:
		print(i)


# db_file = "d2.db"
# conn = create_connection(db_file)
# create_table(conn)

# n = int(input())
# for i in range(n):
# 	discord_id = input()
# 	d2_id = input()
# 	d2_member_id = input()
# 	ret = add_user(conn, discord_id, d2_id, d2_member_id)
# 	if(ret == False):
# 		print("user already added")
# 	else:
# 		print("user added")

# print(get_d2_member_id(conn, "hosay_halapeno#8650"))

# disp_db(conn)
# conn.close()