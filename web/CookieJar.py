#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Simple web interface for CookieJar
#   Lets you grab, query and inject cookies from the following browsers:
#    - Mozilla Firefox
#    more to come
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# Imports
import os
import sys
_runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_runPath, "../lib"))

import argparse
import signal
import time

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import Flask, render_template, request, redirect, jsonify
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug import secure_filename

from Config import Configuration as conf
from DatabaseConnection import selectAllFrom, addToJar, grabJar
from Toolkit import getUsers
from MozillaGrabber import MozillaGrabber

# Variables
shutdowntime=3
app=Flask(__name__,static_folder='static',static_url_path='/static')

# Functions
def grabable():
  users={}
  for u in getUsers():
    browsers={}
    for s in supported:
      p=s.getProfiles(u)
      if p: browsers[s.getBrowserName()]=p
    users[u]=browsers
  return users

def sig_handler(sig,frame):
  print('Caught signal: %s'%sig)
  IOLoop.instance().add_callback(shutdown)

def shutdown():
  print('[*] Stopping the server')
  http_server.stop()
  print('[*]  Server will shut down in %s seconds...'%shutdowntime)
  io_loop=IOLoop.instance()
  deadline=time.time()+shutdowntime
  def stop_loop():
    now=time.time()
    if now<deadline and (io_loop._callbacks or io_loop._timeouts):
      io_loop.add_timeout(now+1,stop_loop)
    else:
      io_loop.stop()
      print('[*] Server shut down')
  stop_loop()

# Routes
@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html",info=info)

@app.route('/grab')
def grab():
  return render_template("grab.html",info=info, grabable=grabable())

@app.route('/query')
def query():
  c=selectAllFrom(info['db'], 'CookieJar')
  return render_template("query.html", cookies=c ,info=info)

# AJAX routes
@app.route('/_grab')
def _grab():
  items=request.args.get('grab', type=str).split(",")
  grabbers={"Mozilla Firefox": MozillaGrabber(args)}
  cookies=[]
  failed=[]
  for x in items:
    try:
      xs=x.split('|')
      if len(xs)>0: xs[0]=xs[0].replace("chk:","")
      if len(xs)==3:
        cookies.extend(grabbers[xs[1]].grab(xs[0], xs[2], rc=True))
      if len(xs)==2:
        cookies.extend(grabbers[xs[1]].grab(xs[0], rc=True))
      if len(xs)==1:
        for g in grabbers:
          cookies.extend(g.grab(xs[0], rc=True))
    except Exception as e:
      ex=x.replace("chk:","")
      ex.replace("|", " > ")
      failed.append(ex)
  try:
    added=addToJar(info['db'], cookies)
  except Exception as e:
    print(e)
    return jsonify({"store":"failure", "failures":failed, "all":len(cookies)})
  return jsonify({"store":"success", "failures":failed, "new":added, "all":len(cookies)})

@app.route('/_query')
def _query():
  domain= request.args.get('domain', type=str).strip()
  name=   request.args.get('name', type=str).strip()
  id=     request.args.get('id', type=str).strip()
  value=  request.args.get('value', type=str).strip()
  browser=request.args.get('browser', type=str).strip()
  user=   request.args.get('user', type=str).strip()
  where = []
  if domain:  where.append('domain="%s"'%domain)
  if name:    where.append('name="%s"'%name)
  if id:      where.append('id="%s"'%id)
  if value:   where.append('value="%s"'%value)
  if browser: where.append('browser="%s"'%browser)
  if user:    where.append('user="%s"'%user)
  results=selectAllFrom(info['db'], 'CookieJar', where)
  for x in results:
    x['timejarred']  =toDate(x['timejarred'])
    x['lastused']    =toDate(x['lastused'])
    x['creationtime']=toDate(x['creationtime'])
  return jsonify({"results":results})

# Filters
@app.template_filter('user')
def getUser(x):
  return x.split(':')[0]

@app.template_filter('toDate')
def toDate(x):
  return time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(x/1000000))

# Main
if __name__=='__main__':
  # Argparse
  description='''CookieJar web interface'''
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('db', metavar='database', nargs='?', help='Database')
  args = parser.parse_args()

  db=args.db if args.db else conf.getCookieJar()
  grabJar(db)

  host=conf.getHost()
  port=conf.getPort()

  global info
  info={'db':db,
        'supported':['Mozilla Firefox']}
  global supported
  supported=[MozillaGrabber(args)]

  if conf.getDebug():
    app.run(host=host, port=port, debug=True)
  else:
    print("[*] Starting server...")
    if conf.useSSL():
      cert=conf.getSSLCert()
      key=conc.getSSLKey()
      ssl_opttions={"certfile":cert, "keyfile":key}
    else:
      ssl_options=None
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    global http_server
    http_server=HTTPServer(WSGIContainer(app),ssl_options=ssl_options)
    http_server.bind(port, address=host)
    http_server.start(0)
    IOLoop.instance().start()
