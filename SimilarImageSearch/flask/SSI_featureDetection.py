import cv2
from docopt import docopt
import glob
import logging
import os
import sys
from IPython.display import Image, display_png
import numpy as np
import pandas as pd
import SSI_preprocess as ps



# setting
img_size = (200, 200)
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
detector = cv2.AKAZE_create()


def CalcDBImg_feature(comparing_dir_path):

    # get parameters
    # args = sys.argv
    # comparing_dir_path = dbImg_path

    # get comparing files
    # pattern = '%s/*.jpg'
    # comparing_files = glob.glob(pattern % (comparing_dir_path))
    # comparing_files = []
    # comparing_filesList = [glob.glob(dbImg_path + "/*/*." + ext) for ext in ALLOWED_EXTENSIONS]
    # for s in comparing_filesList:
    #     comparing_files.extend(s)

    # if len(comparing_files) == 0:
    #     logging.error('no files.')
    #     sys.exit(1)
    comparing_files = ps.getImageFilesFromDir(comparing_dir_path)

    comparing_descriptions = []
    comparing_noFeaturefiles = []

    for comparing_file in comparing_files:
        # comparing_file_name = os.path.basename(comparing_file)
        # if comparing_file_name == target_file_name:
        #     continue
        # read comparing image
        comparing_img_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            comparing_file,
        )
        comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
        comparing_img = cv2.resize(comparing_img, img_size)
        # キーポイントをdetectして(feature detection)一意な表現方法で記述(feature description) = 識別生
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
        # print(comparing_kp)
        # n行61列の2次元ndarrayが帰ってくる
        # print(str(comparing_des.shape) + " = " + str(comparing_des.size) + "  dim: " + str(comparing_des.ndim) + " " + str(type(comparing_des)))
        # print(comparing_des[0]) # 一行目
        if comparing_des is None:
            print(comparing_file + " has no feature description.")
            comparing_noFeaturefiles.append(comparing_file)
        else:
            comparing_descriptions.append(comparing_des)

    [comparing_files.remove(f) for f in comparing_noFeaturefiles] # 特徴点が検出できなかった画像はリストから削除
    comparing_featuredescriptions_list = np.array([comparing_files, comparing_descriptions], dtype=object)
    np.save("static/database/lists/comparing_feature_list.npy", comparing_featuredescriptions_list)




def CalcDef_feature(target_img_url):

    sortedImgList = pd.DataFrame([]) # for return
    dif = {}

    comparing_featuredescriptions_list = np.load("static/database/lists/comparing_feature_list.npy")
    comparing_path = comparing_featuredescriptions_list[0]
    comparing_descriptions = comparing_featuredescriptions_list[1]

    # read target image
    # target_file_name = os.path.basename(target_file_path)
    target_file_path = target_img_url
    target_img = cv2.imread(target_file_path, cv2.IMREAD_GRAYSCALE)
    target_img = cv2.resize(target_img, img_size)
    # 特徴点(keypoint), description = detector.detectAndCompute(target画像, マスク(殆どの場合Noneとしてる))
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)

    if target_des is not None:
        for i in range(len(comparing_path)):
            # detect
            matches = bf.match(target_des, comparing_descriptions[i])
            dist = [m.distance for m in matches]
            # print(matches)
            # print(dist)
            if dist is not None:
                dif[comparing_path[i]] = sum(dist) / len(dist)
            else:
                print("dist is None.")
    else:
        print("Target image has no feature.")
        # TODO
        # クライアント側にAlert出すリクエスト処理をapp.pyに追加してここで呼び出し
    # print(dif)

    # sort
    for k, v in sorted(dif.items(), reverse=False, key=lambda x: x[1]):
        k = k.strip("static/") # ssiクラスでの返り値に揃えます...
        sortedImgList = sortedImgList.append([k],[v]) # kを0列目、vを1列目にappendしていく(テキトーに書いたのに...)
    return sortedImgList


# if __name__ == '__main__':
