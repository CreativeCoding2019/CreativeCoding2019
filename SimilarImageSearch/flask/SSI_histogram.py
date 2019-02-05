# python histogram_matching.py static/database/_practice/airplanes_image_0001.jpg static/database/_practice/

import cv2
from docopt import docopt
import glob
import logging
import os
import sys
from statistics import mean
import pandas as pd
import numpy as np
import SSI_preprocess as ps



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
img_size = (200, 200)
channels = (0, 1, 2)
mask = None
histogram_size = 256
ranges = (0, 256)

def CalcDBImg_histogram(dbImg_path):
# def histogramMatching(_target_file_path, _comparing_dir_path):
# if __name__ == '__main__':


    # logging config
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    # logging.info('%s start.' % (__file__))

    # get parameters
    # args = docopt(__doc__)
    # target_file_path = args['--target_file_path']
    # comparing_dir_path = args['--comparing_dir_path']
    # args = sys.argv
    # target_file_path = args[1]
    # comparing_dir_path = args[2]
    # target_file_path = _target_file_path
    # comparing_dir_path = _comparing_dir_path
    # comparing_dir_path = databaseImagesPath


    # setting

    # histogram_size = 256
    # ranges = (0, 256)
    # ret = {}

    # get comparing files
    # pattern = '%s/*.jpg'
    # comparing_files = glob.glob(pattern % (comparing_dir_path))

    comparing_files = ps.getImageFilesFromDir(dbImg_path)

    # 拡張子複数対応. 不格好...
    # comparing_files = []
    # # comparing_filesList = [glob.glob(comparing_dir_path + "/*." + ext) for ext in ALLOWED_EXTENSIONS]
    # comparing_filesList = [glob.glob(dbImg_path + "/*/*." + ext) for ext in ALLOWED_EXTENSIONS]
    # for s in comparing_filesList:
    #     comparing_files.extend(s)
    # # print("Comparing Files ...")
    # # print(comparing_files)

    # if len(comparing_files) == 0:
    #     logging.error('no files.')
    #     sys.exit(1)

    # print("comparing_files : " + str(len(comparing_files)))

    # 3次元配列
    # [
    #  [ファイル0の長さ256のヒストグラム_channel0, ファイル0の長さ256のヒストグラム_channel1, ファイル0の長さ256のヒストグラム_channel2,
    #  [ファイル1の長さ256のヒストグラム_channel0, ファイル1の長さ256のヒストグラム_channel1, ファイル1の長さ256のヒストグラム_channel2,
    # ]
    comparing_histogram_0ch = []
    comparing_histogram_1ch = []
    comparing_histogram_2ch = []


    for comparing_file in comparing_files:

        # comparing_file_name = os.path.basename(comparing_file)
        # if comparing_file_name == target_file_name:
        #     continue

        tmp_3ch = []

        for channel in channels:
            # calc histogram of target image

            # read comparing image
            # フルパスにしてる?
            comparing_img_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                comparing_file,
            )
            comparing_img = cv2.imread(comparing_img_path)
            comparing_img = cv2.resize(comparing_img, img_size)
            # calc histogram of comparing image
            # 長さ256の1次元行列<class 'numpy.ndarray'>で帰ってくる
            comparing_histogram = cv2.calcHist([comparing_img], [channel], mask, [histogram_size], ranges)
            tmp_3ch.append(comparing_histogram)

        comparing_histogram_0ch.append(tmp_3ch[0])
        comparing_histogram_1ch.append(tmp_3ch[1])
        comparing_histogram_2ch.append(tmp_3ch[2])
        # print("comparing_histogram_3ch")
        # print(type(comparing_histogram_3ch))
        # comparing_histogram_3chMean.append([[comparing_file],[mean(tmp)]])


    comparing_histogram_list = np.array([comparing_files, comparing_histogram_0ch, comparing_histogram_1ch, comparing_histogram_2ch], dtype=object)
    # pathhistogramList = np.array([comparing_files, comparing_histogram_0ch, comparing_histogram_1ch, comparing_histogram_2ch])
    np.save("static/database/lists/comparing_histogram_list.npy", comparing_histogram_list)
    # pathhistogramList = pd.DataFrame([comparing_files, comparing_histogram_0ch, comparing_histogram_1ch, comparing_histogram_2ch])
    # pathhistogramList = pd.DataFrame([comparing_files, comparing_histogram_3ch])
    # comparing_histogram_3ch = pd.DataFrame(comparing_histogram_3ch)
    # pathhistogramList.to_csv("static/database/lists/pathhistogramList.csv", index=False, header=False)
    # print("> comparing_histogram_list.npy is created. (" + str(len(comparing_histogram_list)) + " files)")



def CalcDef_histogram(target_img_url):
    # print(inputImgUrl) #static/uploads/hack01.jpg
    # print("********************")
    sortedImgList = pd.DataFrame([]) # for return
    dif = {}

    # read target image
    # target_file_name = os.path.basename(inputImgUrl)
    target_img = cv2.imread(target_img_url)
    target_img = cv2.resize(target_img, img_size)
    target_histogram_0ch = cv2.calcHist([target_img], [0], mask, [histogram_size], ranges)
    target_histogram_1ch = cv2.calcHist([target_img], [1], mask, [histogram_size], ranges)
    target_histogram_2ch = cv2.calcHist([target_img], [2], mask, [histogram_size], ranges)

    comparing_histogram_list = np.load("static/database/lists/comparing_histogram_list.npy")
    comparing_path = comparing_histogram_list[0]
    comparing_histogram_0ch = comparing_histogram_list[1]
    comparing_histogram_1ch = comparing_histogram_list[2]
    comparing_histogram_2ch = comparing_histogram_list[3]


    for i in range(len(comparing_path)):
        meanDif = (cv2.compareHist(target_histogram_0ch, comparing_histogram_0ch[i], 0) + \
                   cv2.compareHist(target_histogram_1ch, comparing_histogram_1ch[i], 0) + \
                   cv2.compareHist(target_histogram_2ch, comparing_histogram_2ch[i], 0)) / 3
        # print(meanDif)
        dif[comparing_path[i]] = meanDif

    # print(dif)

    # sort
    for k, v in sorted(dif.items(), reverse=True, key=lambda x: x[1]):
    # for k, v in sorted(ret.items(), reverse=True, key=lambda x: x[1]):
        # logging.info('%s: %f.' % (k, v))
        k = k.strip("static/") # ssiクラスでの返り値に揃えます...
        sortedImgList = sortedImgList.append([k],[v]) # kを0列目、vを1列目にappendしていく(テキトーに書いたのに...)
    return sortedImgList
    # logging.info('%s end.' % (__file__))
    # sys.exit(0)

