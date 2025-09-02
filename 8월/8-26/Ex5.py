from keras.datasets import mnist
from keras.models import load_model
from matplotlib import pyplot as plt
import cv2

def s_f(in_x):
    x = cv2.resize(in_x, (28, 28), interpolation=cv2.INTER_CUBIC)
    s_x = x.reshape(-1, 28*28)/255.0
    return s_x

m = load_model('m.keras')

def end_f(py):
    out = py.argmax(axis=1)
    return out