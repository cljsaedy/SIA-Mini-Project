import pyshorteners
import csv 
import os 
import datetime
from faker import Faker
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, 
                             QTabWidget, QTextEdit, QApplication)
from PyQt6.QtCore import Qt

CSV_FILE = 'generated_data.csv'
SMS_LOG_FILE = 'sms_logs.txt'

class UtilityScreen(QWidget):
    def __init__(self, logout_callback, current_user):
        super().__init__()
        self.logout_callback = logout_callback
        self.current_user = current_user
        self.fake = Faker()
        
        self.session_data = [] 
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)

        # header
        header_layout = QHBoxLayout()
        header_layout.addStretch() 
        self.lbl_user = QLabel(f"Logged in as: {self.current_user}")
        self.lbl_user.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 15px; font-family: 'Poppins', sans-serif;")
        header_layout.addWidget(self.lbl_user)
        main_layout.addLayout(header_layout)

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                background: white;
                border-radius: 6px;
                top: -1px; 
            }
            QTabBar::tab {
                background: #f4f7f6;
                color: #7f8c8d;
                padding: 12px 25px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
                border: 1px solid transparent;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #4a90e2; 
                border: 1px solid #e0e0e0;
                border-bottom: 1px solid white; 
            }
            QTabBar::tab:hover {
                background: #e9ecef;
            }
            QTabBar:focus { outline: none; }
        """)
        
        self.tabs.addTab(self.create_url_tab(), "URL Shortener")
        self.tabs.addTab(self.create_sms_tab(), "SMS Messaging")
        self.tabs.addTab(self.create_fake_tab(), "Fake Data Generator")
        main_layout.addWidget(self.tabs)

        # footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch() 
        btn_logout = QPushButton("Logout")
        btn_logout.setFixedWidth(120) 
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton { 
                background-color: #ff6b6b; 
                color: white; 
                border-radius: 6px; 
                padding: 10px; 
                font-weight: bold; 
                font-family: 'Poppins', sans-serif;
                outline: 0;
            }
            QPushButton:hover { background-color: #fa5252; }
        """)
        btn_logout.clicked.connect(self.logout_callback) 
        footer_layout.addWidget(btn_logout)
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    # url shortener
    def create_url_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(15)

        lbl = QLabel("Enter Long URL:")
        lbl.setStyleSheet("font-weight: bold; color: #2c3e50; font-family: 'Poppins', sans-serif;")
        layout.addWidget(lbl)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com/very-long-link") 
        self.url_input.setStyleSheet("""
            padding: 10px; border: 1px solid #ced4da; border-radius: 6px; color: #495057; font-family: 'Poppins', sans-serif;
        """)
        layout.addWidget(self.url_input)

        btn_shorten = QPushButton("Shorten URL")
        btn_shorten.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_shorten.setStyleSheet("""
            QPushButton { background-color: #2ecc71; color: white; padding: 10px; border-radius: 6px; font-weight: bold; outline: 0; font-family: 'Poppins', sans-serif;}
            QPushButton:hover { background-color: #27ae60; }
        """)
        btn_shorten.clicked.connect(self.run_shortener)
        layout.addWidget(btn_shorten)

        layout.addWidget(QLabel("Shortened Result:"))
        
        result_layout = QHBoxLayout()
        self.url_output = QLineEdit()
        self.url_output.setReadOnly(True)
        self.url_output.setStyleSheet("background-color: #f8f9fa; border: 1px solid #ced4da; border-radius: 6px; padding: 10px; color: #4a90e2; font-weight: bold; font-family: 'Poppins', sans-serif;")
        result_layout.addWidget(self.url_output)

        btn_copy = QPushButton("Copy")
        btn_copy.setFixedWidth(80)
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.setStyleSheet("""
            QPushButton { background-color: #95a5a6; color: white; padding: 10px; border-radius: 6px; font-weight: bold; outline: 0; font-family: 'Poppins', sans-serif;}
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        btn_copy.clicked.connect(lambda: QApplication.clipboard().setText(self.url_output.text()))
        result_layout.addWidget(btn_copy)

        layout.addLayout(result_layout)
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

    # sms messaging
    def create_sms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(15)

        layout.addWidget(QLabel("Recipient Number:"))
        self.sms_num_input = QLineEdit()
        self.sms_num_input.setText("+63") 
        self.sms_num_input.setStyleSheet("""
            padding: 10px; border: 1px solid #ced4da; border-radius: 6px; color: #495057; font-family: 'Poppins', sans-serif;
        """)
        layout.addWidget(self.sms_num_input)

        layout.addWidget(QLabel("Message:"))
        self.sms_msg_input = QLineEdit() 
        self.sms_msg_input.setPlaceholderText("Type your message here...")
        self.sms_msg_input.setStyleSheet("""
            padding: 10px; border: 1px solid #ced4da; border-radius: 6px; color: #495057; font-family: 'Poppins', sans-serif;
        """)
        layout.addWidget(self.sms_msg_input)

        btn_send = QPushButton("Send Message")
        btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_send.setStyleSheet("""
            QPushButton { background-color: #f39c12; color: white; padding: 10px; border-radius: 6px; font-weight: bold; outline: 0; font-family: 'Poppins', sans-serif;}
            QPushButton:hover { background-color: #e67e22; }
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

        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] TO: {number} | MSG: {msg}\n"
            with open(SMS_LOG_FILE, "a") as f:
                f.write(log_entry)
            QMessageBox.information(self, "Success", f"Message processed and logged to {SMS_LOG_FILE}")
            self.sms_msg_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save log: {e}")

    # fake data generator
    def create_fake_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(15)
        
        btn_layout = QHBoxLayout()

        btn_gen = QPushButton("Generate Identity")
        btn_gen.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_gen.setStyleSheet("""
            QPushButton { background-color: #9b59b6; color: white; padding: 10px; border-radius: 6px; font-weight: bold; outline: 0; font-family: 'Poppins', sans-serif;}
            QPushButton:hover { background-color: #8e44ad; }
        """)
        btn_gen.clicked.connect(self.run_fake_data)
        btn_layout.addWidget(btn_gen)

        btn_save = QPushButton("Save to CSV")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; padding: 10px; border-radius: 6px; font-weight: bold; outline: 0; font-family: 'Poppins', sans-serif;}
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_save.clicked.connect(self.save_to_csv)
        btn_layout.addWidget(btn_save)

        layout.addLayout(btn_layout)

        self.fake_output = QTextEdit()
        self.fake_output.setReadOnly(True)
        self.fake_output.setStyleSheet("background-color: #f8f9fa; border: 1px solid #ced4da; border-radius: 6px; padding: 10px; font-size: 14px; font-family: 'Poppins', sans-serif;")
        layout.addWidget(self.fake_output)
        
        tab.setLayout(layout)
        return tab

    def run_fake_data(self):
        name = self.fake.name()
        addr = self.fake.address()
        email = self.fake.email()
        job = self.fake.job()
        
        current_person_data = {
            "Name": name,
            "Email": email,
            "Job": job,
            "Address": addr.replace("\n", ", ")
        }
        
        self.session_data.append(current_person_data)

        new_entry = f"Name: {name}\nEmail: {email}\nJob: {job}\nAddress: {addr}"
        
        current_text = self.fake_output.toPlainText()
        if current_text:
            updated_text = new_entry + "\n" + ("-" * 40) + "\n" + current_text
        else:
            updated_text = new_entry
        self.fake_output.setText(updated_text)

    def save_to_csv(self):
        if not self.session_data:
            QMessageBox.warning(self, "Error", "No new data to save!")
            return
            
        file_exists = os.path.isfile(CSV_FILE)
        count = len(self.session_data)

        try:
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                fieldnames = ['Name', 'Email', 'Job', 'Address']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader() 
                
                writer.writerows(self.session_data)
                
            QMessageBox.information(self, "Saved", f"Successfully saved {count} identities to {CSV_FILE}")
            
            self.session_data.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")