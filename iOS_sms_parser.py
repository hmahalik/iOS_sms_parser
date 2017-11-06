#! /usr/bin/env python
# -*- coding: cp1252 -*-

# iOS_sms_parser.py = Extracts SMS, iMessage and MMS from iOS sms.db.
# Verified for iOS 7 - 11.0.1
# Your data must have iOS11 messages or the script will not work
# Please validate on test data!
# Copyright (C) 2017 Heather Mahalik (heather@smarterforensics.com)
# Special thanks to the Cheeky4n6monkey for his guidance and patience me
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can view the GNU General Public License at <http://www.gnu.org/licenses/>
#
# Version History:
# v2017-10-28 Initial Version
 

import sys
import sqlite3
from optparse import OptionParser
from os import path

version_string = "iOS_sms_parser v2017-10-28"
print "Running " + version_string

usage = "Usage: %prog -d sms.db -o sms_output.tsv"

parser = OptionParser(usage=usage)
parser.add_option("-d", dest="smsdb", 
                  action="store", type="string",
                  help="sms database input file")
parser.add_option("-o", dest="outputtsv",
                  action="store", type="string",
                  help="Message output in Tab Separated format")

(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

if (options.smsdb == None):
    parser.print_help()
    print "\SMS database filename not specified!"
    exit(-1)

if (options.outputtsv == None):
    parser.print_help()
    print "\nOutput filename not specified!"
    exit(-1)

# check db file exists before trying to connect
if path.isfile(options.smsdb):
    chatscon = sqlite3.connect(options.smsdb)
else:
    print "Specified SMS Database does not exist!"
    exit(-1)

# open chat output file if reqd
if (options.outputtsv != None):
    try:
        import codecs
        outputfile = codecs.open(options.outputtsv, "w", "utf-8")
    except:
        print ("Trouble Opening SMS Output File For Writing")
        exit(-1)

# write header for contacts output file
if (options.outputtsv != None):
    outputfile.write("rowid\tchat_id\thandle_id\ttest\tservice\taccount\taccount_login\tchat_identifier\tmessage_date\tdate_read\tis_read\tlast_read_message_timestamp\tfilename\tcreated_date\tmime_type\ttotal_bytes\n")

smsquery = """SELECT message.rowid,
chat_message_join.chat_id,
message.handle_id,
message.text,
message.service,
message.account,
chat.account_login,
chat.chat_identifier,
datetime(message.date/1000000000 + 978307200,'unixepoch','localtime'),
case when LENGTH(chat_message_join.message_date)=18 then 
datetime(chat_message_join.message_date/1000000000 + 978307200,'unixepoch','localtime')
when LENGTH(chat_message_join.message_date)=9 then 
datetime(chat_message_join.message_date + 978307200,'unixepoch','localtime')
else 'NA'
END,
datetime(message.date_read + 978307200,'unixepoch','localtime'),
message.is_read,\
case when LENGTH(chat.last_read_message_timestamp)=18 then 
datetime(chat.last_read_message_timestamp/1000000000+978307200,'unixepoch','localtime')
when LENGTH(chat.last_read_message_timestamp)=9 then
datetime(chat.last_read_message_timestamp + 978307200,'unixepoch','localtime')
else 'NA'
END,
attachment.filename,
attachment.created_date,
attachment.mime_type,
attachment.total_bytes
FROM message
left join chat_message_join on chat_message_join.message_id=message.ROWID
left join chat on chat.ROWID=chat_message_join.chat_id
left join attachment on attachment.ROWID=chat_message_join.chat_id
order by message.date_read desc;"""


"""MESSAGE.ROWID = 0
CHAT_MESSAGE_JOIN.CHAT_ID = 1
MESSAGE.HANDLE_ID = 2
MESSAGE.TEXT = 3
MESSAGE.SERVICE = 4
MESSAGE.ACCOUNT = 5
CHAT.ACCOUNT_LOGIN = 6
CHAT.CHAT_IDENTIFIER = 7
CHAT_MESSAGE_JOIN.MESSAGE_DATE = 8
MESSAGE.DATE_READ = 9
MESSAGE.IS_READ = 10
CHAT.LAST_READ_MESSAGE_TIMESTAMP = 11
ATTACHMENT.FILENAME = 12
ATTACHMENT.CREATED_DATE = 13
ATTACHMENT.MIME_TYPE = 14
ATTACHMENT.TOTAL_BYTES = 15"""


chatcursor = chatscon.cursor()
chatcursor.execute(smsquery)

chatrow = chatcursor.fetchone()
chatcount = 0
while chatrow:
        #does this for each row
        #print chatrow # for now print it to command line.

        if (chatrow[3] is None):
            msg = ""
        else:
            msg = chatrow[3].replace('\n','<newline>').replace('\t','<tab>')
            
        outputfile.write(str(chatrow[0])+\
                         "\t" + str(chatrow[1])+\
                         "\t"+ str(chatrow[2])+\
                         "\t" + msg+\
                         "\t" + str(chatrow[4])+\
                         "\t" + str(chatrow[5])+\
                         "\t" + str(chatrow[6])+\
                         "\t" + str(chatrow[7])+\
                         "\t" + str(chatrow[8])+\
                         "\t" + str(chatrow[9])+\
                         "\t" + str(chatrow[10])+\
                         "\t" + str(chatrow[11])+\
                         "\t" + str(chatrow[12])+\
                         "\t" + str(chatrow[13])+\
                         "\t" + str(chatrow[14])+\
                         "\t" + str(chatrow[15])+\
                         "\n")
        chatcount += 1
        chatrow = chatcursor.fetchone() #get new row
#ends while chatrow
        
chatcursor.close()
chatscon.close()
outputfile.close()


print "\nExtracted " + str(chatcount) + "records\n"


exit(0)
