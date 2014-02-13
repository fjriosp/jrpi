#! /usr/bin/python

import os,stat
import subprocess
from flask import Flask,render_template,request,abort,redirect,url_for

app = Flask(__name__,static_url_path='')

bg = {}

def getProcess(name):
  proc = bg.get('omxplayer',None)
  if proc == None:
    return None

  p = proc.get('process',None)
  if p == None:
    return None
  if p.poll() != None:
    return None

  return proc


@app.route('/omxplayer/command')
def omxplayer_command():
  command = request.args.get('command', None)

  # Check already running omxplayer
  omxplayer = getProcess('omxplayer')
  if omxplayer != None:
    p = omxplayer['process']
    if command == 'pause':
      p.stdin.write('p')
    elif command == 'stop':
      p.stdin.write('q')
    elif command == 'seek+30':
      p.stdin.write('\x1B[C')
    elif command == 'seek-30':
      p.stdin.write('\x1B[D')
    elif command == 'seek+600':
      p.stdin.write('\x1B[A')
    elif command == 'seek-600':
      p.stdin.write('\x1B[B')

  return redirect(url_for('omxplayer'));

@app.route('/omxplayer')
def omxplayer():
  # Check already running omxplayer
  omxplayer = getProcess('omxplayer')
  return render_template('omxplayer.html',playing=omxplayer)

@app.route('/play')
def play():
  path = request.args.get('path', None)
  if path == None:
    abort(404);
  
  # Check already running omxplayer
  omxplayer = getProcess('omxplayer')

  if omxplayer == None:
    # Run omxplayer in background
    p = subprocess.Popen(['omxplayer',path],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
    bg['omxplayer']={'process':p,'file':path}
  else:
    print 'omxplayer found... ignoring'

  return redirect(url_for('omxplayer'));

@app.route('/list')
def list():
  path = request.args.get('path', '/')

  files   = []
  folders = []

  if not path.endswith('/'):
    path = path+'/'

  for f in os.listdir(path):
    fpath = path+f
    fstat = os.stat(fpath)
    if stat.S_ISDIR(fstat.st_mode):
      folders.append({'name':f,'path':fpath});
    else:
      files.append({'name':f,'path':fpath});

  files.sort()
  folders.sort()

  return render_template('list.html',files=files,folders=folders);

@app.route('/')
def hello_world():
  return render_template('index.html')

if __name__ == '__main__':
#  app.debug = True
  app.run(host='0.0.0.0',port=8000)
