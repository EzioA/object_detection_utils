'''
检查VOC数据集中train, val, test各个子集中目标的数量;
'''

import os
import argparse
from collections import defaultdict
from terminaltables import AsciiTable

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


def fetch_status(vocdevkit, fd):
	anno_list = list(map(lambda x: x.strip(), fd.readlines()))
	status = defaultdict(int)

	for anno in anno_list:
		tree = ET.ElementTree(file = os.path.join(vocdevkit, "VOC2007", "Annotations", anno+".xml"))
		root = tree.getroot()
		object_set = root.findall("object")
		for object in object_set:
			status[object.find("name").text] += 1

	return status


def check_targets_status(vocdevkit):
	assert os.path.exists(os.path.join(vocdevkit, "VOC2007", "Annotations"))
	assert os.path.exists(os.path.join(vocdevkit, "VOC2007", "ImageSets", "Main"))

	with open(os.path.join(vocdevkit, "VOC2007", "ImageSets", "Main", "train.txt")) as f:
		train_status = fetch_status(vocdevkit, f)
		train_table = [["Class", "Total"]]
		_data = [[k, v] for k, v in train_status.items()]
		train_table.extend(_data)
		train_table = AsciiTable(train_table)
	with open(os.path.join(vocdevkit, "VOC2007", "ImageSets", "Main", "val.txt")) as f:
		val_status = fetch_status(vocdevkit, f)
		val_table = [["Class", "Total"]]
		_data = [[k, v] for k, v in val_status.items()]
		val_table.extend(_data)
		val_table = AsciiTable(val_table)
	with open(os.path.join(vocdevkit, "VOC2007", "ImageSets", "Main", "test.txt")) as f:
		test_status = fetch_status(vocdevkit, f)
		test_table = [["Class", "Total"]]
		_data = [[k, v] for k, v in test_status.items()]
		test_table.extend(_data)
		test_table = AsciiTable(test_table)

	return train_table, val_table, test_table


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--voc_dir", type=str, default="VOCdevkit", help="the path to VOCdevkit")

	opt = parser.parse_args()
	train_table, val_table, test_table = check_targets_status(opt.voc_dir)

	print("===Train status===")
	print(train_table.table)

	print("===Val status===")
	print(val_table.table)

	print("===Test status===")
	print(test_table.table)
