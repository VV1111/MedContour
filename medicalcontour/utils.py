import numpy as np
import math
import cv2
from PyQt5.QtGui import QImage
from matplotlib import pyplot as plt
from scipy import ndimage as ndi
from itertools import cycle

def normalize(slice_data):
    """Normalize the image data to the range [0, 255]"""
    min_val = np.min(slice_data)
    max_val = np.max(slice_data)
    normalized = 255 * (slice_data - min_val) / (max_val - min_val)
    return normalized.astype(np.uint8)

def rgb2gray(img):
    """Convert a RGB image to gray scale."""
    return 0.2989 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]


def inverse_gaussian_gradient(image, alpha=100.0, sigma=5.0):
    """Inverse of gradient magnitude.
    Compute the magnitude of the gradients in the image and then inverts the
    result in the range [0, 1]. 
    """
    gradnorm = ndi.gaussian_gradient_magnitude(image, sigma, mode='nearest')
    return 1.0 / np.sqrt(1.0 + alpha * gradnorm)



class _fcycle(object):

    def __init__(self, iterable):
        """Call functions from the iterable each time it is called."""
        self.funcs = cycle(iterable)

    def __call__(self, *args, **kwargs):
        f = next(self.funcs)
        return f(*args, **kwargs)


# SI and IS operators for 2D and 3D.
_P2 = [np.eye(3),
       np.array([[0, 1, 0]] * 3),
       np.flipud(np.eye(3)),
       np.rot90([[0, 1, 0]] * 3)]


def sup_inf(u):
    """SI operator."""
    if np.ndim(u) == 2:
        P = _P2
    else:
        raise ValueError("u has an invalid number of dimensions ")
    erosions = []
    for P_i in P:
        erosions.append(ndi.binary_erosion(u, P_i))

    return np.array(erosions, dtype=np.int8).max(0)

def inf_sup(u):
    """IS operator."""

    if np.ndim(u) == 2:
        P = _P2
    else:
        raise ValueError("u has an invalid number of dimensions")

    dilations = []
    for P_i in P:
        dilations.append(ndi.binary_dilation(u, P_i))

    return np.array(dilations, dtype=np.int8).min(0)


_curvop = _fcycle([lambda u: sup_inf(inf_sup(u)),   # SIoIS
                   lambda u: inf_sup(sup_inf(u))])  # ISoSI


def _check_input(image, init_level_set):
    """Check that shapes of `image` and `init_level_set` match."""
    if image.ndim not in [2, 3]:
        raise ValueError("`image` must be a 2 or 3-dimensional array.")

    if len(image.shape) != len(init_level_set.shape):
        raise ValueError("The dimensions of the initial level set do not "
                         "match the dimensions of the image.")


def generate_Initial_mask(image, mode, key_points):
    """
    Generate a binary mask using a mode" region, similar to the logic of circular or rectangle mask generation.
    """    
    image_shape = image.shape
    grid = np.mgrid[[slice(i) for i in image_shape]]   
    if len(key_points) ==2:
        [(x1, y1),(x2,y2)] = key_points
        
        # ensure Boundary is within the image range
        x1 = max(0, min(x1, image_shape[1]))
        x2 = max(0, min(x2, image_shape[1]))
        y1 = max(0, min(y1, image_shape[0]))
        y2 = max(0, min(y2, image_shape[0]))

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        center = (center_y, center_x)


        if mode == "rectangle":
            mask_x = (grid[1] >= x1) & (grid[1] <= x2)
            mask_y = (grid[0] >= y1) & (grid[0] <= y2)
            mask = np.int8(mask_x & mask_y)
            roi = image[y1:y2+1, x1:x2+1]
            mean_roi = float(np.mean(roi)) if roi.size > 0 else 0.0

        elif  mode =="ellipse":
            semi_major_axis = abs(x2 - x1) / 2  #
            semi_minor_axis = abs(y2 - y1) / 2  # 
            
            grid_y, grid_x = grid

            ellipse = (((grid_x - center_x) ** 2) / (semi_major_axis ** 2) +
                ((grid_y - center_y) ** 2) / (semi_minor_axis ** 2)) <= 1
            mask = np.int8(ellipse)
            roi = image[mask == 1]
            mean_roi = float(np.mean(roi)) if roi.size > 0 else 0.0

        elif mode =="point":
            radius = np.sqrt(abs(x2 - x1)**2+abs(y2 - y1)**2)/2
            grid = (grid.T - center).T
            phi = radius - np.sqrt(np.sum((grid)**2, 0))
            mask = np.int8(phi > 0)
            roi = image[mask == 1]
            mean_roi = float(np.mean(roi)) if roi.size > 0 else 0.0
    elif len(key_points) ==1 and mode =="point":
        radius = min(image_shape[0],image_shape[1]) * 3.0 / 8.0
        center = key_points[0]
        grid = (grid.T - center).T
        phi = radius - np.sqrt(np.sum((grid)**2, 0))
        mask = np.int8(phi > 0)
        roi = image[mask == 1]
        mean_roi = float(np.mean(roi)) if roi.size > 0 else 0.0


    return mask,mean_roi