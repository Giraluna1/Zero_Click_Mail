from os import system
from pymongo.message import query
import pandas
from pymongo import MongoClient
from dotenv import dotenv_values

# Setup Enviroment Variables
config = dotenv_values(".env")

USER_MONGODB = config.get('USER_MONGODB')
PSWD_MONGODB = config.get('PSWD_MONGODB')
ZECLI_DB = config.get('DATABASE')
CLUSTER_MONGODB = config.get('CLUSTER')
URI_CONNECTION = f'mongodb+srv://{USER_MONGODB}:{PSWD_MONGODB}@{CLUSTER_MONGODB}/{ZECLI_DB}'


def mongo_export(campaign_id, db=ZECLI_DB, collection='responses', query='', file_type='csv'):
    """
    Produces a JSON or CSV export of data stored in a MongoDB instance.

    Args:
        campaign_id (str): Its used to generate file name.
        db (str, var env): Mongodb database. Defaults to ZECLI_DB.
        collection (str, ''): Mongodb collection into database. Defaults to ''.
        query (str, jsondumps): Filter, as a JSON string, e.g., '{x:{$gt:1}}'.
        file_type (str, json): The output format, either json or csv. Defaults to 'csv'.

        Returns:
        csv or json: file with the data from the given command.
    """

    # mongodb uri connection string
    uri = URI_CONNECTION

    # This is the first row in the csv file,
    # comma separated list of field names e.g."name,age"
    fields = 'from_,date_,Cc_,Subject_,content_'
    file_name = campaign_id + '.' + file_type

    # Where the file will be save
    path = '/home/Stackez/connection_imap/static/'

    #client = connection()
    if check(client, campaign_id) is True:
        # Create new file
        command_01 = f'mongoexport --uri={uri} --collection={collection} '
        command_02 = f'--fields={fields} --query=\'{query}\' --type={file_type} '
        command_03 = f'--out={path}{file_name}'
        system(command_01 + command_02 + command_03)
    else:
        # Campaing does not exist or is emty
        return 0


def mongo_to_csv(campaign_id, query):
    """
    Get the data from mongodb and convert it to CSV format.

    Args:
        campaign_id (str): To search for a campaign in the database.
        query ([type]): Filter, as a JSON string, e.g., '{x:{$gt:1}}'.

    Returns:
        str: Data converted to CSV format.
    """

    # Connection to mongodb, get the database and collection
    #client = connection()
    db = client.zecli_db
    responses = db.responses

    # Get the data from the database
    exclude_fields = {"_id": False, "Cc_": False}
    cursor = responses.find(query, exclude_fields)

    # Convert the cursor to csv format
    data = pandas.DataFrame(list(cursor))
    data_csv = data.to_csv(header=False, index=False)

    return data_csv


def mongo_docs_count(client, query):

    # Connection to mongodb, get the database and collection
    db = client.zecli_db
    responses = db.responses

    return responses.count_documents(query)
