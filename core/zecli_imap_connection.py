from pymongo.message import query
from core.send_notification import send_notification
import imaplib
from posixpath import split
from db.mongo_connection import check_mongo_doc, connection, insert_new_campaign
import email
import re
from core.find_bot_email import find_bot_email


def zecli_imap_connection(mail, client, client_google):

    mail.select("inbox")
    result, data = mail.uid('search', None, 'UNSEEN')

    inbox_item_list = data[0].split()
    list_emails = []
    root_dict = {}
    db = client.zecli_db
    campaigns = db.campaigns

    for item in inbox_item_list:
        result2, email_data = mail.uid('fetch', item, '(RFC822)')
        raw_email = email_data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)

        # Set variables from emails
        Cc_ = email_message["Cc"]
        from_ = email_message['From']
        subject_ = email_message['Subject']
        #date_ = email_message['Date']
        to_ = email_message['To']
        result_from = re.search("<(.*)>", from_)
        #result_to = re.search("<(.*)>", to_)
        #sender_ = result_to.group(1)
        sender = result_from.group(1)
        message_id = email_message["Message-ID"].replace("<","").replace(">","")
        print(message_id)
  
        bot = find_bot_email(Cc_, to_).strip()
        

        if "RE:" not in subject_ and "Re:" not in subject_:
            query = {"email": sender}
            if check_mongo_doc(client, "staff", query):
                print("This staff is Authorized")
                if bot != None and sender != None:
                    identity_campaing = bot.split("@")[0].split("+")[1]
                    campaign_id = "{}_{}".format(sender, identity_campaing)
                    print("from zecli : " + campaign_id)
                    insert_new_campaign(client, client_google, campaign_id, message_id)
                    return campaign_id
                else:
                    print("Campaign Error from Zecli")
                    send_notification(sender, None, None, 0)
            else:
                print("This staff doesn't Authorized: " + sender)
        else:
            # To save the second reply from email merge
            # bot = bot.replace(" ", "")
            print(bot)
            match = {"Cc_": bot}
            if db.responses.find_one(match):
                campaign_id = db.responses.find_one(match).get("campaignID_")
                print(campaign_id)
                data = {"Message-ID": message_id}
                query = {"campaignID_": campaign_id}
                campaigns.update_one(query,{ "$push": data})
                print("This is a REPLY. only update the Message-ID")
            else:
                print("First response")
