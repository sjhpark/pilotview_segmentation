import torch
from torchvision import transforms
import numpy as np
import glob
import cv2
import os
import argparse
from tqdm import tqdm
import kornia.augmentation as K

class Augment():
    def __init__(self):
        self.brightness = transforms.ColorJitter(brightness=0, contrast=0, saturation=0, hue=0)
        self.contrast = transforms.ColorJitter(brightness=0, contrast=0, saturation=0, hue=0)
        self.rain = K.RandomRain(p=1.0, number_of_drops=(400, 800), drop_height=(4, 10), drop_width=(-4, 4))
        self.snow = K.RandomSnow(snow_coefficient=(0.5, 0.5), brightness=(2, 2), same_on_batch=False, p=1.0, keepdim=False)

    def RandomNight(self, image):
        brightness_factor = (0, 0.5) 
        self.brightness.brightness = brightness_factor

        contrast_factor = (1.5, 2.5)
        self.contrast.contrast = contrast_factor

        image = self.brightness(image)
        image = self.contrast(image)

        return image
    
    def RandomRain(self, image):
        image = self.rain(image)
        return image
    
    def RandomSnow(self, image):
        image = self.snow(image)
        return image

if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--augment", type=str, default="night", help="augmentation type")
    args = parser.parse_args()

    # make directory
    aug_dict = {"night": Augment().RandomNight, "rain": Augment().RandomRain, "snow": Augment().RandomSnow}

    # import all images from train directory
    # augment = Augment()
    image_paths = glob.glob("dataset/train/*.jpg")
    out_dir = f"dataset/train_augmented_{args.augment}/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for path in tqdm(image_paths, desc="Augmenting images", total=len(image_paths)):
        # load image
        image = cv2.imread(path)
        # BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # convert to tensor
        image = transforms.ToTensor()(image)
        # image = augment(image)
        image = aug_dict[args.augment](image)

        # save
        if len(image.shape) == 4: # if there is batch dimension
            image = image.squeeze(0) # remove batch dimension
        image = transforms.ToPILImage()(image)
        image.save(out_dir + path.split("/")[-1].split(".")[0] + f"_augmented_{args.augment}.jpg")
        


