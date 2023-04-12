import time
import base64
import requests
import numpy as np
import cv2
import os
from PIL import Image
IMAGE_LIST = {

}
for path, dir_list, file_list in os.walk('./face_db'):
    for file_name in file_list:
        name = file_name.split('.')[0]
        IMAGE_LIST[str(1)+name] = os.path.join(path, file_name)

URL_SAVE = 'http://127.0.0.1:8000/save_embedding'
URL_FIND = 'http://127.0.0.1:8000/find_embedding'
URL_GET_ANTI='http://127.0.0.1:8000/get_face_anti'
URL_GET_LAND='http://127.0.0.1:8000/get_landmark_parsing'
# 这里请注意，data的key，要和我们上面定义方法的形参名字和数据类型一致
# 有默认参数不输入完整的参数也可以


def base64tonumpy(s):
    img_data = base64.b64decode(s)
    nparr = np.fromstring(img_data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


def numpytobase64(image):
    retval, buffer = cv2.imencode('.jpg', image)
    pic_str = base64.b64encode(buffer)
    return pic_str.decode()

def show_img(img_parse, save_path='test.jpg'):
    # input shape is hwc
    if img_parse.dtype != np.uint8:
        img_parse = img_parse.astype(np.uint8)
    Image.fromarray(img_parse).save(save_path)
# for k, v in IMAGE_LIST.items():
#     img = np.array(Image.open(v))
#     res = requests.post(URL_SAVE,
#                         json={"image": img.tolist(), 'name': k})
#     print(res.json())
#     print('finish add',k)

# time.sleep(3)

# for k, v in IMAGE_LIST.items():
#     img = np.array(Image.open(v))
#     res = requests.post(URL_FIND,
#                     json={"image": img.tolist()})
#     print(res.json())
#     print('finish find',k)

img = np.array(Image.open('./000534.jpg'))
res = requests.post(URL_GET_ANTI,
                    json={"image": img.tolist()})
result_dict=res.json()
# show_img(np.array(result_dict['landmark_image']), 'test_landmark.jpg')
# show_img(np.array(result_dict['parsing_image']), 'test_parsing.jpg')
print(res.json())

