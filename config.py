"""Settings for audio reactive LED strip"""
from __future__ import print_function
from __future__ import division
import os
import yaml

with open('config.yaml') as f:
    config_dict = yaml.safe_load(f)

    DISPLAY_FPS = config_dict["display_fps"]
    DISPLAY_PIXELS = config_dict["display_pixels"]
    MIC_RATE = config_dict["mic_rate"]
    FPS = config_dict["fps"]
    MIN_FREQUENCY = config_dict["min_frequency"]
    MAX_FREQUENCY = config_dict["max_frequency"]
    N_FFT_BINS = config_dict["n_fft_bins"]
    N_ROLLING_HISTORY = config_dict["n_rolling_history"]
    MIN_VOLUME_THRESHOLD = config_dict["min_volume_threshold"]
    EFFECT = config_dict["effect"]


    USE_GUI = False
