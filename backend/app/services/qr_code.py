import qrcode

def generate_qr(data):
    img = qrcode.make(data)
    img.save('new_qr.png')
    return 'new_qr.png'
