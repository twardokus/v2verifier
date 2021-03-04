from Receiver import Receiver
import socket


class CV2XReceiver(Receiver):
    
    def __init__(self, with_gui=False):
        super().__init__(gui_enabled=with_gui)

    def listen_for_wsms(self, gui_socket, gui_socket_lock):

        print("Listening on localhost:4444 for C-V2X WSMs")

        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.bind(('127.0.0.1', 4444))

        while True:
            wsm = listener.recv(1024)
            self.process_packet(wsm.hex()[52:], gui_socket, gui_socket_lock)

    def process_packet(self, payload, s, lock):
        print("Received BSM:", payload)

    def parse_wsm(self, wsm):
        print("Input to parse_wsm:", wsm)
        # assuming that Ethernet headers do not make it to this level - if they do, need to add 8-byte offset
        
        # ignore the 5 WSMP header bytes
        ieee1609dot2data = wsm
        # print(ieee1609dot2data)
        
        bsm_length = int(ieee1609dot2data[12:14], 16)
        
        # extract SAE J2735 BSM
        bsm = ieee1609dot2data[14:(14+(2*bsm_length))]
        
        self.parse_sae_j2735_bsm(bsm)
    
    def parse_sae_j2735_bsm(self, bsm):
        data = {}
        
        data["sender_id"] = bsm[9:16]
        data["latitude"] = bsm[20:28]
        data["longitude"] = bsm[28:36]
        data["elevation"] = bsm[36:40]
        data["speed"] = bsm[49:52]
        data["heading"] = bsm[52:56]
        
        self.report_bsm(data)

    # 3/3/21 - verified that the offsets in this portion are correct (via Wireshark compare)
    def report_bsm(self, data_dict):
        print("BSM from", data_dict["sender_id"], ": vehicle at (" +
            data_dict["latitude"] + "," + 
            data_dict["longitude"] + "," + 
            data_dict["elevation"] +
            ")" +
            " is moving on bearing " +
            str(data_dict["heading"]) + 
            " at " + 
            str(data_dict["speed"]) +
            " m/s") 
        