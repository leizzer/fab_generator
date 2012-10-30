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
        self.__concat_hosts(self.string_question('Host (ex: your.domain.com:port)'))
        )

    self.add(
        self.__concat_user(self.string_question('User (ex: root)'))
        )

    self.add(
        self.__concat_port(self.string_question('Port'))
        )

    self.svn_repo = self.string_question('SVN URL (ex: http://domain.com:port/repo)')
    self.svn_user = self.string_question('SVN username')

    self.destination = self.string_question('Destination directory on server (ex: /home/wwwdata)')
    self.project_name = self.string_question('Project name (ex: project.com)')

    # 0: svn_user, 1: svn_repo, 2: destination, 3: project_name
    self.add(
        self.__concat_body([self.svn_user, self.svn_repo,
          self.destination, self.project_name])
        )

  # private
  def __concat_hosts(self, text):
    return "env.hosts = ['{0}']".format(text)

  def __concat_user(self, text):
    return "env.user = '{0}'".format(text)

  def __concat_port(self, text):
    return "env.port = '{0}'".format(text)

  def __concat_body(self, array):
    return self.__body.format(*array)

  __head = """\
#!/usr/bin/env python
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.contrib import confirm

import datetime
"""
  __body = """\
def deploy():
  local('mkdir svn_export')
  with lcd('svn_export'):
    local('svn export --username={0} {1} current')
    local('tar -cvf current.tar current')
    local('scp -P ' + env.port +' current.tar '+ env.user +'@'+ env.host +':~/')

  # On server side
  with cd('~'):
    run('tar -xvf current.tar')
    run('mv current {2}')

  with cd('{2}/current'):
    # Your extra code on the server side
    # Ex:
    # run('./config')
    # run('make')
    # run('make install')

  # Backup & switch on the server
  with cd('{2}'):
    new_name = '{3}.'+ datetime.datetime.now().strftime('%Y%m%d.%H%M')
    run('mv current '+ new_name)
    run('rm {3}')
    run('ln -s '+ new_name +' {3}')

  # Extra commands
  # Ex:
  # run('sudo /etc/init.d/nginx stop')

  #Claning
  local('rm -rf svn_export')
  run('rm -rf ~/current.tar')
"""

gen = Generator()
