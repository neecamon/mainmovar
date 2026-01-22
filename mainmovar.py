import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,QStackedWidget, QFrame, QFormLayout, QGroupBox, QScrollArea, QListWidget, QMessageBox, QTextEdit, QSlider
)
from PySide6.QtCore import Qt
from datetime import datetime
from database import MovieDatabase

def apply_stylesheet(app, path):
    try:
        with open(path, "r") as file:
            qss = file.read()
            app.setStyleSheet(qss)
    except FileNotFoundError:
        print("File style.qss tidak ditemukan!")

class MovieArchiver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = MovieDatabase()
        self.setWindowTitle("Movar (Movie Archiver)")
        self.resize(400,300)
        self.central_page = QStackedWidget()
        self.setCentralWidget(self.central_page)

        self.login_page()
        self.dashboard()
        self.load_data_to_ui()

    #1. HALAMAN LOGIN
    def login_page(self):
        self.login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.title_login = QLabel("MOVAR")
        self.title_login.setObjectName("loginTitle")
        self.desc_app = QLabel("Welcome to Movar! Let’s get started by sharing your first review of your favorite movie right here.")
        self.desc_app.setObjectName("desc_app")
        layout.addWidget(self.title_login, alignment=Qt.AlignCenter)
        layout.addWidget(self.desc_app, alignment=Qt.AlignCenter)
        
        self.message_label = QLabel("What should we call you?")
        self.message_label.setObjectName("loginMessage")
        layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        self.name_label = QLabel("Your Name : ")
        self.name_label.setObjectName("yourname")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_input = QLineEdit()
        self.name_input.setMaximumWidth(300)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        login_btn = QPushButton("START")
        login_btn.setMaximumWidth(300)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        self.login_widget.setLayout(layout)
        self.central_page.addWidget(self.login_widget)

    #2. LOGIN CONNECTED
    def handle_login(self):
        name = self.name_input.text()
        if name != "":
            self.label_welcome.setText(f"Hello, {name}! welcome to Movar Dashboard")
            self.central_page.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Input Empty", "Please write your name~")

    #3. HALAMAN DASHBOARD (HALAMAN UTAMA)
    def dashboard(self):
        self.dashboard_widget = QWidget()
        self.dashboard_layout = QVBoxLayout()
        self.label_welcome = QLabel()
        self.label_welcome.setObjectName("welcomeLabel")

        #membuat tombol kembali yang akan mengarah ke halaman login
        self.btn_back = QPushButton("Back to start")
        self.btn_back.clicked.connect(lambda: self.central_page.setCurrentIndex(0))

        #membuat tombol profil
        self.btn_profile = QPushButton("Profile")
        self.btn_profile.clicked.connect(self.show_profile)

        #membuat header
        header = QHBoxLayout()
        header.addWidget(self.label_welcome)
        header.addStretch()
        header.addWidget(self.btn_back)
        header.addWidget(self.btn_profile)
        self.dashboard_layout.addLayout(header)

        #Tumpukan kedua yang ada di dalam tab Movie
        self.movie_stack = QStackedWidget()
        self.movie_listpage() #index(0)
        self.movie_formpage() #index(1)
        self.setup_detail_page() #index(2)

        #---MEMBUAT 3 TAB UTAMA---
        self.tabs = QTabWidget()
        self.tabs.setMovable(False)
        self.tab_movie = QListWidget()
        self.tab_watchlist = QListWidget()
        self.tab_favorite = QListWidget()
        self.tabs.addTab(self.movie_stack, "Movie")
        self.tabs.addTab(self.tab_watchlist, "Watchlist")
        self.tabs.addTab(self.tab_favorite, "Favorite")

        self.tab_watchlist.itemClicked.connect(self.show_moviedetail)
        self.tab_favorite.itemClicked.connect(self.show_moviedetail)

        self.dashboard_layout.addWidget(self.tabs)

        # Akhiri dengan set layout
        self.dashboard_widget.setLayout(self.dashboard_layout)
        self.central_page.addWidget(self.dashboard_widget)

    #4. HALAMAN PROFIL
    def show_profile(self):
        name_user = self.name_input.text()
        msg = QMessageBox(self)
        msg.setWindowTitle("User Profile")
        msg.setText(f"Informasi Pengguna:\n\nNama: {name_user}\nStatus: Active Member")
        msg.exec()

    #5 ISI DARI MENU MOVIE
    def movie_listpage(self):
        #Halaman utama Movie (Form + List)
        page = QWidget()
        layout = QVBoxLayout()

        #menambahkan tombol tambah film.
        btn_add = QPushButton("Add Movie")
        btn_add.setStyleSheet("background-color: #b38659; color: white; font-weight: bold; padding: 10px;")
        btn_add.clicked.connect(lambda: self.movie_stack.setCurrentIndex(1))

        layout.addWidget(btn_add)
        layout.addWidget(QLabel("Your Movies : "))
        self.movie_display = QListWidget()
        self.movie_display.itemClicked.connect(self.show_moviedetail)

        layout.addWidget(self.movie_display)
        page.setLayout(layout)
        self.movie_stack.addWidget(page)

    #6. FORM INPUT (halaman yang muncul saat tombol "Add Movies" diklik)
    def movie_formpage(self):
        page = QWidget()
        layout = QVBoxLayout()

        formlayout = QFormLayout()

        self.title_input = QLineEdit()
        self.year_input = QComboBox()
        self.year_input.addItems([str(y) for y in range(datetime.now().year, 1899, -1)])
        self.genre_input = QLineEdit()
        self.actors_input = QLineEdit()
        self.review_input = QTextEdit()
        self.review_input.setMaximumHeight(100)

        #menambahkan fitur rating 
        # Membuat Label untuk keterangan Rating
        self.label_rating_text = QLabel("Rating: 1/10")
        self.label_rating_text.setObjectName("ratingLabel")

        # Membuat Slider
        self.rating_slider = QSlider(Qt.Horizontal)
        self.rating_slider.setMinimum(1)
        self.rating_slider.setMaximum(10)
        self.rating_slider.setValue(1) # Nilai awal
        self.rating_slider.setTickPosition(QSlider.TicksBelow)
        self.rating_slider.setTickInterval(1)

        # Fungsi untuk mengupdate angka saat slider digeser
        self.rating_slider.valueChanged.connect(self.update_rating_label)

        # Tambahkan ke layout utama
        formlayout.addRow("Judul : ", self.title_input)
        formlayout.addRow("Tahun : ", self.year_input)
        formlayout.addRow("Genre : ", self.genre_input)
        formlayout.addRow("Actors : ", self.actors_input)
        formlayout.addRow("Review : ", self.review_input)
        layout.addLayout(formlayout)
        layout.addWidget(self.label_rating_text)
        layout.addWidget(self.rating_slider)

        # Tombol Aksi
        btn_box = QHBoxLayout()
        btn_watched = QPushButton("Save to Watched")
        btn_watched.clicked.connect(self.save_watched)
        btn_watchlist = QPushButton("Save to Watchlist")
        btn_watchlist.clicked.connect(self.save_watchlist)
        btn_back = QPushButton("Batal")
        btn_back.clicked.connect(lambda: self.movie_stack.setCurrentIndex(0))

        btn_box.addWidget(btn_watched)
        btn_box.addWidget(btn_watchlist)
        btn_box.addWidget(btn_back)
        
        #mengatur layout di dalam movie form page
        layout.addLayout(btn_box)
        layout.addStretch()

        page.setLayout(layout)
        self.movie_stack.addWidget(page)

    def update_rating_label(self, value):
        self.label_rating_text.setText(f"Rating: {value}/10")

    def load_data_to_ui(self):
        self.movie_display.clear()
        self.tab_watchlist.clear()
        
        # Ambil semua data dari database.py
        movies = self.db.get_all_movies()
        
        for title, year, status in movies:
            info = f"{title} ({year})"
            if status == "watched":
                self.movie_display.addItem(info)
            elif status == "watchlist":
                self.tab_watchlist.addItem(info)

    def setup_detail_page(self):
        self.detail_page = QWidget()
        layout = QVBoxLayout()

        self.detail_title = QLabel("<h2>Judul Film</h2>")
        self.detail_content = QLabel("Info Lengkap...")
        self.detail_content.setWordWrap(True)
        self.detail_content.setAlignment(Qt.AlignTop)

        btn_action_layout = QHBoxLayout()
    
        btn_fav = QPushButton("⭐ Add to Favorite")
        btn_fav.setStyleSheet("background-color: #f1c40f; color: black; font-weight: bold;")
        btn_fav.clicked.connect(self.add_to_favorite)

        btn_delete = QPushButton("🗑️ Delete Movie")
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_movie)
        
        btn_action_layout.addWidget(btn_fav)
        btn_action_layout.addWidget(btn_delete)

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.movie_stack.setCurrentIndex(0))

        layout.addWidget(self.detail_title)
        layout.addWidget(self.detail_content)
        layout.addLayout(btn_action_layout)
        layout.addStretch()
        layout.addWidget(btn_back)

        self.detail_page.setLayout(layout)
        self.movie_stack.addWidget(self.detail_page) # Ini akan jadi index 2

    def show_moviedetail(self, item):
        full_text = item.text()
        movie_title = full_text.rsplit(" (", 1)[0] # Mengambil bagian judul saja

        data = self.db.get_movie_detail(movie_title)
        if data:
            # data adalah tuple: (id, title, year, genre, actors, review, rating, status)
            self.detail_title.setText(f"<h2>{data[1]}</h2>")
            detail_text = (
                f"<b>Year:</b> {data[2]}<br>"
                f"<b>Genre:</b> {data[3]}<br>"
                f"<b>Actors:</b> {data[4]}<br>"
                f"<b>Rating:</b> {data[6]}/10<br><br>"
                f"<b>Review:</b><br>{data[5]}"
        )
        self.detail_content.setText(detail_text)
        
        # Pastikan tab pindah ke utama agar stacked widget terlihat
        self.tabs.setCurrentIndex(0) 
        self.movie_stack.setCurrentIndex(2)
        
    def save_watched(self):
        title = self.title_input.text()
        year = self.year_input.currentText()

        if title:
        # Kirim data ke database.py
            success = self.db.add_movie(
                title, year, 
                self.genre_input.text(), 
                self.actors_input.text(), 
                self.review_input.toPlainText(), 
                self.rating_slider.value(), 
                "watched"
            )
        
            if success:
                self.movie_display.addItem(f"{title} ({year})")
                self.clear_inputs()
                self.movie_stack.setCurrentIndex(0)
                QMessageBox.information(self, "Sukses", "Film berhasil disimpan ke Watched!")
            else:
                QMessageBox.warning(self, "Error", "Judul film sudah ada di database!")
        else:
            QMessageBox.warning(self, "Input Error", "Judul tidak boleh kosong!")
       

    def save_watchlist(self):
        title = self.title_input.text()
        year = self.year_input.currentText()
    
        if title:
            # 1. Simpan detail lengkap ke database agar bisa dibuka di halaman detail
            self.movie_db[title] = {
                "year": year,
                "genre": self.genre_input.text(),
                "actors": self.actors_input.text(),
                "review": self.review_input.toPlainText(),
                "rating": self.rating_slider.value()
            }
            
            # 2. Tambahkan ke list visual di tab Watchlist
            info = f"{title} ({year})"
            self.tab_watchlist.addItem(info)
            
            # 3. Bersihkan dan kembali
            self.clear_inputs()
            self.movie_stack.setCurrentIndex(0)
            QMessageBox.information(self, "Watchlist", f"'{title}' ditambahkan ke daftar tunggu!")
        else:
            QMessageBox.warning(self, "Input Kosong", "Judul film harus diisi!")

    def add_to_favorite(self):
        # 1. Ambil judul dari label detail (bersihkan tag HTML)
        current_title = self.detail_title.text().replace("<h2>", "").replace("</h2>", "")
        
        # 2. Ambil data lengkap film tersebut dari database
        data = self.db.get_movie_detail(current_title)
        
        if data:
            # data[2] adalah kolom 'year' berdasarkan urutan di database.py
            year = data[2] 
            movie_info = f"{current_title} ({year})"
            
            # 3. Cek apakah sudah ada di list visual favorite agar tidak duplikat
            items = [self.tab_favorite.item(i).text() for i in range(self.tab_favorite.count())]
            
            if movie_info not in items:
                self.tab_favorite.addItem(movie_info)
                QMessageBox.information(self, "Favorite", f"'{current_title}' berhasil ditambahkan ke Favorite!")
            else:
                QMessageBox.warning(self, "Favorite", "Film ini sudah ada di daftar Favorite.")

    def delete_movie(self):
        current_title = self.detail_title.text().replace("<h2>", "").replace("</h2>", "")
        
        reply = QMessageBox.question(self, "Hapus Film", f"Hapus '{current_title}' dari database?", QMessageBox.Yes | QMessageBox.No)
            
        if reply == QMessageBox.Yes:
            # 1. Hapus dari file database SQLite via database.py
            self.db.delete_movie(current_title)
                
            # 2. Refresh tampilan UI agar film hilang dari list
            self.load_data_to_ui()
                
            QMessageBox.information(self, "Berhasil", "Film telah dihapus.")
            self.movie_stack.setCurrentIndex(0) # Kembali ke daftar

    # Fungsi pembantu untuk mencari dan menghapus teks di dalam QListWidget
    def remove_item_from_list(self, list_widget, text_to_remove):
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item and item.text() == text_to_remove:
                list_widget.takeItem(i)
                break
            

    def clear_inputs(self):
        self.title_input.clear()
        self.genre_input.clear()
        self.actors_input.clear()
        self.review_input.clear()
        self.year_input.setCurrentIndex(0) # Kembali ke tahun paling atas
        self.rating_slider.setValue(1)

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
   
    basedir = os.path.dirname(__file__)
    path_qss = os.path.join(basedir, "movartheme.qss")
    
    apply_stylesheet(app, path_qss)

    window = MovieArchiver()
    window.show()
    sys.exit(app.exec())