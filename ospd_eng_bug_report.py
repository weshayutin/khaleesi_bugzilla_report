#!/usr/bin/python3

import ast
import bugzilla
from datetime import datetime
from email.mime.text import MIMEText
import os
import pytz
from dateutil.relativedelta import *
import smtplib

import pdb
msg = ""

#pushd  ~/git/RDO-CI/khaleesi/playbooks/; egrep -rn rhbz | sed 's/.*rhbz//' | cut -b 1-7 > /tmp/list
bz = bugzilla.Bugzilla(url='https://bugzilla.redhat.com/xmlrpc.cgi')
bz.login(os.environ['BZ_USER'], os.environ['BZ_PASSWORD'])
team_to_email = ast.literal_eval(os.environ['TEAM_TO_EMAIL'])
email_server = smtplib.SMTP('smtp.corp.redhat.com', 25)


def email_send(email_from, email_to, subject, body):
    email = MIMEText(str(body))
    email['From'] = email_from
    email['To'] = email_to
    email['Subject'] = subject
    email_server.send_message(email)

# send a list of bugs to the method
def report(bugs):
    msg = ""
    msg += "*"*180 + "\n\n"
    msg += os.environ['TEAM_INTRO_MSG']
    msg += '\n\n'
    msg += "*"*160 + "\n\n"
    msg += "{0:<10} {1:>11} {2:>25}: {3:<15} {4:<40} {5:>30}\n".format("status", "osp version", "component", "severity", "bz url ", "summary")
    msg += "-"*160
    msg += "\n\n"
    bug_list = bz.getbugs(bugs)
    for bug in bug_list:
        #pdb.set_trace()
        msg += "{0:<10} {1:>11} {2:>25}: {3:<15} {4:<40} {5:>30}\n\n".format(bug.status, bug.version, bug.component, bug.severity, bug.weburl, bug.summary )
    return msg


#MAIN

def get_list_of_bugs(file):
    with open(file, "r") as f:
        content = f.read().splitlines()
    return content

list = get_list_of_bugs("/tmp/buglist")
msg = report(list)
print(msg)


email_send(os.environ['REPORT_OWNER'], os.environ['REPORT_LIST'], 'openstack ci workaround/skip report', msg)

