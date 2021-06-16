#!/usr/bin/env python3
""" function that search email bot from cc or to """
import re


def find_bot_email(cc, to):
    """find bot from find_bot"""
    
    email_bot = "z+"
    list_emails = []

    if cc is None or email_bot not in cc:
        cc = to
    for x in cc.split(","):
        if email_bot in x:
                list_emails.append(x)
    
    print(list_emails)
    for i in list_emails:
        try:
            # clean and build
            value = i.split("@")[0].split("+")[1]
            if value is not None and "<" in i:
                x = i.replace('\n','').replace('\r','').replace('\t','').replace(' ','')
                if x is not None:
                    if cc == to and ">" in cc:
                        try: 
                            result = re.search("<(.*)>", x)
                        except:
                            return None
                        return  result.group(1)
                    else:
                        return x
            elif value:
                return i
        except:
            print("Error CampaignId: Mising + in campaign id")
