# SIA-Mini-Project
A Python desktop utility application developed for System Integration and Architecture (SIA).

The application combines several utility functions into a single PyQt6-based desktop interface, including user authentication, URL shortening, SMS message logging, and identity generation with CSV export.

Features
🔐 User Authentication
User registration and login
SQLite database for user accounts
Password hashing
Password visibility toggle
Basic password validation
🔗 URL Shortener
Accepts long URLs
Uses TinyURL through pyshorteners
Displays the shortened URL
Copy shortened URL to clipboard
📱 SMS Messaging
Enter a recipient number and message
Validates basic input requirements
Records messages with timestamps
Saves SMS activity to sms_logs.txt

Note: The SMS feature currently uses local logging and does not send messages through an SMS API.

🪪 Identity Generator
Generates sample identity information using Faker
Generates names, email addresses, jobs, and addresses
Displays generated identities in the application
Saves generated data to CSV
Technologies Used
Python
PyQt6 — desktop GUI
SQLite — user account database
Faker — sample identity generation
pyshorteners — URL shortening through TinyURL
CSV / TXT — local data storage and logging
Screenshots
Login




URL Shortener




SMS Messaging




Identity Generator




Note: The screenshot paths above are placeholders. We will set up the actual image files in the repository before this README is finalized.

Project Structure
SIA-Mini-Project/
├── main.py
├── database.py
├── setup_db.py
├── utilities.py
├── requirements.txt
├── styles/
└── README.md
Project Context

This project was developed as an individual academic project for System Integration and Architecture (SIA).

The project focuses on integrating multiple utilities and supporting components into a single desktop application.

Status:
Completed academic project.
