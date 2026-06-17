"""Step 2: 图像预处理 — 颜色空间 / 缩放 / 滤波 / 形态学"""
import cv2
import numpy as np

SRC = "origin.jpg"
img = cv2.imread(SRC)
assert img is not None, f"cannot read {SRC}"

# ── 1. 颜色空间转换 ──
gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv    = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rgb    = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imwrite("prep_gray.jpg", gray)
cv2.imwrite("prep_hsv.jpg", hsv)
print("1/4 颜色空间: prep_gray.jpg, prep_hsv.jpg")

# ── 2. 缩放 ──
small = cv2.resize(img, (256, 256), interpolation=cv2.INTER_LINEAR)
large = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
cv2.imwrite("prep_small.jpg", small)
cv2.imwrite("prep_large.jpg", large)
print("2/4 缩放: prep_small.jpg (256x256), prep_large.jpg (2x)")

# ── 3. 滤波（去噪 / 平滑） ──
blur      = cv2.blur(img, (7, 7))
gauss     = cv2.GaussianBlur(img, (7, 7), 1.5)
median    = cv2.medianBlur(img, 7)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)
cv2.imwrite("prep_blur.jpg", blur)
cv2.imwrite("prep_gauss.jpg", gauss)
cv2.imwrite("prep_median.jpg", median)
cv2.imwrite("prep_bilateral.jpg", bilateral)
print("3/4 滤波: prep_blur/gauss/median/bilateral.jpg")

# ── 4. 形态学操作（先做二值图做效果更明显） ──
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
kernel = np.ones((5, 5), np.uint8)
dilate  = cv2.dilate(binary, kernel, iterations=1)
erode   = cv2.erode(binary, kernel, iterations=1)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
grad    = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
cv2.imwrite("prep_binary.jpg", binary)
cv2.imwrite("prep_dilate.jpg", dilate)
cv2.imwrite("prep_erode.jpg", erode)
cv2.imwrite("prep_opening.jpg", opening)
cv2.imwrite("prep_closing.jpg", closing)
cv2.imwrite("prep_gradient.jpg", grad)
print("4/4 形态学: prep_binary/dilate/erode/opening/closing/gradient.jpg")
