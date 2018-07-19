import json
import os
import random
import shutil
import base64

import io
from PIL import Image,ImageFile
from flask import Flask,request
from faker import Faker
from flask import Response
from flask import make_response
from flask import send_file

# from io import StringIO

ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
app = Flask(__name__)
fake = Faker()

# prev_name = None

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

def make_wsq(bydata,name):
    if not os.path.exists(os.path.join(BASE_DIR,'wsqf/')):
        os.makedirs(os.path.join(BASE_DIR,'wsqf/'))
    name = name+".wsq"
    # prev_name= name
    path = os.path.join(BASE_DIR,'wsqf/'+name)
    # if isinstance(bydata,str):
    #     bydata = bydata.encode()
    # barr= bytearray(bydata)
    with open(path,'wb') as f:
        f.write(bydata)

def make_bmp(bydata, name):
    # img_stream = Image.open(bydata)
    if not os.path.exists(os.path.join(BASE_DIR,'bmpf/')):
        os.makedirs(os.path.join(BASE_DIR,'bmpf/'))
    name = name + ".bmp"
    basewidth = 800
    baseheight = 800
    path = os.path.join(BASE_DIR, 'bmpf/' + name)
    image = Image.open(io.BytesIO(bydata))
    # wpercent = (basewidth/float(ima))
    image.resize((basewidth,baseheight),Image.ANTIALIAS)
    image.save(path)
    # with open(path,'wb') as f:
    #     f.write(bydata)

def make_png(bydata,name):
    if not os.path.exists(os.path.join(BASE_DIR,'pngf/')):
        os.makedirs(os.path.join(BASE_DIR,'pngf/'))
    name = name+".png"
    path = os.path.join(BASE_DIR,'pngf/'+name)
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





@app.route("/generate_images",methods=['POST'])
def generate_images():

    incoming = json.loads(request.data.decode())

    wsq_incoming = base64.b64decode(incoming['wsq_image'])
    png_incoming = base64.b64decode((incoming['png_image']))
    # incoming = incoming['image']

    name = fake.name()

    # print(incoming)

    make_wsq(wsq_incoming,name)
    # make_png(png_incoming,name)
    make_bmp(png_incoming,name)
    return Response(status=200)

@app.route("/generate_png",methods=['POST'])
def generate_png():
    incoming = json.loads(request.data.decode())

    incoming = base64.b64decode(incoming['image'])
    make_png(incoming)
    return Response(status=200)


@app.route("/download_wsq",methods=['GET'])
def download_wsq():
    make_zip('wsqf')
    try:
        return send_file('wsqf.zip',
                         attachment_filename='wsq_images.zip')
    except Exception as e:
        return str(e)

@app.route("/download_png",methods=['GET'])
def download_png():
    make_zip('pngf')
    try:
        return send_file('pngf.zip',
                         attachment_filename='pmg_images.zip')
    except Exception as e:
        return str(e)


@app.route("/download_bmp",methods=['GET'])
def download_bmp():
    make_zip('bmpf')
    try:
        return send_file('bmpf.zip',
                         attachment_filename='bmp_images.zip')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0')