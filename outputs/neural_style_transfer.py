# -*- coding: utf-8 -*-
"""Neural Style Transfer

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/115egbeHddW9jVm4C1MSe-KeeXOp7NUbB
"""

import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image
from matplotlib import pyplot as plt

import cv2
import numpy as np

def extract_patches(image, patch_size=5, stride=1):
    height, width = image.shape[:2]
    patches = []
    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            patch = image[y:y + patch_size, x:x + patch_size]
            patches.append(patch)
    return np.array(patches)

def calculate_features(patch):
    gray_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
    mean_color = np.mean(gray_patch)
    std_dev = np.std(gray_patch)
    return mean_color, std_dev

def style_transfer(content_img, style_img, patch_size=5, stride=1):
    content_patches = extract_patches(content_img, patch_size, stride)
    style_patches = extract_patches(style_img, patch_size, stride)

    result_img = np.zeros_like(content_img)
    height, width = content_img.shape[:2]
    patch_h, patch_w = patch_size, patch_size

    print(f"Patch count\t content: {len(content_patches)} style: {len(style_patches)}")

    for i, content_patch in enumerate(content_patches):
        content_mean, content_std = calculate_features(content_patch)

        best_match_idx = np.argmin([np.sum((content_mean - style_mean)**2 + (content_std - style_std)**2)
                                    for style_mean, style_std in map(calculate_features, style_patches)])

        y = (i // (width // stride)) * stride
        x = (i % (width // stride)) * stride

        # Handle edges (adjust patch dimensions and slicing for assignment)
        h = min(patch_h, content_img.shape[0] - y)
        w = min(patch_w, content_img.shape[1] - x)

        result_img[y:y + h, x:x + w] = style_patches[best_match_idx][:h, :w]

     # Handle overlapping regions
    overlap_counts = np.zeros_like(result_img)
    for patch in extract_patches(result_img, patch_size, stride=1):
        overlap_counts[y:y + patch_h, x:x + patch_w] += 1

    # Divide and explicitly convert to uint8
    # result_img /= overlap_counts
    # result_img = result_img.astype(np.uint8)

    return result_img.astype(np.uint8) , overlap_counts

# Load your content and style images (assuming they are 100x100)
content_img = cv2.imread('content.png', cv2.IMREAD_COLOR)  # Read only 100x100 region
style_img = cv2.imread('mosaic_style.png', cv2.IMREAD_COLOR)   # Read only 100x100 region

IMG_WDTH = 50
IMG_HGH = 37

content_img = cv2.resize(content_img, (IMG_WDTH, IMG_HGH))
style_img = cv2.resize(style_img, (IMG_WDTH, IMG_HGH))

# Perform style transfer (adjust patch_size and stride as needed)
stylized_img = style_transfer(content_img, style_img, patch_size=2, stride=2)

new_img = stylized_img[0] / (stylized_img[1] + 1)
new_img = new_img.astype(np.uint8)
rgb_image = new_img[:, :, ::-1]

plt.imshow(rgb_image)
plt.axis("off")

import matplotlib.pyplot as plt

cv2.imwrite('stylized_output.jpg', stylized_img[0])
plt.imshow(stylized_img)

style_img

