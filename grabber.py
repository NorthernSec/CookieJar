#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# CookieJar Grabber
#   Searches for cookies on the system it runs on, compares it with the CookieJar (sqlite database), and stores changes.
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports

from lib.Cookie import Cookie
from lib.MozillaGrabber import MozillaGrabber

# Functions
  
# Main
if __name__=='__main__':
  mg=MozillaGrabber()
  mg.grabAndStore("CookieJar.sqlite")
