import numpy as np
import cv2

#Example used
img_path = './Test_data/1_15.png'
# Read image
img = cv2.imread(img_path)


#return folder of input images
def load_file(path):
    images = []
    for filename in os.listdir(path):
        img = cv2.imread(os.path.join(path,filename))
        if img is not None:
            images.append(img)
    return images
    
def manual_choicing_area(image_path):
    showCrosshair = True
    fromCenter = False
    #This allow user select region of interest using mouses
    #I got the raw area of interest 's data/shape using this function
    cv2.namedWindow("image", flags= cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    rect = cv2.selectROI("image", img, showCrosshair, fromCenter)
    #the coordinate to locate the selected area
    (x, y, w, h) = rect
    print("x={}, y={}, w={}, h={}".format(x,y,w,h))
    imCrop = img
    cv2.rectangle(imCrop, (x,y), (x+w,y+h), (255,255,255),1)
    return imCrop

def extract_image(img):
    imgC = img[215:395,43:616] #rough size data based on manual mesurement
    #Using openCV's board detection to determine the final ultrasonic image shape
    gray = cv2.cvtColor(imgC,cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
    _ ,contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    Max = 0
    loc = 0
    for i in range(len(contours)):   
        x = cv2.arcLength(contours[i], 1)
        if(x > Max):
            loc = i
            Max = x
        #print("[{}] {}".format(i,x)) #Debugging 
    #Using the larget contours, the set of point surround the ultrasonic image
    #to get the final image
    x,y,w,h = cv2.boundingRect(contours[loc])  
    # Display cropped image
    #print("C: x={}, y={}, w={}, h={}".format(x,y,w,h)) 
    #cv2.rectangle(imgC,(x,y),(x+w,y+h),(255,255,255),1)    
    #cv2.imshow("image", imgC)
    #cv2.imwrite("image.png", imgC)
    #cv2.waitKey(0)
    #return the choosen area
    return imgC[y:y+h,x:x+w]
    
    
    
# Crop image
ans = extract_image(img)
#cv2.imshow("image_roi", ans)
cv2.imwrite("image_roi.png", ans)
#cv2.waitKey(0)

#print(ans.shape)
#print(img.shape)

