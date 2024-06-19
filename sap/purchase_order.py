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
import logging
import os

def loadFile(file_path, local_dir):
    resp = None
    try:
        file = minidom.parse(file_path)
        wh_site = file.getElementsByTagName(
            "Site")[0].firstChild.nodeValue
        doc_type = file.getElementsByTagName(
            "DocumentType")[0].firstChild.nodeValue
        po_id = file.getElementsByTagName(
            "POID")[0].firstChild.nodeValue

        local_site_dir = local_dir + "/" + wh_site
        
        allow_sync = ['NB','ZCNB', 'ZUR','ZRNB']
        client_code = os.getenv('CLIENT_CODE')

        if client_code != "":
            allow_sync = ['ZNBP', 'ZUR']

        if doc_type in allow_sync:
            local_site_dir = local_dir + "/" + wh_site
            resp = {
                "file_dir": local_site_dir,
                "file_name": 'PO_' + po_id + '.xml'
            }
        print("log", resp)
        remote_sites = os.getenv('REMOTE_SITES')
        if (doc_type == 'NB' or doc_type == 'ZNBP') and remote_sites != "" and remote_sites.find(wh_site) != -1:
            local_site_dir = local_dir + "/" + wh_site
            resp = {
                "file_dir": local_site_dir,
                "file_name": os.path.basename(file_path),
                "po_id": po_id,
                "wh_site": wh_site
            }
        remote_sor_sites = os.getenv('REMOTE_SOR_SITES')
        if doc_type == 'ZUR' and remote_sor_sites != "" and remote_sor_sites.find(wh_site) != -1:
            resp = {
                "request_type": "REQUEST_CREATE_SOR",
                "file_dir": local_site_dir,
                "file_name": os.path.basename(file_path),
                "po_id": po_id,
                "wh_site": wh_site
            }

        # if doc_type == "UB" and po_id != None:
        #     warehouse_siteid = file.getElementsByTagName("RECIPNT_NO")[0].firstChild.nodeValue
        #     request.postRequest({
        #     "ObjectCode": po_id,
        #     "SiteId": wh_site,
        #     "IssueSite":warehouse_siteid,
        #     "RequestType": "CREATE_STO_FROM_SFTP",
        #     "FilePath":  local_dir + "/" + warehouse_siteid + "/" + 'PO_' + po_id + '.xml'
        # })
        print("check resp", resp)
            # request.postRequest({
            #     "ObjectCode": po_id,
            #     "SiteId": wh_site,
            #     "IssueSite": wh_site,
            #     "RequestType": "CREATE_PO_FROM_SFTP",
            #     "FilePath": local_site_dir + '/PO_' + po_id + '.xml'
            # })
            # request.postFile(file_path, "PO");

    except Exception as e:
        logging.error(e, exc_info=True)
        print(e)

    return resp

def sendRocketRequest(data):
    if "po_id" in data:
        request.postRequest({
            "ObjectCode": data["po_id"],
            "SiteId": data["wh_site"],
            "IssueSite": data["wh_site"],
            "RequestType": data.get("request_type", "CREATE_PO_FROM_SFTP"),
            "FilePath": data["file_dir"] + '/' + data["file_name"]
        })

def main():
    _db = db();
    config = _db.getConfig()
    local_dir = config['DES_OUT_PO']
    remote_dir = config['SOURCE_OUT_PO']
    delay_time = 2
    _db.close();
    print(local_dir,'=local_dir=',remote_dir,'=remote_dir=')
    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        
        obj.set_move_forward(sendRocketRequest)
        obj.connect()
        obj.run(loadFile)