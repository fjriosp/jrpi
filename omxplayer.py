#! /usr/bin/python

import subprocess

class OMXPlayer:
  supported_ext = ('.aaf','.3gp','.asf','.avi','.flv','.m1v','.m2v','.fla','.m4v','.mkv','.mov','.mpeg','.mpg','.mpe','.mp4','.mxf','.nsv','.ogg','.rm','.swf','.wmv')
  proc = None
  filepath = None
  filename = None

  def isRunning(self):
    if self.proc is None:
      return False
    ret = self.proc.poll()
    if ret is not None:
      return False
    return True

  def play(self,filepath,filename):
    if self.isRunning():
      self.close()

    # Run omxplayer in background
    p = subprocess.Popen(['omxplayer','-o','hdmi',filepath],close_fds=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
    self.proc = p
    self.filepath = filepath
    self.filename = filename

  def pause(self):
    if self.isRunning():
      self.proc.stdin.write('p')

  def seekF600(self):
    if self.isRunning():
      self.proc.stdin.write('\x1B[A')

  def seekF30(self):
    if self.isRunning():
      self.proc.stdin.write('\x1B[C')

  def seekR30(self):
    if self.isRunning():
      self.proc.stdin.write('\x1B[D')

  def seekR600(self):
    if self.isRunning():
      self.proc.stdin.write('\x1B[B')

  def stop(self):
    if self.isRunning():
      self.proc.stdin.write('q')

  def close(self):
    if self.isRunning():
      self.proc.stdin.write('q')
