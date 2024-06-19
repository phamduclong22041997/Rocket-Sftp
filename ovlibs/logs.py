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


class logs:
    def __init__(self):
        self.client = None

    def getClient(self):
        connection_url = os.getenv("MONGO_URI_LOG")
        if connection_url != None:
            return MongoClient(connection_url)
        return None

    def save(self, data):
        try:
            if self.client == None:
                self.client = self.getClient()
            if self.client != None:
                dbname = self.client[os.getenv('DB_NAME_LOG')]
                collection_name = dbname[os.getenv('DB_COLLECTION_LOG')]
                collection_name.insert_one(data)
        except:
            self.close()

    def close(self):
        if self.client != None:
            self.client.close()
            self.client = None
