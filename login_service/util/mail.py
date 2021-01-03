import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import jsonify


class Mail:

    @classmethod
    def send_mail(cls, to_email, subject, message):
        from_email = os.getenv('FROM_EMAIL')
        from_password = os.getenv('FROM_PASSWORD')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        part1 = MIMEText(message, "plain")
        msg.attach(part1)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            try:
                server.login(from_email, from_password)
                server.sendmail(from_email, to_email, msg.as_string())
                return jsonify({'success': True, 'message': 'Mail Sent'}), 200
            except smtplib.SMTPAuthenticationError as e:
                return jsonify({'success': False, 'message': 'Username and Password not accepted',
                                'Exception': str(e)}), 400
            except Exception as e:
                return jsonify({'success': False, 'message': 'Failed to send email',
                                'Exception': str(e)}), 400

