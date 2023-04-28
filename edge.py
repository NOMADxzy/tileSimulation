import time

import util


def transcode(filename):
    time.sleep(3)
    return filename


if __name__ == "__main__":
    import socket  # Import socket module

    sock = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12312
    sock.connect((host, port))

    util.recv_file(sock, util.recv_tile_name)
    transcode_file = transcode(util.recv_tile_name)
    util.send_file(sock, transcode_file)

    sock.close()
    print("Connection closed")
