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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>New Contact Form Submission</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f7fa; line-height: 1.6;">
            <!-- Main Container -->
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f5f7fa; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <!-- Email Content Card -->
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); overflow: hidden;">

                            <!-- Header with Gradient -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); padding: 40px 30px; text-align: center;">
                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tr>
                                            <td style="text-align: center;">
                                                <!-- Icon Badge -->
                                                <div style="display: inline-block; width: 64px; height: 64px; background-color: rgba(255, 255, 255, 0.2); border-radius: 16px; margin-bottom: 16px;">
                                                    <div style="font-size: 32px; line-height: 64px; color: #ffffff;">✉️</div>
                                                </div>
                                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">New Contact Message</h1>
                                                <p style="margin: 8px 0 0 0; color: rgba(255, 255, 255, 0.9); font-size: 15px; font-weight: 400;">You've received a new inquiry from your portfolio</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- Content Section -->
                            <tr>
                                <td style="padding: 40px 30px;">

                                    <!-- Sender Information Card -->
                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f8fafc; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
                                        <tr>
                                            <td>
                                                <h2 style="margin: 0 0 20px 0; color: #1e293b; font-size: 18px; font-weight: 600;">Contact Details</h2>

                                                <!-- Name -->
                                                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 12px;">
                                                    <tr>
                                                        <td style="padding: 8px 0;">
                                                            <span style="display: inline-block; color: #64748b; font-size: 14px; font-weight: 500; min-width: 80px;">👤 Name:</span>
                                                            <span style="color: #1e293b; font-size: 15px; font-weight: 600;">{sender_name}</span>
                                                        </td>
                                                    </tr>
                                                </table>

                                                <!-- Email -->
                                                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 12px;">
                                                    <tr>
                                                        <td style="padding: 8px 0;">
                                                            <span style="display: inline-block; color: #64748b; font-size: 14px; font-weight: 500; min-width: 80px;">📧 Email:</span>
                                                            <a href="mailto:{sender_email}" style="color: #2563eb; font-size: 15px; font-weight: 500; text-decoration: none;">{sender_email}</a>
                                                        </td>
                                                    </tr>
                                                </table>

                                                <!-- Subject -->
                                                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 12px;">
                                                    <tr>
                                                        <td style="padding: 8px 0;">
                                                            <span style="display: inline-block; color: #64748b; font-size: 14px; font-weight: 500; min-width: 80px;">📝 Subject:</span>
                                                            <span style="color: #1e293b; font-size: 15px; font-weight: 500;">{subject}</span>
                                                        </td>
                                                    </tr>
                                                </table>

                                                <!-- Date -->
                                                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                                    <tr>
                                                        <td style="padding: 8px 0;">
                                                            <span style="display: inline-block; color: #64748b; font-size: 14px; font-weight: 500; min-width: 80px;">🕒 Date:</span>
                                                            <span style="color: #64748b; font-size: 14px;">{datetime.now().strftime("%B %d, %Y at %I:%M %p")}</span>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Message Content Card -->
                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border: 2px solid #e2e8f0; border-left: 4px solid #2563eb; border-radius: 12px; padding: 24px;">
                                        <tr>
                                            <td>
                                                <h3 style="margin: 0 0 16px 0; color: #1e293b; font-size: 16px; font-weight: 600;">Message Content</h3>
                                                <div style="color: #475569; font-size: 15px; line-height: 1.7; white-space: pre-wrap; word-wrap: break-word;">{message}</div>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Reply Button -->
                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top: 32px;">
                                        <tr>
                                            <td align="center">
                                                <a href="mailto:{sender_email}?subject=Re: {subject}" style="display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 10px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);">
                                                    Reply to {sender_name}
                                                </a>
                                            </td>
                                        </tr>
                                    </table>

                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                                    <p style="margin: 0 0 8px 0; color: #64748b; font-size: 13px; line-height: 1.6;">
                                        This email was automatically sent from your portfolio contact form.
                                    </p>
                                    <p style="margin: 0; color: #94a3b8; font-size: 12px;">
                                        You can reply directly to this email to respond to the sender.
                                    </p>
                                    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
                                        <p style="margin: 0; color: #94a3b8; font-size: 12px;">
                                            © {datetime.now().year} Umer Ali Portfolio. All rights reserved.
                                        </p>
                                    </div>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
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
