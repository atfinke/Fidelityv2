import argparse
import datetime
import logging
import os
import re

from apscheduler.schedulers.blocking import BlockingScheduler
import google.cloud.logging
import requests

def fetch():
    s = requests.Session()
    login_url = 'https://login.fidelity.com/ftgw/Fas/Fidelity/RtlCust/Login/Response/'

    with open('username.txt', 'r') as myfile:
        username = myfile.read().replace('\n', '')

    with open('password.txt', 'r') as myfile:
        password = myfile.read().replace('\n', '')

    payload = {
        'SSN': username,
        'PIN': password,
    }

    logging.info("Fidelity: Payload - " + str(payload))

    s.post(login_url, data=payload, headers=dict(
        referer='https://login.fidelity.com'))

    response = s.get(
        'https://oltx.fidelity.com/ftgw/fbc/ofpositions/snippet/portfolioPositions?ALL_ACCTS=Y&SAVE_SETTINGS_WASH_SALE=N&UNADJUSTED_COST_BASIS_INFORMATION=&EXCLUDE_WASH_SALE_IND=&SHOW_FOREIGN_CURRENCY=&REFRESH_DATA=N&REPRICE_FROM_CACHE=Y&ALL_POS=Y&ALL_ACCTS=Y&TXN_SORT_ORDER=0&TABLE_SORT_ORDER=0&TABLE_SORT_DIRECTION=A&SAVE_SETTINGS=N&pf=N&CSV=Y&TXN_COLUMN_SORT_JSON_INFO=&SORT_COL_IND=&IS_ACCOUNT_CHANGED=Y&DISP_FULL_DESC=Y&FONT_SIZE=S&viewBy=&displayBy=&group-by=0&desc=0&NEXTGEN=Y&ACTION=&SHOW_FULL_SECURITY_NAME=N&REQUESTED_SHOW_TYPE_IND=All&REQUESTED_SHOW_TYPE_IND=Mutual+Funds&REQUESTED_SHOW_TYPE_IND=Stocks%2FETFs&REQUESTED_SHOW_TYPE_IND=Cash&REQUESTED_SHOW_TYPE_IND=CIT%2F529')

    if response.status_code == 200:
        disposition = response.headers['content-disposition']
        file_name = re.findall("filename=(.+)", disposition)

        file_path = "output/"
        if len(file_name) > 0:
            file_path += file_name[0].replace('"', '')
        else:
            file_path += datetime.datetime.now().strftime("%m-%d-%Y-%H-%M") + ".csv"

        with open(file_path, 'wb') as f:
            f.write(response.content)
            logging.info("Fidelity: Saved File")
    else:
        logging.error("Fidelity: Error Occurred")
        logging.error(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", required=False, action="store_true")
    args = parser.parse_args()

    if not os.path.exists("output"):
        os.makedirs("output")

    if args.server:
        client = google.cloud.logging.Client()
        client.setup_logging()

        sched = BlockingScheduler()
        sched.add_job(fetch, 'cron', day_of_week='1-5', hour='1')
        sched.start()
    else:
        logging.basicConfig(filename='output/fid.log', level=logging.DEBUG)
        fetch()
