import json
import os
import random
import shutil
import base64

from flask import Flask,request
from faker import Faker
from flask import Response
from flask import make_response
from flask import send_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
app = Flask(__name__)
fake = Faker()
def make_dat(bydata):
    if not os.path.exists(os.path.join(BASE_DIR,'datf/')):
        os.makedirs(os.path.join(BASE_DIR,'datf/'))
    name = fake.name()+".dat"
    path = os.path.join(BASE_DIR,'datf/'+name)
    if isinstance(bydata,str):
        bydata = bydata.encode()
    barr= bytearray(bydata)
    with open(path,'wb') as f:
        f.write(barr)

def make_wsq(bydata):
    if not os.path.exists(os.path.join(BASE_DIR,'wsqf/')):
        os.makedirs(os.path.join(BASE_DIR,'wsqf/'))
    name = fake.name()+".wsq"
    path = os.path.join(BASE_DIR,'wsqf/'+name)
    # if isinstance(bydata,str):
    #     bydata = bydata.encode()
    # barr= bytearray(bydata)
    with open(path,'wb') as f:
        f.write(bydata)



# barr = bytearray(random.getrandbits(8) for i in range (256))
# make_dat(barr)

def make_zip(directory):
    # print(os.path.isdir(directory))
    shutil.make_archive(directory, 'zip', directory)

# make_zip()

@app.route("/generate_dat",methods=['POST'])
def generate():
    incoming = request.data
    make_dat(incoming)
    return Response(status=200)

@app.route("/download",methods=['GET'])
def download_dat():
    make_zip('datf')
    try:
        return send_file('datf.zip',
                         attachment_filename='template_images.zip')
    except Exception as e:
        return str(e)

@app.route("/hello",methods=['GET'])
def hello():
    return "<h2>hello</h2>"

@app.route("/generate_wsq",methods=['POST'])
def generate_wsq():

    incoming = json.loads(request.data.decode())

    incoming = base64.b64decode(incoming['image'])
    # incoming = incoming['image']

    print(incoming)
    make_wsq(incoming)
    return Response(status=200)

@app.route("/download_wsq",methods=['GET'])
def download_wsq():
    make_zip('wsqf')
    try:
        return send_file('wsqf.zip',
                         attachment_filename='wsq_images.zip')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0')