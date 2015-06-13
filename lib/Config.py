#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Config reader to read the configuration file
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# imports
import sys
import os
runPath = os.path.dirname(os.path.realpath(__file__))

import re
import datetime
import configparser
import urllib.parse


class Configuration():
  ConfigParser = configparser.ConfigParser()
  ConfigParser.read(os.path.join(runPath, "../etc/configuration.ini"))
  default = {'host': "127.0.0.1", 'port': 5005,
             'debug': True, 'ssl':False,
             'sslCert': 'web/ssl/CookieJar.crt', 'sslKey':'web/ssl/CookieJar.key',
             'db':'CookieJar.sqlite'}

  @classmethod
  def readSetting(cls, section, item, default):
    result = default
    try:
      if type(default) == bool:
        result = cls.ConfigParser.getboolean(section, item)
      elif type(default) == int:
        result = cls.ConfigParser.getint(section, item)
      else:
        result = cls.ConfigParser.get(section, item)
    except:
      pass
    return result

  # Flask
  @classmethod
  def getHost(cls):
    return cls.readSetting("Server", "Host", cls.default['host'])
  @classmethod
  def getPort(cls):
    return cls.readSetting("Server", "Port", cls.default['port'])
  @classmethod
  def getDebug(cls):
    return cls.readSetting("Server", "Debug", cls.default['debug'])
  # SSL
  @classmethod
  def useSSL(cls):
    return cls.readSetting("Server", "SSL", cls.default['ssl'])
  @classmethod
  def getSSLCert(cls):
    return os.path.join("..", cls.readSetting("SSL", "Certificate", cls.default['sslCert']))
  @classmethod
  def getSSLKey(cls):
    return os.path.join("..", cls.readSetting("SSL", "Key", cls.default['sslKey']))
  # Database
  @classmethod
  def getCookieJar(cls):
    return os.path.join(runPath, "..", cls.readSetting("CookieJar", "Path", cls.default['db']))
