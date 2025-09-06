import qrcode
import io
import base64

# def generate_qr(data):
#     img = qrcode.make(data)
#     img.save('new_qr.png')
#     return 'new_qr.png'

def generate_qr(data: str) -> str:
    img = qrcode.make(data)
    buffered = io.BytesIO()
    img.save(buffered)
    img_base64 = base64.b64encode(buffered.getbuffer()).decode("utf-8")
    return img_base64

