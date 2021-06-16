from pymongo import aggregation
import gspread
import pandas
from db.mongo_export import mongo_docs_count
from google_api.google_sheet import spreadsheet_row_count


def append_rows_gsheet(client, client_google, campaign_id):

    exclude_fields = {"_id": False}
    query = {"campaignID_": campaign_id}
    fields = {
            "_id": 0, "Timestamp": "$timestamps",
            "Name": "$fullname", "Email": "$email",
            "Subject": "$Subject_", "Response": "$response"
            }

    db = client.zecli_db
    campaigns = db.campaigns
    responses = db.responses

    #print('===============================')
    #print(campaign_id)
    mongo_doc = campaigns.find_one(query)
    #print('===============================')
    #print(mongo_doc)
    spreadsheet_id = mongo_doc.get('spreadsheet_id')
    #print(spreadsheet_id)
    #print('===============================')

    spreadsheet = client_google.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1    
    
    rows_count = (spreadsheet_row_count(client_google, spreadsheet_id))

    if not worksheet.acell('A1').value:
        header = ['Timestamp', 'Name', 'Email', 'Subject', 'Response']
        print("There isn't Headers")
        worksheet.update('A1:E1', [header])
        rows_count = rows_count - 1 
    else:
        rows_count = rows_count - 1
    
    docs_count = mongo_docs_count(client, query)

    if docs_count > rows_count:
        aggregation = [{'$match': query}, {"$project": fields}, {"$skip": rows_count}]
        mongo_docs = list(responses.aggregate(aggregation))
        print(mongo_docs)

        data = pandas.DataFrame(mongo_docs).values.tolist()

        worksheet.append_rows(data, table_range='A2')
        print("New response was append")
