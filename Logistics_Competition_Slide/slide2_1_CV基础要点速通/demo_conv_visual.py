"""卷积操作可视化动画 — 演示核如何在图像上滑动并计算"""
import cv2
import numpy as np

OUT = "output/conv_demo.mp4"

# ── 构建一个 8×8 的小图像（数值 0-9，方便观察） ──
img = np.array([
    [1, 2, 3, 0, 5, 6, 7, 8],
    [0, 9, 2, 3, 4, 0, 1, 2],
    [3, 4, 0, 5, 6, 7, 8, 9],
    [5, 6, 7, 8, 0, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 0],
    [2, 3, 4, 5, 6, 0, 7, 8],
    [9, 0, 1, 2, 3, 4, 5, 6],
    [4, 5, 6, 7, 8, 9, 0, 1],
], dtype=np.float32)

# ── Sobel X 核（边缘检测） ──
kernel = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=np.float32)

K = 3         # 核大小
H, W = img.shape
OH, OW = H - K + 1, W - K + 1
result = np.zeros((OH, OW), dtype=np.float32)

# ── 绘制参数 ──
CELL = 64
GAP  = 2
MARGIN = (50, 40)
PAD = 2          # 额外空行数

def draw_grid(base, data, offset_x, offset_y, rows, cols,
              highlight=None, fmt="{:4.1f}", title=None):
    """在 base 图像上绘制网格数据"""
    y0, x0 = offset_y, offset_x
    for r in range(rows):
        for c in range(cols):
            y1 = y0 + r * (CELL + GAP)
            x1 = x0 + c * (CELL + GAP)
            val = data[r, c]
            color = (200, 200, 200)
            if highlight and (r, c) in highlight:
                color = (80, 180, 255)
            cv2.rectangle(base, (x1, y1),
                          (x1 + CELL, y1 + CELL), color, -1)
            cv2.rectangle(base, (x1, y1),
                          (x1 + CELL, y1 + CELL), (80, 80, 80), 1)
            text = fmt.format(val)
            fx, fy = x1 + CELL//2 - 10, y1 + CELL//2 + 6
            cv2.putText(base, text, (fx, fy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)
    if title:
        cv2.putText(base, title, (x0, y0 - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

AH = 16           # 总行高（网格行数 + 空隙）
AW = 16           # 总列宽
W_canvas = MARGIN[0] * 2 + AW * (CELL + GAP)
H_canvas = MARGIN[1] * 2 + AH * (CELL + GAP)

frames = []
total_steps = OH * OW

step = 0
for oy in range(OH):
    for ox in range(OW):
        canvas = np.zeros((int(H_canvas), int(W_canvas), 3), dtype=np.uint8)

        # ── 左区：原始图像 ──
        hl = set()
        for kr in range(K):
            for kc in range(K):
                hl.add((oy + kr, ox + kc))
        draw_grid(canvas, img, MARGIN[0], MARGIN[1], H, W, highlight=hl,
                  title="Input Image")

        # ── 右上：卷积核 ──
        kx = MARGIN[0] + (W + 2) * (CELL + GAP)
        ky = MARGIN[1]
        draw_grid(canvas, kernel, kx, ky, K, K, fmt="{:5.0f}",
                  title="Kernel (Sobel X)")

        # ── 中右：计算过程 ──
        px = kx
        py = ky + (K + 2) * (CELL + GAP)

        tile = img[oy:oy+K, ox:ox+K]
        prod = tile * kernel
        total = prod.sum()
        result[oy, ox] = total

        # 逐元素显示乘法
        draw_grid(canvas, tile, px, py, K, K, fmt="{:4.1f}",
                  title="Image Patch")

        px2 = px + (K + 1) * (CELL + GAP)
        draw_grid(canvas, prod, px2, py, K, K, fmt="{:5.1f}",
                  title="Element-wise *")

        # 求和公式
        eq_y = py + (K + 1) * (CELL + GAP) + 10
        eq_text = f"Sum = {total:.1f}  ->  output[{oy},{ox}] = {total:.1f}"
        cv2.putText(canvas, eq_text, (px, int(eq_y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)

        # ── 右下：结果矩阵（逐步构建） ──
        ry = MARGIN[1] + (H + 2) * (CELL + GAP)
        rx = MARGIN[0]
        # 填充已计算的部分
        filled = np.zeros((OH, OW), dtype=np.float32)
        filled[:oy+1, :ox+1] = result[:oy+1, :ox+1]
        draw_grid(canvas, filled, rx, ry, OH, OW, fmt="{:6.1f}",
                  title="Output (Convolution Result)")

        step += 1
        progress = int(step / total_steps * 100)
        cv2.putText(canvas, f"Step {step}/{total_steps}  ({progress}%)",
                    (MARGIN[0], int(H_canvas - 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (180, 180, 180), 2)

        frames.append(canvas)

# ── 写入视频 ──
h_, w_ = frames[0].shape[:2]
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
vw = cv2.VideoWriter(OUT, fourcc, 6, (w_, h_))
for f in frames:
    vw.write(f)
vw.release()
print(f"OK: 卷积动画已生成 -> {OUT}")
print(f"   图像: {W}x{H},  核: {K}x{K},  输出: {OW}x{OH},  总帧数: {total_steps}")
print(f"   核类型: Sobel X (垂直边缘检测)")

# ── 额外生成一张"固定布局"的完整示意图 ──
canvas = np.zeros((int(H_canvas), int(W_canvas), 3), dtype=np.uint8)
draw_grid(canvas, img, MARGIN[0], MARGIN[1], H, W, title="Input Image")
kx = MARGIN[0] + (W + 2) * (CELL + GAP)
ky = MARGIN[1]
draw_grid(canvas, kernel, kx, ky, K, K, fmt="{:5.0f}", title="Kernel (Sobel X)")
ry = MARGIN[1] + (H + 2) * (CELL + GAP)
rx = MARGIN[0]
draw_grid(canvas, result, rx, ry, OH, OW, fmt="{:6.1f}", title="Output")
titles = [
    "卷积操作示意图 | Convolution Visualization",
    "核 (Kernel) 在图像 (Input) 上滑动，逐元素相乘后求和得到输出 (Output)",
    "Sobel X 核: 突出垂直边缘（左右差异大时响应强）"
]
for i, t in enumerate(titles):
    cv2.putText(canvas, t, (MARGIN[0], int(H_canvas - 70 + i * 22)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
cv2.imwrite("output/conv_overview.jpg", canvas)
print(f"OK: 卷积总览图 -> output/conv_overview.jpg")
