import cv2
import imutils

def charSegmentation(img):
    scale_percent = 380 # percent of original size
    width = int(img.shape[1] * scale_percent /100)
    height = int(img.shape[0] * scale_percent /100)
    dim = (width, height)
    
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    Sum = 0
    cnt = 0
    for vi in v:
        Sum += sum(vi)
        cnt += len(vi)
    Sum /= cnt
    if Sum > 150:
        v = cv2.subtract(v, 125)
    if Sum < 25:
        v = cv2.add(v, 125)
    v[v>255] = 255
    v[v<0] = 0
    final_hsv = cv2.merge((h,s,v))
    brightness = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    # gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(brightness, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray,(5,5),255)
    binary = cv2.threshold(blur,180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
    thre_mor=cv2.bitwise_not(thre_mor)
                    
    thre_mor = imutils.resize(thre_mor, width=400)
    thre_mor = cv2.medianBlur(thre_mor, 5)
    edged = cv2.Canny(thre_mor, 30, 200)

    crop_characters=[]
    S=set()
    maxY=0
    minY=10000
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    lst=[]

    if len(contours)>0:
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            aspectRatio = w / float(h)
            
            heightRatio=h/float(thre_mor.shape[0])
            ratio=float(thre_mor.shape[0])/float(thre_mor.shape[1])
            
            check=False
            if 0.2 < aspectRatio < 1.0  and ((heightRatio>=0.23 and heightRatio<=0.5 and ratio>=0.45) or (heightRatio>=0.43 and heightRatio<=0.95 and ratio <=0.33)) or check:
                subList=(x,y,w,h) 
                maxY=max(maxY,y)
                minY=min(minY,y) 
                flag=True
                thresholdnow=10
                for already in lst:
                    if abs(already[0]-x)<=thresholdnow:
                        if(abs(already[1]-y)<=thresholdnow):
                            flag=False
                            break
                if(flag):
                    lst.append((x,y))
                    S.add(subList)
    firstLine=[]
    secondLine=[]

    for subList in S:
        x,y,w,h=subList
        curRatio=y/float(thre_mor.shape[0])
        if curRatio>=0.05 and curRatio<=0.4:
            firstLine.append(subList)
        else:
            secondLine.append(subList)
    firstLine=sorted(firstLine,key=lambda x: (x[0]))
    secondLine=sorted(secondLine,key=lambda x: (x[0]))

    for subList in firstLine:
        x,y,w,h=subList
        crop_con=thre_mor[y:y+h,x:x+w]
        _, crop_con = cv2.threshold(crop_con, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        crop_characters.append(crop_con)

    for subList in secondLine:
        x,y,w,h=subList
        crop_con=thre_mor[y:y+h,x:x+w]
        _, crop_con = cv2.threshold(crop_con, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        crop_characters.append(crop_con)
    return crop_characters
