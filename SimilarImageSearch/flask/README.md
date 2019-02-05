# Scratch類似画像検索 [GUI版]
- 2019.02.05
- Python v3.7.2
- PythonでのWebアプリ作成用のフレームワークflaskを使用.
- 動作確認済みブラウザ Google Chrome Version 71.0.3578.98 (Official Build) (64-bit)
- OS macOSX 10.14

# 実行方法
0. [flask](https://pypi.org/project/Flask/1.0.2/)をインストールする (pipでインストールしました)
1. [GitHub](https://github.com/CreativeCoding2019/CreativeCoding2019)からリポジトリをクローンまたはzipでダウンロードするなどして、ワーキングディレクトリの構成を後述のディレクトリ構成にする
2. シェル(ターミナル.appとか)でワーキングディレクトリの中のflaskディレクトリの中に移動する</br>
(例) `$ cd ~/WorkSpace/CreativeCoding2019/SimilarImageSearch/flask `
3. app.pyを実行する→ローカルサーバが起動する</br>
   `$ python app.py`
4. ブラウザで `http://127.0.0.1:8000`にアクセスする
5. Choose Fileボタンからinput画像を選んでsearchボタンを押すと、画面中央に検索結果が表示される
6. 各画像をクリックすると、「画像が使用されたプロジェクトIDのコードを示すJSON」が画面左側に表示される
7. 「Show more ...」ボタンをクリックすると、複数枚ずつ画像が追加される


# ディレクトリ構成
- **flask**
	- app.py                       : サーバ側のメイン処理0。クライアントとの通信など
	- SSI_hash.py                  : サーバ側のメイン処理1。ハッシュ値による類似画像検索
	- SSI_histogram.py             : サーバ側のメイン処理2。カラーヒストグラムによる類似画像検索
	- SSI_featureDetection.py      : サーバ側のメイン処理3。特徴点検出による類似画像検索
	- **templates**
		- index.html               : ボタンなど。JavaScript, Ajax, JQueryもごちゃまぜに入っている(Webのつぎはぎなので...)
		- layout.html              : タイトルとかheadとか
	- **static**
		- **css**
			- style.cssとdummy.png  : dummy.pngは最初の読み込み時にinput画像の代わりに表示する画像。 のちにD&D実装するのでなくなる
		- **database**
			- **lists**                : 類似画像検索に使うデータベース上の画像の情報を保存しているファイルたち
				- comparing_hash_list.npy
				- comparing_histogram_list.npy
				- comparing_feature_list.npy
			- **project1**             : 検索対象の画像たち
			- ...
		- **uploads**                  : inputとしてアップロードされた画像たち。念のため保存してるだけで、index.html読み込み時に前回のものは毎回削除される
			- .pngとか.jpgとか
# TODO
- .npyを作るときと作らない時の処理(データベースファイルに変更があった時のみ変更があったファイルのみに対してhashを計算するようにしないと、時間かかって大変)。
- JSON表示をスクラッチ用に整形。

