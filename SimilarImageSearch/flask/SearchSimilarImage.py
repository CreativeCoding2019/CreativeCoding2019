# 2019.01.22
# Python v3.7.2
#
# TODO:
# - 高速化、精度向上
#	 - ファイル探索処理工夫できないか確認
#	 - サイズの影響が強いかどうか調べる
# - まったく同じ画像を除外などする工夫
# - Input画像とOutput画像のサイズとかの情報取得する
# 参考
# https://qiita.com/redshoga/items/60db7285a573a5e87eb6

from PIL import Image, ImageFile
import numpy as np
import imagehash
import os
from glob import glob
import re
import pprint
from collections import OrderedDict
import time
import pandas as pd
import codecs
import json
import shutil

# ---------------------------------
# グローバル変数など
# ---------------------------------
# 表示する類似画像の個数
showImgNum = 5
# サイズの大きな画像をスキップしない
ImageFile.LOAD_TRUNCATED_IMAGES = True


# ---------------------------------
# 前回のアップロード画像等を削除し、必要なディレクトリを作成
# ---------------------------------
def DeleteCash():
	# shutil.rmtree("static/database/lists")
	if not os.path.isdir("static/database/lists"):
		os.mkdir("static/database/lists")

	shutil.rmtree("static/uploads")
	os.mkdir("static/uploads")
	print("> Previous lists and uploaded files are deleted.")

# ---------------------------------
# アップロードされた画像のハッシュ値を計算
# ---------------------------------
def CalcInputImgHash(inputImgUrl):
	inputImgHash = imagehash.phash(Image.open(inputImgUrl))
	# print(">> " + str(inputImgHash))
	inputImgHashDf = pd.DataFrame([inputImgUrl, inputImgHash])
	inputImgHashDf.to_csv("static/database/lists/inputImgHash.csv", index=False, header=False)
	print("> inputImgHash.csv is created.")
	return inputImgHash


# ---------------------------------
# クリックされた画像のURLからプロジェクトのJSONを取得
# ---------------------------------
def getCodeJSON(clickedImgUrl):
	print("=========================")
	print(">>>>> URL of clicked image : " + clickedImgUrl)
	clickedImgUrl = "static/" + re.sub("http://127.0.0.1:8000/", "", clickedImgUrl)
	projectJSONPath = re.sub("/\d{1,}.[a-xA-Z]+", "/project.json", clickedImgUrl)
	print(">>>>> Path of project.json : " + projectJSONPath)
	try:
		with open(projectJSONPath) as f:
			df = json.load(f)
			# pprint.pprint(df, width=40)
			return df
	except:
		return 'Code not found.'


# ---------------------------------
# データベースにある画像ファイルからハッシュ値のリストを作成
# ---------------------------------
def CalcDBImgHash():

	# # 正規表現メモ: 任意の1桁以上の数値\d{1,}
	# # 正規表現メモ: 任意の英数字以外[\W]や英数字[\w]の0回以上の繰り返し*と記号/にマッチする部分を取り除く
	# すべての画像のパス取得
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
	tempList = [glob("static/database/*/*/*." + ext) for ext in ALLOWED_EXTENSIONS]
	pathList = []
	for s in tempList:
		pathList.extend(s)
	# input画像が所属するProjectIDはハッシュ値算出から取り除く
	# pathList = [path for path in pathList if prjID not in path] # 内包表記 [繰り返しindex for 繰り返しindex in 検索元]と[if 特定の文字列 in 検索元]

	# input画像以外のすべての画像のハッシュ値を算出
	hashList = [imagehash.phash(Image.open(img)) for img in pathList]

	# flaskで"static/"は自動指定されるので"static/"を抜かす
	pathList = [p.strip("static/") for p in pathList]

	pathHashList = pd.DataFrame([pathList, hashList])
	pathHashList.to_csv("static/database/lists/pathHashList.csv", index=False, header=False)
	print("> pathHashList.csv is created. (" + str(len(pathList)) + " files)")


# ---------------------------------
# 予め作成したDB画像のハッシュ値リストとアップロード画像のハッシュ値との差分を計算
# ---------------------------------
def CalcDef(inputImgUrl):
	inputImgHash = int(str(CalcInputImgHash(inputImgUrl)), 16)
	dbImgHashList = pd.read_csv("static/database/lists/pathHashList.csv", header=None)
	dbPathList = dbImgHashList.iloc[0,:]
	dbHashList = [int(val, 16) for val in dbImgHashList.iloc[1,:]]

	difList = [abs(inputImgHash - int(hashVal)) for hashVal in dbHashList] # intのlistで帰る
	# print(difList)

	dic = OrderedDict((dbPathList[i], difList[i]) for i in range(len(dbPathList)))
	# print(k, v) for k, v in dic.items() # 辞書型の確認はこの方法のみ
	# Value(difList(ハッシュ値差分)の値)で降順でソート
	# lambdaは無名関数の定義で用いる決まり文句. "x[1]を返す無名の関数をkeyパラメータに入れる"的な意味らしい
	sortedDic = sorted(dic.items(), key = lambda x:x[1]) # tupleのlistで帰ってくる
	# TODO
	# ハッシュ値の差分0 (= 全く同じ画像)は削除する?
	sortedImgList = pd.DataFrame(sortedDic)
	sortedImgList.to_csv("static/database/lists/sortedImgList.csv", index=False, header=False)
	print("> sortedImgList.csv is created.")

	return sortedImgList


# def main():

# 	start = time.time()
# 	DeleteCash()
# 	CalcDBImgHash()

# 	e_time = time.time() - start
# 	print ("e_time:{0}".format(e_time) + "[s]")




# if __name__ == '__main__':
# 	main()


