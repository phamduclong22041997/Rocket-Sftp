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
import re
import os

# _db_mapping = db()

def loadFile(file_path, local_dir):
    resp = None
    try:
        client_code = os.getenv('CLIENT_CODE')
        file = minidom.parse(file_path)
        wh_site = file.getElementsByTagName(
            "SourceId")[0].firstChild.nodeValue
        sto_status = file.getElementsByTagName(
            "Status")[0].firstChild.nodeValue
        
        po_eles = file.getElementsByTagName("Poid")
        do_list = []
        for ele in po_eles:
            val = ele.firstChild.nodeValue
            is_exists = val in do_list
            if is_exists == False:
                do_list.append(val)
        sto_number = "_".join(do_list)
        stofc_number = "_".join(do_list)
        do_id = file.getElementsByTagName(
            "DoId")[0].firstChild.nodeValue
        sto_number = do_id
        # if len(do_list) > 1:
        #     sto_number = do_id
        # else:
        #     if client_code == "PLH":
        #         sto_number = do_id
            
        #  pass for uat test
        if wh_site == '1293':
            sto_number = do_id
        
        if sto_status == 'A':
            local_site_dir = local_dir + "/" + wh_site
            resp = {
            "file_dir": local_site_dir,
            "file_name": 'DO_' + sto_number + '.xml'
        }

        # FC flow
        if re.search("^83", do_id) and sto_status == 'A':
            site_id = file.getElementsByTagName(
            "DestinationId")[0].firstChild.nodeValue
            if os.path.exists(local_dir + "/" + wh_site + "/" + 'DO_' + stofc_number + '.xml') == False:
                request.postFCRequest({
                    "ObjectCode": do_id,
                    "SiteId": wh_site,
                    "IssueSite": site_id,
                    "RequestType": "DO",
                    "FilePath": local_dir + "/" + wh_site + "/" + 'DO_' + stofc_number + '.xml'
                })
            resp = {
            "file_dir": local_site_dir,
            "file_name": 'DO_' + sto_number + '.xml'
            }
        # GR flow
        # if client_code == 'PLH' and re.search("^88", do_id) and sto_status == 'C':
        #     wh_site = file.getElementsByTagName(
        #         "DestinationId")[0].firstChild.nodeValue
        #     _resp = _db_mapping.hasDCSite(wh_site)
        #     if _resp == True:
        #         site_id = file.getElementsByTagName(
        #         "SourceId")[0].firstChild.nodeValue

        #         local_site_dir = local_dir + "/" + wh_site
        #         resp = {
        #             "file_dir": local_site_dir,
        #             "file_name": 'DO_' + do_id + '.xml'
        #         }
        #         if os.path.exists(local_dir + "/" + wh_site + "/" + 'DO_' + do_id + '.xml') == False:
        #             request.postGRRequest({
        #                 "ObjectCode": do_id,
        #                 "ClientCode": "PLH",
        #                 "SiteId": site_id,
        #                 "IssueSite": wh_site,
        #                 "RequestType": "GR_PO",
        #                 "FilePath": local_dir + "/" + wh_site + "/" + 'DO_' + do_id + '.xml'
        #             })

    except Exception as e:
        print(e)
    return resp


def main():
    _db = db()
    config = _db.getConfig()
    local_dir = config['DES_OUT_DO']
    remote_dir = config['SOURCE_OUT_DO']
    delay_time = 2
    _db.close()

    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        obj.connect()
        obj.run(loadFile)
