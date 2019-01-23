# 2019.01.22
# Scratch類似画像検索GUI化.
# Python v3.7.2,
# PythonでのWebアプリ作成用のフレームワークFlaskを使用.
#
# 実行方法
# 0. flaskをインストールする (pipを使ってインストールしました)
#    (https://pypi.org/project/Flask/1.0.2/)
# 1. GitHub()からリポジトリをクローンまたはzipでダウンロードするなどして、
#    ワーキングディレクトリの構成を下記ディレクトリ構成にする
# 2. シェル(ターミナル.appとか)でワーキングディレクトリの中のflaskディレクトリの中に移動する
#    $ cd Workspace/ (例)
# 3. app.pyを実行する
#    $ python app.py
# 4. ブラウザで http://127.0.0.1:8000にアクセスする
# 5. input画像を選んでsearchを押すと、画面中央に検索結果が表示される
# 6. 各画像をクリックすると、画像が使用されたプロジェクトIDのコードを示すJSONの中身が画面左側に表示される.
#
# ディレクトリ構成
# - flask
# 	- app.py                       : サーバ側のメイン処理1. クライアントとの通信など
# 	- SearchSimilarImage.py        : サーバ側のメイン処理.	類似画像検索の具体的な処理
# 	- templates
# 		- index.html               : ボタンなど. JavaScript, Ajax, JQueryもごちゃまぜに入っている(Webのつぎはぎなので...)
# 		- layout.html              : タイトルとか<head>とか
# 	- static
# 		- css                      : css
# 			- style.cssとdummy.png  : dummy.pngは最初の読み込み時にinput画像の代わりに表示する画像. のちにD&D実装するのでなくなる
# 		- database
# 			- lists                : 類似画像検索結果を保存しているcsvたち
# 				- inputImgHash.csv : input画像のパスとhash値のリスト(といっても1行しかない).
# 									 input画像がサーバにsubmitされたときに作成される. 軽い
# 				- pathHashList.csv : データベース内にある画像ファイルのパスとhash値のリスト.
# 									 index.html読み込み時にこの名前のファイルがなければ作成され(数分かかる)、あればそのまま使う
# 				- sortedImgList.csv : input画像hash値とデータベース画像hash値の差分を降順にソートしたリスト.
# 									 searchボタン押下時に毎回作成される. 時間かかる.
# 			- project1             : 検索対象の画像たち
# 			- ...
# 		- uploads                  : inputとしてアップロードされた画像たち. 念のため保存してるだけで、index.html読み込み時に毎回削除される
# 			- *.png
#
# TODO
# - 段階的な検索結果表示(莫大なデータ数への対応)
# - pathHashList.csvを作るときと作らない時の処理(データベースファイルに変更があった時のみ
# 	変更があったファイルのみに対してhashを計算する).



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


