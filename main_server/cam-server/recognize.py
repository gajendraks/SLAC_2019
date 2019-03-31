import os
import glob
import cv2
import numpy as np
import pytesseract


img = cv2.imread("file.jpg",0)
(thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#cv2.imwrite("work.jpg", im_bw)
"""
for i in range(len(img)):
    for j in range(len(img[0])):
         for k in range(-3,4):
             for l in range(-3,4):
                 if i+k<0 or j+l<0 or i+k >= len(img) or j+l >= len(img[0]):
                     continue
                 if img[i][j]-img[i+k][j+l]>30:
                     img[i][j]=img[i+k][j+l]
"""
kernel = np.ones((4,4),np.uint8)
res = cv2.dilate(im_bw,kernel,iterations=1)
res = cv2.erode(res,kernel,iterations=1)
cv2.imwrite("file2.jpg",res)
os.system("tesseract "+"file2.jpg "+" -l eng output2.txt")
os.system("tesseract "+"file.jpg "+" -l eng output.txt")

#text = pytesseract.image_to_string(img, lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
#print(text)
