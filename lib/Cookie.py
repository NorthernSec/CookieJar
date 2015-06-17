#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Cookie object

# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# Imports
import time

class Cookie():
  def __init__(self, domain, host, name, value, browser, user, lastUsed=None, creationTime=None, timeJarred=None, notes=None):
    self.domain=domain
    self.host=host
    self.name=name
    self.value=value
    self.browser=browser
    self.user=user
    self.lastUsed=lastUsed
    self.creationTime=creationTime
    self.timeJarred=timeJarred if timeJarred else int(time.time()*10000000)
    self.notes=notes
