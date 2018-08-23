from pyzbar.pyzbar import decode
from PIL import Image
print(decode(Image.open('output2.jpg')))
