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
from ovlibs import ovsftp, db
from xml.dom import minidom
import os

_db = db()

def loadFile(file_path, local_dir):
    resp = None
    try:
        file = minidom.parse(file_path)
        obj_number = file.getElementsByTagName(
            "ClaimId")[0].firstChild.nodeValue

        wh_site = ""
        obj = _db.getMapping(obj_number)

        if obj != None:
            wh_site = obj['Val']

        if wh_site != "":
            resp = {
                "file_dir": local_dir + "/" + wh_site,
                "file_name": 'STOResult_' + obj_number + '.xml'
            }

    except Exception as e:
        print(e)
    return resp


def main():
    _db = db()
    config = _db.getConfig()

    local_dir = config['DES_OUT_CLAIM_RESULT']
    remote_dir = config['SOURCE_OUT_CLAIM_RESULT']
    delay_time = 60

    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        obj.connect()
        obj.run(loadFile)