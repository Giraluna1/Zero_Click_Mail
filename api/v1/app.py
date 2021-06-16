#!/usr/bin/env python3
#import uvicorn
from fastapi import FastAPI
import json
import pymongo
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import FileResponse
from db.mongo_export import mongo_export


app = FastAPI()
statics = f"{os.getcwd()}/static"


@app.get("/static/{campaign_id_csv}")
async def get_csv_file(campaign_id_csv: str):
    """
        This route gets responses by campaign ID

    Args:
        campaing_id_csv (str): Campaign id that represents a campaign.

    Returns:
       csv or json: File that contains the data by unique campaign.
    """

    # Could be json or csv format
    try:
        file_type = campaign_id_csv.split('.')[2]
        only_campaign_id = campaign_id_csv[:-len(file_type)-1]
        query = json.dumps({"campaignID_": only_campaign_id})

        mongo_export(campaign_id=only_campaign_id,
                    query=query, file_type=file_type)

    except:
        print('exception')
        return 'Invalid sintaxys'
    
    file_csv = os.path.join(statics, campaign_id_csv)
    
    try:
        with open(file_csv) as f:
            return FileResponse(file_csv)

        # Do something with the file
    except IOError:
        print("File not accessible")
        return FileResponse(os.path.join(statics, 'default_not_responses.csv'))


#if __name__ == '__main__':
    #uvicorn.run(app, host='0.0.0.0', port=80)
