#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# CookieJar Grabber
#   Searches for cookies on the system it runs on, compares it with the CookieJar (sqlite database), and stores changes.
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import os
import platform
import sys
runpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath, '../lib'))

import argparse
from Config import Configuration as conf
from Cookie import Cookie
from MozillaGrabber import MozillaGrabber
from ChromiumGrabber import ChromiumGrabber
from ChromeGrabber import ChromeGrabber

# Functions
  
# Main
if __name__=='__main__':
  description='''Grabs all the cookies it can access, on the system it runs on'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-v', action='store_true',           help='Verbose')
  parser.add_argument('db', metavar='database', nargs='?', help='Database')
  args = parser.parse_args()

  db=args.db if args.db else conf.getCookieJar()
  if platform.system() == "Linux":
    sgrabbers=[MozillaGrabber(args), ChromiumGrabber(args)]
  elif platform.system() == "Windows":
    grabbers=[MozillaGrabber(args), ChromeGrabber(args)]
  else:
    sys.exit("Unsupported platform")
  for x in grabbers:
    x.grabAndStore(db)
