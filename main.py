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

DB_NAME = 'users.db'

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIA Mini Project")
        self.setFixedSize(700, 600) 

        # faker
        self.fake = Faker()
        self.current_user = "" 

        # center
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # stacked layout
        self.stack = QStackedWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.stack)

        # tabs
        self.create_login_screen()   
        self.create_utility_screen() 
        self.create_register_screen() 

        # login screen prio
        self.stack.setCurrentIndex(0)

        # center window
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # login screen
    def create_login_screen(self):
        self.page_login = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        # input styling
        input_style = "padding: 8px; border: 1px solid #ccc; border-radius: 4px;"

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Username")
        self.input_user.setFixedWidth(250)
        self.input_user.setStyleSheet(input_style) 
        layout.addWidget(self.input_user, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Password")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password) 
        self.input_pass.setFixedWidth(250)
        self.input_pass.setStyleSheet(input_style) 
        layout.addWidget(self.input_pass, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(10) 

        # login button
        btn_login = QPushButton("Login")
        btn_login.setFixedWidth(150)
        btn_login.setStyleSheet("""
            background-color: #0d6efd; 
            color: white; 
            font-weight: bold; 
            padding: 8px; 
            border-radius: 4px;
            outline: 0px;
        """)
        btn_login.clicked.connect(self.verify_login)
        layout.addWidget(btn_login, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(5) 

        # register
        btn_register = QPushButton("Create Account")
        btn_register.setFixedWidth(150)
        btn_register.setStyleSheet("""
            background-color: #198754; 
            color: white; 
            font-weight: bold; 
            padding: 8px; 
            border-radius: 4px;
            outline: 0px;
        """)
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

    # main screen
    def create_utility_screen(self):
        self.page_utils = QWidget()
        main_layout = QVBoxLayout()

        # header
        header_layout = QHBoxLayout()
        header_layout.addStretch() 
        self.lbl_user_display = QLabel("User: ???")
        self.lbl_user_display.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.lbl_user_display.setStyleSheet("color: #198754; margin-right: 15px; font-size: 14px;")
        header_layout.addWidget(self.lbl_user_display)
        main_layout.addLayout(header_layout)

        # tabs 
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                height: 40px;
                width: 150px;
                font-size: 14px;
                font-weight: bold;
                background: #e9ecef;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                outline: 0px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom: 2px solid #0d6efd;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabBar:focus {
                outline: none;
            }
        """)
        
        self.tabs.addTab(self.create_url_tab(), "URL Shortener")
        self.tabs.addTab(self.create_sms_tab(), "SMS Messaging")
        self.tabs.addTab(self.create_fake_tab(), "Fake Data Generator")
        
        main_layout.addWidget(self.tabs)

        # footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch() 
        
        btn_logout = QPushButton("Logout")
        btn_logout.setFixedWidth(100) 
        btn_logout.setStyleSheet("""
            background-color: #dc3545; 
            color: white; 
            font-weight: bold; 
            padding: 8px; 
            border-radius: 4px;
            outline: 0px;
        """)
        btn_logout.clicked.connect(self.logout)
        footer_layout.addWidget(btn_logout)
        
        main_layout.addLayout(footer_layout)

        self.page_utils.setLayout(main_layout)
        self.stack.addWidget(self.page_utils)

    def update_user_label(self):
        self.lbl_user_display.setText(f"Logged in as: {self.current_user}")

    # url shortener
    def create_url_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        input_style = "padding: 8px; border: 1px solid #ccc; border-radius: 4px;"

        layout.addWidget(QLabel("Enter Long URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...") 
        self.url_input.setStyleSheet(input_style)
        layout.addWidget(self.url_input)

        btn_shorten = QPushButton("Shorten URL")
        btn_shorten.setStyleSheet("""
            background-color: #198754; 
            color: white; 
            font-weight: bold; 
            padding: 10px; 
            border-radius: 4px;
            margin-top: 10px;
            outline: 0px;
        """)
        btn_shorten.clicked.connect(self.run_shortener)
        layout.addWidget(btn_shorten)

        layout.addWidget(QLabel("Shortened Result:"))
        self.url_output = QLineEdit()
        self.url_output.setReadOnly(True)
        self.url_output.setStyleSheet(input_style + " background-color: #f8f9fa;")
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

    # sms (simulation pa lang)
    def create_sms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        input_style = "padding: 8px; border: 1px solid #ccc; border-radius: 4px;"

        layout.addWidget(QLabel("Recipient Number:"))
        
        self.sms_num_input = QLineEdit()
        self.sms_num_input.setText("+63") 
        self.sms_num_input.setPlaceholderText("+63...") 
        self.sms_num_input.setStyleSheet(input_style)
        layout.addWidget(self.sms_num_input)

        layout.addWidget(QLabel("Message:"))
        self.sms_msg_input = QLineEdit() 
        self.sms_msg_input.setPlaceholderText("Type your message here...")
        self.sms_msg_input.setStyleSheet(input_style)
        layout.addWidget(self.sms_msg_input)

        btn_send = QPushButton("Send Message")
        btn_send.setStyleSheet("""
            background-color: #fd7e14; 
            color: white; 
            font-weight: bold; 
            padding: 10px; 
            border-radius: 4px;
            margin-top: 10px;
            outline: 0px;
        """)
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

        QMessageBox.information(self, "Success", f"Message sent to {number}!\nStatus: OK")
        self.sms_msg_input.clear()

    # fake data
    def create_fake_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        btn_gen = QPushButton("Generate Identity")
        btn_gen.setStyleSheet("""
            background-color: #6f42c1; 
            color: white; 
            font-weight: bold; 
            padding: 10px; 
            border-radius: 4px;
            margin-bottom: 15px;
            outline: 0px;
        """)
        btn_gen.clicked.connect(self.run_fake_data)
        layout.addWidget(btn_gen)

        self.fake_output = QTextEdit()
        self.fake_output.setReadOnly(True)
        self.fake_output.setFont(QFont("Arial", 12))
        self.fake_output.setStyleSheet("border: 1px solid #ccc; border-radius: 4px; background-color: #f8f9fa;")
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

    # register 
    def create_register_screen(self):
        self.page_register = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Create Account")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        input_style = "padding: 8px; border: 1px solid #ccc; border-radius: 4px;"

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("New Username")
        self.reg_user.setFixedWidth(250)
        self.reg_user.setStyleSheet(input_style)
        layout.addWidget(self.reg_user, alignment=Qt.AlignmentFlag.AlignCenter)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("New Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.setFixedWidth(250)
        self.reg_pass.setStyleSheet(input_style)
        layout.addWidget(self.reg_pass, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(10)

        btn_submit = QPushButton("Register")
        btn_submit.setFixedWidth(150)
        btn_submit.setStyleSheet("""
            background-color: #198754; 
            color: white; 
            font-weight: bold; 
            padding: 8px; 
            border-radius: 4px;
            outline: 0px;
        """)
        btn_submit.clicked.connect(self.register_user)
        layout.addWidget(btn_submit, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_back = QPushButton("Back to Login")
        btn_back.setFixedWidth(150)
        btn_back.setStyleSheet("""
            background-color: #6c757d; 
            color: white; 
            font-weight: bold; 
            padding: 8px; 
            border-radius: 4px;
            outline: 0px;
        """)
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

        # hash pw
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed_pw))
            conn.commit()
            
            QMessageBox.information(self, "Success", "Account Created! You can now login.")
            
            self.stack.setCurrentIndex(0) 
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
