from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
from image_process import canny
from datetime import datetime
import os
import string
import random

SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        # 変換
        img = canny(img)


        # 検索
        

        # 保存
        dt_now = datetime.now().strftime("%Y_%m_%d%_H_%M_%S_") + random_str(5)
        save_path = os.path.join(SAVE_DIR, dt_now + ".png")
        cv2.imwrite(save_path, img)

        print("save", save_path)

        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)

# # https://qiita.com/ynakayama/items/2cc0b1d3cf1a2da612e4
# # Flask などの必要なライブラリをインポートする
# from flask import Flask, render_template, request, redirect, url_for
# import numpy as np
# import os

# # 自身の名称を app という名前でインスタンス化する
# app = Flask(__name__)

# UPLOAD_FOLDER = os.path.basename('uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/upload', methods = ['POST'])
# def selectImage():
# 	file = request.files['image']
# 	f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# 	# add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
# 	file.save(f)
# 	return render_template('index.html')

# 	# imagePath = "/Users/yukako/Downloads/IMG_0091 copy 3.PNG"
# 	# return imagePath









# # メッセージをランダムに表示するメソッド
# def picked_up():
#     messages = [
#         "こんにちは、あなたの名前を入力してください",
#         "やあ！お名前は何ですか？",
#         "あなたの名前を教えてね"
#     ]
#     # NumPy の random.choice で配列からランダムに取り出し
#     return np.random.choice(messages)

# # ここからウェブアプリケーション用のルーティングを記述
# # index にアクセスしたときの処理
# @app.route('/')
# def index():
#     title = "ようこそ"
#     message = picked_up()
#     # index.html をレンダリングする
#     return render_template('index.html',
#                            message=message, title=title)

# # /post にアクセスしたときの処理
# @app.route('/post', methods=['GET', 'POST'])
# def post():
#     title = "こんにちは"
#     if request.method == 'POST':
#         # リクエストフォームから「名前」を取得して
#         name = request.form['name']
#         # index.html をレンダリングする
#         return render_template('index.html',
#                                name=name, title=title)
#     else:
#         # エラーなどでリダイレクトしたい場合はこんな感じで
#         return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.debug = True # デバッグモード有効化
#     app.run(host='0.0.0.0') # どこからでもアクセス可能に