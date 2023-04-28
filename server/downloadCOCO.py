from pycocotools.coco import COCO
import requests

# instantiate COCO specifying the annotations json path
coco = COCO('../coco/annotations/instances_val2017.json')
# coco = COCO('../coco/annotations/instances_train2017.json')
catIds = coco.getCatIds(catNms=['car'])
# catIds = coco.getCatIds(catNms=['motocycle'])
imgIds = coco.getImgIds(catIds=catIds)
images = coco.loadImgs(imgIds)
for im in images:
    img_data = requests.get(im['coco_url']).content
    with open('../coco/val_car/' + im['file_name'], 'wb') as handler:
        handler.write(img_data)
