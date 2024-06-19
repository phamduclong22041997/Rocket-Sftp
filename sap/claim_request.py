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
from ovlibs import ovsftp, db
from xml.dom import minidom
import requests

def postFile(file_path, warehouse_code):
    if os.environ["OPS_URL"] == "":
        return
    url = os.environ["OPS_URL"] + "/" + warehouse_code + "/api/v1/claim/receiveFile"

    payload={
    'WarehouseCode': warehouse_code}
    files=[
    ('file',(os.path.basename(file_path),open(file_path,'rb'),'text/xml'))
    ]
    headers = {
    'Authorization': 'Bearer ' + os.environ["OPS_INTERNAL_TOKEN"]
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)


def loadFile(file_path, local_dir):
    resp = None
    try:
        file = minidom.parse(file_path)
        wh_site = file.getElementsByTagName(
            "DestinationId")[0].firstChild.nodeValue

        local_site_dir = local_dir + "/" + wh_site
        resp = {
            "file_dir": local_site_dir,
            "file_name": os.path.basename(file_path)
        }

        _wh_list = {"1236": "cch"}
        if wh_site in _wh_list:
            postFile(file_path, _wh_list[wh_site]);

    except Exception as e:
        print(e)
    return resp


def main():
    _db = db()
    config = _db.getConfig()
    local_dir = config['DES_OUT_CLAIM_REQUEST']
    remote_dir = config['SOURCE_OUT_CLAIM_REQUEST']
    delay_time = 300

    _db.close()
    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        obj.connect()
        obj.run(loadFile)
