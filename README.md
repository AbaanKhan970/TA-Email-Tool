# 📬 Gmail Email Clustering Tool (AI-Powered for TAs)

This project is a **smart, browser-based tool** that fetches emails from your Gmail inbox, analyzes the content using machine learning, and clusters them into similar groups with keyword summaries and sender information.

---

### 🎯 Why This Project?

As a Teaching Assistant, I was receiving many student emails about similar topics — like circuit simulation errors, MOSFET theory, or lab clarifications. Instead of manually reading each email, I wanted to:
- Automatically group similar questions  
- Identify frequently asked topics  
- Prepare better review sessions

This tool solves that by using **KMeans clustering**, **TF-IDF**, and a clean **Streamlit UI** to make it intuitive and effective.

---

## 🚀 Features

- 🔐 Login with your Gmail email + app password  
- 🔎 Filter emails by subject keyword (e.g., "2EI4", "project", "help")  
- 📊 Cluster emails using machine learning (KMeans + TF-IDF)  
- 🧠 Shows top keywords per cluster  
- 👤 Displays sender name/email for every message  
- 🌐 Streamlit UI – no terminal needed  

---

## 🖥️ Demo Preview

![image](https://github.com/user-attachments/assets/b2b8f93f-3e67-4583-b347-585dbbf3ed4a)

---

## ⚙️ How to Use

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR-USERNAME/email-clustering-tool.git
cd email-clustering-t
```


### 2. Install Required Libraries
```bash
pip install streamlit scikit-learn
```

### 3. Run the App
```bash
streamlit run ta_email_tool.py
```

### 4. Gmail Setup (App Password Required)

Because Gmail blocks less secure apps, you need to use an App Password:

1)Go to https://myaccount.google.com/security

2)Enable 2-Step Verification

3)Visit https://myaccount.google.com/apppasswords

4)Generate a 16-character password for “Mail” > “Other”

5)Use this password in the app (instead of your real password)

---
### 📚 Tech Stack

Python 3

Streamlit

scikit-learn

TF-IDF Vectorizer

KMeans Clustering

IMAP (via Python's imaplib)

email (built-in parsing)

