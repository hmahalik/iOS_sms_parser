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
