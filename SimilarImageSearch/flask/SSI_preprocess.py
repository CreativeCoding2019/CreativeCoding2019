import os
import shutil

# ---------------------------------
# 前回のアップロード画像等を削除し、必要なディレクトリを作成
# ---------------------------------
def DeletePreviousData():
	# shutil.rmtree("static/database/lists")
	if not os.path.isdir("static/database/lists"):
		os.mkdir("static/database/lists")

	shutil.rmtree("static/uploads")
	os.mkdir("static/uploads")
	print("> Previous lists and uploaded files are deleted.")


def getImageFilesFromDir(dbImg_path):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
    comparing_files = []
    comparing_filesList = [glob.glob(dbImg_path + "/*/*." + ext) for ext in ALLOWED_EXTENSIONS]
    for s in comparing_filesList:
        comparing_files.extend(s)
    # print("Comparing Files ...")
    # print(comparing_files)

    if len(comparing_files) == 0:
        logging.error('no files.')
        sys.exit(1)

    return comparing_files




# TODO
# データベースに変更があった時のみ新しく差分分のハッシュかヒストグラムを計算し直す処理