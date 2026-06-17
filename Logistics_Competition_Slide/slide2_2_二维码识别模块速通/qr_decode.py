import cv2
from pyzbar.pyzbar import decode


def detect_qr(frame):
    qr_codes = decode(frame)
    results = []
    for qr in qr_codes:
        data = qr.data.decode("utf-8")
        results.append(data)
        (x, y, w, h) = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return results


if __name__ == "__main__":
    cap = cv2.VideoCapture(1) 
    if not cap.isOpened():
        print("无法打开摄像头")
        raise SystemExit(1)

    print("按 'q' 退出")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = detect_qr(frame)
        for data in results:
            print(f"检测到二维码: {data}")
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
