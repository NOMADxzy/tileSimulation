import util
import datetime, time
import threading
import subprocess

time_list = []

def slice_video(filename, n):
    time.sleep(2)
    tiles = []
    for i in range(n):
        tiles.append(f"tile{i}.mp4")
    return tiles


class VideoToTile(threading.Thread):
    def __init__(self, tid, ln, tile_name):
        threading.Thread.__init__(self)
        self.tid = tid
        self.listener = ln
        self.tile_name = tile_name

    def run(self):
        try:
            start_time = time.time()
            conn, addr = self.listener.accept()  # Establish connection with client.
            print(f"Got connection from {addr}")

            util.send_file(conn, self.tile_name)
            util.recv_file(conn, "tile_" + str(self.tid) + ".mp4")
            conn.close()
            end_time = time.time()
            print('thread{0} done, process_time={1}s'.format(self.tid, end_time - start_time))
            time_list.append(end_time - start_time)
        except Exception as e:
            print(e)


def run_server() -> None:
    import socket

    port = 12312  # Reserve a port for your service.
    sock = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    sock.bind((host, port))  # Bind to the port
    sock.listen(5)  # Now wait for client connection.

    print("Server listening....")
    i = 0
    thread_num = 4
    tiles = slice_video(util.original_name, thread_num)


    while True:
        vt = VideoToTile(i, sock, tiles[i])
        vt.setDaemon(True)
        vt.start()
        i += 1
        if i==thread_num:
            break

    time.sleep(1000)
    sock.shutdown(1)
    sock.close()


if __name__ == "__main__":
    run_server()
