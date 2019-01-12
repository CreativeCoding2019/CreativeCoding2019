類似画像検索について
190109 高田

参考サイトは↓
https://tech.unifa-e.com/entry/2017/11/27/111546

→適当に画像を用意する。例えばSimilarImageSSearch/imageを利用
→2画像間のハッシュ値の差分を求め、この数値を評価関数として類似画像を検索する。
（差が小さい方が似ている）。
→ハッシュ値の差分を求める関数はSimilarImage_Hush.txt参照。
　このままjupyterに貼ると動くはず。pythonコード。画像へのパスは適宜修正してください。。

