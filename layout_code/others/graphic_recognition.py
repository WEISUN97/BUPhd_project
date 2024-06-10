import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import sys


# 加载图像
image_path = "/Users/bubble/Desktop/PyProjects/daily/parrot.jpg"
# 应用图像滤镜进行美化（例如，模糊/边缘增强）
image = Image.open(image_path)

# 应用滤镜（例如，边缘增强）
image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

# 转换为灰度以简化图像
image = image.convert("L")

# 保存或展示处理后的图像
image.save("processed_image.jpg")
# image.show()
image = cv2.imread("processed_image.jpg", cv2.IMREAD_GRAYSCALE)
blurred = cv2.GaussianBlur(image, (5, 5), 0)


# 使用Canny算法检测边缘
edges = cv2.Canny(blurred, 100, 200)
# cv2.imshow("Edges", edges)
# cv2.imwrite("edges.jpg", edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 提取点坐标
points = np.column_stack(np.where(edges > 0))
# 可选：打印坐标点
# print(points)


# contours 是一个列表，每个元素都是一个轮廓，即一组点
contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
