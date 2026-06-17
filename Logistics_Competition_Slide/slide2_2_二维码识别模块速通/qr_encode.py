import qrcode


def text_to_qr(text: str, file_path: str = "qr_code.png") -> None:
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    print(f"二维码已保存到: {file_path}")


if __name__ == "__main__":
    text = input("请输入要编码的文本: ")
    file_path = input("请输入保存文件名（默认 qr_code.png）: ").strip()
    if not file_path:
        file_path = "qr_code.png"
    text_to_qr(text, file_path)
