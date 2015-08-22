#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Cookiegrabber for Google Chrome
#   Grabs the cookies from Google Chrome 
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
from Toolkit import getUsers, subdirsOf, webkit_to_epoch, epoch_to_webkit

class ChromeGrabber():
  def __init__(self, args):
    self.args=args
    if platform.system() == "Linux":
      sys.exit("Not iImplemented yet")
    elif platform.system() == "Windows":
      self.cookieTrail='C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\%s\\Cookies'
      self.profiles='C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data'
    else:
      sys.exit("Unsupported platform")

  def grabAndStore(self, database=None, allUsers=False, users=None):
    path = database if database else "../CookieJar.sqlite"
    if not users or type(users) is not list:
      users=getUsers() if allUsers else [getpass.getuser()]
    grabJar(path)
    cookies=selectAllFrom(path, "CookieJar")
    if self.args.v: print("Starting with Google Chrome Cookies")
    for u in users:
      if self.args.v: print(" |- Grabbing cookies of %s"%u)
      for p in self.getProfiles(u):
        if not os.path.isfile(self.cookieTrail%(u,p)):
          if args.v: print(" |   | -> Profile %s does not have cookies"%p)
          continue
        if self.args.v: print(" |   |- Grabbing cookies of profile %s"%p)
        added=addToJar(path, [Cookie(c['host_key'],c['host_key'],c['name'],c['value'], 'chrome', '%s:%s'%(u,p), webkit_to_epoch(c['last_access_utc']),webkit_to_epoch(c['creation_utc'])) for c in self.grab(u,p)])
        if self.args.v: print(" |   | -> Stored %s new cookies"%added)

  def grab(self, user, profile=None, rc=False):
    profiles = [profile] if profile is not None else self.getProfiles(user)
    cookies=[]
    for p in profiles:
      for c in selectAllFrom(self.cookieTrail%(user,p), "cookies"):
        if rc:
          cookies.append(Cookie(c['host_key'],c['host_key'],c['name'],c['value'], 'chrome', '%s:%s'%(user,p), c['last_access_utc'],c['creation_utc']))
        else:
          cookies.append(c)
    return cookies

  def getProfiles(self, user):
    p=subdirsOf(self.profiles%user)
    if "Avatars" in p: p.remove("Avatars")
    if "Caps" in p: p.remove("Caps")
    if "Crash Reports" in p: p.remove("Crash Reports")
    if "EVWhitelist" in p: p.remove("EVWhitelist")
    if "PepperFlash" in p: p.remove("PepperFlash")
    if "pnacl" in p: p.remove("pnacl")
    if "PnaclTranslationCache" in p: p.remove("PnaclTranslationCache")
    if "SwiftShader" in p: p.remove("SwiftShader")
    if "SwReporter" in p: p.remove("SwReporter")
    if "WidevineCDM" in p: p.remove("WidevineCDM")
    return p

  def getBrowserName(self):
    return "Google Chrome"

  def inject(self, cookies, user, profile=None):
    profiles = [profile] if profile is not None else self.getProfiles(user)
    if type(cookies)!=list:
      cookies=[cookies]
    for p in profiles:
      chr=sqlite3.connect(self.cookieTrail%(user,p))
      for c in cookies:
        chr.execute('''INSERT OR REPLACE INTO cookies
                      (creation_utc, host_key,  name, value, path, expires_utc, secure, httponly, last_access_utc)
                       VALUES(:cre,:host,:name,:val,:path,:exp,:sec,:http,:la)''',
                      {'cre':epoch_to_webkit(c.creationTime),'host':c.host, 'name': c.name,  'val':c.value, 'path':'/',
                       'exp':epoch_to_webkit(int(time.time()*1000000)+2592000),'sec':0, 'http':0, 'la':epoch_to_webkit(c.lastUsed)})
      chr.commit()
      chr.close()

