#!/usr/bin/env python
import os
import re
import sys
import time
import platform
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import parsedatetime

class Reminder:
   def __init__(self, _content, _time):
      self.content = _content
      self.time = _time

class ReminderAppBase:
   def create(self, content, time):
      self.reminder = self.register(content, time)
      print self.message()

   def formatTime(self, time):
      raise

   def register(self, content, time):
      raise

   def message(self):
      return "Reminder \"" + self.reminder.content + "\" on " + self.formatTime(self.reminder.time) + " created."

class AppleReminder(ReminderAppBase):
   def formatTime(self, time):
      v, _, _ = platform.mac_ver()
      v = '.'.join(v.split('.')[:2])
      # TODO: does time format really depend on versions?
      if v == '10.8':
         return time.strftime("%d/%m/%Y %H:%M:%S")
      elif v == '10.9':
         return time.strftime("%d/%m/%Y %H:%M:%S")
      else:
         # Unknown version. Whatever format is OK, hope it works.
         return time.strftime("%d/%m/%Y %H:%M:%S")

   def register(self, content, time):
      formattedTime = self.formatTime(time);

      # http://apple.stackexchange.com/questions/66981/how-can-i-add-reminders-via-the-command-line
      script = """
      on run argv
          set myDate to date (item 2 of argv)
          tell application "Reminders"
              make new reminder with properties {name:item 1 of argv, remind me date:myDate}
          end tell
      end run
      """
      p = Popen(['osascript', '-', content, formattedTime], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
      output = p.communicate(input=script)[0]
      # successfuul output format:
      #   10.9 => 'reminder id x-apple-reminder:...'
      #   10.8 => 'reminder id ...'
      if re.match('^reminder id', output):
         # TODO: create proper Reminder object
         return Reminder(content, time)
      else:
         print 'Reminder could not be created.'
         print 'Please report it to https://github.com/Genki-S/rem/issues/new'
         return None

def getReminder():
   p = sys.platform
   if p == 'darwin':
      return AppleReminder()
   else:
      print 'rem can only create Reminder.app reminders for now'
      print 'Please request other adapters to https://github.com/Genki-S/rem/issues/new'
      raise

def main():
   if len(sys.argv) != 3:
       print "Usage:", os.path.basename(sys.argv[0]), "CONTENT TIME"
       sys.exit(1)

   content, timeStr = sys.argv[1:]
   cal = parsedatetime.Calendar()
   parsedTime = datetime.fromtimestamp(time.mktime(cal.parse(timeStr)[0]))

   reminder = getReminder()
   reminder.create(content, parsedTime)
