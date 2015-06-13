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
sys.path.append(os.path.join(runpath, '../lib'))

import argparse
from Cookie import Cookie
from Config import Configuration as conf
from DatabaseConnection import selectAllFrom, grabJar

# Functions

# Main
if __name__=='__main__':
  description='''Queries the database for cookies matching criteria'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-s',  action='store_true', help='Display stats')
  parser.add_argument('-d',  metavar='domain',    help='Domain to query cookies from (e.g github.com)')
  parser.add_argument('-b',  metavar='browser',   help='Browser the cookie was grabbed from (e.g firefox)')
  parser.add_argument('-n',  metavar='name',      help='Cookie name')
  parser.add_argument('-v',  metavar='value',     help='Cookie value')
  parser.add_argument('-u',  metavar='user',      help='User:profile the cookies originate from (e.g NorthernSec:12345ua0.default)')
  parser.add_argument('-id', metavar='id',        help='ID of stored cookie')
  parser.add_argument('db',  metavar='database', nargs='?', help='Database')
  args = parser.parse_args()

  where=[]
  if args.d:  where.append("domain='%s'"%args.d)
  if args.b:  where.append("browser='%s'"%args.b)
  if args.n:  where.append("name='%s'"%args.n)
  if args.v:  where.append("value='%s'"%args.v)
  if args.u:  where.append("user='%s'"%args.u)
  if args.id: where.append("id='%s'"%args.id)
  db=args.db if args.db else conf.getCookieJar()
  print(db)
  cookies = selectAllFrom(db, 'CookieJar', where)
  print("id | domain | host | name | value | browser | user | lastUsed | creationTime | timeJarred | notes")
  for c in cookies:
    print("%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s"%(c['id'],c['domain'],c['host'],c['name'],c['value'],c['browser'],c['user'],c['lastused'],c['creationtime'],c['timejarred'],c['notes']))
  if args.s:
    print("Total of %s cookie(s)"%len(cookies))
