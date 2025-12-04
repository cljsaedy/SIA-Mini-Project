import pyshorteners
import csv 
import os 
import datetime
from faker import Faker
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, 
                             QTabWidget, QTextEdit, QApplication)
from PyQt6.QtCore import Qt, QTimer

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
        main_layout.setContentsMargins(40, 40, 40, 40) 

        # header
        header_layout = QHBoxLayout()
        header_layout.addStretch() 
        self.lbl_user = QLabel(f"Hello, {self.current_user}")
        self.lbl_user.setStyleSheet("color: #00a8ff; font-weight: 800; font-size: 18px;")
        header_layout.addWidget(self.lbl_user)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(20)

        # tabs styling
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #353b48;
                background: #1e272e; 
                border-radius: 15px;
            }
            QTabBar::tab {
                background: #2f3640;
                color: #dcdde1;
                padding: 12px 25px;
                border-radius: 20px; 
                font-weight: 600;
                margin-right: 10px;
                margin-bottom: 10px;
                border: 1px solid #353b48;
            }
            QTabBar::tab:selected {
                background: #00a8ff; 
                color: white;
                border: 1px solid #00a8ff;
            }
            QTabBar::tab:hover {
                background: #353b48;
            }
            QTabBar:focus { outline: none; }
        """)
        
        self.tabs.addTab(self.create_url_tab(), "Link Shortener")
        self.tabs.addTab(self.create_sms_tab(), "SMS Messaging")
        self.tabs.addTab(self.create_fake_tab(), "Identity Generator")
        main_layout.addWidget(self.tabs)

        # footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch() 
        btn_logout = QPushButton("Sign Out")
        btn_logout.setFixedWidth(120) 
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton { 
                background-color: #e84118; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; 
                font-weight: bold; 
                outline: 0;
            }
            QPushButton:hover { background-color: #c23616; }
        """)
        btn_logout.clicked.connect(self.logout_callback) 
        footer_layout.addWidget(btn_logout)
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    # url shortener
    def create_url_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)

        lbl = QLabel("Paste your long URL here:")
        lbl.setStyleSheet("font-weight: bold; color: #f5f6fa; font-size: 16px;")
        layout.addWidget(lbl)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("[https://example.com/very-long-link](https://example.com/very-long-link)") 
        self.url_input.setStyleSheet("""
            padding: 14px; border: 2px solid #353b48; border-radius: 10px; color: #f5f6fa; font-size: 14px; background: #2f3640;
        """)
        layout.addWidget(self.url_input)

        btn_shorten = QPushButton("Shorten Link")
        btn_shorten.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_shorten.setStyleSheet("""
            QPushButton { background-color: #4cd137; color: white; padding: 12px; border-radius: 10px; font-weight: bold; outline: 0; font-size: 14px;}
            QPushButton:hover { background-color: #44bd32; }
        """)
        btn_shorten.clicked.connect(self.run_shortener)
        layout.addWidget(btn_shorten)

        layout.addSpacing(20)
        lbl_res = QLabel("Result:")
        lbl_res.setStyleSheet("color: #dcdde1;")
        layout.addWidget(lbl_res)
        
        result_layout = QHBoxLayout()
        self.url_output = QLineEdit()
        self.url_output.setReadOnly(True)
        self.url_output.setStyleSheet("background-color: #2f3640; border: 2px solid #353b48; border-radius: 10px; padding: 12px; color: #00a8ff; font-weight: bold;")
        result_layout.addWidget(self.url_output)

        self.btn_copy = QPushButton("Copy")
        self.btn_copy.setFixedWidth(90)
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn_style_normal = """
            QPushButton { background-color: #718093; color: white; padding: 12px; border-radius: 10px; font-weight: bold; outline: 0;}
            QPushButton:hover { background-color: #7f8fa6; }
        """
        self.btn_copy.setStyleSheet(self.copy_btn_style_normal)
        self.btn_copy.clicked.connect(self.action_copy_text)
        result_layout.addWidget(self.btn_copy)

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

    def action_copy_text(self):
        text = self.url_output.text()
        if text:
            QApplication.clipboard().setText(text)
            self.btn_copy.setText("Copied!")
            self.btn_copy.setStyleSheet("""
                QPushButton { background-color: #4cd137; color: white; padding: 12px; border-radius: 10px; font-weight: bold; outline: 0;}
            """)
            QTimer.singleShot(2000, self.reset_copy_btn)

    def reset_copy_btn(self):
        self.btn_copy.setText("Copy")
        self.btn_copy.setStyleSheet(self.copy_btn_style_normal)

    # sms messaging (logging simulation)
    def create_sms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)

        lbl1 = QLabel("Recipient Number:")
        lbl1.setStyleSheet("color: #dcdde1;")
        layout.addWidget(lbl1)
        
        self.sms_num_input = QLineEdit()
        self.sms_num_input.setText("+63") 
        self.sms_num_input.setStyleSheet("""
            padding: 14px; border: 2px solid #353b48; border-radius: 10px; color: #f5f6fa; font-size: 14px; background: #2f3640;
        """)
        layout.addWidget(self.sms_num_input)

        lbl2 = QLabel("Message Body:")
        lbl2.setStyleSheet("color: #dcdde1;")
        layout.addWidget(lbl2)
        
        self.sms_msg_input = QLineEdit() 
        self.sms_msg_input.setPlaceholderText("Type your message here...")
        self.sms_msg_input.setStyleSheet("""
            padding: 14px; border: 2px solid #353b48; border-radius: 10px; color: #f5f6fa; font-size: 14px; background: #2f3640;
        """)
        layout.addWidget(self.sms_msg_input)

        btn_send = QPushButton("Send Message")
        btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        # Soft Orange
        btn_send.setStyleSheet("""
            QPushButton { background-color: #e1b12c; color: white; padding: 12px; border-radius: 10px; font-weight: bold; outline: 0; font-size: 14px;}
            QPushButton:hover { background-color: #fbc531; }
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
            QPushButton { background-color: #9c88ff; color: white; padding: 12px; border-radius: 10px; font-weight: bold; outline: 0;}
            QPushButton:hover { background-color: #8c7ae6; }
        """)
        btn_gen.clicked.connect(self.run_fake_data)
        btn_layout.addWidget(btn_gen)

        btn_save = QPushButton("Save to CSV")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton { background-color: #00a8ff; color: white; padding: 12px; border-radius: 10px; font-weight: bold; outline: 0;}
            QPushButton:hover { background-color: #0097e6; }
        """)
        btn_save.clicked.connect(self.save_to_csv)
        btn_layout.addWidget(btn_save)

        layout.addLayout(btn_layout)

        self.fake_output = QTextEdit()
        self.fake_output.setReadOnly(True)
        self.fake_output.setStyleSheet("background-color: #2f3640; border: 2px solid #353b48; border-radius: 10px; padding: 12px; font-size: 14px; color: #f5f6fa;")
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
        try:
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                fieldnames = ['Name', 'Email', 'Job', 'Address']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader() 
                writer.writerows(self.session_data)
            QMessageBox.information(self, "Saved", f"Successfully saved identities to {CSV_FILE}")
            self.session_data.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")