# 仓库介绍
 
本仓库包含一些目标检测中可能会用到的工具脚本

**crop_image_and_objects.py**  
适用于对图像和标注文件进行同时切割，子图像中包含对应子标注文件中个的局部目标；当图像尺寸极大时可考虑使用  
举例，将下图切割为4个（2x2）子块：  
![panda](https://github.com/EzioA/object_detection_utils/blob/main/assets/panda_gt.png)  
第一个子块及对应标注应如下图所示:  
![panda_patch](https://github.com/EzioA/object_detection_utils/blob/main/assets/panda_0_gt.png)  
目前仅支持规则的无覆盖切割;  
目前支持voc和yolo两种标注数据的切割，在指定切割模式后，对应生成voc和yolo的子文件夹;  
给定的路径文件夹必须包含全部图像和对应标注文件;

**voc_allocator.py**  
在给定目录下生成VOC路径格式的数据集，同时对数据集进行划分;
给定的路径文件夹必须包含全部图像和对应标注文件;

**draw_gt_images.py**  
区分两种模式:  
指定VOC模式时，只绘制VOC数据集中的test子集的ground truth图像，此时给定路径指向VOCdevkit;  
不指定VOC模式时，绘制给定文件夹中的ground truth图像，此时给定的路径文件夹必须包含全部图像和对应标注文件

**voc_target_status.py**  
 给定VOCdevkit，分别统计train子集、val子集、test子集中不同目标的数量


# 使用
**crop_image_and_objects.py**  
```
$ python crop_image_and_objects.py --data_dir dataset --mode voc --h_slice 2 --w_slice 2
$ python crop_image_and_objects.py --data_dir dataset --mode yolo --h_slice 2 --w_slice 2
$ python crop_image_and_objects.py --data_dir dataset --h_slice 2 --w_slice 2 --crop_only
```
指定的目录 _**data\_dir**_ 包含全部图像及对应的标注文件(.txt for YOLO, or .xml for VOC)，_**h\_slice**_ 与 _**w\_slice**_ 指定将高、宽分别切割几份。  
脚本同时支持仅仅切割图像而不处理标注文件，参数为 _**crop\_only**_。  
执行完毕后，路径树应如下:  
```
dataset
├── cropped_images
├── voc
└── yolo
```

**voc_allocator.py**  
```
$ python voc_allocator.py --data_dir dataset/voc --trainval_per 0.8 --train_per 0.8
```
在指定的目录下生成VOCdevkit，并划分数据集。  
参数 _**trainval\_per**_ 指定trainval子集占图像总数的比例，参数 _**train\_per**_ 指定train子集占trainval子集的比例。
执行完毕后，路径树应如下:  
```
dataset
├── cropped_images
├── voc
│   └── VOCdevkit
│       └── VOC2007
│           ├── Annotations
│           ├── ImageSets
│           │   └── Main
│           └── JPEGImages
└── yolo
```

**draw_gt_images.py**  
```
 $ python draw_gt_images.py --data_dir dataset/voc/VOCdevkit --voc
 $ python draw_gt_images.py --data_dir dataset
```
指定参数 _**voc**_ 后，绘制由 _**data\_dir**_ 指定的VOC数据集中test子集的ground truth图像；  
不指定参数 _**voc**_ 时，绘制 _**data\_dir**_ 中全部图像的ground truth图像，此时 _**data\_dir**_ 应包含全部图像及对应标注文件。  
执行完毕后，路径树应如下:  
```
dataset
├── cropped_images
├── gt
├── voc
│   └── VOCdevkit
│       └── VOC2007
│           ├── Annotations
│           ├── ImageSets
│           │   └── Main
│           ├── JPEGImages
│           └── gt
└── yolo
```

**voc_target_status.py**  
```
$ python voc_target_status.py --voc_dir dataset/voc/VOCdevkit
```
在终端显示由参数 _**voc\_dir**_ 指定的VOC数据集中，train子集、val子集和test子集的目标数量统计。

更多参数信息，请参考帮助文档:  
```
$ python xxx.py --help
```

# 更新历史
v0.1 原始版本.