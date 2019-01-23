# 2019.01.22
# Scratch類似画像検索GUI化.
# Python v3.7.2

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import os
from werkzeug import secure_filename
import json
import sys
import SearchSimilarImage as ssi
from tkinter import messagebox

# ---------------------------------
# グローバル変数とか
# ---------------------------------
imgList = ""
imgUrl = "css/dummy.png" # 最初の読み込み時はダミー画像を表示する
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
UPLOAD_FOLDER = 'static/uploads'

# ---------------------------------
# 謎 とりあえずおまじない
# ---------------------------------
app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ---------------------------------
# index.htmlが読み込まれた時の処理
# ---------------------------------
@app.route('/')
def index():
	ssi.DeleteCash()
	if not os.path.exists("static/database/lists/pathHashList.csv"):
		print("Calculating hash values of images in database ...")
		ssi.CalcDBImgHash()
	return render_template('index.html', inputImgUrl = imgUrl, imgList = imgList)


# ---------------------------------
# http://127.0.0.1:8000/search が読み込まれた時の処理
# ---------------------------------
# https://codehandbook.org/python-flask-jquery-ajax-post/
@app.route('/search', methods=['GET','POST'])
def search():
	if request.method == "POST":
		searchedImgUrl = request.json['searchedImgUrl']
		print("Received clicked image URL : " + searchedImgUrl)
		codeJSON = ssi.getCodeJSON(searchedImgUrl)
		return json.dumps(codeJSON)
		# return json.dumps({'result': 'ok', 'value': searchedImgUrl})




# ---------------------------------
# http://127.0.0.1:8000/upload が読み込まれた時の処理
# ---------------------------------
# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
	# print(os.getcwd())
	if request.method == 'POST':
		# 例外処理1
		if 'inputImg' not in request.files:
			print("> [[EXCEPTION]]\n> inputImg not in request.files!!")
			return render_template('index.html', inputImgUrl = "css/dummy.png", imgList = "")

		# クライアント側からinput画像のurlという値を受け取り
		inputImg = request.files['inputImg']

		# 例外処理2
		if inputImg.filename == '':
			print("> [[EXCEPTION]]\n> inputImg.filename == empty!!")
			return render_template('index.html', inputImgUrl = "css/dummy.png", imgList = "")

		# 受け取ったinput画像urlを使って類似画像検索
		if inputImg and allowed_file(inputImg.filename):
			filename = secure_filename(inputImg.filename)
			inputImg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			imgUrl = UPLOAD_FOLDER + "/" + filename

			# 類似画像検索を実施
			sortedImgList = ssi.CalcDef(imgUrl)

			# index.htmlのリダイレクト用にurlをごにょごにょする
			imgUrl = imgUrl.strip("static/")
			imgList = sortedImgList.iloc[:,0].tolist()

			return render_template('index.html', inputImgUrl = imgUrl, imgList = imgList)


		else:
			return ''' <p>Invalid file (only .png, .jpg, gif)</p> '''

	else:
		return redirect(url_for('index'))



def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=8000)


