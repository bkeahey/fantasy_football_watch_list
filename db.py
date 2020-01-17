import sqlite3

class Database:
	def __init__(self, db):
		self.conn = sqlite3.connect(db)
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, player text, position text, rank text, value text)")
		self.conn.commit()

	def fetch(self):
		self.cur.execute("SELECT * FROM players")
		rows = self.cur.fetchall()
		return rows

	def insert(self, player, position, rank, value):
		self.cur.execute("INSERT INTO players VALUES (NULL, ?, ?, ?, ?)", (player, position, rank, value))
		self.conn.commit()

	def remove(self, id):
		self.cur.execute("DELETE FROM players WHERE id = ?", (id,))
		self.conn.commit()

	def update(self, id, player, position, rank, value):
		self.cur.execute("UPDATE players SET player = ?, position = ?, rank = ?, value = ? WHERE id = ?", (player, position, rank, value, id))
		self.conn.commit()

	def __del__(self):
		self.conn.close()

#db = Database("rankings.db")

#test player insert
#db.insert("Diontae Johnson", "WR", "30", "Round 7")
