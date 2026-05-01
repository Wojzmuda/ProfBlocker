import numpy as np
import sqlite3
from pathlib import Path


class DataBaseManager():
    def __init__(self, db_path="users_info.db"):
        project_root = Path(__file__).parent.resolve().parent
        self.db_path = project_root / db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL UNIQUE,
                                embedding BLOB NOT NULL,
                                picture TEXT NOT NULL
                         )
                         ''')
            

    def save_user(self, name, embedding, picture):
        try:
            with sqlite3.connect(self.db_path) as conn:
                emb_blob = embedding.tobytes()
                conn.execute("INSERT INTO users (name, embedding, picture) VALUES(?, ?,? )", (name, emb_blob, picture)         
                ) 
            return True, "Success"
        except sqlite3.IntegrityError:
            return False, "User with this name already exists"

    def load_all_users(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name, embedding, picture FROM users")
            rows = cursor.fetchall()

            users_data=[]
            for name, emb_blob, picture in rows:
                emb = np.frombuffer(emb_blob, dtype=np.float64)
                users_data.append((name,emb,picture))
            return users_data
        
    def delete_user(self, name):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM users where name = ?", (name,))
            conn.commit()

if __name__=="__main__":
    manager = DataBaseManager()

