# convert_image.py
from PIL import Image

img = Image.open("friend.jpeg").convert("RGB")  # Ensure 8-bit RGB
img.save("friend_rgb.jpg", format="JPEG")
print("Saved as friend_rgb.jpg")
