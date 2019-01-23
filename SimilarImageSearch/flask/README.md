# Scratch類似画像検索 [GUI版]
- 2019.01.22
- Python v3.7.2
- PythonでのWebアプリ作成用のフレームワークFlaskを使用.
- 動作確認済みブラウザ Google Chrome Version 71.0.3578.98 (Official Build) (64-bit)
- OS macOSX 10.14

# 実行方法
0. [flask(https://pypi.org/project/Flask/1.0.2/)]をインストールする (pipを使ってインストールしました)
1. [GitHub(https://github.com/CreativeCoding2019/CreativeCoding2019)]からリポジトリをクローンまたはzipでダウンロードするなどして、ワーキングディレクトリの構成を下記ディレクトリ構成にする
2. シェル(ターミナル.appとか)でワーキングディレクトリの中のflaskディレクトリの中に移動する</br>
   `$ cd Workspace/ (例)`
3. app.pyを実行する</br>
   `$ python app.py`
4. ブラウザで `http://127.0.0.1:8000`にアクセスする
5. Choose Fileボタンからinput画像を選んでsearchボタンを押すと、画面中央に検索結果が表示される
6. 各画像をクリックすると、「画像が使用されたプロジェクトIDのコードを示すJSON」が画面左側に表示される.

# ディレクトリ構成
- flask
	- app.py                       : サーバ側のメイン処理1. クライアントとの通信など
	- SearchSimilarImage.py        : サーバ側のメイン処理.	類似画像検索の具体的な処理
	- templates
		- index.html               : ボタンなど. JavaScript, Ajax, JQueryもごちゃまぜに入っている(Webのつぎはぎなので...)
		- layout.html              : タイトルとか<head>とか
	- static
		- css                      : css
			- style.cssとdummy.png  : dummy.pngは最初の読み込み時にinput画像の代わりに表示する画像. のちにD&D実装するのでなくなる
		- database
			- lists                : 類似画像検索結果を保存しているcsvたち
				- inputImgHash.csv : input画像のパスとhash値のリスト(といっても1行しかない). input画像がサーバにsubmitされたときに作成される. 軽い
				- pathHashList.csv : データベース内にある画像ファイルのパスとhash値のリスト. index.html読み込み時にこの名前のファイルがなければ作成され(数分かかる)、あればそのまま使う
				- sortedImgList.csv : input画像hash値とデータベース画像hash値の差分を降順にソートしたリスト. searchボタン押下時に毎回作成される. 時間かかる.
			- project1             : 検索対象の画像たち
			- ...
		- uploads                  : inputとしてアップロードされた画像たち 念のため保存してるだけで、index.html読み込み時に毎回削除される
			- *.png
# TODO
- 段階的な検索結果表示(莫大なデータ数への対応)
- pathHashList.csvを作るときと作らない時の処理(データベースファイルに変更があった時のみ変更があったファイルのみに対してhashを計算するようにしないと、時間かかって大変).
- JSON表示をスクラッチ用に整形.

