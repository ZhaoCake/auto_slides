"""Step 4: 几何变换 — 仿射 / 透视"""
import cv2
import numpy as np
from pathlib import Path

SRC = "origin.jpg"
OUT = Path("output")
OUT.mkdir(exist_ok=True)

img = cv2.imread(SRC)
h, w = img.shape[:2]
assert img is not None

# ── 1. 仿射变换 ──

# 1a 平移
M_trans = np.float32([[1, 0, 50], [0, 1, 100]])
translated = cv2.warpAffine(img, M_trans, (w, h))
cv2.imwrite(str(OUT / "warp_translate.jpg"), translated)

# 1b 旋转 (绕中心旋转 45°)
M_rot = cv2.getRotationMatrix2D((w//2, h//2), 45, 1.0)
rotated = cv2.warpAffine(img, M_rot, (w, h))
cv2.imwrite(str(OUT / "warp_rotate.jpg"), rotated)

# 1c 缩放 + 旋转 (用 2x3 矩阵手动)
scale = 0.6
M_scale = np.float32([[scale, 0, 0], [0, scale, 0]])
scaled = cv2.warpAffine(img, M_scale, (int(w*scale), int(h*scale)))
cv2.imwrite(str(OUT / "warp_scale.jpg"), scaled)

# 1d 自定义仿射 (三点映射)
pts_src = np.float32([[50, 50], [200, 50], [50, 200]])
pts_dst = np.float32([[70, 80], [180, 40], [80, 220]])
M_affine = cv2.getAffineTransform(pts_src, pts_dst)
custom_affine = cv2.warpAffine(img, M_affine, (w, h))
cv2.imwrite(str(OUT / "warp_affine_custom.jpg"), custom_affine)

print("1/2 仿射变换 -> output/warp_translate|rotate|scale|affine_custom.jpg")

# ── 2. 透视变换 (矫正倾斜) ──
# 模拟"拍摄倾斜"效果: 取四个角点并偏移两个
corners_src = np.float32([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]])
corners_dst = np.float32([[w*0.1, 0], [w*0.9, 0], [w-1, h-1], [0, h-1]])
M_persp = cv2.getPerspectiveTransform(corners_src, corners_dst)
skewed = cv2.warpPerspective(img, M_persp, (w, h))
cv2.imwrite(str(OUT / "persp_skewed.jpg"), skewed)

# 再矫正回来
M_inv = cv2.getPerspectiveTransform(corners_dst, corners_src)
corrected = cv2.warpPerspective(skewed, M_inv, (w, h))
cv2.imwrite(str(OUT / "persp_corrected.jpg"), corrected)

print("2/2 透视变换 -> output/persp_skewed.jpg + persp_corrected.jpg")
