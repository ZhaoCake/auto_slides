"""Step 1: 图像读写与显示 — imread / imwrite / imshow"""
import cv2
import numpy as np

SRC = "origin.jpg"

img = cv2.imread(SRC)
if img is None:
    print(f"FAIL: 无法读取 {SRC}，请确认文件存在")
    exit(1)

print(f"OK: shape={img.shape}, dtype={img.dtype}")
print(f"   像素总数: {img.size}, 通道数: {img.shape[2] if len(img.shape) == 3 else 1}")

out = "copy_origin.jpg"
cv2.imwrite(out, img)
print(f"OK: 已保存副本: {out}")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("copy_gray.jpg", gray)
print(f"OK: 已保存灰度版: copy_gray.jpg")

print()
print("imshow 会弹出 GUI 窗口，在 CLI 中不可见，已在代码中注释掉")
print("若有桌面环境，取消下方注释即可查看:")
print("  cv2.imshow('origin', img)")
print("  cv2.waitKey(0)")
print("  cv2.destroyAllWindows()")

cv2.imshow('origin', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
