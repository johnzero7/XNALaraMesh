# -*- coding: utf-8 -*-

from XNALaraMesh import xps_const

def readline(file):
    line = file.readline()
    line = line.strip()
    return line

def getFloat(value):
    if value:
        try:
          return float(value)
        except ValueError:
          return float('NaN')
    return value

def getInt(value):
    try:
      return int(value)
    except ValueError:
      return None

def ignoreComment(line):
    line = line.replace('#',' ')
    line = line.split()[0]
    return line

def ignoreStringComment(line):
    line = line.split('#')[0]
    return line

def readInt(file):
   line = readline(file)
   value = ignoreComment(line)
   number = getInt(value)
   return number

def readString(file):
    #String Lenght
    line = readline(file)
    string = ignoreStringComment(line)
    return string

def splitValues(line):
    line = line.replace('#',' ')
    values = line.split()
    return values

