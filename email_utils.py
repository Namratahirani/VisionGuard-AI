import smtplib
import ssl
from email.message import EmailMessage
import os
import json

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] config.json file not found.")
        return {}
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse config.json.")
        return {}

def send_email(subject, body, attachment_path=None):
    """
    Function to send an email with an optional attachment.
    :param subject: Subject of the email.
    :param body: Body content of the email.
    :param attachment_path: Path to the file to attach (optional).
    """
    # Load config
    config = load_config()

    EMAIL_SENDER = config.get("email_sender")
    EMAIL_PASSWORD = config.get("email_password")
    EMAIL_RECEIVER = config.get("email_receiver")
    SMTP_SERVER = config.get("smtp_server", "smtp.gmail.com")
    SMTP_PORT = config.get("smtp_port", 587)

    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("[ERROR] Missing essential email configurations in config.json.")
        return

    msg = EmailMessage()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach a file if the path is provided and the file exists
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
                print(f"[INFO] Attachment added: {file_name}")
        except Exception as e:
            print(f"[ERROR] Failed to attach file: {e}")

    # Set up SSL context for secure email sending
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[INFO] Email sent to {EMAIL_RECEIVER}")
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Authentication failed. Check your email sender and password.")
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP error occurred: {e}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
