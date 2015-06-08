#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# CookieJar Query
#   Queries the database for cookies matching specific criteria
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
from lib.DatabaseConnection import selectAllFrom, grabJar

# Functions

# Main
if __name__=='__main__':
  description='''Queries the database for cookies matching criteria'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-s',        action='store_true', help='Display stats')
  parser.add_argument('-d',        metavar='domain',    help='Domain to query cookies from (e.g github.com)')
  parser.add_argument('-b',        metavar='browser',   help='Browser the cookie was grabbed from (e.g firefox)')
  parser.add_argument('-n',        metavar='name',      help='Cookie name')
  parser.add_argument('-v',        metavar='value',     help='Cookie value')
  parser.add_argument('-u',        metavar='user',      help='User:profile the cookies originate from (e.g NorthernSec:12345ua0.default)')
  parser.add_argument('-id',       metavar='id',        help='ID of stored cookie')
  parser.add_argument('database',  metavar='database',  help='sqlite database file')
  args = parser.parse_args()

  where=[]
  if args.d:  where.append("domain='%s'"%args.d)
  if args.b:  where.append("browser='%s'"%args.b)
  if args.n:  where.append("name='%s'"%args.n)
  if args.v:  where.append("value='%s'"%args.v)
  if args.u:  where.append("user='%s'"%args.u)
  if args.id: where.append("id='%s'"%args.id)
  if len(where)==0:
    sys.exit("At least specify one argument")
  db=args.database if args.database else "CookieJar.sqlite"
  cookies = selectAllFrom(db, "CookieJar", where)
  for c in cookies:
    print(c)
  if args.s:
    print("Total of %s cookie(s)"%len(cookies))
