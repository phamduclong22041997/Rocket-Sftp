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
import sys
import os
import time
import asyncio
import threading
from dotenv import load_dotenv
from sap import delivery_order, purchase_order, po2_gr, sync_file, reverse_do, fc_so, fc_purchase, sor_tray

load_dotenv()

def main(argv):
    if os.environ["OV_SFTP_SECRET"] != '':
        # delivery order
        print("Running...")
        delivery_order_client = threading.Thread(target=delivery_order.main)
        delivery_order_client.start()

        time.sleep(5)

        # # purchase order
        purchase_order_client = threading.Thread(target=purchase_order.main)
        purchase_order_client.start()

        time.sleep(5)

        # #  GR
        po2_gr_client = threading.Thread(target=po2_gr.main)
        po2_gr_client.start()


        time.sleep(5)

        # reverse_do
        reverse_do_client = threading.Thread(target=reverse_do.main)
        reverse_do_client.start()

        time.sleep(5)

        # Sync file
        sync_file_client = threading.Thread(target=sync_file.main)
        sync_file_client.start()

        time.sleep(5)

        # Sync file
        fc_so_client = threading.Thread(target=fc_so.main)
        fc_so_client.start()

        # Sync file
        fc_purchase_client = threading.Thread(target=fc_purchase.main)
        fc_purchase_client.start()

        # # claim request
        # claim_request_client = threading.Thread(target=claim_request.main)
        # claim_request_client.start()

        # # claim request
        # claim_return_client = threading.Thread(target=claim_return.main)
        # claim_return_client.start()

        # time.sleep(5)
        # sync_file_golden_buy = threading.Thread(target=golden_buy.main)
        # sync_file_golden_buy.start()


        sor_pull_file = threading.Thread(target=sor_tray.main)
        sor_pull_file.start()

if __name__ == "__main__":
    main(sys.argv[1:])
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()
