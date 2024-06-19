#
# @copyright
# Copyright (c) 2023 OVTeam
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

def loadFile(file_path, local_dir):
    try:
        return {
            "file_dir": local_dir,
            "file_name": os.path.basename(file_path)
        }
    except Exception as e:
        print(e)
    return None

def run():
    try:
        _db = db()
        config = _db.getConfig()
        local_dir = config.get('LOCAL_FILE_GOLDEN_BUY_SALE_PRICE')
        remote_dir = config.get('SOURCE_FILE_GOLDEN_BUY_SALE_PRICE')
        delay_time = 2
        _db.close()

        if local_dir != '' and remote_dir != '':
            obj = ovsftp({"remote_dir": remote_dir,
                            "local_dir": local_dir, "delay_time": delay_time})
            obj.connect()
            obj.run(loadFile)
    except Exception as e:
        print(e)
        pass

def main():
    while True:
        print('Begin download files GOLDEN BUY')
        run()
        time.sleep(300)
        print('End download files GOLDEN BUY')
