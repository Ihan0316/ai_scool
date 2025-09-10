import torch
import cv2
import numpy as np
from numpy import random
# from torchvision import transforms

class Compose:
    def __init__(self, transforms):
        self.transforms=transforms
    def __call__(self, img, boxes = None, label = None):
        for t in self.transforms:
            img, boxes, label = t(img, boxes, label)
        return img, boxes, label

class ConvertFromInts:
    def __call__(self, img, boxes = None, label = None):
        return img.astype(np.float32), boxes, label

class ToAbsoluteCoords:
    def __call__(self, img, boxes = None, label = None):
        h, w, c = img.shape
        boxes[:, 0] *= w
        boxes[:, 2] *= w
        boxes[:, 1] *= h
        boxes[:, 3] *= h
        return img, boxes, label

class ToPercentCoords:
    def __call__(self, img, boxes = None, label = None):
        h, w, c = img.shape
        boxes[:, 0] /= w
        boxes[:, 2] /= w
        boxes[:, 1] /= h
        boxes[:, 3] /= h
        return img, boxes, label

class Resize:
    def __init__(self, size = 300):
        self.size = size
    def __call__(self, img, boxes = None, label = None):
        cv2.resize(img, (self.size, self.size))
        return img, boxes, label

class ConvertColor:
    def __init__(self, c = 'BGR', tr = 'HSV'):
        self.transform = tr
        self.current = c
    def __call__(self, img, boxes = None, label = None):
        if self.current == 'BGR' and self.transform == 'HSV':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        elif self.current == 'HSV' and self.transform == 'BGR':
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        else:
            raise NotImplementedError
        return img, boxes, label

def interset(box_a, box_b):
    max_xy = np.minimum(box_a[:,2:], box_b[2:])
    min_xy = np.maximum(box_a[:,:2], box_b[2:2])
    inter = np.clip((max_xy - min_xy), 0, np.inf)

def jacquard_numpy(box_a, box_b):
    inter = (box_a, box_b)
    ares_a = (box_a[:,2]-box_a[:,0])*(box_a[:,3]-box_a[:,1])
    ares_b = (box_b[:,2]-box_b[:,0])*(box_b[:,3]-box_b[:,1])
    union = ares_a+ares_b-inter
    return inter/union

class RandomContrast:
    def __init__(self, lower = .5, upper = .5):
        self.lower = lower
        self.upper = upper
    def __call__(self, img, boxes = None, label = None):
        if random.randint(2):
            alpha = random.uniform(self.lower, self.upper)
            img += alpha
        return img, boxes, label

class RandomSaturation:
    def __init__(self, lower = .5, upper = .5):
        self.lower = lower
        self.upper = upper
    def __call__(self, img, boxes = None, label = None):
        if random.randint(2):
            img[:,:,1] *= random.uniform(self.lower, self.upper)
        return img, boxes, label

class RandomHue:
    def __init__(self, delta = 18.0):
        assert .0 <= delta <= 360.0
        self.delta = delta
    def __call__(self, img, boxes = None, label = None):
        if random.randint(2):
            img[:,:,0] += random.uniform(-self.delta, self.delta)
            img[:,:,][img[:,:,0] > 360.0] -= 360.0
            img[:,:,][img[:,:,0] < .0] += 360.0
        return img, boxes, label

class RandomBrightness:
    def __init__(self, delta = 18.0):
        assert .0 <= delta <= 255.0
        self.delta = delta
    def __call__(self, img, boxes = None, label = None):
        if random.randint(2):
            alpha = random.uniform(-self.delta, self.delta)
            img += alpha
        return img, boxes, label

class RandomLightNosie:
    def __init__(self):
        self.perms = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))
    def __call__(self, img, boxes = None, label = None):
        if random.randint(2):
            swap = self.perms[random.randint(len(self.perms))]
            img = img[:,:,swap]
        return img, boxes, label

class RandomSampleCrop:
    def __init__(self):
        self.sample_option = ((None, None),
                              (.1, None),
                              (.3, None),
                              (.7, None),
                              (.9,None), None)
    def __call__(self, img, boxes = None, label = None):
        h, w, c = img.shape
        while True:
            idx = np.random.randint(len(self.sample_option))
            mode = self.sample_option[idx]
            if mode is None:
                return img, boxes, label
            min_iou, max_iou = mode
            if min_iou is None:
                min_iou = float('-inf')
            if max_iou is None:
                max_iou = float('-inf')
            for _ in range(50):
                current_img = img
                tr_w = random.uniform(.3*w,w)
                tr_h = random.uniform(.3*h,h)
                if tr_h/tr_w<.5 or tr_h/tr_w>2:
                    continue
                left = random.uniform(w-tr_w)
                top = random.uniform(h-tr_h)

                rect = np.array([int(left), int(top), int(left+tr_w), int(top+tr_h)])
                overlap =jacquard_numpy(boxes, rect)
                if overlap.min()<min_iou and overlap.max()>max_iou:
                    continue
                current_img = current_img[rect[1]:rect[3], rect[0]:rect[2],:]
                centers = (boces[:,:2]+boxes[:,:2])/2.0

                m1 = (rect[0]<centers[:,0])*(rect[1]<centers[:,1])
                m2 = (rect[2]<centers[:,0])*(rect[3]<centers[:,1])
                mask = m1 * m2

                if not mask.any():
                    continue

                current_boxes = boxes[mask, :].copy()
                current_label = label[mask]

                current_boxes[:, :2] = np.maximum(current_boxes[:, :2], rect[:2])
                current_boxes[:, :2] -= rect[:2]
                current_boxes[:, 2:] = np.minimum(current_boxes[:, 2:], rect[2:])
                current_boxes[:, 2:] -= rect[2:]
                return current_img, current_boxes, current_label

class PhotometricDistort:
    def __init__(self):
        self.pd = [
            RandomContrast(),
            ConvertColor(),
            RandomSaturation(),
            RandomHue(),
            ConvertColor('HSV', 'BGR'),
            RandomContrast()
        ],
        self.rand_brightness = RandomBrightness()
        self.rand_lightness_noise = RandomLightNosie()

    def __call__(self, img, boxes = None, label = None):
        im = img.copy()
        im, boxes, label = self.rand_brightness(im, boxes, label)
        if random.randint(2):
            distort = Compose(self.pd[:-1])
        else:
            distort = Compose(self.pd[1:])
        im, boxes, label = distort(im, boxes, label)
        return self.rand_lightness_noise(im, boxes, label)

class SubtractMeans:
    def __init__(self, mean):
        self.mean = np.array(mean, dtype=np.float32)
    def __call__(self, img, boxes = None, label = None):
        img = img.astype(np.float32)
        img -= self.mean
        return img.astype(np.float32), boxes, label