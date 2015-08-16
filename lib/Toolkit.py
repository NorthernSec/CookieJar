#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Toolkit
#   Functions that are used everywhere
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import calendar
import os
import platform
from datetime import datetime, timedelta

def subdirsOf(dir):
  try:
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]
  except:
    return []

def getUsers():
  users=None
  if platform.system() == "Linux":
    users=subdirsOf("/home")
    if "lost+found" in users: users.remove("lost+found")
  elif platform.system() == "Windows":
    users= subdirsOf("C:/users")
    if "Public" in users: users.remove("Public")
  return users

def webkit_to_epoch(ts):
  estart=datetime(1601,1,1)
  delta=timedelta(microseconds=int(ts))
  return calendar.timegm((estart+delta).timetuple())*1000000

def epoch_to_webkit(ts):
  estart=datetime(1601,1,1)
  delta=timedelta(microseconds=int(ts))
  return calendar.timegm((estart-delta).timetuple())*-1000000
