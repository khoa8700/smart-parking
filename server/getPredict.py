from characterSegment import charSegmentation
import numpy as np
import vehicle
import plate
import char
import cv2
import torch
from utils.plots import plot_one_box
from utils.general import xyxy2xywh
from utils.torch_utils import time_synchronized
gn = 0
def cmp(e):
    global gn
    tmp = (xyxy2xywh(torch.tensor(e[1]).view(1, 4)) / gn).view(-1).tolist()
    # print(tmp)
    return abs(tmp[0]-0.5)**2 + abs(tmp[1]-0.5)**2
# names = ['motorcycle', 'car']
# colors = [50,100]
def getPredict(img0):
    # t0 = time_synchronized()
    # t1 = time_synchronized()
    global gn
    gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]
    
    results = vehicle.detect(img0)
    if len(results) == 0:
        return ["",""]
        return img0
    results.sort(key = cmp)

    type_vehicle = results[0][0]
    xyxyVehicle = results[0][1]
    x1=int(xyxyVehicle[0].item())
    y1=int(xyxyVehicle[1].item())
    x2=int(xyxyVehicle[2].item())
    y2=int(xyxyVehicle[3].item())
    img1=img0[y1:y2,x1:x2]

    
    # t2 = time_synchronized()
    # print(f'vehicle: {t2 - t1:.3f}s')
    # t1 = time_synchronized()
    # cv2.imshow('img1',img1)
    # cv2.waitKey(0)
    
    resultPlate = plate.detect(img1)
    if len(resultPlate) == 0:
        return ["",""]
        # results[0][1]+= '-None'
        for label,xyxy in results:
            plot_one_box(xyxy, img0, label=label, color=20, line_thickness=3)
        return img0
    xyxyPlate = resultPlate[0][1]
    x1=int(xyxyPlate[0].item())
    y1=int(xyxyPlate[1].item())
    x2=int(xyxyPlate[2].item())
    y2=int(xyxyPlate[3].item())
    img2=img1[y1:y2,x1:x2]
    
    # t2 = time_synchronized()
    # print(f'plate: {t2 - t1:.3f}s')
    # t1 = time_synchronized()
    # cv2.imshow('img2',img2)
    # cv2.waitKey(0)
    characters_list = charSegmentation(img2)
    # t2 = time_synchronized()
    # print(f'character segmentation: {t2 - t1:.3f}s')
    # t1 = time_synchronized()
    license = ''
    # print(len(characters_list))
    for character in characters_list:
        title = np.array2string(char.detect(character))
        license+=title.strip("'[]")
    # t2 = time_synchronized()
    # print(f'char: {t2 - t1:.3f}s')
    # print(f'overal: {t2 - t0:.3f}s')
    # print(license)
    
    return type_vehicle, license
    xyxy = xyxyPlate
    xyxy[0] += xyxyVehicle[0]
    xyxy[1] += xyxyVehicle[1]
    xyxy[2] += xyxyVehicle[0]
    xyxy[3] += xyxyVehicle[1]
    plot_one_box(xyxy, img0, label=license, color=20, line_thickness=3)
    # results[0][0]+= '-'+license
    print(license)
    for label,xyxy in results:
        plot_one_box(xyxy, img0, label=label, color=20, line_thickness=3)
    # cv2.imshow('img0',img0)
    # cv2.waitKey(0)
    return img0
    