import cv2
from mjpeg_test import mjpeg
import struct, numpy as np


cap = cv2.VideoCapture(0)

_, frame = cap.read()

