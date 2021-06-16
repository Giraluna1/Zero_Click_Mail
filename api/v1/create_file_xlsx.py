#!/usr/bin/env python3
from xlsxwriter import Workbook


def create_xlsx(campaigns, campaign_id):

    campaign_name = list(campaigns.keys())[0]
    table_name = campaign_name.split('|')[1]
    responses_list = campaigns[campaign_id]

    # list object calls by index but dict object calls items randomly
    ordered_list = ['from_', 'date_', 'Cc_',
                    'campaignID_', 'Subject_', 'content_']

    spreadsheet = Workbook(campaign_name + ".xlsx")
    sheet = spreadsheet.add_worksheet(table_name)

    first_row = 0
    for header in ordered_list:
        column = ordered_list.index(header)  # we are keeping order.
        # we have written first row which is the header of worksheet also.
        sheet.write(first_row, column, header)

    row = 1
    for response in responses_list:
        for key, value in response.items():
            column = ordered_list.index(key)
            if type(value) is list:
                value = str(value)
            sheet.write(row, column, value)
        row += 1  # enter the next row

    print('file created')
    spreadsheet.close()
    return spreadsheet
