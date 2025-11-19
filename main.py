import sys
import sqlite3
import hashlib
import pyshorteners
from faker import Faker
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QTabWidget, QTextEdit, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Database Name
DB_NAME = 'users.db'

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIA Lab Project - Standard")
        self.setFixedSize(700, 600) 

        # Initialize Faker
        self.fake = Faker()
        self.current_user = "" 

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Stacked Layout to switch between screens
        self.stack = QStackedWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.stack)

        # --- Create the Three Screens ---
        self.create_login_screen()   # Index 0
        self.create_utility_screen() # Index 1
        self.create_register_screen() # Index 2

        # Show Login Screen first
        self.stack.setCurrentIndex(0)

        # CENTER THE WINDOW
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # ============================================
    # PART 1: LOGIN SCREEN
    # ============================================
    def create_login_screen(self):
        self.page_login = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("SIA Mini Project")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Utilities Features")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #555555;")
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        # Inputs
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Username")
        self.input_user.setFixedWidth(250)
        layout.addWidget(self.input_user, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Password")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password) 
        self.input_pass.setFixedWidth(250)
        layout.addWidget(self.input_pass, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(10) 

        # Login Button
        btn_login = QPushButton("Login")
        btn_login.setFixedWidth(150)
        btn_login.clicked.connect(self.verify_login)
        layout.addWidget(btn_login, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(5) 

        # Create Account Button
        btn_register = QPushButton("Create Account")
        btn_register.setFixedWidth(150)
        btn_register.clicked.connect(lambda: self.stack.setCurrentIndex(2)) 
        layout.addWidget(btn_register, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page_login.setLayout(layout)
        self.stack.addWidget(self.page_login)

    def verify_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == hashed_password:
            self.current_user = username 
            self.update_user_label()     
            self.stack.setCurrentIndex(1) # Go to Utilities
            self.input_user.clear()
            self.input_pass.clear()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Username or Password")

    # ============================================
    # PART 2: UTILITY SCREEN
    # ============================================
    def create_utility_screen(self):
        self.page_utils = QWidget()
        main_layout = QVBoxLayout()

        # --- HEADER ---
        header_layout = QHBoxLayout()
        header_layout.addStretch() 
        self.lbl_user_display = QLabel("User: ???")
        self.lbl_user_display.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.lbl_user_display.setStyleSheet("color: green; margin-right: 10px;")
        header_layout.addWidget(self.lbl_user_display)
        main_layout.addLayout(header_layout)

        # --- TABS ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                height: 40px;
                width: 150px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        self.tabs.addTab(self.create_url_tab(), "URL Shortener")
        self.tabs.addTab(self.create_sms_tab(), "SMS Messaging")
        self.tabs.addTab(self.create_fake_tab(), "Fake Data Gen")
        
        main_layout.addWidget(self.tabs)

        # --- FOOTER ---
        footer_layout = QHBoxLayout()
        footer_layout.addStretch() 
        
        btn_logout = QPushButton("Logout")
        btn_logout.setFixedWidth(100) 
        btn_logout.clicked.connect(self.logout)
        footer_layout.addWidget(btn_logout)
        
        main_layout.addLayout(footer_layout)

        self.page_utils.setLayout(main_layout)
        self.stack.addWidget(self.page_utils)

    def update_user_label(self):
        self.lbl_user_display.setText(f"Logged in as: {self.current_user}")

    # --- Feature 1: URL Shortener ---
    def create_url_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(QLabel("Enter Long URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...") 
        layout.addWidget(self.url_input)

        btn_shorten = QPushButton("Shorten URL")
        btn_shorten.clicked.connect(self.run_shortener)
        layout.addWidget(btn_shorten)

        layout.addWidget(QLabel("Shortened Result:"))
        self.url_output = QLineEdit()
        self.url_output.setReadOnly(True)
        layout.addWidget(self.url_output)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def run_shortener(self):
        long_url = self.url_input.text()
        if not long_url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        
        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(long_url)
            self.url_output.setText(short_url)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection Failed: {e}")

    # --- Feature 2: SMS Simulation ---
    def create_sms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(QLabel("Recipient Number:"))
        
        self.sms_num_input = QLineEdit()
        self.sms_num_input.setText("+63") 
        self.sms_num_input.setPlaceholderText("+63...") 
        layout.addWidget(self.sms_num_input)

        layout.addWidget(QLabel("Message:"))
        self.sms_msg_input = QLineEdit() 
        self.sms_msg_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.sms_msg_input)

        btn_send = QPushButton("Send Message")
        btn_send.clicked.connect(self.run_sms)
        layout.addWidget(btn_send)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def run_sms(self):
        number = self.sms_num_input.text()
        msg = self.sms_msg_input.text()

        if len(number) < 4 or not msg:
            QMessageBox.warning(self, "Error", "Please check number and message")
            return

        QMessageBox.information(self, "Success", f"Message sent to {number}!\nStatus: 200 OK")
        self.sms_msg_input.clear()

    # --- Feature 3: Fake Data ---
    def create_fake_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        btn_gen = QPushButton("Generate Identity")
        btn_gen.clicked.connect(self.run_fake_data)
        layout.addWidget(btn_gen)

        self.fake_output = QTextEdit()
        self.fake_output.setReadOnly(True)
        self.fake_output.setFont(QFont("Arial", 12))
        layout.addWidget(self.fake_output)

        tab.setLayout(layout)
        return tab

    def run_fake_data(self):
        name = self.fake.name()
        addr = self.fake.address()
        email = self.fake.email()
        job = self.fake.job()
        
        result = f"Name: {name}\nEmail: {email}\nJob: {job}\nAddress: {addr}"
        self.fake_output.setText(result)

    def logout(self):
        self.current_user = ""
        self.stack.setCurrentIndex(0) 

    # ============================================
    # PART 3: REGISTER SCREEN
    # ============================================
    def create_register_screen(self):
        self.page_register = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Create Account")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("New Username")
        self.reg_user.setFixedWidth(250)
        layout.addWidget(self.reg_user, alignment=Qt.AlignmentFlag.AlignCenter)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("New Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.setFixedWidth(250)
        layout.addWidget(self.reg_pass, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(10)

        btn_submit = QPushButton("Register")
        btn_submit.setFixedWidth(150)
        btn_submit.clicked.connect(self.register_user)
        layout.addWidget(btn_submit, alignment=Qt.AlignmentFlag.AlignCenter)

        # Back button
        btn_back = QPushButton("Back to Login")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page_register.setLayout(layout)
        self.stack.addWidget(self.page_register)

    def register_user(self):
        user = self.reg_user.text()
        pw = self.reg_pass.text()

        if not user or not pw:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        # Hash Password
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed_pw))
            conn.commit()
            
            # --- FIXED LINE BELOW ---
            # Changed from QMessageBox.showinfo to QMessageBox.information
            QMessageBox.information(self, "Success", "Account Created! You can now login.")
            
            self.stack.setCurrentIndex(0) # Go back to login
            self.reg_user.clear()
            self.reg_pass.clear()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")
        finally:
            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())