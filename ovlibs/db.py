#
# @copyright
# Copyright (c) 2022 OVTeam
#
# All Rights Reserved
#
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://choosealicense.com/licenses/mit/
#

import os
from pymongo import MongoClient

class db:
    def __init__(self):
        self.client = None;

    def getClient(self):
        return MongoClient(os.getenv("MONGO_URI"))

    def getConfig(self):
        data = None
        try:
            if self.client == None:
                self.client = self.getClient()

            client_code = os.getenv('CLIENT_CODE')
            config_key = "SFTP_CONFIGS"
            if client_code != "":
                config_key = client_code + "_" + "SFTP_CONFIGS"
            dbname = self.client[os.getenv('DB_NAME')]
            collection_name = dbname[os.getenv('DB_COLLECTION_CONFIG')]

            print("XXXX: " + config_key)
            obj = collection_name.find_one({"Name": config_key})
            if obj != None:
                data = obj['Value']
        except:
            pass
        return data

    def getMapping(self, key):
        data = None
        try:
            if self.client == None:
                self.client = self.getClient()

            dbname = self.client[os.getenv('DB_NAME')]
            collection_name = dbname[os.getenv('DB_COLLECTION_WH_MAPPING')]
            obj = collection_name.find_one({"Key": key})
            if obj != None:
                data = obj['Value']
        except:
            pass
        return data
    
    def hasDCSite(self, key):
        data = False
        try:
            if self.client == None:
                self.client = self.getClient()

            dbname = self.client[os.getenv('DB_NAME')]
            collection_name = dbname["WH.Warehouses"]
            obj = collection_name.find_one({"Sites.Code": key})
            if obj != None:
                data = True
        except:
            pass
        return data
    
    def getSyncSites(self, db_name = ""):
        data = None
        try:
            if self.client == None:
                self.client = self.getClient()

            if db_name == "":
                db_name = os.getenv('DB_NAME')
            
            dbname = self.client[db_name]
            collection_name = dbname[os.getenv('DB_COLLECTION_WH_FILE')]
            filters = {"IsSync": 0}
            pipeline = [
                {"$match": filters},
                {"$group": {"_id": {"SiteId": "$SiteId", "Type": "$Type"}}},
                {"$sort": {"_id.Frequency": 1}}
            ]
            return list(collection_name.aggregate(pipeline))
        except:
            pass
        return data

    def getSyncFileList(self, options={}, db_name = ""):
        data = None
        try:
            if db_name == "":
                db_name = os.getenv('DB_NAME')

            if self.client == None:
                self.client = self.getClient()
            
            filters = {"IsSync": 0, "Type": options['Type'], "SiteId": options["SiteId"], "ClientCode": "WIN"}
            client_code = os.getenv('CLIENT_CODE')

            if client_code != '':
                filters['ClientCode'] = client_code
                print(filters)
            dbname = self.client[db_name]
            collection_name = dbname[os.getenv('DB_COLLECTION_WH_FILE')]
            return collection_name.find(filters, {"_id": 1, "LocalFilePath": 1, "RemoteFilePath": 1 }).limit(40).sort("Frequency", 1);
        except:
            pass
        return data
    
    def updateSyncFile(self, id, results=None, db_name=""):
        try:
            if db_name == "":
                db_name = os.getenv('DB_NAME')
            if self.client == None:
                self.client = self.getClient()
            dbname = self.client[db_name]
            collection_name = dbname[os.getenv('DB_COLLECTION_WH_FILE')]
            return collection_name.update_one({"_id": id}, {"$set": {"IsSync": 1, "Results": results}})
        except:
            pass

    def close(self):
        if self.client != None:
            self.client.close()
            self.client = None
