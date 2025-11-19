import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from llm_service import enhance_email_body

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_meeting_email(sender_email, recipients, subject, body):
    """
    Sends formatted meeting summary email to selected recipients.
    Body is enhanced by LLM before sending (adds greeting + closing).
    """
    try:
        # Step 1: Enhance the body with salutation and closing via LLM
        enhanced_body = enhance_email_body(body)

        # Step 2: Prepare the HTML email
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        body_html = enhanced_body.replace("\n", "<br>")

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color:#222; background-color:#f9fafb; padding:20px;">
            <div style="max-width:700px; margin:auto; background:white; border-radius:10px; padding:25px; box-shadow:0 0 8px rgba(0,0,0,0.1);">
                <h2 style="color:#0057b8;">📋 Meeting Summary</h2>
                <div style="line-height:1.6; font-size:15px;">
                    {body_html}
                </div>
                <br><hr style="border:0.5px solid #ddd;">
                <p style="font-size:13px; color:#555;">Sent via <b>AI Meeting Assistant 🤖</b></p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        # Step 3: Send via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(sender_email, recipients, msg.as_string())

        return {"status": "success", "message": f"✅ Email sent to {len(recipients)} members."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

