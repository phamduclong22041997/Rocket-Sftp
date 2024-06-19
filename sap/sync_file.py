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
import os
import time
from datetime import datetime
import logging


def syncFile():
    _db = db()
    local_dir = "SyncFile"
    remote_dir = os.environ['SFTP_REMOTE_PATH']
    delay_time = 60
    _sftp = ovsftp({"remote_dir": remote_dir,
                    "local_dir": local_dir, "delay_time": 0})
    while True:
        file_list = None
        site_list = None
        try:
            site_list = _db.getSyncSites()
        except Exception as e:
            print(e)
            _db.close()
        if site_list != None and len(site_list) > 0:
            try:
                _sftp.connect()
                for site in site_list:
                    file_list = _db.getSyncFileList(site['_id'])
                    if file_list != None and file_list.count() > 0:
                        now = datetime.now()
                        print(file_list)
                        print("Start put file: ", now.strftime(
                            "%Y/%m/%d %H:%M:%S"))
                        for item in file_list:
                            print(os.path.exists(item['LocalFilePath']))
                            if os.path.exists(item['LocalFilePath']) == True:
                                print("vao")
                                rs = _sftp.write(item['LocalFilePath'],
                                                 item['RemoteFilePath'])
                                print("rs==")
                                print(rs)
                                if rs != None:
                                    _db.updateSyncFile(item['_id'], rs)
                        print("End put file: ", now.strftime(
                            "%Y/%m/%d %H:%M:%S"))
                _sftp.close()
            except Exception as e:
                print("log error", e)
                logging.error(e, exc_info=True)
                _sftp.close()

        # Using for SFT2
        syncFileV2()
        
        time.sleep(delay_time)

def syncFileV2():
    _db = db()
    local_dir = "SyncFile"
    remote_dir = os.environ['SFTP_REMOTE_PATH']
    delay_time = 60
    _sftp = ovsftp({"remote_dir": remote_dir,
                    "local_dir": local_dir, "delay_time": 0})
    file_list = None
    site_list = None
    try:
        site_list = _db.getSyncSites(db_name=os.getenv('DB_ADMIN_V2_NAME'))
    except Exception as e:
        print(e)
        _db.close()
    if site_list != None and len(site_list) > 0:
        try:
            _sftp.connect()
            for site in site_list:
                file_list = _db.getSyncFileList(options=site['_id'], db_name=os.getenv('DB_ADMIN_V2_NAME'))
                if file_list != None and file_list.count() > 0:
                    now = datetime.now()
                    print("Start put file: ", now.strftime(
                        "%Y/%m/%d %H:%M:%S"))
                    for item in file_list:
                        if os.path.exists(item['LocalFilePath']) == True:
                            rs = _sftp.write(item['LocalFilePath'],
                                                item['RemoteFilePath'])
                            if rs != None:
                                _db.updateSyncFile(id=item['_id'], results=rs, db_name=os.getenv('DB_ADMIN_V2_NAME'))
                    print("End put file: ", now.strftime(
                        "%Y/%m/%d %H:%M:%S"))
            _sftp.close()
        except Exception as e:
            logging.error(e, exc_info=True)
            _sftp.close()

    time.sleep(delay_time)

def main():
    syncFile()

def main2():
    _db = db()
    local_dir = "SyncFile"
    remote_dir = os.environ['SFTP_REMOTE_PATH']
    delay_time = 70
    _sftp = ovsftp({"remote_dir": remote_dir,
                    "local_dir": local_dir, "delay_time": 0})

    while True:
        file_list = None
        try:
            file_list = _db.getSyncFileList()
        except Exception as e:
            print(e)
            _db.close()
        if file_list != None and file_list.count() > 0:
            now = datetime.now()
            print("Start put file: ", now.strftime("%Y/%m/%d %H:%M:%S"))
            try:
                _sftp.connect()
                for item in file_list:
                    if os.path.exists(item['LocalFilePath']) == True:
                        rs = _sftp.write(item['LocalFilePath'],
                                         item['RemoteFilePath'])
                        if rs != None:
                            _db.updateSyncFile(item['_id'], rs)
                _sftp.close()
            except Exception as e:
                logging.error(e, exc_info=True)
                _sftp.close()
            print("End put file: ", now.strftime("%Y/%m/%d %H:%M:%S"))

        time.sleep(delay_time)
