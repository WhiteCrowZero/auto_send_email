import os
import json

# 定义读取文件夹下图片并生成映射的函数
def generate_image_mapping(folder_path):
    images = {}
    # 遍历文件夹中的所有文件
    for idx, filename in enumerate(os.listdir(folder_path)):
        # 只处理图片文件，可以根据需要扩展支持的图片类型
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            """
            # 统一键名
            placeholder = f'image1'
            images.setdefault(placeholder, []).append(os.path.join(folder_path, filename))
            """
            placeholder = f'image{idx+1}'
            images[placeholder] = os.path.join(folder_path, filename)
    return images

# 指定图片文件夹路径
folder_path = './img'

# 生成图片映射
image_mapping = generate_image_mapping(folder_path)

# 将映射写入JSON文件
with open('image_mapping.json', 'w', encoding='utf-8') as json_file:
    json.dump(image_mapping, json_file, ensure_ascii=False, indent=4)

# print(image_mapping)
print("图片映射已生成并保存到 image_mapping.json 文件中")
