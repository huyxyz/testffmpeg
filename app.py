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

@application.route('/', method=['GET'])
def home():
 return template('./static/index.html') 

def makeVideo(key, audio, fr):
 cmd = "ffmpeg -framerate {fr} -i ./upload/{key}/{key}%03d.png -i {audio} -c:v libx264 -pix_fmt yuv420p -shortest ./upload/{key}/out_{key}.mp4".format(fr = fr , key = key, audio = audio)
 p = subprocess.call(cmd, shell=True)
 return 1

def convertImg(key):
 cmd = "ls | grep '.data' | xargs -n 1 bash -c 'convert \"$0\" \"${0%.*}.png\"'"
 p = subprocess.call(cmd, shell=True, cwd="./upload/{dir}".format(dir = key))
 return 1

@application.route('/upload', method=['POST'])
def upload():
 upload1 = request.files.get('upload1')
 upload2 = request.files.get('upload2')
 upload3 = request.files.get('upload3')
 audio = request.forms.get('audio')
 time = request.forms.get('time')
 key = str(datetime.datetime.now())
 key = re.sub(r"[^\w\s]", '', key)  
 key = re.sub(r"\s+", '', key)
 dir = "./upload/{d}".format(d = key)
 if not os.path.exists(dir):
  os.makedirs(dir)
 file1 = "{path}/{file}".format(path = dir, file = key + "001.data")
 file2 = "{path}/{file}".format(path = dir, file = key + "002.data")
 file3 = "{path}/{file}".format(path = dir, file = key + "003.data")
 upload1.save(file1)
 upload2.save(file2)
 upload3.save(file3)
 print "1. upload finished!"
 print "2. converting images..."
 convertImg(key)
 print "3. generating video..."
 makeVideo(key, audio, 0.11) 
 print "3. video generated!"
 return "Your video file: </br><a href='/upload/" + key + "/out_" + key +".mp4'>" + key  + ".mp4</a>"


if __name__ == "__main__":
 application.run(host='0.0.0.0')
