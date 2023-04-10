from retrieve_utils import cache_outputs_coco
from cocoTripletDataset import TripletCOCOdatabase
from torchvision.models.detection import maskrcnn_resnet50_fpn_v2, MaskRCNN_ResNet50_FPN_V2_Weights
from torchvision import transforms
import torch
import os
from net import ResNet_Triplet_COCO

if __name__ == "__main__":
    device = "cuda"
    batch_size = 1
    size = (240,320)#(480, 640)#(240,320)
    allLabelsTrain = "./COCO/instances_train2014.json"
    allLabelsTest = "./COCO/instances_val2014.json"
    
    # Load MASK RCNN pretrained in COCO
    #model = maskrcnn_resnet50_fpn_v2(MaskRCNN_ResNet50_FPN_V2_Weights.COCO_V1)
    model = ResNet_Triplet_COCO()
    # Get backbone
    #model = model.backbone
    model = model.to(device)
    # Load trained weights
    weights = "trained_Mask_backbone_5_epoch_1e-5_margin5.pth"
    model.load_state_dict(torch.load(weights, map_location=device))
    
    
    # Transform
    transformsPretrained = MaskRCNN_ResNet50_FPN_V2_Weights.COCO_V1.transforms()
    transforms = torch.nn.Sequential(
        transformsPretrained,
        transforms.Resize(size),
    )

    # Init dataset
    section = "database"
    databaseImagesPath = "./COCO/train2014/"#"./COCO/train2014/"
    databaseImages = os.listdir(databaseImagesPath)
    jsonPath = "./COCO/mcv_image_retrieval_annotations.json"
    database_dataset = TripletCOCOdatabase(databaseImagesPath, databaseImages, jsonPath,
                                           transforms, section, allLabelsTrain)
    database_loader = torch.utils.data.DataLoader(database_dataset, 
                                               batch_size=batch_size, shuffle=False)#, collate_fn=collate_fn)
    
    cache_filename = weights[:-4] + "_" + section + ".txt"
    cache_outputs_coco(database_loader, model, cache_filename, device)    