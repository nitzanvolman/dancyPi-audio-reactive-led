"""
This File should run on the raspberry pi that is driving the strip.
it will listed on
"""
import time
import comm
from datetime import datetime

STRIP_TYPE = 'APA102' #APA102 or NEOPIXEL
strip = None

TARGET_FPS = 25

if STRIP_TYPE == 'NEOPIXEL':
    import neopixel
    import board
    class NeoPixelStrip:
        def __init__(self, num_pixels=144, pixel_pin = board.D18, ORDER = neopixel.GRB):
            self.pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,pixel_order=ORDER, bpp=3)

        def render_pixels(self, data):
            # print(len(data))
            for i in range(0, len(data)):
                self.pixels[i] = data[i]
            self.pixels.show()

        def clear(self):
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
    strip = NeoPixelStrip(144)

elif STRIP_TYPE == 'APA102':
    import apa102
    class APA102Strip:
        def __init__(self, num_pixels=144):
            self.strip = apa102.APA102(num_pixels)

        def render_pixels(self, data):
            # print(len(data))
            for i in range(0, len(data)):
                self.strip.set_pixel(i, data[i][0], data[i][1], data[i][2])
            self.strip.show()

        def clear(self):
            self.strip.clear_strip()
    strip = APA102Strip(144)


pkt_count = 0
frame_count = 0
start = 0
last_td = 0
last_frame_count = 0
last_pkt_count = 0

pixel_channel = comm.PixelsChannel()
pixel_channel.listen()

all_data = []


start_time = int(time.time()*1000.0)
prev_ts = 0
while True:
    pm = pixel_channel.recv()
    ts = int(time.time()*1000.0) - start_time
    # print(from_start - prev_from_start)


    data = pm.pixels

    if len(data) == 0:
        strip.clear()
        continue

    # s1 = int(time.time()*1000.0)
    strip.render_pixels(data)
    # print(int(time.time()*1000.0 - s1))

    # # print(len(data))
    # for i in range(0, len(data)):
    #     pixels[i] = data[i]
    # pixels.show()

    # frame_count += 1
    # td = (int(time.time()*1000.0) - start)
    # if td - last_td > 2000:
    #     fps = 1000*(frame_count - last_frame_count)/(td-last_td)
    #     print('fps-%s, pkt-%s, frm-%s, time=%s' % (fps, (pkt_count-last_pkt_count), (frame_count-last_frame_count), td))
    #     last_td = td
    #     last_frame_count = frame_count
    #     last_pkt_count = pkt_count

    # if (ts - prev_ts) < (1000/TARGET_FPS):
    #     print('fast')
    #     time.sleep(1)
    #     continue

    print('ready')
    prev_ts = ts

