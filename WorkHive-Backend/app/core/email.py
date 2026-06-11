import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger("app.email")


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using configured API (Resend, SendGrid, Brevo) or SMTP settings.
    If no provider is configured, prints to stdout for local debugging/testing.
    """
    # Create HTML formatted text for cleaner terminal prints
    clean_body = body.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n").replace("<strong>", "").replace("</strong>", "")
    
    # default sender
    sender = settings.SMTP_FROM if settings.SMTP_FROM else "noreply@workhive.com"

    # 1. Try Resend API (HTTP-based, bypasses Render port blocking)
    if getattr(settings, "RESEND_API_KEY", None):
        import urllib.request
        import urllib.error
        import json
        try:
            resend_sender = sender
            if not resend_sender or resend_sender == "noreply@workhive.com":
                resend_sender = "WorkHive <onboarding@resend.dev>"
            
            req_data = json.dumps({
                "from": resend_sender,
                "to": [to_email],
                "subject": subject,
                "html": body
            }).encode("utf-8")
            
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=req_data,
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            
            try:
                with urllib.request.urlopen(req, timeout=10.0) as response:
                    status_code = response.getcode()
                    resp_body = response.read().decode("utf-8")
                    if status_code in [200, 201, 202]:
                        logger.info(f"Email sent successfully via Resend API to {to_email}")
                        print(f"[RESEND SUCCESS] Sent email to {to_email} | Subject: {subject}")
                        return
                    else:
                        logger.error(f"Failed to send email via Resend API: {status_code} - {resp_body}")
                        print(f"[RESEND FAIL] Status: {status_code} | Error: {resp_body}")
            except urllib.error.HTTPError as err:
                status_code = err.code
                resp_body = err.read().decode("utf-8")
                logger.error(f"Failed to send email via Resend API: {status_code} - {resp_body}")
                print(f"[RESEND FAIL] Status: {status_code} | Error: {resp_body}")
        except Exception as err:
            logger.error(f"Exception sending email via Resend API: {err}")
            print(f"[RESEND EXCEPTION] Error: {err}")

    # 2. Try SendGrid API (HTTP-based, bypasses Render port blocking, allows single sender verification)
    if getattr(settings, "SENDGRID_API_KEY", None):
        import urllib.request
        import urllib.error
        import json
        try:
            req_data = json.dumps({
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": sender, "name": "WorkHive"},
                "subject": subject,
                "content": [{"type": "text/html", "value": body}]
            }).encode("utf-8")
            
            req = urllib.request.Request(
                "https://api.sendgrid.com/v3/mail/send",
                data=req_data,
                headers={
                    "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            
            try:
                with urllib.request.urlopen(req, timeout=10.0) as response:
                    status_code = response.getcode()
                    resp_body = response.read().decode("utf-8")
                    if status_code in [200, 201, 202]:
                        logger.info(f"Email sent successfully via SendGrid API to {to_email}")
                        print(f"[SENDGRID SUCCESS] Sent email to {to_email} | Subject: {subject}")
                        return
                    else:
                        logger.error(f"Failed to send email via SendGrid API: {status_code} - {resp_body}")
                        print(f"[SENDGRID FAIL] Status: {status_code} | Error: {resp_body}")
            except urllib.error.HTTPError as err:
                status_code = err.code
                resp_body = err.read().decode("utf-8")
                logger.error(f"Failed to send email via SendGrid API: {status_code} - {resp_body}")
                print(f"[SENDGRID FAIL] Status: {status_code} | Error: {resp_body}")
        except Exception as err:
            logger.error(f"Exception sending email via SendGrid API: {err}")
            print(f"[SENDGRID EXCEPTION] Error: {err}")

    # 3. Try Brevo API (HTTP-based, bypasses Render port blocking, allows single sender verification)
    if getattr(settings, "BREVO_API_KEY", None):
        import urllib.request
        import urllib.error
        import json
        try:
            req_data = json.dumps({
                "sender": {"name": "WorkHive", "email": sender},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": body
            }).encode("utf-8")
            
            req = urllib.request.Request(
                "https://api.brevo.com/v3/smtp/email",
                data=req_data,
                headers={
                    "api-key": settings.BREVO_API_KEY,
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            
            try:
                with urllib.request.urlopen(req, timeout=10.0) as response:
                    status_code = response.getcode()
                    resp_body = response.read().decode("utf-8")
                    if status_code in [200, 201, 202]:
                        logger.info(f"Email sent successfully via Brevo API to {to_email}")
                        print(f"[BREVO SUCCESS] Sent email to {to_email} | Subject: {subject}")
                        return
                    else:
                        logger.error(f"Failed to send email via Brevo API: {status_code} - {resp_body}")
                        print(f"[BREVO FAIL] Status: {status_code} | Error: {resp_body}")
            except urllib.error.HTTPError as err:
                status_code = err.code
                resp_body = err.read().decode("utf-8")
                logger.error(f"Failed to send email via Brevo API: {status_code} - {resp_body}")
                print(f"[BREVO FAIL] Status: {status_code} | Error: {resp_body}")
        except Exception as err:
            logger.error(f"Exception sending email via Brevo API: {err}")
            print(f"[BREVO EXCEPTION] Error: {err}")

    # 4. Try SMTP (Blocked on Render Free, but works locally/other hosts)
    if getattr(settings, "SMTP_HOST", None):
        try:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(sender, to_email, msg.as_string())
            logger.info(f"Email sent successfully via SMTP to {to_email}")
            print(f"[SMTP SUCCESS] Sent email to {to_email} | Subject: {subject}")
            return
        except Exception as e:
            logger.error(f"Failed to send email via SMTP to {to_email}: {e}")
            print(f"\n[SMTP FAIL] To: {to_email} | Sub: {subject} | Error: {e}")

    # 5. Print Mock (No provider configured or all failed)
    print("\n" + "="*60)
    print(f" [MOCK EMAIL SENT (FALLBACK)]")
    print(f"To:      {to_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{clean_body.strip()}")
    print("="*60 + "\n")
    logger.info(f"Mock email sent to {to_email} with subject '{subject}'")
