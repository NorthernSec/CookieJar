#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Toolkit
#   Functions that are used everywhere
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import os
import platform

def subdirsOf(dir):
  return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

def getUsers():
  if platform.system() == "Linux":
    users=subdirsOf("/home")
    users.remove("lost+found")
    return users
  elif platform.system() == "Windows":
    return subdirsOf("C:/users")
  else:
    return None

