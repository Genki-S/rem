#!/usr/bin/env python
import os
import re
import sys
import time
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
      # For OS X 10.9
      return time.strftime("%m/%d/%Y %I:%M:%S%p")

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
      if re.match('^reminder id x-apple-reminder:', output):
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
