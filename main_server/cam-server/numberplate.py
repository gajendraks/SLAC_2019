
import numpy as np
import cv2
from copy import deepcopy
from PIL import Image
import pytesseract as tess

def im2double(im):
    res = np.zeros(shape=[len(im),len(im[0])])
    for i in range(len(im)):
        for j in range(len(im[0])):
            res=float(im[i][j])
    return res
def preprocess(img):
	cv2.imshow("Input",img)
	imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
	gray = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)

	sobelx = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=3)
	cv2.imshow("Sobel",sobelx)
	cv2.waitKey(0)
	ret2,threshold_img = cv2.threshold(sobelx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	cv2.imshow("Threshold",threshold_img)
	cv2.waitKey(0)
	return threshold_img

def cleanPlate(plate):
	print("CLEANING PLATE. . .")
	gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
	#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
	#thresh= cv2.dilate(gray, kernel, iterations=1)

	_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
	im1,contours,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	if contours:
		areas = [cv2.contourArea(c) for c in contours]
		max_index = np.argmax(areas)

		max_cnt = contours[max_index]
		max_cntArea = areas[max_index]
		x,y,w,h = cv2.boundingRect(max_cnt)

		if not ratioCheck(max_cntArea,w,h):
			return plate,None

		cleaned_final = thresh[y:y+h, x:x+w]
		#cv2.imshow("Function Test",cleaned_final)
		return cleaned_final,[x,y,w,h]

	else:
		return plate,None


def extract_contours(threshold_img):
	element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
	morph_img_threshold = threshold_img.copy()
	cv2.morphologyEx(src=threshold_img, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
	#cv2.imshow("Morphed",morph_img_threshold)
	#cv2.waitKey(0)

	im2,contours, hierarchy= cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
	cv2.imshow("Cropped",im2)
	cv2.waitKey(0)
	
	kernel = np.ones((10,30),np.uint8)
	erode = cv2.erode(im2,kernel,iterations=1)
	dilate = cv2.dilate(erode,kernel, iterations=1)
	kernel = np.ones((20,70),np.uint8)
	erode = cv2.dilate(dilate,kernel,iterations=1)
	dilate = cv2.erode(erode,kernel, iterations=1)
	im2double(dilate)
	cv2.imshow("Cropped",dilate)
	cv2.waitKey(0)
	return dilate


def ratioCheck(area, width, height):
	ratio = float(width) / float(height)
	if ratio < 1:
		ratio = 1 / ratio

	aspect = 4.7272
	min = 15*aspect*15  # minimum area
	max = 125*aspect*125  # maximum area

	rmin = 3
	rmax = 6

	if (area < min or area > max) or (ratio < rmin or ratio > rmax):
		return False
	return True

def isMaxWhite(plate):
	avg = np.mean(plate)
	if(avg>=115):
		return True
	else:
 		return False

def validateRotationAndRatio(rect):
	(x, y), (width, height), rect_angle = rect

	if(width>height):
		angle = -rect_angle
	else:
		angle = 90 + rect_angle

	if angle>15:
	 	return False

	if height == 0 or width == 0:
		return False

	area = height*width
	if not ratioCheck(area,width,height):
		return False
	else:
		return True



def cleanAndRead(img,contours):
	#count=0
	for i,cnt in enumerate(contours):
		min_rect = cv2.minAreaRect(cnt)

		if validateRotationAndRatio(min_rect):

			x,y,w,h = cv2.boundingRect(cnt)
			plate_img = img[y:y+h,x:x+w]


			if(isMaxWhite(plate_img)):
				#count+=1
				clean_plate, rect = cleanPlate(plate_img)

				if rect:
					x1,y1,w1,h1 = rect
					x,y,w,h = x+x1,y+y1,w1,h1
					#cv2.imshow("Cleaned Plate",clean_plate)
					#cv2.waitKey(0)
					plate_im = Image.fromarray(clean_plate)
					text = tess.image_to_string(plate_im, lang='eng')
					print("Detected Text : ",text)
					img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
					#cv2.imshow("Detected Plate",img)
					#cv2.waitKey(0)

	#print "No. of final cont : " , count



if __name__ == '__main__':
	print("DETECTING PLATE . . .")

	#img = cv2.imread("testData/Final.JPG")
	img = cv2.imread("dataset/2.jpg")

	threshold_img = preprocess(img)
	mask= extract_contours(threshold_img)
	print(type(mask[0][0]))
	img = cv2.imread("dataset/2.jpg",0)
	#cv2.imshow("Image",img)
	#cv2.waitKey(0)
	#res = cv2.multiply(img,mask)/255
	#cv2.imshow("Image",res)
	#cv2.waitKey(0)
	minmr = -1
	maxmr = -1
	minmc = -1
	maxmc = -1
	minm=-1
	maxm=-1
	#res = np.zeros(shape=[len(img),len(img[0])])
	for i in range(len(img)):
	    for j in range(len(img[i])):
	         if mask[i][j]>0:
	             if minmr<i or minmr==-1:
	                 minmr = i
	             if minmc<j or minmc==-1:
	                 minmc = j
	             if maxmr>i or maxmr==-1:
	                 maxmr = i
	             if maxmr>j or maxmr==-1:
	                 maxmc = j
	             if minm>img[i][j] or minm==-1:
	                 minm = img[i][j]
	             if maxm<img[i][j] or maxm==-1:
	                 maxm = img[i][j]
	minmr,minmc,maxmr,maxmc=maxmr,maxmc,minmr,minmc
	print(minmr,maxmr,minmc,maxmc)
	res = np.zeros(shape=[(maxmr-minmr+1)*3,(maxmc-minmc+1)*3])
	for i in range(minmr,maxmr+1):
	    for j in range(minmc,maxmc+1):
	        for k in range(-1,2):
	            for l in range(-1,2):
	              res[(i-minmr)*3+k][(j-minmr)*3+l]=(img[i][j]-minm)/(maxm-minm)*255
	#kernel = np.ones((3,3),np.uint8)
	#res = cv2.erode(res,kernel,iterations=1)
	#res = cv2.dilate(res,kernel,iterations=1)
	#res = cv2.erode(res,kernel,iterations=1)
	cv2.imshow("Image",res)
	cv2.waitKey(0)
	kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	res = cv2.filter2D(res, -1, kernel)
	res = cv2.GaussianBlur(res, (7,7),0)
	cv2.imwrite("file.jpg",res)
