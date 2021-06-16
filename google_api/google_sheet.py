from gspread import service_account
import gspread
from dotenv import dotenv_values

# Setup Enviroment Variables
config = dotenv_values(".env")
SERVICE_ACCOUNT_FILE = config.get('KEY_API_JSON')


def connection_google_api():

    print("Connected to Google API")
    return service_account(filename=SERVICE_ACCOUNT_FILE)


def create_spreadsheet(client_google, campaign_id):
    """
    Create a new blank spreadsheet for each campaing.

    Args:
        campaign_id (str): Campaign to create a new spreadsheet.

    Returns:
        str: spreadsheet id of the new spreadsheet.
    """

    # campaing creator or staff
    campaign_admin = campaign_id.split("_")[0]
    print(campaign_admin)

    # create new spreadsheet
    spreadsheet_id = client_google.create(campaign_id).id
    print(spreadsheet_id)

    # add header to the new spreadsheet
    spreadsheet = client_google.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1
    header = ['Timestamp', 'Name', 'Email', 'Subject', 'Response']
    worksheet.append_row(header, table_range='A1')

    # permissions only for campaign_admin
    #session.insert_permission(spreadsheet_id, None, perm_type='user', role='writer', notify=True)

    # permissions for everyone
    client_google.insert_permission(
        spreadsheet_id, None, perm_type='anyone', role='writer')

    return spreadsheet_id


def spreadsheet_row_count(client_google, spreadsheet_id):

    spreadsheet = client_google.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1
    row_count = len(worksheet.get_all_values())

    return row_count
