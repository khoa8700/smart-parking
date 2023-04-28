from flask import Flask, request, render_template
import cv2
import numpy as np
from getPredict import getPredict
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
# fourcc = 'mp4v'  # output video codec
# vid_writer = cv2.VideoWriter('data/result.mp4', cv2.VideoWriter_fourcc(*fourcc), 10, (640, 480))
@app.route('/predict/', methods=['POST'])
def predict():
    # f = request.files['img']
    # f.save('./data/image.png')
    # img = cv2.imread('./data/image.png')

    nparr = np.frombuffer(request.data, np.uint8)  
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imshow('img',img)
    # cv2.waitKey(500)
    # cv2.destroyWindow("img")
    # im = getPredict(img)
    # vid_writer.write(im)
    vehicle, license = getPredict(img)
    return vehicle +'-' + license
    # return 'Car-43A12345'

authenticate = 'None'
@app.route('/auth/', methods =['GET','POST']) # xac nhan lay xe
def auth():
    global authenticate
    if request.method == 'GET':
        tmp = authenticate
        authenticate = 'None'
        return tmp
    else:
        authenticate = request.get_data().decode()
        return 'ok'

predictResult = 'None' 
@app.route('/selfPredict/', methods =['GET','POST']) # nhan dien thu cong
def selfPredict():
    global predictResult
    if request.method == 'GET':
        tmp = predictResult
        predictResult = 'None'
        return tmp
    else:
        predictResult = request.get_data().decode()
        return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
