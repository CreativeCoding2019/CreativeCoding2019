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
from glob import glob
# import pprint
from collections import OrderedDict
import pandas as pd
import SSI_preprocess as ps
# import codecs

# ---------------------------------
# グローバル変数など
# ---------------------------------
# 表示する類似画像の個数
showImgNum = 5
# サイズの大きな画像をスキップしない
ImageFile.LOAD_TRUNCATED_IMAGES = True


# ---------------------------------
# データベースにある画像ファイルからハッシュ値のリストを作成
# ---------------------------------
def CalcDBImg_hash(comparing_dir_path):

	# # 正規表現メモ: 任意の1桁以上の数値\d{1,}
	# # 正規表現メモ: 任意の英数字以外[\W]や英数字[\w]の0回以上の繰り返し*と記号/にマッチする部分を取り除く
	# すべての画像のパス取得

	# tempList = [glob(databaseImagesPath + "*/*." + ext) for ext in ALLOWED_EXTENSIONS] # テストデータ用
	# # tempList = [glob("static/database/_practice/*." + ext) for ext in ALLOWED_EXTENSIONS] # テストデータ用
	# # tempList = [glob("static/database/*/*/*." + ext) for ext in ALLOWED_EXTENSIONS]
	# pathList = []
	# for s in tempList:
	# 	pathList.extend(s)

	comparing_files = ps.getImageFilesFromDir(comparing_dir_path)
	# input画像が所属するProjectIDはハッシュ値算出から取り除く
	# pathList = [path for path in pathList if prjID not in path] # 内包表記 [繰り返しindex for 繰り返しindex in 検索元]と[if 特定の文字列 in 検索元]

	# input画像以外のすべての画像のハッシュ値を算出
	comparing_hash = [imagehash.phash(Image.open(p)) for p in comparing_files]

	# flaskで"static/"は自動指定されるので"static/"を抜かす
	comparing_files = [p.strip("static/") for p in comparing_files]

	comparing_hash_list = np.array([comparing_files, comparing_hash], dtype=object)
	np.save("static/database/lists/comparing_hash_list.npy", comparing_hash_list)
	# pathHashList = pd.DataFrame([pathList, hashList])
	# pathHashList.to_csv("static/database/lists/pathHashList.csv", index=False, header=False)
	# print("> pathHashList.csv is created. (" + str(len(pathList)) + " files)")


# ---------------------------------
# 予め作成したDB画像のハッシュ値リストとアップロード画像のハッシュ値との差分を計算
# ---------------------------------
def CalcDef_hash(target_img_url):
	# print(inputImgUrl) # static/uploads/e4rth_15b.JPG

	target_hash = int(str(imagehash.phash(Image.open(target_img_url))), 16)
	comparing_hash_list = np.load("static/database/lists/comparing_hash_list.npy")
	comparing_path = comparing_hash_list[0]
	comparing_hash = [int(str(i), 16) for i in comparing_hash_list[1]]

	dif_list = [abs(target_hash - hashVal) for hashVal in comparing_hash] # intのlistで帰る
	# print(difList)

	dic = OrderedDict((comparing_path[i], dif_list[i]) for i in range(len(comparing_path)))
	# print(k, v) for k, v in dic.items() # 辞書型の確認はこの方法のみ
	# Value(difList(ハッシュ値差分)の値)で降順でソート
	# lambdaは無名関数の定義で用いる決まり文句. "x[1]を返す無名の関数をkeyパラメータに入れる"的な意味らしい
	sortedImgList = pd.DataFrame(sorted(dic.items(), key = lambda x:x[1])) # tupleのlistで帰ってくる
	# TODO
	# ハッシュ値の差分0 (= 全く同じ画像)は削除する?
	# sortedImgList = pd.DataFrame(sortedDic)
	# sortedImgList.to_csv("static/database/lists/sortedImgList.csv", index=False, header=False)
	# print("> sortedImgList.csv is created.")
	return sortedImgList


# def main():

# 	start = time.time()
# 	e_time = time.time() - start
# 	print ("e_time:{0}".format(e_time) + "[s]")




# if __name__ == '__main__':
# 	main()


