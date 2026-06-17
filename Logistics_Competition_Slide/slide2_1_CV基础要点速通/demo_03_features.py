"""Step 3: 特征提取与分析 — 边缘 / 轮廓 / 直线 / 圆 / 角点"""
import cv2
import numpy as np
from pathlib import Path

SRC = "origin.jpg"
OUT = Path("output")
OUT.mkdir(exist_ok=True)

img = cv2.imread(SRC)
assert img is not None, f"cannot read {SRC}"
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ── 1. 边缘检测 ──
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
sobel_x   = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y   = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
canny     = cv2.Canny(gray, 50, 150)

cv2.imwrite(str(OUT / "edge_laplacian.jpg"), np.abs(laplacian).astype(np.uint8))
cv2.imwrite(str(OUT / "edge_sobel_x.jpg"), np.abs(sobel_x).astype(np.uint8))
cv2.imwrite(str(OUT / "edge_sobel_y.jpg"), np.abs(sobel_y).astype(np.uint8))
cv2.imwrite(str(OUT / "edge_canny.jpg"), canny)
print("1/5 边缘检测 -> output/edge_*.jpg")

# ── 2. 轮廓检测 ──
contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
canvas = img.copy()
cv2.drawContours(canvas, contours, -1, (0, 255, 0), 2)
cv2.imwrite(str(OUT / "contours_all.jpg"), canvas)
print(f"2/5 轮廓检测 -> output/contours_all.jpg ({len(contours)} 个轮廓)")

# ── 3. 直线检测 (HoughLinesP) ──
lines = cv2.HoughLinesP(canny, rho=1, theta=np.pi/180, threshold=50,
                        minLineLength=30, maxLineGap=10)
canvas2 = img.copy()
if lines is not None:
    for x1, y1, x2, y2 in lines[:, 0]:
        cv2.line(canvas2, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imwrite(str(OUT / "lines_hough.jpg"), canvas2)
n_lines = len(lines) if lines is not None else 0
print(f"3/5 直线检测 -> output/lines_hough.jpg ({n_lines} 条直线)")

# ── 4. 圆形检测 (HoughCircles) ──
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                           param1=50, param2=30, minRadius=10, maxRadius=100)
canvas3 = img.copy()
if circles is not None:
    circles = np.round(circles[0, :]).astype(int)
    for cx, cy, r in circles:
        cv2.circle(canvas3, (cx, cy), r, (255, 0, 0), 2)
        cv2.circle(canvas3, (cx, cy), 2, (0, 0, 255), 3)
cv2.imwrite(str(OUT / "circles_hough.jpg"), canvas3)
n_circles = len(circles) if circles is not None else 0
print(f"4/5 圆形检测 -> output/circles_hough.jpg ({n_circles} 个圆)")

# ── 5. 角点检测 ──
# 5a Harris
harris = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
canvas4 = img.copy()
canvas4[harris > 0.01 * harris.max()] = [0, 0, 255]
cv2.imwrite(str(OUT / "corners_harris.jpg"), canvas4)

# 5b Shi-Tomasi (goodFeaturesToTrack)
corners = cv2.goodFeaturesToTrack(gray, maxCorners=50, qualityLevel=0.01,
                                  minDistance=10)
canvas5 = img.copy()
if corners is not None:
    corners = corners.astype(int)
    for cx, cy in corners[:, 0]:
        cv2.circle(canvas5, (cx, cy), 4, (0, 0, 255), -1)
cv2.imwrite(str(OUT / "corners_shitomasi.jpg"), canvas5)
n_corners = len(corners) if corners is not None else 0
print(f"5/5 角点检测 -> output/corners_harris.jpg + corners_shitomasi.jpg ({n_corners} 个角点)")
