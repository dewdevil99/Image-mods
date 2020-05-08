import os
import numpy as np
import cv2
import datetime
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST','GET'])
def upload_file():
	if(request.method=="POST"):
		if 'file' not in request.files:
			print('no file')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print('no filename')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename).rsplit('.')[0]+str(int(datetime.datetime.timestamp(datetime.datetime.now())))+"."+secure_filename(file.filename).rsplit('.')[1]
			print(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			img=cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			option=request.form['options']
			if(option=="Red"):
				img[:,:,0]=np.zeros([img.shape[0],img.shape[1]])
				img[:,:,1]=np.zeros([img.shape[0],img.shape[1]])
				cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],filename),img)
			elif(option=="Blue"):
				img[:,:,1]=np.zeros([img.shape[0],img.shape[1]])
				img[:,:,2]=np.zeros([img.shape[0],img.shape[1]])
				cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],filename),img)
			elif(option=="Green"):
				img[:,:,0]=np.zeros([img.shape[0],img.shape[1]])
				img[:,:,2]=np.zeros([img.shape[0],img.shape[1]])
				cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],filename),img)
			elif(option=="Grayscale"):
				b,g,r=cv2.split(img)
				grey=np.ones(b.shape,dtype=b.dtype)
				for i in range(img.shape[0]):
					for j in range(img.shape[1]):
						grey[i][j]=((0.3*r[i][j])+(0.59*g[i][j])+(0.11*b[i][j]))
				cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],filename),grey)
			return redirect(url_for('uploaded_file',filename=filename))
	return render_template("upimage.html")


@app.route('/upload/<filename>')
def uploaded_file(filename):
	return render_template("image.html",filename=filename)

if __name__ == '__main__':
	app.debug=True
	app.run()