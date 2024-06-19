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
import requests

def postFile(file_path, type):
    if os.environ["ROCKET_URL"] == "":
        return
    url = os.environ["ROCKET_URL"] + "/api/v1/receiveFile"

    payload={
    'Type': type}
    files=[
    ('file',(os.path.basename(file_path),open(file_path,'rb'),'text/xml'))
    ]
    headers = {
    'Authorization': 'Bearer ' + os.environ["OPS_INTERNAL_TOKEN"]
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

def postFCRequest(post_data):
    if os.environ["ROCKET_URL"] == "":
        return
    url = os.environ["ROCKET_URL"] + "/api/v1/fc/createFCRequest"

    payload= post_data
    headers = {
    'Authorization': 'Bearer ' + os.environ["OPS_INTERNAL_TOKEN"]
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("FC: {0}".format(response.text))

def postGRRequest(post_data):
    if os.environ["ROCKET_URL"] == "":
        return
    url = os.environ["ROCKET_URL"] + "/api/v1/sap/createGRRequest"

    payload= post_data
    headers = {
    'Authorization': 'Bearer ' + os.environ["OPS_INTERNAL_TOKEN"]
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("GR: {0}".format(response.text))

def postRequest(post_data):
    if os.environ["ROCKET_URL"] == "":
        return
    url = os.environ["ROCKET_URL"] + "/api/v1/sap/createRequest"

    payload= post_data
    headers = {
    'Authorization': 'Bearer ' + os.environ["OPS_INTERNAL_TOKEN"]
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("PO Request: {0}".format(response.text))