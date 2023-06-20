from twisted.internet import reactor
from quarry.net.proxy import UpstreamFactory, Upstream, DownstreamFactory, Downstream, Bridge
from colorama import init as colorama_init
from colorama import Fore, Back, Style
import struct
import time
import random
import math

colorama_init(autoreset=True)

class QuietBridge(Bridge):
    prev_pos = None
    prev_look = None

    def packet_unhandled(self, buff, direction, name):
        # print(f"[*][{direction}] {name}")
        if direction == "downstream":
            #print(f"[*][${direction}] {name}")
            self.downstream.send_packet(name, buff.read())
        elif direction == "upstream":
            self.upstream.send_packet(name, buff.read())

    def packet_upstream_plugin_message(self, buff):
        buf = buff.read()
        
        # unpacking
        identifier = struct.unpack('H', buf[:2])[0]  # Assuming the identifier is a 2-byte unsigned short (16 bits)
        byte_array_data = buf[1:]
        byte_array_data2 = buf[2:]

        print(f"{colors.UPSTREAM} Identifier: {identifier} | Data: {convert_byte_array_to_string(byte_array_data)}")
        
        # checks
        
        strings_to_check = [b'DL|', b'PERMISSIONSREPL']
        for string in strings_to_check:
            if string in byte_array_data:
                print(f"{colors.BLOCKED} {convert_byte_array_to_string(byte_array_data)}")
                return
        
        # repacking
        modified_byte_array_data = byte_array_data2.replace(b'cmclient:f1df6c8', b'cummod:1337').replace(b'LiteLoader', b'Lunarclient:v2.7.1-2324')
        packed_data = struct.pack('H', identifier) + modified_byte_array_data
        
        print(f"{colors.MOD_BRAND} {convert_byte_array_to_string(modified_byte_array_data)}")
        
        self.upstream.send_packet('plugin_message', packed_data)
        
    def packet_downstream_plugin_message(self, buff):
        buf = buff.read()
        
        # unpacking
        identifier = struct.unpack('H', buf[:2])[0]  # Assuming the identifier is a 2-byte unsigned short (16 bits)
        byte_array_data = buf[1:]
        
        print(f"{colors.DOWNSTREAM} Identifier: {identifier} | Data: {convert_byte_array_to_string(byte_array_data)}")
        
        self.downstream.send_packet('plugin_message', buf)


class QuietDownstreamFactory(DownstreamFactory):
    bridge_class = QuietBridge
    motd = "Brand Strip"
    online_mode = False

class colors:
    MOD_BRAND = f'{Back.CYAN}{Fore.WHITE}[Brand]{Style.RESET_ALL}{Fore.CYAN}'
    UPSTREAM = f'{Back.BLUE}{Fore.WHITE}[↑ Upstream]{Style.RESET_ALL}{Fore.BLUE}'
    DOWNSTREAM = f'{Back.MAGENTA}{Fore.WHITE}[↓ Downstream]{Style.RESET_ALL}{Fore.MAGENTA}'
    BLOCKED = f'{Back.RED}{Fore.WHITE}[Blocked]{Style.RESET_ALL}{Fore.RED}'
    
def convert_byte_array_to_string(byte_array):
    try:
        return byte_array.decode('utf-8').replace('\n', ' ')
    except UnicodeDecodeError:
        return "Failed to parse"

# python brand_strip.py -q 12345
def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--listen-host", default="0.0.0.0", help="address to listen on")
    parser.add_argument("-p", "--listen-port", default=25565, type=int, help="port to listen on")
    parser.add_argument("-b", "--connect-host", default="127.0.0.1", help="address to connect to")
    parser.add_argument("-q", "--connect-port", default=25565, type=int, help="port to connect to")
    args = parser.parse_args(argv)

    # Create factory
    factory = QuietDownstreamFactory()
    factory.connect_host = args.connect_host
    factory.connect_port = args.connect_port

    # Listen
    factory.listen(args.listen_host, args.listen_port)
    print(f"{Back.GREEN}{Fore.WHITE}[*]{Style.RESET_ALL}{Fore.GREEN} Proxy Started {args.listen_host}:{args.listen_port} --> {args.connect_host}:{args.connect_port}")
    reactor.run()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])