import cvzone
from cvzone.ColorModule import ColorFinder
import cv2
import socket
import numpy as np


def adjust_saturation(img, saturation_scale=1.0):

    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    hsv_image[:, :, 1] = cv2.multiply(hsv_image[:, :, 1], saturation_scale)


    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 255)


    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return adjusted_image


image_path ="test1.jpg"


img = cv2.imread(image_path)
if img is None:
    print("Error: Unable to open image.")
    exit()

img = adjust_saturation(img, saturation_scale=1.5)  # Increase saturation by 50%

h, w, _ = img.shape

myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 54}


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5057)

while True:
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)

    if contours:
        data = contours[0]['center'][0], \
            h - contours[0]['center'][1], \
            int(contours[0]['area'])
        print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)


    imgContour = cv2.resize(imgContour, (0, 0), None, 1, 1)
    cv2.imshow("ImageContour", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
