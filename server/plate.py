import torch
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.torch_utils import select_device
import numpy as np

device = select_device()
half = device.type != 'cpu' 

weights = 'weights/plate.pt'
model = attempt_load(weights, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride

if half:
    model.half()  # to FP16

# Get names
names = model.module.names if hasattr(model, 'module') else model.names

if device.type != 'cpu':
    model(torch.zeros(1, 3, 640, 640).to(device).type_as(next(model.parameters())))

def detect(im0s):
    img = letterbox(im0s, 640, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
        
    pred = model(img)[0]
    # Apply NMS
    pred = non_max_suppression(pred)
    results =[]
    for det in pred:  # detections per image
        label = 'None'
        accuracy = 0
        XyXy = [torch.tensor(0),torch.tensor(0),torch.tensor(0),torch.tensor(0)]
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]}'
                results.append([label,xyxy])
    return results