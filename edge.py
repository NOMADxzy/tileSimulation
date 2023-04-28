import time
import socket
import util
import subprocess


def transcode(filename):
    subprocess.call(
        'ffmpeg -i \"%s\" -vf scale=640:360 \"%s\" -hide_banner' % filename,util.transcode_tile_name,
        stdout=subprocess.PIPE, shell=True)
    return util.transcode_tile_name


if __name__ == "__main__":

    port = 12312  # Reserve a port for your service.
    listener = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    listener.bind((host, port))  # Bind to the port
    listener.listen(5)  # Now wait for client connection.
    print("Server listening....")

    sock, addr = listener.accept()  # Establish connection with client.
    print(f"Got connection from {addr}")

    util.recv_file(sock, util.recv_tile_name)
    transcode_file = transcode(util.recv_tile_name)
    util.send_file(sock, transcode_file)

    sock.close()
    listener.close()
    print("Connection closed")
