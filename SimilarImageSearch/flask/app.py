# <!-- https://m-school.biz/dev/css-coding/036-css-list-grid.htm -->
# 		<!-- <ul id="searchedImgList">
# 			{% for path in imgList %}
# 			<li>
# 				<img src={{ url_for('static', filename = path) }} id = "searchedImg" style="margin-top: 10px; vertical-align: bottom; width: 100px;">
# 			</li>
# 			{% endfor %}
# 		</ul> -->
# 2019.01.22
# Scratch類似画像検索GUI化.
# Python v3.7.2

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import os
from werkzeug import secure_filename
import json
import sys
# from tkinter import messagebox
import re
import time


import SSI_preprocess as ps
import SSI_hash as ha
import SSI_histogram as hi
import SSI_featureDetection as fd

# ---------------------------------
# グローバル変数とか
# ---------------------------------
# 練習用に検索対象ディレクトリ変えるときはここ
# databaseImagesPath = "static/database/project1_practice/"
# databaseImagesPath = "static/database/_practice/"
databaseImagesPath = "static/database/project1/"

imgList = ""
imgUrl = "css/dummy.png" # 最初の読み込み時はダミー画像を表示する
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
UPLOAD_FOLDER = 'static/uploads'

# for prototype
PROCESS_NUM = 0 # 試す検索処理の場合分け [0でhash,1でhistogram,2でfeature]

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
	ps.DeletePreviousData()

	start = time.time()

	if PROCESS_NUM is 0:
		print("================ Start [Hash Method] ================")

		if not os.path.exists("static/database/lists/comparing_hash_list.npy"):
			print(" Calculating hash values of images in database ...")
			ha.CalcDBImg_hash(databaseImagesPath)

	elif PROCESS_NUM is 1:
		print("================ Start [Histogram Method] ================")

		if not os.path.exists("static/database/lists/comparing_histogram_list.npy"):
			print(" Calculating histogram values of images in database ...")
			hi.CalcDBImg_histogram(databaseImagesPath)


	elif PROCESS_NUM is 2:
		print("================ Start [Feature Detection Method] ================")
		if not os.path.exists("static/database/lists/comparing_feature_list.npy"):
			print(" Calculating features of images in database ...")
			fd.CalcDBImg_feature(databaseImagesPath)

	e_time = time.time() - start
	print (" time: {0}".format(e_time) + " [s]")

	print(" End Preprocess ...")
	return render_template('index.html', inputImgUrl = imgUrl, imgList = imgList)


# ---------------------------------
# http://127.0.0.1:8000/search が読み込まれた時の処理
# ---------------------------------
# https://codehandbook.org/python-flask-jquery-ajax-post/
@app.route('/search', methods=['GET','POST'])
def search():
	if request.method == "POST":
		searchedImgUrl = request.json['searchedImgUrl']
		print(" Received clicked image URL : " + searchedImgUrl)
		codeJSON = getCodeJSON(searchedImgUrl)
		return json.dumps(codeJSON)
		# return json.dumps({'result': 'ok', 'value': searchedImgUrl})




# ---------------------------------
# http://127.0.0.1:8000/upload が読み込まれた時の処理
# ---------------------------------
# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
	# print(os.getcwd())
	start = time.time()

	if request.method == 'POST':
		# 例外処理1
		if 'inputImg' not in request.files:
			print(" > [[EXCEPTION]]\n> inputImg not in request.files!!")
			return render_template('index.html', inputImgUrl = "css/dummy.png", imgList = "")

		# クライアント側からinput画像のurlという値を受け取り
		inputImg = request.files['inputImg']

		# 例外処理2
		if inputImg.filename == '':
			print(" > [[EXCEPTION]]\n> inputImg.filename == empty!!")
			return render_template('index.html', inputImgUrl = "css/dummy.png", imgList = "")

		# 受け取ったinput画像urlを使って類似画像検索
		if inputImg and allowed_file(inputImg.filename):

			# 一時的にinput画像をサーバに保存
			ps.DeletePreviousData()
			filename = secure_filename(inputImg.filename)
			inputImg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			imgUrl = UPLOAD_FOLDER + "/" + filename

			sortedImgList = [];
			# sortedImgList = pd.DataFrame([]);

			###############################
			# 類似画像検索を実施
			if PROCESS_NUM is 0:
				# Hash法
				sortedImgList = ha.CalcDef_hash(imgUrl)
				# print(sortedImgList) # database/_practice/airplanes_image_0018.jpg

			elif PROCESS_NUM is 1:
				# ヒストグラム法
				sortedImgList = hi.CalcDef_histogram(imgUrl)

				# print(sortedImgList) # database/_practice/headphone_image_0021.jpg

			elif PROCESS_NUM is 2:
				# 特徴点
				sortedImgList = fd.CalcDef_feature(imgUrl)

			###############################


			# index.htmlのリダイレクト時に引数としてパスを渡す用に画像urlから"staic/"を削除
			# (index.html内で画像url指定してるところで、「"static"ディレクトリ内の」という指定の仕方を
			# してるので、パスに"static/"を入れる必要はないっぽい)
			imgUrl = imgUrl.strip("static/")
			imgList = sortedImgList[0].tolist()
			# imgList = sortedImgList.iloc[:,0].tolist()
			# print(imgList)

			e_time = time.time() - start
			print (" time: {0}".format(e_time) + " [s]")
			print(" " + str(len(imgList)) + " files are listed.")

			print("=====================================================")

			return render_template('index.html', inputImgUrl = imgUrl, imgList = imgList)


		else:
			return ''' <p>Invalid file (only .png, .jpg, gif)</p> '''

	else:
		return redirect(url_for('index'))



def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# ---------------------------------
# クリックされた画像のURLからプロジェクトのJSONを取得
# ---------------------------------
def getCodeJSON(clickedImgUrl):
	print("> Clicked image : " + clickedImgUrl)
	clickedImgUrl = "static/" + re.sub("http://127.0.0.1:8000/", "", clickedImgUrl)
	projectJSONPath = re.sub("/\d{1,}.[a-xA-Z]+", "/project.json", clickedImgUrl)
	print("> Path of project.json : " + projectJSONPath)
	try:
		with open(projectJSONPath) as f:
			df = json.load(f)
			# pprint.pprint(df, width=40)
			return df
	except:
		return 'Code not found.'



if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=8000)


