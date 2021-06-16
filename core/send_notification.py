#!/usr/bin/env python3
from smtplib import SMTP
from email.message import EmailMessage


# Enviroment variables
SENDER = 'z@zeroclickmail.com'
PASSWORD = 'Holberton2021'


def send_notification(recipient, campaign_id, spreadsheet_id, notification_id):
    """
        Send a notification to the staff when any event happen, e.g.:
          - New campaign created.
          - Campaign id missing.

        Arguments:
            recipient: The email who will receive the notification.

            campaing_id: Campaing id.

            spreadsheet_id: This is a google spreadsheet id

            content_id: Notification code.
                - 0: Missing campaign id
                - 1: Campaign created.
    """

    # Missing campaign id
    if notification_id == 0:
        subject = 'Missing campaign id'
        content = "Campaign id is missing, unfortunately I can't create the campaign"

    # Campaign created
    if notification_id == 1:
        url_file = "https://docs.google.com/spreadsheets/d/" + spreadsheet_id
        subject = 'Campaign succesfully created!'
        content = """
                    Campaign {} has been created !
                    google spreadsheet: {}
                    """.format(campaign_id, url_file)

    # Set email headers
    message = EmailMessage()
    message['From'] = SENDER
    message['To'] = [recipient]
    message['Subject'] = subject
    message.set_content(content)

    # set up the SMTP session
    with SMTP('mail.zeroclickmail.com', 587) as session:
        # Encript the trafic and session login
        session.starttls()
        session.login(SENDER, PASSWORD)

        # send email
        session.send_message(message)
