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
import subprocess
import shutil
import pysftp
import time
from datetime import datetime
import pytz
import jwt
import logging
import gc
import json
from . import logs

timeZone = pytz.timezone('Asia/Ho_Chi_Minh')

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

class ovsftp:
    def __init__(self, config):
        self.sftp = None
        self.MAX_FILE_IN_DIR = 10
        self.remote_dir = config['remote_dir']
        self.local_dir = config['local_dir']
        self.local_tmp_dir = "/tmp/" + os.path.basename(config['local_dir'])
        self.delay_time = config["delay_time"] if config["delay_time"] else 3
        self.logs = logs.logs()
        self.secret_config = None
        self.move_forward = None
        _secret_config = os.environ['OV_SFTP_SECRET'] if os.environ['OV_SFTP_SECRET'] else None
        if _secret_config == None:
            raise Exception("Invalid config")
        self.secret_config = jwt.decode(_secret_config, options={
                                        "verify_signature": False})
        self.__init()

    def connect(self):
        try:
            if self.sftp == None:
                # cnopts.hostkeys = None or disableHostKey checking (cnopts.hostkeys = None).
                self.sftp = pysftp.Connection(
                    host=self.secret_config['HOST'],
                    username=self.secret_config['USER'],
                    password=self.secret_config['PASS'],
                    # port=self.secret_config['PORT'],
                    cnopts=self.cnopts
                )
                if self.hostkeys != None:
                    print("Connected to new host, caching its hostkey")
                    self.hostkeys.add(self.secret_config['HOST'], self.sftp.remote_server_key.get_name(
                    ), self.sftp.remote_server_key)
                    self.hostkeys.save(pysftp.helpers.known_hosts())
        except Exception as e:
            print(e)
            logging.error(e, exc_info=True)
            self.sftp = None

    def close(self):
        if self.sftp != None:
            try:
                self.sftp.close()
                time.sleep(10)
                self.sftp = None
            except:
                pass

    def __init(self):
        self.cnopts = pysftp.CnOpts()
        self.hostkeys = None
        if self.cnopts.hostkeys.lookup(self.secret_config['HOST']) == None:
            print("New host - will accept any host key")
            # Backup loaded .ssh/known_hosts file
            self.hostkeys = self.cnopts.hostkeys
            # And do not verify host key of the new host
            self.cnopts.hostkeys = None

        if not os.path.exists(self.local_tmp_dir):
            os.makedirs(self.local_tmp_dir)

        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)

        # if not os.path.exists("/root/.ssh/known_hosts"):
        #     secret_config = os.environ['OV_SFTP_SECRET'] if os.environ['OV_SFTP_SECRET'] else None
        #     if secret_config == None:
        #         raise Exception("Invalid config")
        #     secret_config = jwt.decode(secret_config, options={
        #                                "verify_signature": False})
        #     cmd = "ssh-keyscan -t rsa " + secret_config['HOST'] + " >> /root/.ssh/known_hosts"
        #     os.system(cmd)
        # time.sleep(1)

    def download_files(self, callback=None):
        if self.sftp != None:
            while True:
                print(self.remote_dir);
                if self.remote_dir == None:
                    continue

                fileList = self.sftp.listdir(self.remote_dir)
                total_files = 0
                while len(fileList) > 0:
                    filename = fileList.pop()
                    if total_files >= self.MAX_FILE_IN_DIR:
                        total_files = 0
                        self.move_file(callback)
                        gc.collect()
                    total_files += 1
                    self.sftp.get(self.remote_dir + "/" + filename,
                                self.local_tmp_dir + "/" + filename, preserve_mtime=True)
                
                self.move_file(callback)
                gc.collect()
                time.sleep(self.delay_time);

    def run(self, callback = None):
        try:
            now = datetime.now()
            print("Download file in directory: ", self.remote_dir)
            print("Start at: ", now.strftime("%Y/%m/%d %H:%M:%S"))
            self.connect()
            self.download_files(callback)
            self.close()
        except Exception as e:
            logging.error(e, exc_info=True)
            self.close()

        try: 
            self.move_file(callback)
        except:
            pass;
        self.close()
        gc.collect()
        now = datetime.now()
        print("End at: ", now.strftime("%Y/%m/%d %H:%M:%S"))
        if self.delay_time > 0:
            print("Waiting for next [", format(
                self.delay_time), " seconds]")
            self.next(callback)
    
    def move_file(self, callback = None):
        self.move(callback)

    def next(self, callback=None):
        time.sleep(self.delay_time)
        self.run(callback)

    def copy(self):
        try:
            self.sftp.get_d(self.remote_dir, self.local_tmp_dir,
                            preserve_mtime=True)
        except Exception as e:
            logging.error(e, exc_info=True)
            raise Exception("Error: Copy file from sftp");

    def write(self, localPath, remotePath):
        if is_non_zero_file(localPath) == False:
            return None
        try:
            self.connect()
            rs = self.sftp.put(localpath=localPath, remotepath=remotePath)
            return rs.__dict__
        except Exception as e:
            print(localPath)
            print("remote ====",remotePath)
            logging.error(e, exc_info=True)
            self.close();
            raise Exception("Error: write file from sftp", e);

    def move(self, callback=None):
        now = datetime.now(timeZone)
        for file_name in os.listdir(self.local_tmp_dir):
            try:
                _allow_move_file = False
                _file_metadata = False
                _local_file_path = self.local_dir
                _new_file_name = file_name
                if callback != None:
                    resp = callback(self.local_tmp_dir + "/" +
                                    file_name, self.local_dir)
                    if resp != None:
                        _allow_move_file = True
                        _local_file_path = resp['file_dir']
                        _new_file_name = resp['file_name']
                        _file_metadata = resp.get("file_metadata")

                _local_file_path = _local_file_path + "/" + _new_file_name
                _local_dir = os.path.dirname(_local_file_path)
                _local_backup_dir = self.local_dir + \
                    "/backup/" + now.strftime("%Y/%m/%d")

                if not os.path.exists(_local_dir):
                    os.makedirs(_local_dir)
                if not os.path.exists(_local_backup_dir):
                    os.makedirs(_local_backup_dir)

                if self.logs != None:
                    self.logs.save({
                        "SrcFileName": file_name,
                        "DesFileName": _new_file_name,
                        "DesFilePath": _local_file_path,
                        "CreatedDate": datetime.now(timeZone),
                        "UpdatedDate": datetime.now(timeZone),
                        "Keygen": datetime.now(timeZone).strftime("%Y%m%d")
                    })
                if _allow_move_file == True:
                    shutil.copy(self.local_tmp_dir + "/" + 
                                file_name, _local_file_path)
                    
                    if _file_metadata:
                        # write_metadata
                        self.write_metadata(_local_file_path.replace(".xml", ".json"), {
                            "file_path": _local_file_path,
                            "original_file_name": file_name,
                            "received_date": datetime.now(timeZone).strftime("%Y%m%d %H:%M:%S")
                        })

                    
                    # Trigger request
                    if self.move_forward != None:
                        self.move_forward(resp)
                
                shutil.copy(self.local_tmp_dir + "/" + file_name,
                            _local_backup_dir + "/" + file_name)
                os.remove(self.local_tmp_dir + "/" + file_name)
                
                if os.path.exists(_local_backup_dir + "/" + file_name):
                    if is_non_zero_file(_local_backup_dir + "/" + file_name) == True:
                        print("R: " + self.remote_dir + "/" + file_name)
                        self.sftp.remove(self.remote_dir + "/" + file_name)
            except Exception as e:
                logging.error(e, exc_info=True)
                raise Exception("Error: Move file")

    def count(self):
        cmd = 'ls ' + self.local_tmp_dir + ' | wc -l'
        res = subprocess.run(cmd, capture_output=True, shell=True)
        return int(res.stdout.decode().strip())
    
    def set_move_forward(self, func):
        self.move_forward = func
    
    def write_metadata(self, file_path, data):
        try:
            with open(file_path, "w") as outfile:
                outfile.write(json.dumps(data))
        except:
            pass
