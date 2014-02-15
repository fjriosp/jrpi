#! /usr/bin/python

import os,stat
import subprocess
from flask import Flask,render_template,request,abort,redirect,url_for
from omxplayer import OMXPlayer
import youtube

app = Flask(__name__,static_url_path='')
path_media = os.path.dirname(os.path.realpath(__file__))+'/media'
omxplayer = OMXPlayer()

@app.route('/omxplayer')
def omxplayer_status():
  filename = None
  if omxplayer.isRunning():
    filename = omxplayer.filename
  return render_template('omxplayer.html',playing=filename)

@app.route('/omxplayer/command')
def omxplayer_command():
  command = request.args.get('command', None)

  if command == 'play':
    rpath = request.args.get('path', None)
    if rpath == None:
      abort(404);
    filepath = path_media+'/'+rpath
    filename = os.path.basename(filepath)
    omxplayer.play(filepath,filename)
    return redirect(url_for('list',path=os.path.dirname(rpath)));
  if command == 'pause':
    omxplayer.pause()
  elif command == 'stop':
    omxplayer.stop()
  elif command == 'seek+30':
    omxplayer.seekF30()
  elif command == 'seek-30':
    omxplayer.seekR30()
  elif command == 'seek+600':
    omxplayer.seekF600()
  elif command == 'seek-600':
    omxplayer.seekR600()

  return redirect(url_for('omxplayer_status'));

@app.route('/youtube/search')
def youtube_search():
  query = request.args.get('q', '')
  return render_template('youtube_search.html',videos=youtube.search(query),q=query)

@app.route('/youtube/play')
def youtube_play():
  vid = request.args.get('id', '')
  vname = request.args.get('name', '')
  query = request.args.get('q', '')

  omxplayer.play(youtube.getStream(vid),vname)

  return redirect(url_for('youtube_search',q=query));

@app.route('/list')
def list():
  rpath = request.args.get('path', '.')

  files   = []
  folders = []

  if '/../' in rpath:
    rpath='.'

  if not rpath.endswith('/'):
    rpath = rpath+'/'

  for f in os.listdir(path_media+'/'+rpath):
    file_rpath = rpath+f
    fstat = os.stat(path_media+'/'+file_rpath)
    if stat.S_ISDIR(fstat.st_mode):
      folders.append({'name':f,'path':file_rpath});
    else:
      files.append({'name':f,'path':file_rpath});

  media_files = [i for i in files if i['name'].lower().endswith(omxplayer.supported_ext)]

  media_files.sort()
  folders.sort()

  return render_template('list.html',files=media_files,folders=folders);

@app.route('/')
def status():
  if omxplayer.isRunning():
    status = 'running'
  else:
    status = 'stop'

  return render_template('index.html',omxplayer=status)

if __name__ == '__main__':
#  app.debug = True
  app.run(host='0.0.0.0',port=8000)
