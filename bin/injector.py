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
import sys
runpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath, '..'))

import argparse
from lib.Cookie import Cookie
from lib.DatabaseConnection import selectAllFrom
from lib.MozillaGrabber import MozillaGrabber

# Functions

# Main
if __name__=='__main__':
  description='''Injects cookies into a browser'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-v', action='store_true',            help='Verbose')
  parser.add_argument('-d', metavar='domain',               help='Domain the cookies come from')
  parser.add_argument('-n', metavar='name',                 help='Name the cookies come from')
  parser.add_argument('-b', metavar='browser',              help='Browser the cookies come from')
  parser.add_argument('-u', metavar='user',                 help='User the cookies come from')
  parser.add_argument('-i', metavar='id',                   help='ID of the cookie in the CookieJar database')
  parser.add_argument('-t', metavar='browser:user:profile', help='Browser, user and profile to inject the cookies in')
  parser.add_argument('db', metavar='database',             help='Database the cookies are stored in')
  args = parser.parse_args()

  where=[]
  if args.d: where.append("domain='%s'"%args.d)
  if args.n: where.append("name='%s'"%args.n)
  if args.b: where.append("browser='%s'"%args.b)
  if args.u: where.append("user='%s'"%args.u)
  if args.i: where.append("id='%s'"%args.i)

  browser=args.t.split(':')[0].lower()
  user=args.t.split(':')[1]
  profile=args.t.split(':')[2]

  if browser == 'firefox':
    injector=MozillaGrabber(args)
  db=args.db if args.db else os.path.join(runpath, '../CookieJar.sqlite')

  cookies=[Cookie(x['domain'], x['host'], x['name'], x['value'], x['browser'], x['user'], x['lastused'], x['creationtime'], x['timejarred'], x['notes']) for x in selectAllFrom(db, 'CookieJar', where=where)]
  if args.v:
    print("Injecting %s cookies"%len(cookies))
  injector.inject(cookies, user, profile)
