import glob
import os
import shutil
import tempfile
import urllib.request
import zipfile
import cv2
from shutil import copyfile

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

_temp_path = tempfile.gettempdir() + os.sep + 'descriptors' + os.sep + 'databases' + os.sep


def _load_dataset(*, file_path, dataset_name, ext, kind='', black=0, white=1, size=0):
    """

    :param dataset_name:
    :param kind:
    :param black:
    :param white:
    :param size:
    :return: dictionary with file name as a key and array of 0 and 1 representing image as a corresponding value
    """
    ret = {}

    if not os.path.exists(_temp_path):
        os.makedirs(_temp_path)

    copyfile(file_path + dataset_name + '.zip', _temp_path + dataset_name + '.zip')

    if not os.path.exists(_temp_path + dataset_name):
        with zipfile.ZipFile(_temp_path + dataset_name + '.zip') as zf:
                zf.extractall(_temp_path + dataset_name)

    for file in glob.glob(_temp_path + dataset_name + os.sep + kind + ext):
        img = Image.open(file)
        try:
            data = np.asarray(img, dtype='uint8')
        except SystemError:
            data = np.asarray(img.getdata(), dtype='uint8')
        img.close()

        if np.unique(data).tolist() == [0, 255]:
            data = data // 255
        elif np.unique(data).tolist() == [0, 1] and dataset_name == 'regular_polygons':
            data = data ^ 1
        else:
            raise ValueError("Wrong type of image")

        ret[os.path.basename(file)] = data
        size -= 1
        if size == 0:
            break

    return ret

if __name__ == "__main__":
    images = _load_dataset(file_path='C:\pyshape\\', dataset_name='regular_polygons', ext="*.png")
    #images = _load_dataset(file_path='C:\pyshape\\', dataset_name='MPEG7dataset',  ext="*.gif", kind='apple', size=1)

    print(images)
    for v in images.values():
        print(np.unique(v))
        im = Image.fromarray(v)
        plt.imshow(v, interpolation='nearest')
        plt.show()
