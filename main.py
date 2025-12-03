import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import database 
from utilities import UtilityScreen

# styling
STYLESHEET = """
    /* Main Background */
    QMainWindow {
        background-color: #f4f7f6; 
    }
    QWidget {
        font-size: 14px;
        color: #333333;
    }

    /* The White Cards (Login/Register Box) */
    QFrame#LoginCard {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }

    /* Input Fields */
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 6px;
        padding: 10px;
        color: #495057;
    }
    QLineEdit:focus {
        border: 1px solid #4a90e2; 
        background-color: #fff;
    }

    /* Headings */
    QLabel#Header {
        font-size: 26px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: -15px; 
        padding-bottom: 0px;
    }
    QLabel#SubHeader {
        font-size: 14px;
        color: #7f8c8d;
        margin-top: -5px;    
        padding-top: 0px;
    }

    /* Buttons */
    QPushButton {
        border-radius: 6px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
        border: none;
        outline: 0; 
    }
    QPushButton:focus {
        outline: none;
    }
"""

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIA Utilities")
        self.setFixedSize(900, 700) 
        
        self.icon_path = os.path.join('styles', 'icon.png')

        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path)) 
        else:
            print(f"Warning: {self.icon_path} not found.")

        self.setStyleSheet(STYLESHEET)

        database.initialize_db()

        self.current_user = "" 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.stack = QStackedWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.stack)

        self.create_login_screen()      
        self.create_register_screen()   

        self.stack.setCurrentIndex(0)
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # login
    def create_login_screen(self):
        self.page_login = QWidget()
        
        page_layout = QVBoxLayout()
        page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("LoginCard") 
        card.setFixedSize(400, 450)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(0) 
        card_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("SIA Mini Project") 
        title.setObjectName("Header")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Utility Tools") 
        subtitle.setObjectName("SubHeader")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(35)

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Username")
        card_layout.addWidget(self.input_user)

        card_layout.addSpacing(15)

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Password")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password) 
        card_layout.addWidget(self.input_pass)

        card_layout.addSpacing(25)

        btn_login = QPushButton("Login")
        btn_login.setStyleSheet("""
            QPushButton { background-color: #4a90e2; color: white; outline: 0; }
            QPushButton:hover { background-color: #357abd; }
        """)
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self.process_login)
        card_layout.addWidget(btn_login)

        card_layout.addSpacing(10)

        btn_register = QPushButton("Create New Account")
        btn_register.setStyleSheet("""
            QPushButton { background-color: transparent; color: #4a90e2; border: 1px solid #e0e0e0; outline: 0; }
            QPushButton:hover { background-color: #f8f9fa; }
        """)
        btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_register.clicked.connect(lambda: self.stack.setCurrentIndex(1)) 
        card_layout.addWidget(btn_register)

        page_layout.addWidget(card)
        self.page_login.setLayout(page_layout)
        self.stack.addWidget(self.page_login)

    def process_login(self):
        user = self.input_user.text()
        pw = self.input_pass.text()

        if database.check_credentials(user, pw):
            self.current_user = user
            self.input_user.clear()
            self.input_pass.clear()
            
            self.utility_screen = UtilityScreen(self.handle_logout, self.current_user)
            self.stack.addWidget(self.utility_screen) 
            self.stack.setCurrentWidget(self.utility_screen)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Username or Password")

    def handle_logout(self):
        self.current_user = ""
        self.stack.removeWidget(self.utility_screen)
        self.utility_screen.deleteLater()
        self.utility_screen = None
        self.stack.setCurrentIndex(0)

    # register
    def create_register_screen(self):
        self.page_register = QWidget()
        page_layout = QVBoxLayout()
        page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("LoginCard")
        card.setFixedSize(400, 520)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(0) 
        card_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Create Account")
        title.setObjectName("Header")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(30)

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("New Username")
        card_layout.addWidget(self.reg_user)

        card_layout.addSpacing(15)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("New Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.reg_pass)

        card_layout.addSpacing(25)

        btn_submit = QPushButton("Sign Up")
        btn_submit.setStyleSheet("""
            QPushButton { background-color: #2ecc71; color: white; outline: 0; }
            QPushButton:hover { background-color: #27ae60; }
        """)
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.clicked.connect(self.process_register)
        card_layout.addWidget(btn_submit)

        card_layout.addSpacing(10)

        btn_back = QPushButton("Back to Login")
        btn_back.setStyleSheet("""
            QPushButton { background-color: transparent; color: #7f8c8d; outline: 0; }
            QPushButton:hover { color: #333; }
        """)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        card_layout.addWidget(btn_back)

        page_layout.addWidget(card)
        self.page_register.setLayout(page_layout)
        self.stack.addWidget(self.page_register)

    def process_register(self):
        user = self.reg_user.text()
        pw = self.reg_pass.text()

        if not user or not pw:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        if len(pw) < 8:
            QMessageBox.warning(self, "Weak Password", "Password must be at least 8 characters long.")
            return

        if database.add_new_user(user, pw):
            QMessageBox.information(self, "Success", "Account Created! You can now login.")
            self.stack.setCurrentIndex(0)
            self.reg_user.clear()
            self.reg_pass.clear()
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())