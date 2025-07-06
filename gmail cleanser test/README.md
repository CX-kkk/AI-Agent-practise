# ✉️ Gmail Cleanser Tool

A Python script for cleaning up your Gmail inbox by filtering and deleting messages based on specific criteria (e.g., subject keywords, date ranges, or sender). Ideal for personal email cleanup or basic automation tasks.

---

## 📌 Features

- 🔍 Search Gmail emails by keywords or sender
- 🗑️ Delete matching emails in bulk
- 👀 Dry-run mode (preview emails before deleting)
- 🔐 OAuth 2.0 authentication using Google API

---

## ⚙️ Setup Instructions

### 1. Enable Gmail API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the **Gmail API**.
4. Go to **APIs & Services → Credentials**.
5. Create **OAuth client ID** (type: Desktop).
6. Download the `client_secret.json` file.

### 2. Prepare Your Local Environment

1. Place `client_secret.json` in this folder (`gmail cleanser test/`).
2. Install dependencies (if applicable):

```bash
pip install -r requirements.txt
```
If requirements.txt is not provided, install:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


### 🚀 How to Use
1. Run the script:
```bash
python gmail_cleaner.py
```
2. A browser window will open. Log in to your Gmail and authorize access.
3. Follow the on-screen prompts in the terminal to:
- Enter search filters (e.g., keyword, sender)
- Choose between dry-run or delete mode
- Confirm deletion (if not in dry-run)
You can modify the script to change the default filter behavior (e.g., delete all emails older than X days).

### 📂 Files in This Folder
gmail cleanser test/
├── gmail_cleaner.py         # Main script
├── client_secret.json       # Google API credentials (you provide)
├── token.json               # Auto-generated after first auth
└── README.md                # This file


### ✅ Example Use Case
- Delete all emails from a newsletter sender:  
  ```text
  Keyword: "example@newsletter.com"
  ```
- Delete emails with subject "Daily Report":  
  ```text
  Keyword: "subject:Daily Report"
  ```
You can customize filters inside the script by editing the query string.


### 🔒 Notes
This script uses OAuth and stores a local token.json to remember your Gmail session.
Your credentials are never shared and only used locally.


### 📄 License
This tool is provided for personal use only.
Do not use it to automate spam, phishing, or violate Gmail’s Terms of Service.
