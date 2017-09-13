import bottle
import os
import re
import datetime
from bottle import route, run, template, static_file, request
import subprocess

application = bottle.app()

@route('/upload/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./upload')

@route('<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@application.route('/', method=['GET'])
def home():
 return template('./static/index.html') 

def makeVideo(key, audio, fr):
 cmd = "ffmpeg -framerate {fr} -vcodec mjpeg -i ./upload/{key}/{key}%03d.jpg -i {audio} -c:v libx264 -pix_fmt yuv420p -shortest ./upload/{key}/out_{key}.mp4".format(fr = fr , key = key, audio = audio)
 p = subprocess.call(cmd, shell=True)
 return 1

def convertImg(key):
 cmd = "ls | grep '.data' | xargs -n 1 bash -c 'convert -resize 50% \"$0\" \"${0%.*}.jpg\"'"
 p = subprocess.call(cmd, shell=True, cwd="./upload/{dir}".format(dir = key))
 return 1

@application.route('/upload', method=['POST'])
def upload():
 files = request.files.getall('fileselect')


 audio = request.forms.get('audio')
 time = request.forms.get('time')
 key = str(datetime.datetime.now())
 key = re.sub(r"[^\w\s]", '', key)  
 key = re.sub(r"\s+", '', key)
 dir = "./upload/{d}".format(d = key)
 if not os.path.exists(dir):
  os.makedirs(dir)
 count = len(files)
 for f in range(0, count):
  filename = "{path}/{file}".format(path = dir, file = key + "00" + str(f + 1) + ".data")
  files[f].save(filename)
 print "1. upload finished!"
 print "2. converting images..."
 convertImg(key)
 print "3. generating video..."
 makeVideo(key, audio, count / 30.0) 
 print "3. video generated!"
 return "Your video file: </br><a href='/upload/" + key + "/out_" + key +".mp4'>" + key  + ".mp4</a>"


if __name__ == "__main__":
 application.run(host='0.0.0.0')
