import bottle
from bottle import route, run, template, static_file, request
import subprocess

application = bottle.app()

@route('/upload/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./upload')

@application.route('/', method=['GET'])
def home():
 return template('./static/index.html') 

def makeVideo(image, audio):
 cmd = ["./run", image, audio]
 p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
 out, err = p.communicate()
 return out

@application.route('/upload', method=['POST'])
def upload():
 upload = request.files.get('upload')
 file_path = "upload/{file}".format(file = upload.filename)
 upload.save(file_path)
 print "1. upload finished!" 
 makeVideo(upload.filename, "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
 print "2. video generated!"
 return "Your video file: </br><a href='/upload/out_" + upload.filename +".mp4'>" + upload.filename + ".mp4</a>"


if __name__ == "__main__":
 application.run(host='0.0.0.0')
