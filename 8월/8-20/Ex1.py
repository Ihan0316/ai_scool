import cv2
import matplotlib.pyplot as plt

data1 = cv2.imread('./8월/8-20/maltipoo.jpg', cv2.IMREAD_COLOR)
data2 = cv2.imread('./8월/8-20/maltipoo.jpg', cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('image')
cv2.imshow('image', data1)

rgb = cv2.cvtColor(data1, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(data2, cv2.COLOR_GRAY2RGB)

# print(type(data1))
# print(type(data2))

cv2.waitKey(0)
plt.imshow(rgb)
plt.axis('off')
plt.show()
cv2.destroyAllWindows()