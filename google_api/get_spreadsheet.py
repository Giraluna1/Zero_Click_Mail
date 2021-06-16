import gspread


session = gspread.service_account(filename='key_api.json')

titles_list = []
for spreadsheet in session.openall():
    titles_list.append(spreadsheet.id)
    #session.del_spreadsheet(spreadsheet.id)
print(titles_list)
