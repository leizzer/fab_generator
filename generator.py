class Generator:

  def __init__(self):
    self.boolean_question("Create fabfile?")

  def boolean_question(self, message):
    ans = raw_input(message + " (y/N): ")
    return True if ans == "y" else False

  def create_fab_file(self):
    self.file = open('fabfile.py', 'wr')
    self.file.write(__head)

  # private
  __head = """
          #!/usr/bin/env python
          from __future__ import with_statement
          from fabric.api import *
          from fabric.contrib.contrib import confirm

          import datetime
          """

gen = Generator()
