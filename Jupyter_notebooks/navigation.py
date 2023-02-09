# functions for navigational and solar parameters

import numpy as np

def avg_angle(angle):
    """Averages a sequence of angles. Input: single angle or 1-D numpy array
    Angles in degrees"""
    return (np.arctan2(
        np.sin(angle * np.pi / 180.).mean(), 
        np.cos(angle * np.pi / 180.).mean()) * 180. / np.pi + 360) % 360