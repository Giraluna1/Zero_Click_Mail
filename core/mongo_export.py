from os import system

# VARIABLES ENVIROMENT
USER_MONGODB = 'Giraluna1'
PSWD_MONGODB = 'Giraluna1'
ZECLI_DB = 'zecli_db'
CLUSTER_MONGODB = 'cluster0.bwtow.mongodb.net'


def mongo_export(campaign_id, db=ZECLI_DB, collection=None,
                 query='', file_type='csv'):
    """
    Export collection from MongoDB to CSV or JSON
    Args:
        campaign_id (str): Its used to generate file name.
        db (str, var env): Mongodb database. Defaults to ZECLI_DB.
        collection (str, None): Mongodb collection into database.
            Defaults to None.
        query (str, optional): . Defaults to ''.
        file_type (str, optional): [description]. Defaults to 'csv'.
    """

    uri = f'mongodb+srv://{USER_MONGODB}:{PSWD_MONGODB}\
            @{CLUSTER_MONGODB}/{ZECLI_DB}'

    # This is the first row in the csv file
    fields = 'from_,date_,Cc_,Subject_,content_'
    file_name = campaign_id + '.' + file_type
    path = 'api/v1/static/'

    command = f'mongoexport --uri={uri} --db={db} --collection={collection}\
                --fields={fields} --query={query} --type={file_type}\
                --out={path}{file_name}'

    system(command)
