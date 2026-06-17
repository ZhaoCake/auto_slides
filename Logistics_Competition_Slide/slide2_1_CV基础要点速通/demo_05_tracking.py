"""Step 5: 目标跟踪 — CamShift / Meanshift"""
import cv2
import numpy as np
from pathlib import Path

OUT = Path("output")
OUT.mkdir(exist_ok=True)
VIDEO = str(OUT / "tracking_demo.mp4")

# ── 1. 生成合成视频：一个移动的彩色圆球 ──
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
vw = cv2.VideoWriter(VIDEO, fourcc, 30, (640, 480))
cx = 50
for _ in range(150):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.circle(frame, (cx, 240), 30, (0, 128, 255), -1)
    cx += 4
    if cx > 610:
        cx = 50
    vw.write(frame)
vw.release()
print(f"  合成视频已生成: {VIDEO}")

# ── 2. Meanshift 跟踪 ──
cap = cv2.VideoCapture(VIDEO)
ret, first = cap.read()
assert ret
# 手动指定 ROI 跟踪橙色小球
x, y, w_roi, h_roi = 40, 210, 80, 80
roi = first[y:y+h_roi, x:x+w_roi]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([roi_hsv], [0], None, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
meanshift_frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    backproj = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    ret_ms, (x, y, w_roi, h_roi) = cv2.meanShift(backproj, (x, y, w_roi, h_roi), term)
    out = frame.copy()
    cv2.rectangle(out, (x, y), (x+w_roi, y+h_roi), (0, 255, 0), 2)
    cv2.putText(out, "Meanshift", (x, y-8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    meanshift_frames.append(out)
cap.release()

ms_out = str(OUT / "tracking_meanshift.mp4")
vw = cv2.VideoWriter(ms_out, fourcc, 30, (640, 480))
for f in meanshift_frames:
    vw.write(f)
vw.release()
print(f"1/2 Meanshift -> {ms_out} ({len(meanshift_frames)} frames)")

# ── 3. CamShift 跟踪（自适应窗口） ──
cap = cv2.VideoCapture(VIDEO)
ret, first = cap.read()
x, y, w_roi, h_roi = 40, 210, 80, 80
roi = first[y:y+h_roi, x:x+w_roi]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([roi_hsv], [0], None, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
track_window = (x, y, w_roi, h_roi)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
camshift_frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    backproj = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    ret_cs, track_window = cv2.CamShift(backproj, track_window, term)
    pts = cv2.boxPoints(ret_cs)
    pts = np.intp(pts)
    out = frame.copy()
    cv2.polylines(out, [pts], True, (0, 0, 255), 2)
    cv2.putText(out, "CamShift", (track_window[0], track_window[1]-8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    camshift_frames.append(out)
cap.release()

cs_out = str(OUT / "tracking_camshift.mp4")
vw = cv2.VideoWriter(cs_out, fourcc, 30, (640, 480))
for f in camshift_frames:
    vw.write(f)
vw.release()
print(f"2/2 CamShift -> {cs_out} ({len(camshift_frames)} frames)")
