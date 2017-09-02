import bottle
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

def makeVideo(key, audio):
 key = key + "%03d.png"
 cmd = ["./run", key, audio]
 p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
 out, err = p.communicate()
 return out

@application.route('/upload', method=['POST'])
def upload():
 upload1 = request.files.get('upload1')
 upload2 = request.files.get('upload2')
 upload3 = request.files.get('upload3')
 audio = request.forms.get('audio')
 key = "abc"
 key = str(datetime.datetime.now())
 key = re.sub(r"[^\w\s]", '', key)  
 key = re.sub(r"\s+", '', key)
 file1 = "upload/{file}".format(file = key + "001.png")
 file2 = "upload/{file}".format(file = key + "002.png")
 file3 = "upload/{file}".format(file = key + "003.png")
 upload1.save(file1)
 upload2.save(file2)
 upload3.save(file3)
 print "1. upload finished!" 
 makeVideo(key, audio) 
 print "2. video generated!"
 return "Your video file: </br><a href='/upload/out_" + key +".mp4'>" + key  + ".mp4</a>"


if __name__ == "__main__":
 application.run(host='0.0.0.0')
