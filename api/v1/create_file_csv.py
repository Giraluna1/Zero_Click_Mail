from to_json import to_json
import pandas


def create_file_csv(docs_dict):
    file_name = list(docs_dict.keys())[0]
    print('---------------------------------')
    print(file_name)
    print('---------------------------------')
    json_str = to_json(docs_dict)

    json_obj = pandas.read_json(json_str)
    json_obj.to_csv(r'/home/zero_click_emails_form/connection_imap/api/v1/static/{}'.format(file_name), index=None)

    print('file created')
    return(file_name)
