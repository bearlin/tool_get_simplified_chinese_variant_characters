#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re
#  import pdb

################################################################################
# Usage
################################################################################
class FileFilter():
  def __init__(self, aInputFilePath, aOutputFilePath):
    print "aInputFilePath:%s" % (aInputFilePath)
    print "aOutputFilePath:%s" % (aOutputFilePath)

    # Open result file
    self._resultFile = codecs.open(aOutputFilePath, "w+", "utf-8")
    self._logFile = codecs.open(aOutputFilePath + ".log", "w+", "utf-8")
    # Open input file
    file = open(aInputFilePath)

    # Private variables
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

      # Found new sections
      if (query <= 'Z') and (query >= 'A'):
        self._section = query
        print "[%d]Found new section:%s" % (self._lineNumber, self._section)
        continue

      # Found new pronounces
      if (query[0] <= 'z') and (query[0] >= 'a'):
        self._pronounce = query
        print "[%d]Found new pronounce:%s" % (self._lineNumber, self._pronounce)
        continue

      # Skip Non-Chinese line
      if (self.HasChineseCharacter(query) == False):
        print "Skip Non-Chinese line [%d]:%s" % (self._lineNumber, query)
        continue;

      # Start to extract Chinese characters with format A〔B[C|D|...]〕, assume
      # A-Z is Chinese characters, and generate final_result string
      print "[%d]:%s" % (self._lineNumber, query)
      result = self._pronounce + ","
      for char in query.decode('utf-8'):
        # Tell if this character in CJK_Unified_Ideographs_(Unicode_block)
        # [References]
        # https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
        # https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
        if ((char >= u'\u4e00' and char <= u'\u9fff')         or # CJK Unified Ideographs
            (char >= u'\u3400' and char <= u'\u4dbf')         or # CJK Unified Ideographs Extension A
            (char >= u'\U00020000' and char <= u'\U0002a6df')    # CJK Unified Ideographs Extension B
           ):
          result += char.encode('utf-8') + ","
        else:
          print >> self._logFile, "@@@:%c" % (char)

      length = len(result)
      final_result = result[:length-1] # '-1' is to remove the last ','
      print final_result
      print

      #  pdb.set_trace()
      #  continue

      # Write this query line to new file
      print >> self._resultFile, "%s" % (final_result.decode('utf-8'))

  def HasChineseCharacter(self, aString):
    for char in aString.decode('utf-8'):
      # Tell if this character in CJK_Unified_Ideographs_(Unicode_block)
      # [References]
      # https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
      # https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
      if ((char >= u'\u4e00' and char <= u'\u9fff')         or # CJK Unified Ideographs
          (char >= u'\u3400' and char <= u'\u4dbf')         or # CJK Unified Ideographs Extension A
          (char >= u'\U00020000' and char <= u'\U0002a6df')    # CJK Unified Ideographs Extension B
         ):
        return True
    return False;

def show_usage():
  print "Usage: ", sys.argv[0], "<InputFilePath>"
  #  pdb.set_trace()

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

  outputFilePath = "output/chinese_variant_characters.txt"

  FileFilter(inputFilePath, outputFilePath)

