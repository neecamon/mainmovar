import sqlite3

class MovieDatabase:
    def __init__(self, db_name="movar_database.db"):
        # Membuat koneksi ke file database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Membuat tabel movies jika belum ada
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE,
                year TEXT,
                genre TEXT,
                actors TEXT,
                review TEXT,
                rating INTEGER,
                status TEXT
            )
        ''')
        self.conn.commit()

    def add_movie(self, title, year, genre, actors, review, rating, status):
        """Menyimpan film baru ke database"""
        try:
            self.cursor.execute('''
                INSERT INTO movies (title, year, genre, actors, review, rating, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, year, genre, actors, review, rating, status))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Mengembalikan False jika judul film sudah ada (karena UNIQUE)
            return False

    def get_all_movies(self):
        """Mengambil semua film untuk ditampilkan di list utama"""
        self.cursor.execute("SELECT title, year, status FROM movies")
        return self.cursor.fetchall()

    def get_movie_detail(self, title):
        """Mengambil detail lengkap satu film berdasarkan judul"""
        self.cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
        return self.cursor.fetchone()

    def delete_movie(self, title):
        """Menghapus film dari database"""
        self.cursor.execute("DELETE FROM movies WHERE title = ?", (title,))
        self.conn.commit()

    def close(self):
        """Menutup koneksi database"""
        self.conn.close()