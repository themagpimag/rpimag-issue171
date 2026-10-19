import network
import picographics
import rp2
import socket
import time

rp2.country("GB")

ssid = "<Wi-Fi SSID>"
psk = "<Wi-Fi Password>"

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, psk)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
  time.sleep(0.5)
print("Connected! IP:", wlan.ifconfig()[0])

# Initialize display with RGB332
display = picographics.PicoGraphics(
    display=picographics.DISPLAY_PICO_DISPLAY_2,
    pen_type=picographics.PEN_RGB332,
)

# Turn on the backlight
display.set_backlight(1.0)

width, height = display.get_bounds()
print(f"Display resolution initialized as: {width}x{height}")

# Create a backing bytearray and map it to the framebuffer
frame_size = width * height
fb_data = bytearray(frame_size)
display.set_framebuffer(fb_data)
mv = memoryview(fb_data)

# Connect to Mac server socket
sockaddr = socket.getaddrinfo("<IP address of computer>", 2000)[0][-1]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to streaming server...")
sock.connect(sockaddr)
print("Streaming active!")

# Streaming loop
try:
  while True:
    bytes_read = 0
    while bytes_read < frame_size:
      chunk = sock.readinto(mv[bytes_read:])
      if not chunk:
        raise OSError("Connection closed by server (EOF)")
      bytes_read += chunk

    # Push the buffer to the screen
    display.update()

except Exception as e:
  print("Error:", e)
  sock.close()