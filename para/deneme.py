# -*- coding: utf-8 -*-

"""Notification for Indicative Exchange Rates Announced by the Central Bank of Turkey for Python

Usage: para [options]

Options:
  -h, --help              show this help
  -e  --email             send notification email.
  -r  --refresh           refresh para.conf file

Examples:
  para      shows EURO and US DOLLAR information
  para -e   send email for  EURO and US DOLLAR information.You can create cron job for receive email periodicly
  para -r   refresh para.conf file smtp information

"""

import os
import sys
import getopt
import smtplib
from xml.etree.ElementTree import parse
import urllib2
from email.mime.text import MIMEText
import ConfigParser


DEFAULTS = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': '587',
    'CONFIG_FILE': '~/.para.conf',
    'URL': "http://www.tcmb.gov.tr/kurlar/today.xml"
}


def create_para_config():

    if os.path.exists(os.path.expanduser(DEFAULTS.get('CONFIG_FILE'))):
        print "dosya var"

    username = raw_input('Enter your gmail account username:')
    password = raw_input('Enter your gmail account password:')

    try:
        file_dir = os.path.expanduser('~')
        config_file = open(file_dir+'/.para.conf', 'w')
        config_string = '[EMAILINFO]\nSMTP_USERNAME=%s\nSMTP_PASSWORD=%s\nSMTP_SERVER=%s\nSMTP_PORT=%s' % (username, password, DEFAULTS.get('SMTP_SERVER'), DEFAULTS.get('SMTP_PORT'))
        config_file.write(config_string)
        config_file.close()

    except Exception, e:
        print(e)


def get_para_config():

    config = ConfigParser.ConfigParser()
    if os.path.exists(os.path.expanduser(DEFAULTS.get('CONFIG_FILE'))):
        try:
            config.read(os.path.expanduser(DEFAULTS.get('CONFIG_FILE')))
        except Exception, e:
            print(e)
            sys.exit(2)
        return config
    else:
        create_para_config()
        try:
            config.read(os.path.expanduser(DEFAULTS.get('CONFIG_FILE')))
        except Exception, e:
            print(e)
            sys.exit(2)
        return config

def get_url():
    return DEFAULTS.get('URL')


def print_values():

    url = get_url()
    message = get_data(url)
    print(message)

def get_data(url):

    kur_xml = urllib2.urlopen(url)
    doc = parse(kur_xml)
    message = ""
    for item in doc.iterfind('Currency'):
        currency_name = item.findtext('CurrencyName')

        if currency_name:
            forex_buying = item.findtext('ForexBuying')
            forex_selling = item.findtext('ForexSelling')
            banknote_buying = item.findtext('BanknoteBuying')
            banknote_selling = item.findtext('BanknoteSelling')
            message += ("\n\t\t\tDöviz Alış\tDöviz Satış\tEfektif Alış\tEfektif Satış\n%s\t\t%s\t\t%s\t\t%s\t\t%s\n" % (currency_name, forex_buying, forex_selling, banknote_buying, banknote_selling))
    return message

def refresh_config():

    if not os.path.exists(os.path.expanduser(DEFAULTS.get('CONFIG_FILE'))):
        raise LookupError("config file not found.try -h or --help command")

    username = raw_input('Enter your gmail account username:')
    password = raw_input('Enter your gmail account password:')

    try:
        file_dir = os.path.expanduser('~')
        config_file = open(file_dir+'/.para.conf', 'w')
        config_string = '[EMAILINFO]\nSMTP_USERNAME=%s\nSMTP_PASSWORD=%s\nSMTP_SERVER=%s\nSMTP_PORT=%s' % (username, password, DEFAULTS.get('SMTP_SERVER'), DEFAULTS.get('SMTP_PORT'))
        config_file.write(config_string)
        config_file.close()
    except Exception, e:
        print(e)
        exit(2)

def usage():
    print __doc__

def send_mail():

    url = get_url()
    config = get_para_config()
    if config:

        EMAIL_USERNAME = config.get('EMAILINFO', 'SMTP_USERNAME')
        EMAIL_PASSWORD = config.get('EMAILINFO', 'SMTP_PASSWORD')
        SMTP_SERVER = DEFAULTS.get('SMTP_SERVER')
        SMTP_PORT = DEFAULTS.get('SMTP_PORT')

        message = get_data(url)

        msg = MIMEText(message)
        msg['Subject'] = "TCMB Kurları"
        msg['To'] = EMAIL_USERNAME
        msg['From'] = 'notifier@para.com'
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail('noreply@para.py', EMAIL_USERNAME, msg.as_string())
        server.quit()
    else:
        print('No config file')

def main(argv):

    try:
        opts, args = getopt.getopt(argv, 'ehr', ['email', 'help', 'refresh'])
        if not opts:
            print_values()
    except Exception, e:
        print(e)
        usage()
        sys.exit(2)

    for opt, args in opts:

        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)

        elif opt in ('-e', '--email'):
            send_mail()

        elif opt in ('-r', '--refresh'):
            refresh_config()

        else:
            usage()
            sys.exit(2)


if __name__ == '__main__':

    main(sys.argv[1:])














