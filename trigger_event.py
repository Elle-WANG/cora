#!/user/bin/env python3

import os
import time
import requests
import xmltodict
import argparse
import logging
# from io import StringIO

import smtplib
from email.message import EmailMessage

'''
To check if a SBID was deposited/released
'''

# log_stream = StringIO()
log = logging.getLogger(__name__)

__author__ = "Yuanming Wang <yuanmingwang@swin.edu.au>"


def _main():
    parser = argparse.ArgumentParser(prog='VOevent', description='VO Event trigger')
    parser.add_argument('sbid', nargs='+')
    parser.add_argument('-d', '--deposited', action='store_true', 
                        help='check DEPOSITED sbid instead of the default RELEASED sbid')
    parser.add_argument('-e', '--email', default=None, nargs='+', 
                        help='send email notification to a list of email addresses')
    parser.add_argument('-r', '--refresh-rate', default=600, type=int, 
                        help='Refresh rate for data checking in unit of seconds. Default is every 10min')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='make it verbose')
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(
            # stream=log_stream, 
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(
            # stream=log_stream, 
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

    log.debug(args)


    if args.email is not None:
        # sender_email = input("Enter sender gmail address: ")
        sender_email = 'wym20131028@gmail.com'
        sender_pwd = os.getenv('SMTP_PWD')


    while True:

        moodlist = []
        for sbid in args.sbid:
            mood = get_voevent(sbid, args)
            moodlist.append(mood)

        if moodlist.count('Yayy') != 0 and args.email is not None:
            log.info('Excellent - ready to send an email...')
            # msgs = log_stream.getvalue()
            # print(msgs)
            body = ' '.join(args.sbid) + '\n' + ' '.join(moodlist)

            for receiver_email in args.email:
                email_alert(body, sender_email, sender_pwd, receiver_email)
                log.info('Yayy!!!')
            
            break

        else:
            log.info('----------------------------')

        time.sleep(args.refresh_rate)



def get_voevent(sbid, args):

    if args.deposited:
        endpoint_template = "https://casda.csiro.au/casda_data_access/observations/events?sbid={}&event=DEPOSITED"
    else:
        endpoint_template = "https://casda.csiro.au/casda_data_access/observations/events?sbid={}&event=RELEASED"

    endpoint_url = endpoint_template.format(sbid)

    r = requests.get(endpoint_url)
    data_dict = xmltodict.parse(r.content)

    if 'voe:VOEvent' in data_dict['list'].keys():
        log.info('%s is available', sbid)
        return 'Yayy'
    
    else:
        log.info('%s is not available', sbid)
        return 'Hmmm'



def email_alert(body, sender_email, sender_pwd, receiver_email):

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = 'CORA observations are available'
    msg['from'] = sender_email
    msg['to'] = receiver_email

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(sender_email, sender_pwd)
    # sending the mail
    # s.sendmail(sender_email, receiver_email, msgs)
    s.send_message(msg)
    # terminating the session
    s.quit()
    


if __name__ == '__main__':
    _main()    
