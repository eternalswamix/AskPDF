import os
import smtplib
from email.mime.text import MIMEText


def send_credentials_email(to_email: str, username: str, password: str):
    """
    Sends credentials email to user after register.
    Uses Gmail SMTP (App Password required).
    """

    mail_host = os.getenv("MAIL_HOST")
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM", mail_username)

    if not all([mail_host, mail_port, mail_username, mail_password, mail_from]):
        raise ValueError("❌ Email config missing in .env (MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM)")

    subject = "✅ Welcome to PDF.AI - Your Login Credentials"

    body = f"""
Hello 👋

Your account has been created successfully ✅

🔹 Username: {username}
🔹 Password: {password}

You can login here:
http://127.0.0.1:5000/login

⚠️ Please keep your password safe.

Thanks,  
PDF.AI Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(mail_host, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.sendmail(mail_from, [to_email], msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print("❌ Email send failed:", str(e))
        raise
