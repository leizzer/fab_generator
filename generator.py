class Generator:

  def __init__(self):
    if self.boolean_question("Create fabfile?"):
      self.create_fab_file()
      self.generation_steps()

  def boolean_question(self, message):
    ans = raw_input(message + " (y/N): ")
    return True if ans == "y" else False

  def string_question(self, message):
    ans = raw_input(message + ": ")
    return ans

  def add(self, text):
    self.file.write("\n" + text)

  def create_fab_file(self):
    self.file = open('fabfile.py', 'wr')
    self.file.write(self.__head)

  def generation_steps(self):
    self.add(
        self.__hosts(self.string_question('Host (ex: your.domain.com:port)'))
        )

    self.add(
        self.__user(self.string_question('User (ex: root)'))
        )

    self.add(
        self.__port(self.string_question('Port'))
        )

  # private
  def __hosts(self, text):
    return "env.hosts = ['{0}']".format(text)

  def __user(self, text):
    return "env.user = '{0}'".format(text)

  def __port(self, text):
    return "env.port = '{0}'".format(text)

  __head = """\
#!/usr/bin/env python
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.contrib import confirm

import datetime
"""

gen = Generator()
