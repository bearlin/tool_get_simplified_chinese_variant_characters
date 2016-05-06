#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re
import pdb

################################################################################
# Usage
################################################################################
class FileFilter():
  def __init__(self, aInputFilePath, aSeparatorLeft, aSeparatorRight, aOutputFilePath):
    print "aInputFilePath:%s" % (aInputFilePath)
    print "aSeparatorLeft:%s" % (aSeparatorLeft)
    print "aSeparatorRight:%s" % (aSeparatorRight)
    print "aOutputFilePath:%s" % (aOutputFilePath)

    # Open result file
    self._resultFile = codecs.open(aOutputFilePath, "w+", "utf-8")
    # Open input file
    file = open(aInputFilePath)

    self._foundFirstSection = False
    self._section = ''
    self._pronounce = ''
    self._lineNumber = 0
    for query in file:
      self._lineNumber += 1

      # Skip comment-out line
      if ("#" == query[0]) or (";" == query[0]):
        print "\nSkip comment-out line [%d]:%s" % (self._lineNumber, query)
        continue

      # Skip empty line
      query = query.strip()
      if (query == ''):
        #  print "\nSkip empty line [%d]" % (self._lineNumber)
        continue


      # Skip line before first section
      if (self._foundFirstSection == False):
        if (query != 'A'):
          print "\nSkip line before first section[%d]:%s" % (self._lineNumber, query)
          continue
        else:
          self._foundFirstSection = True

      if (query <= 'Z') and (query >= 'A'):
        self._section = query
        print "[%d]Found new section:%s" % (self._lineNumber, self._section)

      if (query[0] <= 'z') and (query[0] >= 'a'):
        self._pronounce = query
        print "[%d]Found new pronounce:%s" % (self._lineNumber, self._pronounce)

      #  pdb.set_trace()
      continue
      print "\n[%d]:%s" % (self._lineNumber, query)

      # Re-Construct the input query string
      self._inputList = query.split(aSeparatorLeft, 13)
      poiName = self._inputList[1].strip(' ')
      # Non-Chinese query string will be skipped
      if (self.HasChineseCharacter(poiName) == False):
        # print "Skip Compressed Poi Header Non-Chinese [%d]:%s" % (self._lineNumber, query)
        continue;

      # Write this query line to new file
      print >> self._resultFile, "%s" % (query.decode('utf-8'))

  def HasChineseCharacter(self, aString):
    for char in aString.decode('utf-8'):
      if (char >= u'\u4e00' and char <= u'\u9fff'):
        return True
    return False;

def show_usage():
  #  print "Usage: ", sys.argv[0], "<InputFilePath> <Separator, e.g. '|', ';', ',', etc.> <OutputFilePath>"
  print "Usage: ", sys.argv[0], "<InputFilePath>"
  pdb.set_trace()

# ----------------------------------
# -------------- Main --------------
# ----------------------------------
if __name__ == "__main__":
  if len(sys.argv) < 2:
    show_usage()
    sys.exit(1)

  inputFilePath = sys.argv[1]
  if (os.path.isfile(inputFilePath) == False):
    print "Please input a correct file path..."
    show_usage()
    sys.exit(1)

  separatorLeft = "〔".decode('utf-8')
  separatorRight = "〕".decode('utf-8')
  outputFilePath = "output/chinese_variant_characters.txt"

  FileFilter(inputFilePath, separatorLeft, separatorRight, outputFilePath)
