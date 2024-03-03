import json
import os
 
# 路径配置（根据自己的路径修改）
images_dir = r'img'
annotations_dir = r'labels'
 
# 类别映射字典（根据自己的内容修改）
categories = {
    0: "disconnection",
    1: "spots",
    2: "black line",
    3: "dirty",
    4: "Oblique white line",
    5: "Abnormal roller",
    6: "clew",
    7: "Abnormal duckbill"
}
 
# COCO格式的基本结构
coco_output = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": [{"id": k, "name": v, "supercategory": ""} for k, v in categories.items()]
}
 
# 图片和标注的ID计数器
image_id = 1
annotation_id = 1
 
# 遍历annotations目录下的所有TXT文件
for filename in os.listdir(annotations_dir):
    if filename.endswith('.txt'):
        # 假设文件名与图片文件名一致（不包含扩展名）
        image_filename = filename.replace('.txt', '.jpg')
        image_path = os.path.join(images_dir, image_filename)
        
        # TODO: 如果每张图片的大小都一样，你可以在这里指定
        # 如果大小不一样，你需要读取图片文件来获取实际尺寸
        # image_width = 960
        # image_height = 960

        try:
            with Image.open(image_path) as img:
                image_width, image_height = img.size
                print(f"Actual Image Dimensions: {image_width} x {image_height}")
        except Exception as e:
            print(f"Error reading image: {e}")       
        
        # 添加图片信息到COCO数据结构
        coco_output['images'].append({
            "id": image_id,
            "file_name": image_filename,
            "width": image_width,
            "height": image_height
        })
        
        # 读取每个TXT文件并添加标注信息
        txt_file_path = os.path.join(annotations_dir, filename)
        with open(txt_file_path, 'r') as file:
            for line in file:
                class_id, x_center, y_center, width, height = map(float, line.strip().split())
                
                # COCO要求bbox是[x_min, y_min, width, height]，而不是中心点坐标
                x_min = (x_center - width / 2) * image_width
                y_min = (y_center - height / 2) * image_height
                width = width * image_width
                height = height * image_height
                
                # 添加标注信息
                coco_output['annotations'].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": class_id,
                    "bbox": [x_min, y_min, width, height],
                    "area": width * height,
                    "segmentation": [],  # 如果你有分割信息可以在这里添加
                    "iscrowd": 0
                })
                
                annotation_id += 1
        
        # 更新图片ID
        image_id += 1
 
# 将COCO数据结构写入JSON文件（保存的json路径自己修改）
with open('train.json', 'w') as json_file:
    json.dump(coco_output, json_file, indent=4)
 
print("Conversion completed!")