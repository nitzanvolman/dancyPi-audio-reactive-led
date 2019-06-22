import socket
import sys
import numpy as np
import time
import board
import neopixel
from datetime import datetime


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
ORDER = neopixel.GRB
# The number of NeoPixels
num_pixels = 144

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,pixel_order=ORDER)



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.0)

# Bind the socket to the port
server_address = ('10.0.0.2', 7777)
print ( 'starting up on %s port %s' % server_address)
sock.bind(server_address)

pixels.fill((0, 0, 0))
pixels.show()

target_fps = 20

pkt_count = 0
frame_count = 0
start = 0
last_td = 0
last_frame_count = 0
last_pkt_count = 0

while True:
    # print ('\nwaiting to receive message')
    data, address = None, None
    rcv = True
    while rcv:
        try:
            data, address = sock.recvfrom(4096)
            if pkt_count==0:
                start = int(time.time()*1000.0)
            pkt_count += 1
        except:
            if data == None:
                time.sleep(1)
                continue
            rcv = False

    if len(data) == 0:
        pixels.fill((0, 0, 0))
        pixels.show()
    # print ('(%s,%s,%s,%s),(%s,%s,%s,%s))' % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))

    # pix_delta = np.split(data, 4)

    for i in range(0, len(data), 4):
        pixels[data[i]] = (data[i+1], data[i+2], data[i+3])
    pixels.show()
    frame_count += 1
    td = (int(time.time()*1000.0) - start)
    if td - last_td > 2000:
        fps = 1000*(frame_count - last_frame_count)/(td-last_td)
        print('fps-%s, pkt-%s, frm-%s, time=%s' % (fps, (pkt_count-last_pkt_count), (frame_count-last_frame_count), td))
        last_td = td
        last_frame_count = frame_count
        last_pkt_count = pkt_count

    if td - last_td < 1000/target_fps:
        time.sleep(((1000/target_fps) - (td - last_td))/1000)
