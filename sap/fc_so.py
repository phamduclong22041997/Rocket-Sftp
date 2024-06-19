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

from ovlibs import ovsftp, db, request
from xml.dom import minidom
import os

def loadFile(file_path, local_dir):
    resp = None
    try:
        file = minidom.parse(file_path)
        wh_site = file.getElementsByTagName(
            "SourceId")[0].firstChild.nodeValue

        do_id = file.getElementsByTagName(
            "DOID")[0].firstChild.nodeValue
        
        local_site_dir = local_dir + "/" + wh_site
        resp = {
            "file_dir": local_site_dir,
            "file_name": 'SO_' + do_id + '.xml'
        }

        site_id = file.getElementsByTagName(
        "DestinationId")[0].firstChild.nodeValue

        reason_code = ""
        try:
            reason_node = file.getElementsByTagName(
            "ReasonCode")
            if reason_node != None:
                reason_code = reason_node[0].firstChild.nodeValue
        except:
            reason_code = ""
            pass

        if os.path.exists(local_site_dir + "/" + 'SO_' + do_id + '.xml') == False:
            _request_type = "STO"
            if reason_code == "Z6":
                _request_type = "CANCEL_STO"

            request.postFCRequest({
                "ObjectCode": do_id,
                "SiteId": wh_site,
                "IssueSite": site_id,
                "RequestType": _request_type,
                "FilePath": local_site_dir + "/" + 'SO_' + do_id + '.xml'
            })

    except Exception as e:
        print(e)
    return resp


def main():
    _db = db()
    config = _db.getConfig()
    local_dir = config['DES_OUT_FC_SO']
    remote_dir = config['SOURCE_OUT_FC_SO']
    delay_time = 6
    _db.close()

    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        obj.connect()
        obj.run(loadFile)
