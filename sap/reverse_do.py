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
import logging


def loadFile(file_path, local_dir):
    resp = None
    try:
        file = minidom.parse(file_path)
        do_id = file.getElementsByTagName(
            "DeliveryDocument")[0].firstChild.nodeValue
        resp = {
            "file_dir": local_dir,
            "file_name": 'RET_REVERSE_GI_DO_' + do_id + '.xml'
        }

    except Exception as e:
        logging.error(e, exc_info=True)
        print(e)

    return resp


def main():
    _db = db()
    config = _db.getConfig()
    local_dir = config["DES_OUT_DO_REVERSE"] if config["DES_OUT_DO_REVERSE"] else ""
    remote_dir = config["SOURCE_OUT_DO_REVERSE"] if config["SOURCE_OUT_DO_REVERSE"] else ""
    delay_time = 45
    _db.close()

    if local_dir != '' and remote_dir != '':
        obj = ovsftp({"remote_dir": remote_dir,
                      "local_dir": local_dir, "delay_time": delay_time})
        obj.connect()
        obj.run(loadFile)
