import streamlit as st
import imaplib
import email
from email.header import decode_header
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

IMAP_SERVER = "imap.gmail.com"
MAX_EMAILS = 20

# Clean plain text
def clean(text):
    return ''.join(c for c in text.lower() if c.isalnum() or c.isspace())

# Fetch emails (now returns (body, sender) tuples)
def fetch_emails(email_user, email_pass, subject_filter):
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(email_user, email_pass)
    imap.select("inbox")
    status, messages = imap.search(None, f'SUBJECT "{subject_filter}"')
    email_ids = messages[0].split()
    emails = []

    for mail_id in email_ids[-MAX_EMAILS:]:
        _, msg_data = imap.fetch(mail_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg.get("From", "Unknown")
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors='ignore')
                            emails.append((clean(body.strip()), sender))
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')
                    emails.append((clean(body.strip()), sender))
    imap.logout()
    return emails

# Cluster questions + show top keywords + sender info
def cluster(emails, num_clusters):
    questions = [e[0] for e in emails]
    senders = [e[1] for e in emails]

    if len(questions) < num_clusters:
        st.warning(f"Only {len(questions)} emails found. Not enough for {num_clusters} clusters.")
        for q, s in zip(questions, senders):
            st.write(f"- **From:** {s} \n📩 {q}")
        return

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    labels = kmeans.fit_predict(X)

    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    for i in range(num_clusters):
        st.subheader(f"📦 Cluster {i + 1}")
        st.markdown(f"**🔑 Top keywords:** {', '.join([terms[ind] for ind in order_centroids[i, :3]])}")
        for j, label in enumerate(labels):
            if label == i:
                st.markdown(f"**From:** {senders[j]}")
                st.write(f"📩 {questions[j]}")
                st.markdown("---")

# --- Streamlit UI ---
st.title("📬 Email Clustering Tool")
st.markdown("Securely fetch and cluster Gmail messages based on subject!")

with st.form("login_form"):
    email_user = st.text_input("📧 Gmail address", type="default")
    email_pass = st.text_input("🔑 App Password", type="password")
    subject_filter = st.text_input("🔎 Subject filter", value="job")
    num_clusters = st.slider("📊 Number of clusters", min_value=2, max_value=10, value=3)
    submitted = st.form_submit_button("🚀 Fetch and Cluster Emails")

if submitted:
    with st.spinner("Connecting to Gmail and fetching emails..."):
        try:
            emails = fetch_emails(email_user, email_pass, subject_filter)
            if not emails:
                st.error("No emails found with that subject filter.")
            else:
                cluster(emails, num_clusters)
        except Exception as e:
            st.error(f"❌ Error: {e}")
