'''
绘制ground truth图像，目前支持绘制voc的test子集，以及绘制数据文件夹中的图像;
'''

import argparse
import cv2
import os
import glob

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


def draw_voc_gt(vocdevkit="VOCdevkit"):
	assert os.path.exists(os.path.join(vocdevkit, "VOC2007", "Annotations"))
	assert os.path.exists(os.path.join(vocdevkit, "VOC2007", "ImageSets", "Main"))
	assert os.path.exists(os.path.join(vocdevkit, "VOC2007", "JPEGImages"))

	gt_dir = os.path.join(vocdevkit, "VOC2007", "gt")
	os.makedirs(gt_dir, exist_ok=True)

	with open(os.path.join(vocdevkit, "VOC2007", "ImageSets", "Main", "test.txt")) as f:
		_list = list(map(lambda x: x.strip(), f.readlines()))

	for image_name in _list:
		image_path = os.path.join(vocdevkit, "VOC2007", "JPEGImages", image_name+".jpg")
		anno_path = os.path.join(vocdevkit, "VOC2007", "Annotations", image_name+".xml")

		image = cv2.imread(image_path)

		tree = ET.ElementTree(file=anno_path)
		root = tree.getroot()
		object_set = root.findall("object")
		for object in object_set:
			# name = object.find("name").text
			xmin = int(object.find("bndbox").find("xmin").text)
			ymin = int(object.find("bndbox").find("ymin").text)
			xmax = int(object.find("bndbox").find("xmax").text)
			ymax = int(object.find("bndbox").find("ymax").text)

			cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(255, 0, 0), thickness=4)
		#     cv2.putText(image, name, (xmin, ymin), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=255)

		cv2.imwrite(os.path.join(gt_dir, os.path.splitext(os.path.basename(image_path))[0] + "_gt.jpg"), image)


def draw_common_gt(data_dir="dataset"):
	gt_dir = os.path.join(data_dir, "gt")
	os.makedirs(gt_dir, exist_ok=True)

	suffix = ["tif", "tiff", "png", "jpg", "jpeg", "bmp"]
	image_list = sum([glob.glob(f"{data_dir}/*.{_suffix}") for _suffix in suffix], [])
	for image_path in image_list:
		anno_path = os.path.join(os.path.dirname(image_path), os.path.splitext(os.path.basename(image_path))[0] + ".xml")
		if not os.path.exists(anno_path):
			anno_path = os.path.join(os.path.dirname(image_path), os.path.splitext(os.path.basename(image_path))[0] + ".txt")
			if not os.path.exists(anno_path):
				continue

		if anno_path.endswith("xml"):
			image = cv2.imread(image_path)

			tree = ET.ElementTree(file=anno_path)
			root = tree.getroot()
			object_set = root.findall("object")
			for object in object_set:
				xmin = int(object.find("bndbox").find("xmin").text)
				ymin = int(object.find("bndbox").find("ymin").text)
				xmax = int(object.find("bndbox").find("xmax").text)
				ymax = int(object.find("bndbox").find("ymax").text)

				cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(255, 0, 0), thickness=4)

			cv2.imwrite(os.path.join(gt_dir, os.path.splitext(os.path.basename(image_path))[0] + "_gt.jpg"), image)
		else:
			image = cv2.imread(image_path)
			labels = []
			coor = []
			with open(anno_path, "r") as f:
				for line in f.readlines():
					label = str(int(float(line.strip().split(" ")[0])))
					line = list(map(float, line.strip().split(" ")[1:]))
					labels.append(label)
					coor.append(line)

			img_height, img_width = image.shape
			for label, bbox in zip(labels, coor):
				x, y, w, h = bbox
				x *= img_width
				y *= img_height
				w *= img_width
				h *= img_height

				cv2.rectangle(image, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)),
							  color=(255, 0, 0), thickness=4)
				# cv2.putText(image, label, (int(x - w / 2), int(y - h / 2)), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
				# 			fontScale=2, color=255)
			cv2.imwrite(os.path.join(gt_dir, os.path.splitext(os.path.basename(image_path))[0] + "_gt.jpg"), image)


def pre_process(data_dir="dataset", voc=False):
	if voc:
		draw_voc_gt(data_dir)
	else:
		draw_common_gt(data_dir)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--data_dir", type=str, default="dataset", help="when in VOC mode, this is the path to VOCdevkit; "
																		"otherwise, this is the directory containing all the images and annotations")
	parser.add_argument("--voc", action="store_true", help="where draw gts in mode VOC")

	opt = parser.parse_args()
	pre_process(opt.data_dir, opt.voc)
