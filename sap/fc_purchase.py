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
from ovlibs import ovsftp, db, request
from xml.dom import minidom

def loadFile(file_path, local_dir):
    resp = None
    try:
        file = minidom.parse(file_path)
        wh_site = file.getElementsByTagName(
            "StoreId")[0].firstChild.nodeValue

        ponumber = file.getElementsByTagName(
            "Ponumber")[0].firstChild.nodeValue

        resp = {
            "file_dir": local_dir + "/files",
            "file_name": os.path.basename(file_path)
        }

        _file_path = local_dir + "/files/" + os.path.basename(file_path)
        if os.path.exists(_file_path) == False:
            request.postFCRequest({
                "ObjectCode": "{0}_{1}".format(ponumber, wh_site),
                "SiteId": wh_site,
                "IssueSite": ponumber,
                "RequestType": "PO_REQUEST",
                "FilePath": _file_path
            })

    except Exception as e:
        print(e)
    return resp


def main():
    _db = db()
    config = _db.getConfig()
    local_dir = config['DES_OUT_FC_PO_REQUEST']
    remote_dir = config['SOURCE_OUT_FC_PO_REQUEST']
    delay_time = 20
    _db.close()

    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        obj.connect()
        obj.run(loadFile)