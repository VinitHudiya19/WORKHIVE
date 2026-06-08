import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger("app.email")


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using configured Resend API or SMTP settings.
    If neither is configured, prints to stdout for local debugging/testing.
    """
    # Create HTML formatted text for cleaner terminal prints
    clean_body = body.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n").replace("<strong>", "").replace("</strong>", "")
    
    # 1. Try Resend API (HTTP-based, bypasses Render port blocking)
    if getattr(settings, "RESEND_API_KEY", None):
        import httpx
        try:
            # default to SMTP_FROM, fallback to onboarding@resend.dev
            sender = settings.SMTP_FROM
            if not sender or sender == "noreply@workhive.com":
                # For Resend free accounts, onboarding@resend.dev is the only valid sender
                # unless they verify their custom domain.
                sender = "WorkHive <onboarding@resend.dev>"
            
            response = httpx.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": sender,
                    "to": [to_email],
                    "subject": subject,
                    "html": body
                },
                timeout=10.0
            )
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully via Resend API to {to_email}")
                print(f"[RESEND SUCCESS] Sent email to {to_email} | Subject: {subject}")
                return
            else:
                logger.error(f"Failed to send email via Resend API: {response.status_code} - {response.text}")
                print(f"[RESEND FAIL] Status: {response.status_code} | Error: {response.text}")
        except Exception as err:
            logger.error(f"Exception sending email via Resend API: {err}")
            print(f"[RESEND EXCEPTION] Error: {err}")
        # If Resend failed, we fall through to try SMTP or mock as fallback.

    # 2. Try SMTP
    if getattr(settings, "SMTP_HOST", None):
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
            logger.info(f"Email sent successfully via SMTP to {to_email}")
            print(f"[SMTP SUCCESS] Sent email to {to_email} | Subject: {subject}")
            return
        except Exception as e:
            logger.error(f"Failed to send email via SMTP to {to_email}: {e}")
            print(f"\n[SMTP FAIL] To: {to_email} | Sub: {subject} | Error: {e}")
            # If SMTP fails, we print a mock fallback print

    # 3. Print Mock (No provider configured or all failed)
    print("\n" + "="*60)
    print(f" [MOCK EMAIL SENT (FALLBACK)]")
    print(f"To:      {to_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{clean_body.strip()}")
    print("="*60 + "\n")
    logger.info(f"Mock email sent to {to_email} with subject '{subject}'")
