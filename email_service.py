import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

async def send_contact_email(sender_name: str, sender_email: str, subject: str, message: str) -> bool:
    """
    Sends contact form data to your Gmail using SMTP with App Password.

    Args:
        sender_name: Name of the person contacting you
        sender_email: Email of the person contacting you
        subject: Subject of the message
        message: Message content

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get environment variables
        your_email = os.getenv("GMAIL_ADDRESS")
        app_password = os.getenv("GMAIL_APP_PASSWORD")

        if not your_email or not app_password:
            print("Error: Gmail credentials not found in environment variables")
            return False

        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = your_email
        msg["To"] = your_email  # Sending to yourself
        msg["Subject"] = f"Portfolio Contact: {subject}"
        msg["Reply-To"] = sender_email

        # Create HTML body
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">
                        New Contact Form Submission
                    </h2>

                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong style="color: #555;">From:</strong> {sender_name}</p>
                        <p><strong style="color: #555;">Email:</strong> <a href="mailto:{sender_email}">{sender_email}</a></p>
                        <p><strong style="color: #555;">Subject:</strong> {subject}</p>
                        <p><strong style="color: #555;">Date:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                    </div>

                    <div style="background-color: #fff; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0;">
                        <h3 style="color: #555; margin-top: 0;">Message:</h3>
                        <p style="white-space: pre-wrap;">{message}</p>
                    </div>

                    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; font-size: 12px;">
                        <p>This email was sent from your portfolio contact form.</p>
                        <p>Reply directly to this email to respond to {sender_name}.</p>
                    </div>
                </div>
            </body>
        </html>
        """

        # Create plain text version as fallback
        text_body = f"""
        New Contact Form Submission
        ===========================

        From: {sender_name}
        Email: {sender_email}
        Subject: {subject}
        Date: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

        Message:
        {message}

        ---
        Reply directly to this email to respond to {sender_name}.
        """

        # Attach both versions
        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")
        msg.attach(part1)
        msg.attach(part2)

        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(your_email, app_password)
            server.send_message(msg)

        print(f"Email sent successfully from {sender_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP Authentication failed. Check your Gmail credentials.")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
