'''
生成VOC路径的数据集，并进行数据集的划分;
划分代码来源网络;
'''

import os
import shutil
import glob
from PIL import Image
import argparse
import os
import random

suffix = ["tif", "tiff", "png", "jpg", "jpeg", "bmp"]


def voc_allocator(root_dir, trainval_per=0.8, train_per=0.8):
	os.makedirs(os.path.join(root_dir, "VOCdevkit", "VOC2007", "Annotations"), exist_ok=True)
	os.makedirs(os.path.join(root_dir, "VOCdevkit", "VOC2007", "ImageSets", "Main"), exist_ok=True)
	os.makedirs(os.path.join(root_dir, "VOCdevkit", "VOC2007", "JPEGImages"), exist_ok=True)

	image_root = root_dir
	anno_root = root_dir
	image_dst = os.path.join(root_dir, "VOCdevkit", "VOC2007", "JPEGImages")
	anno_dst = os.path.join(root_dir, "VOCdevkit", "VOC2007", "Annotations")

	image_list = sum([glob.glob(f"{image_root}/*.{_suffix}") for _suffix in suffix], [])
	for image_path in image_list:
		label_path = os.path.join(anno_root, os.path.splitext(os.path.basename(image_path))[0]+".xml")
		if os.path.exists(label_path):
			image = Image.open(image_path)
			image.save(os.path.join(image_dst, os.path.splitext(os.path.basename(image_path))[0]+".jpg"))
			shutil.copyfile(label_path, os.path.join(anno_dst, os.path.basename(label_path)))


	os.chdir(os.path.join(root_dir, "VOCdevkit", "VOC2007"))

	xmlfilepath = 'Annotations'
	txtsavepath = os.path.join("ImageSets", "Main")
	total_xml = os.listdir(xmlfilepath)

	num = len(total_xml)
	list = range(num)
	tv = int(num * trainval_per)
	tr = int(tv * train_per)
	trainval = random.sample(list, tv)
	train = random.sample(trainval, tr)

	ftrainval = open(os.path.join(txtsavepath, "trainval.txt"), 'w')
	ftest = open(os.path.join(txtsavepath, "test.txt"), 'w')
	ftrain = open(os.path.join(txtsavepath, "train.txt"), 'w')
	fval = open(os.path.join(txtsavepath, "val.txt"), 'w')

	for i in list:
		name = total_xml[i][:-4] + '\n'
		if i in trainval:
			ftrainval.write(name)
			if i in train:
				ftrain.write(name)
			else:
				fval.write(name)
		else:
			ftest.write(name)

	ftrainval.close()
	ftrain.close()
	fval.close()
	ftest.close()



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--data_dir", type=str, default="dataset", help="the directory containing all images and annotations")
	parser.add_argument("--trainval_per", type=float, default=0.8, help="the fraction of trainval within the total dataset")
	parser.add_argument("--train_per", type=float, default=0.8, help="the fraction of train within trainval")

	opt = parser.parse_args()
	voc_allocator(opt.data_dir, opt.trainval_per, opt.train_per)
