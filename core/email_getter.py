#!/usr/bin/env python3
from core.find_bot_email import find_bot_email
import email
import imaplib
from time import sleep
from bs4 import BeautifulSoup
from base64 import b64decode
import os.path
import re
from db.mongo_connection import connection, crud_zeroclick_db, check_mongo_doc
from core.find_bot_email import find_bot_email
from core.zecli_imap_connection import zecli_imap_connection
from google_api.google_sheet import connection_google_api
import html
from email.iterators import _structure
from dotenv import dotenv_values


# Setup Enviroment Variables
config = dotenv_values(".env")

client = connection()
client_google = connection_google_api()

username = config.get('USERNAME')
password = config.get('PASSWORD')
mail_imap = config.get('MAILIMAP')

mail = imaplib.IMAP4_SSL(mail_imap)
mail.login(username, password)

username_z = config.get('USERNAME_Z')
password_z = config.get('PASSWORD_Z')

mail_z = imaplib.IMAP4_SSL(mail_imap)
mail_z.login(username_z, password_z)

# Check inbox responses
while(not sleep(1)):

    zecli_imap_connection(mail_z, client, client_google)
    mail.select("inbox")
    result, data = mail.uid('search', None, 'UNSEEN')

    inbox_item_list = data[0].split()
    list_emails = []
    root_dict = {}
    campaigns = []

    for item in inbox_item_list:
        result2, email_data = mail.uid('fetch', item, '(RFC822)')
        raw_email = email_data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        In_reply_to = email_message["In-Reply-To"]
        if In_reply_to is None:
            continue
        references = email_message["References"].split(">")[0].replace("<","").replace("\r","").replace("\n","").replace(" ","")
        query_references = {"Message-ID": references}     
        db_campaings = client.zecli_db
        campaign_id = db_campaings.campaigns.find_one(query_references)
        if campaign_id:
            campaign_id = campaign_id["campaignID_"]


        #Assingament
        to_ = email_message['To']
        Cc_ = find_bot_email(email_message["Cc"], to_).strip()
        print("**********")
        print(">{}".format(Cc_))
        from_ = email_message['From']
        subject_ = email_message['Subject']
        date_ = email_message['Date']
        result_from = re.search("<(.*)>", from_)

        result_from_clean = result_from.group(1)

        if result_from_clean in campaign_id:
            continue
        content_charset = email_message["Content-Type"]
        try:
            decode = content_charset.split(";")[1]
            result_decode = re.search('"(.*)"', decode)
            decode_result = result_decode.group(1)
        except:
            decode_result =  ""
        body = None
        plain = False
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True)
                if "charset" not in content_charset:
                    try:
                        body = body.decode("utf-8")
                    except:
                        body = body.decode("iso-8859-1") 
                else:
                    body = body.decode(decode_result) 
                text_plain = body.split("\r\n\r\n")[0]
                if "UTF-8" not in decode_result or "utf-8" not in decode_result:
                    text_plain = text_plain.split("_______")[0]
                break
            if content_type == "text/html":
                """ continue here """
                html_ = email_message.get_payload(decode=True)
                soup_ = BeautifulSoup(html_, "html.parser")
                text = soup_.get_text()
                if "Sent from" in text:
                    text_plain = text.split("Sent from")[0].replace("\xa0", "")
                print(text_plain)
        # Obtain type encoding
        if "plain" or "html" in content_type:
            emails = {}
            #Asing variable to root_dict
            emails["email"] = result_from.group(1)
            emails["fullname"] = from_.split("<")[0]
            emails["timestamps"] = date_
            emails["Cc_"] = Cc_
            emails["campaignID_"] = campaign_id
            if Cc_ != None and "+" in Cc_ and "z" in Cc_:
                identity_campaing = Cc_.split("@")[0].split("+")[1]

            emails["Subject_"] = subject_
            # emails["response"] = html.unescape(text_plain)
            emails["response"] = text_plain.replace("\r","").replace("\n", ". ")

            print("------")
            #append only the emails with campaignid
            new_query = {"campaignID_": emails["campaignID_"]}
            check_mongo_doc(client, "campaigns", new_query)
            if emails["campaignID_"] and identity_campaing:

                if not emails["campaignID_"] in campaigns:
                    campaigns.append(emails["campaignID_"])

                if emails["campaignID_"] in root_dict:
                 root_dict[emails["campaignID_"]].append(emails)
                else:
                    root_dict[emails["campaignID_"]] = []
                    root_dict[emails["campaignID_"]].append(emails)
            else:
                print("Error with Capaign id")

        else:
           pass
    
    crud_zeroclick_db(client, client_google, root_dict)
