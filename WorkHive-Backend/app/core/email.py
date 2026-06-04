import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger("app.email")


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using configured SMTP settings.
    If no SMTP host is configured, prints to stdout for local debugging/testing.
    """
    # Create HTML formatted text for cleaner terminal prints
    clean_body = body.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n").replace("<strong>", "").replace("</strong>", "")
    
    if not getattr(settings, "SMTP_HOST", None):
        print("\n" + "="*60)
        print(f" [MOCK EMAIL SENT]")
        print(f"To:      {to_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{clean_body.strip()}")
        print("="*60 + "\n")
        logger.info(f"Mock email sent to {to_email} with subject '{subject}'")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
        logger.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        # Print fallback to console on actual error
        print(f"\n[EMAIL FAIL FALLBACK] To: {to_email} | Sub: {subject} | Error: {e}")
