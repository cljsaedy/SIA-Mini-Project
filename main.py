import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QFrame, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QFontDatabase, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
import database 
from utilities import UtilityScreen

# styling (dark theme)
STYLESHEET = """
    /* Main Background - Dark Gradient */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #2b5876, stop:1 #4e4376);
    }
    QWidget {
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #ecf0f1;
    }

    /* The Cards (Dark Glass Effect) */
    QFrame#LoginCard {
        background-color: #1e272e;
        border-radius: 20px;
        border: 1px solid #353b48;
    }

    /* Input Fields */
    QLineEdit {
        background-color: #2f3640;
        border: 2px solid #353b48;
        border-radius: 10px;
        padding: 12px;
        color: #f5f6fa;
        selection-background-color: #00a8ff;
    }
    QLineEdit:focus {
        border: 2px solid #00a8ff; 
        background-color: #353b48;
    }

    /* Headings */
    QLabel#Header {
        font-size: 28px;
        font-weight: 800;
        color: #f5f6fa;
        margin-bottom: -10px;
    }
    QLabel#SubHeader {
        font-size: 15px;
        color: #dcdde1;
        font-weight: 500;
    }

    /* Buttons */
    QPushButton {
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
        font-size: 15px;
        border: none;
        outline: 0; 
    }
    QPushButton:focus {
        outline: none;
    }
    
    /* Checkbox Styling */
    QCheckBox { color: #dcdde1; font-size: 13px; font-weight: 600; spacing: 8px;}
    QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #7f8fa6; border-radius: 4px; background: #2f3640;}
    QCheckBox::indicator:checked { background-color: #00a8ff; border: 2px solid #00a8ff; }
"""

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIA Utilities")
        self.setFixedSize(950, 750) 
        
        self.icon_path = os.path.join('styles', 'icon.png')
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path)) 

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

    def add_shadow(self, target_widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 100)) 
        target_widget.setGraphicsEffect(shadow)

    # login
    def create_login_screen(self):
        self.page_login = QWidget()
        page_layout = QVBoxLayout()
        page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("LoginCard") 
        card.setFixedSize(420, 520) 
        self.add_shadow(card)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(0)
        card_layout.setContentsMargins(50, 50, 50, 50)

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
        self.input_pass.returnPressed.connect(self.process_login)
        card_layout.addWidget(self.input_pass)

        card_layout.addSpacing(10)
        self.check_show_pass_login = QCheckBox("Show Password")
        self.check_show_pass_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_show_pass_login.toggled.connect(lambda checked: self.toggle_password(checked, self.input_pass))
        card_layout.addWidget(self.check_show_pass_login)

        card_layout.addSpacing(20)

        btn_login = QPushButton("Login to Dashboard")
        btn_login.setStyleSheet("""
            QPushButton { background-color: #00a8ff; color: white; }
            QPushButton:hover { background-color: #0097e6; margin-top: 2px; }
        """)
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self.process_login)
        card_layout.addWidget(btn_login)

        card_layout.addSpacing(15)

        btn_register = QPushButton("Create New Account")
        btn_register.setStyleSheet("""
            QPushButton { background-color: transparent; color: #dcdde1; border: 2px solid #718093; }
            QPushButton:hover { background-color: #718093; color: white; }
        """)
        btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_register.clicked.connect(lambda: self.stack.setCurrentIndex(1)) 
        card_layout.addWidget(btn_register)

        page_layout.addWidget(card)
        self.page_login.setLayout(page_layout)
        self.stack.addWidget(self.page_login)

    # register
    def create_register_screen(self):
        self.page_register = QWidget()
        page_layout = QVBoxLayout()
        page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("LoginCard")
        card.setFixedSize(420, 540)
        self.add_shadow(card)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(0) 
        card_layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Create Account")
        title.setObjectName("Header")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(35)

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Choose Username")
        card_layout.addWidget(self.reg_user)

        card_layout.addSpacing(15)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Choose Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.returnPressed.connect(self.process_register)
        card_layout.addWidget(self.reg_pass)

        card_layout.addSpacing(10)
        self.check_show_pass_reg = QCheckBox("Show Password")
        self.check_show_pass_reg.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_show_pass_reg.toggled.connect(lambda checked: self.toggle_password(checked, self.reg_pass))
        card_layout.addWidget(self.check_show_pass_reg)


        card_layout.addSpacing(20)

        btn_submit = QPushButton("Sign Up")
        btn_submit.setStyleSheet("""
            QPushButton { background-color: #4cd137; color: white; }
            QPushButton:hover { background-color: #44bd32; margin-top: 2px; }
        """)
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.clicked.connect(self.process_register)
        card_layout.addWidget(btn_submit)

        card_layout.addSpacing(15)

        btn_back = QPushButton("Back to Login")
        btn_back.setStyleSheet("""
            QPushButton { background-color: transparent; color: #7f8fa6; }
            QPushButton:hover { color: #f5f6fa; }
        """)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        card_layout.addWidget(btn_back)

        page_layout.addWidget(card)
        self.page_register.setLayout(page_layout)
        self.stack.addWidget(self.page_register)

    # show pass
    def toggle_password(self, checked, line_edit):
        if checked:
            line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def process_login(self):
        user = self.input_user.text()
        pw = self.input_pass.text()

        if database.check_credentials(user, pw):
            self.current_user = user
            self.input_user.clear()
            self.input_pass.clear()
            self.check_show_pass_login.setChecked(False)
            
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
            self.check_show_pass_reg.setChecked(False)
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())