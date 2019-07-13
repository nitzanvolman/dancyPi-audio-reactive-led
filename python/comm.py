import socket


class PixelsChannel:
    def __init__(self, udp_ip=None, port=7777):
        self.port = port
        self.ip = udp_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.all_data = []


#binds the socket and starts listening
    def listen(self):
        # Create a TCP/IP socket
        sock = self.sock
        sock.settimeout(0.0)

        # Bind the socket to the port
        server_address = ('0.0.0.0', self.port)
        print( 'starting up on %s port %s' % server_address)
        sock.bind(server_address)


    #return the next available datagram or None if the socket is empty.
    #if several datagrams accumulated then skip to the last one and return it.
    def recv(self):
        skipped = -1
        data, address = None, None
        rcv = True
        while rcv:
            try:
                data, address = self.sock.recvfrom(4096)
            except:
                if data == None:
                    # time.sleep(1)
                    continue
                rcv = False
        pm = PixelsMessage.from_bytes(data)
        return pm


    #send the next data_packat
    def send(self, pixels, brightness):
        pm = PixelsMessage(pixels, 0, 0, brightness)
        msg = pm.to_bytes()
        # print(len(msg))
        self.sock.sendto(msg, (self.ip, self.port))
        return


class PixelsMessage:
    def __init__(self, pixels, mode=0, bpm=0, brightness=100):
        self.mode = mode
        self.bpm = bpm
        self.pixels = pixels
        self.brightness = brightness

    def to_bytes(self):
        bts = []
        bts += [b for b in self.mode.to_bytes(1, 'big')]
        bts += [b for b in self.brightness.to_bytes(1, 'big')]
        bts += [b for b in self.bpm.to_bytes(2, 'big')]
        bts += [b for b in len(self.pixels).to_bytes(2, 'big')]
        for p in self.pixels:
            bts += [b for b in p]
        return bytes(bts)

    @staticmethod
    def from_bytes(data):
        bts = bytearray(data)
        mode = int.from_bytes([bts.pop(0)], 'big')
        brightness = int.from_bytes([bts.pop(0)], 'big')
        bpm = int.from_bytes([bts.pop(0), bts.pop(0)], 'big')
        ln = int.from_bytes([bts.pop(0), bts.pop(0)], 'big')
        pixels = []
        for i in range(0, ln):
            pixels += [(bts[i*3], bts[i*3+1], bts[i*3+2])]
        # print(pixels)

        return PixelsMessage(pixels, mode, bpm, brightness)


print('loaded comm.py')