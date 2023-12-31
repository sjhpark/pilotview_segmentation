import os, sys
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from args import get_args
from utils import init_cfg, get_predictor, visualize_prediction

args = get_args()
base_model = args.model

cfg = init_cfg(base_model)

predictor = get_predictor(cfg, "model_final_iter3000_batch4_threshold0.7_freeze0.pth", threshold=0.6)
visualize_prediction(predictor, "test", num_display=248)
