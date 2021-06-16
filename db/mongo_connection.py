#!/usr/bin/env python3
""" This module conect to DB """

from core.sed_hash_seed import hash_id
import uuid
from google_api.google_sheet import create_spreadsheet
from numpy.lib.function_base import append
import pymongo
from core.send_notification import send_notification
from core.mongo_to_gsheet import append_rows_gsheet
from dotenv import dotenv_values

# Setup Enviroment Variables
config = dotenv_values(".env")

def connection():
    """ Make the connection with Atlas MongoDB cluster """
    MONGODB_HOST = config.get('IP_SERVER')  
    MONGODB_PORT = config.get('PORT') #port mongo atlas by default is 27017
    

    URI_CONNECTION = config.get('URI') # link provided by connection in mongo atlas
    try:
        client = pymongo.MongoClient(URI_CONNECTION)
        print('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST))
        client.close()

    except:
        print("Error in the conection")

    return (client)


def check_mongo_doc(client, collection, query):
    """ This function check_mongo_docs if the query is into
        the collection specific
    """
    db = client.zecli_db
    collec = db[collection]

    if collec.find_one(query):
        return True
    else:
        return False


def crud_zeroclick_db(client, client_google, root_dict):
    """ this fuction create data base, create collection,
    insert documents by recipients and update the new responses
    ARGS:
        client: client conecction with atlas
        root_dict (dic): fields email parsed by campaign
    """
    db = client.zecli_db

    for campaign_id, list_responses in root_dict.items():
        # Make colection responses
        print("Esto es camp´: {}".format(campaign_id))
        print("Esto es data: {}".format(list_responses))

        responses = db.responses

        for response_dict in list_responses:

            user_email = response_dict.get('email')
            response_dict['user_id'] = hash_id(user_email)

            insert_data = responses.insert_one(response_dict)
            print("There is a new data")

        append_rows_gsheet(client, client_google, campaign_id)


def insert_new_campaign(client, client_google, campaign_id, MessageID):
    """ this function insert new campaign_id
    into the collection campaigns
    """
    db = client.zecli_db

    campaigns = db.campaigns
    recipient = campaign_id.split("_")[0]
    query = {"campaignID_": campaign_id}
    if check_mongo_doc(client, "campaigns", query) == True:
        print("The campaign already exist")
        campaigns.update_one( query,{ "$push": {"Message-ID": MessageID}})

    else:
        spreadsheet_id = create_spreadsheet(client_google, campaign_id)

        query = {
            "campaignID_": campaign_id,
            "spreadsheet_id": spreadsheet_id,
            "Message-ID" : [MessageID]
        }

        insert_data = campaigns.insert_one(query)
        print("Make -- Notification CREATION CAMPAIGN")
        send_notification(recipient, campaign_id, spreadsheet_id, 1)

def docs_in_collection(client, collection):
    """ This fuction count the number of all documents in any 
        collection
        ARGS:
            client (): Session to connect with DB
            collection (): collection tht you need to count 
        Return number of documents
    """
    db = client.zecli_db
    return db.campaigns.count()
