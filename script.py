from pymongo.message import query
from db.mongo_connection import connection
from google_api.google_sheet import create_spreadsheet, spreadsheet_row_count
import gspread
import pandas


""" SERVICE_ACCOUNT_FILE = '/home/zero_click_mail/connection_imap/google_api/key_api.json'
session = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)

campaign_id = "2344@holbertonschool.com_5050"
query = {"campaignID_": campaign_id}
fields = {"_id": 0, "Timestamp":"$timestamps", "Name": "$fullname", "Email": "$email", "Subject": "$Subject_", "Response": "$response"}
spreadsheet_id = '1mZev1w4rV8SUJUuuutORYkQdYqrOI7XaBy70EUm31nY' """

#spreadsheet_id = create_spreadsheet(session, campaign_id)
#print(spreadsheet_id)

client = connection()
db = client.zecli_db
staff_col = db.staff

sender = "stackez@gmail.com"
field = "email"
collec = staff_col

if collec.find_one({field:sender}):
    print("This staff is Authorized")
else:
    print("This staff doesn't Authorized")
