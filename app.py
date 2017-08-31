import bottle
from bottle import route, run, template, request
import subprocess

application = bottle.app()

@application.route('/', method=['GET'])
def home():
 return template('./static/index.html') 

@application.route('/test', method=['GET'])
def test():
 cmd = ["./run",""]
 p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
 out, err = p.communicate()
 return out

@application.route('/upload', method=['POST'])
def upload():
 upload = request.files.get('upload')
 file_path = "upload/{file}".format(file = upload.filename)
 upload.save(file_path)



if __name__ == "__main__":
 application.run(host='0.0.0.0')
