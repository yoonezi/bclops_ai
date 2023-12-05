import os
import time
from io import BytesIO

import cv2
import requests
from matplotlib import pyplot as plt
from PIL import Image

from displayresult import (drawAll, drawJointset, getDataFrame, makeStereonet,
                           saveDataFrameAsImage)
from function import evaluate, imageProcessing
from jointExtract import getLine, make_data, redImage

print('start')
start = time.time()

####################################################################################
################################## 이미지 경로 #######################################
img_path = "./url_param.txt" 

# img_url = "https://bclops.s3.ap-northeast-2.amazonaws.com/samples/input_1.png"

img_url1 = "https://bclops.s3.ap-northeast-2.amazonaws.com/input_1.png"
img_url2 = "https://bclops.s3.ap-northeast-2.amazonaws.com/input_2.png"
img_url3 = "https://bclops.s3.ap-northeast-2.amazonaws.com/input_3.png"
img_url4 = "https://bclops.s3.ap-northeast-2.amazonaws.com/input_4.png"
####################################################################################
####################################################################################


# URL을 파일에서 읽어옴
with open(img_path , 'r') as file:
    img_url = file.read().strip() 

# URL에서 이미지를 가져와 처리
response = requests.get(img_url)

img = Image.open(BytesIO(response.content))
img = img.resize((1024, 512))

save_dir = './evaluate/image/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# 이미지를 저장
img.save('./evalutate/image/input.png')

original_image = "./evalutate/image/input.png"
ai_image = evaluate()
print("ai fin")
output = imageProcessing(original_image, ai_image)
cv2.imshow("output", output)

# 카메라팀
redImage = redImage(output)
jointPoint = getLine(redImage)
distance = 100
data = make_data(jointPoint, distance)

original_img = cv2.imread(original_image)
resultImg = drawAll(original_img, data)

cv2.imwrite("resultimg.jpg", resultImg)
for i in range(0, len(data)):
    jointset_result = drawJointset(original_img, data, "jointset%d" % i, setnum=i)
    cv2.imshow("resultimg%d" % i, jointset_result)
    cv2.imwrite("resultjointset%d.jpg" % i, jointset_result)
plt.close('all')
stereonet = makeStereonet(data)
plt.savefig('stereonetImg.jpg')
plt.show()
dataFrame = getDataFrame(data)
print(dataFrame)
dataFrame.to_csv("resultData.csv")
saveDataFrameAsImage(dataFrame, "table.jpg")

stop = time.time()
print("testing time :", round(stop - start, 3), "ms")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("testing time :", round(stop - start, 3), "ms")
cv2.waitKey(0)
cv2.destroyAllWindows()

# [
#     {
#         'lines': [[[461, 415], [479, 160]], [[482, 298], [489, 91]], [[481, 412], [492, 91]], [[512, 180], [522, 23]]], 
#         'angles': [94, 91, 91, 93], 
#         'spacing': [[0.21526290295732453, 0.24002264159732967, 2.1833733289700508], [11.772175622290344]], 
#         'length': [255.63, 207.12, 321.19, 157.32]
#     },
#     {
#         'lines': [[[49, 333], [610, 238]], [[682, 412], [852, 393]]], 
#         'angles': [170, 173], 
#         'spacing': [[0.21526290295732453, 0.24002264159732967, 2.1833733289700508], [11.772175622290344]], 
#         'length': [568.99, 171.06]
#     }
# ]


# [
#     {
#         "lines":  [[[1, 151], [799, 135]],[[1, 321], [799, 225]]],
#         "angles":  [179,173],
#         "spacing":  [11],
#         "length":  [63.190031585185174,65]
#     },
#     {
#         "lines":  [[[512, 1], [583, 449]], [[138, 1], [363, 449]]],
#         "angles":  [81, 63],
#         "spacing":  [24.275037034],
#         "length":  [35.99496464444444, 39.279395199999996]
#     }
# ]


# [
#     {
#         'lines': [[[461, 415], [479, 160]], [[482, 298], [489, 91]], [[481, 412], [492, 91]], [[512, 180], [522, 23]]], 
#         'angles': [94, 91, 91, 93], 
#         'spacing': [[0.21526290295732453, 0.24002264159732967, 2.1833733289700508], [11.772175622290344]], 
#         'length': [255.63, 207.12, 321.19, 157.32]
#     }, 
#     {
#         'lines': [[[49, 333], [610, 238]], [[682, 412], [852, 393]]], 
#         'angles': [170, 173], 
#         'spacing': [[0.21526290295732453, 0.24002264159732967, 2.1833733289700508], [11.772175622290344]], 
#         'length': [568.99, 171.06]
#     }
# ]