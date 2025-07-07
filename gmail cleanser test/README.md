# ✉️ Gmail Cleanser Tool

A Python script to help you clean up your Gmail inbox by:
✅ Logging into your Gmail account
✅ Finding specific types of emails (e.g., promotions, ads, unread, older than 30 days)
✅ Automatically archiving, deleting, or marking emails as read
✅ Setting custom rules (e.g., filter by sender, keywords, or date)

Perfect for personal inbox cleanup and simple email automation.

---

## ✨ What You’ll Need

To make this AI agent work, you will need:

✅ **Basic Requirements**  
- A Google account (Gmail)  
- Gmail API access enabled  
- A Python environment (locally or on a platform like Replit or Google Colab)  
- A Google OAuth credentials file (`credentials.json`)  

---

## ⚙️ Setup Instructions

### 1. Create a New Project in Google Cloud Console

#### 1️⃣ Go to the [Google Cloud Console](https://console.cloud.google.com/).
1. Make sure you are logged in with your Google account.
2. Create a new project (for example "Gmail Cleaner").

#### 2️⃣ Create a New Project
You can create a new project in Google Cloud Console by either method:

**Method 1: Using the Top Bar**  
- Click on the current project name near the top-left corner (e.g., “My First Project”).  
- In the popup **Project Picker**, click **“New Project”** at the top-right.

**Method 2: Using the Sidebar**  
- Click the **menu icon** (☰) at the top-left corner.  
- Navigate to **IAM & Admin → All Projects**.  
- Click the **“New Project”** button.

Fill in the project name and other details, then click **Create**.

#### 3️⃣ Fill in Project Details

On the **New Project** page, fill out the fields as follows:

| Field          | Description                                  |
| -------------- | -------------------------------------------- |
| Project Name   | Choose any name, e.g., **Gmail Cleaner**     |
| Organization   | Leave empty or default if you don’t have one |
| Location       | Automatically generated, no action needed    |

Then, click the **Create** button at the bottom of the page.

#### 4️⃣ Wait for Project Creation

You will see a notification at the top-right saying "Creating project…".  
Wait a few seconds until the project is created successfully.

Then, make sure the newly created project (e.g., **Gmail Cleaner**) is selected as the active project.  
If not, click the project selector at the top-left to switch to it.

### 2. Enable Gmail API

1. In the left sidebar, click **APIs & Services** → then click **Library**.  
2. In the search bar at the top, type: `Gmail API`  
3. Click on **Gmail API** from the search results.  
4. Click the **Enable** button.

✅ Done! The Gmail API is now enabled for your project.

### 3. Create and Configure OAuth Credentials (`credentials.json`)
Now, let’s create the credentials your script will use to access your Gmail.

📌 Step-by-Step: Create OAuth 2.0 Client ID

1. In the left sidebar, go to **APIs & Services → Credentials**.  
2. Click the **+ CREATE CREDENTIALS** button at the top.  
3. Choose **OAuth client ID**.

You may be asked to configure the OAuth consent screen first (only once per project):

1. Choose **External** → Click **Create**.  
2. Fill in the **App name** (e.g., "Gmail Cleaner").  
3. Fill in **User support email** (your email).  
4. Scroll down to **Developer contact information**, enter your email.  
5. Click **Save and Continue** (you can skip the scopes and test users for now).  
6. Finish by clicking **Back to Dashboard** if prompted.
7. Create **OAuth client ID** (Application type: Select **Desktop app**, Name: For example: Gmail Cleaner App)
8. Download Your `credentials.json` file. (Move this file to the same folder as your Python script.)

You now have:  
- Gmail API enabled for your project  
- OAuth 2.0 credentials saved as `credentials.json`  

#### Put `credentials.json` files in One Folder
Organize your files inside a folder, for example, `gmail cleanser test/`:

```bash
gmail cleanser test/
├── gmail_cleaner.py         # the Python script  
├── credentials.json       # your OAuth file downloaded from Google  
├── token.json               # Auto-generated after first authentication
└── README.md                # This file
```

> *Note: The `token.json` file will be created automatically after you run the script and complete the authorization process for the first time.*

### 4. Ready to run the Python code!

#### 1️⃣ Install Required Python Libraries

Open your terminal (Command Prompt, PowerShell, or Terminal on Mac/Linux), and run:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
This installs the required libraries for Gmail API access.

#### 2️⃣ Run the Script

1. Open your terminal and navigate to the folder you created:

```bash
cd path/to/gmail_cleaner
```

2. Run the script:
```bash
python gmail_cleaner.py
```

The first time you run it:
A browser window will open asking you to log in to your Google account.


### ✅ Fixing "Access blocked" OAuth Error

If you see the warning "Access blocked: Gmail Cleaner has not completed the Google verification process," add yourself as a test user by following these steps:

#### 1️⃣ Go to the OAuth Consent Screen Settings

Open the following link:  
👉 [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)

Make sure you're in your **Gmail Cleaner** project.

#### 2️⃣ Add Yourself as a Test User
- Scroll down to the **Test Users** section  
- Click **“Add Users”**  
- Enter your email address
- Click **Save**

✅ You can add multiple emails if you want others to test the app too.

#### 3️⃣ Run the Script Again

```bash
python gmail_cleaner.py
```

This time, when the browser opens and you log in, it should work, since you're now an approved test user.

Once done, a file named **token.json** will be saved locally.
This file allows the script to reuse your credentials without requiring you to log in every time.

---

## 📂 Files in This Folder
```bash
gmail cleanser test/
├── gmail_cleaner.py         # Main script
├── credentials.json       # Google API credentials (you provide)
├── token.json               # Auto-generated after first auth
└── README.md                # This file
```

---

## ✅ Example Use Case
- Delete all emails from a newsletter sender:  
  ```text
  Keyword: "example@newsletter.com"
  ```
- Delete emails with subject "Daily Report":  
  ```text
  Keyword: "subject:Daily Report"
  ```
You can customize filters inside the script by editing the query string.

---

## 🔒 Notes
This script uses OAuth and stores a local token.json to remember your Gmail session.
Your credentials are never shared and only used locally.

---

## 📄 License
This tool is provided for personal use only.
Do not use it to automate spam, phishing, or violate Gmail’s Terms of Service.
