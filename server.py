import util, os
import datetime, time
import threading
import subprocess, socket

slice_time = 0
start_time = 0
time_list = []
ip_list = [("127.0.0.1", 12312), ("127.0.0.1", 12313), ("127.0.0.1", 12314), ("127.0.0.1", 12315)]

def slice_video(filename, n):
    start = time.time()
    tiles = []
    crop_list = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for i in range(n):
        tile_name = f"tile{i}.mp4"
        if os.path.exists(tile_name):
            os.remove(tile_name)
        subprocess.call(
            'ffmpeg -i {0} -vf crop=iw/4:ih/4:{1}*iw/4:{2}*ih/4 -c:v libx264 -qp 22 -x264-params keyint=30:min-keyint=30:scenecut=0:no-scenecut=1 -an -f mp4 {3}'.format(filename, crop_list[i][0],crop_list[i][1], tile_name),
            stdout=subprocess.PIPE, shell=True)
        tiles.append(tile_name)
    end = time.time()
    print('slice done, process_time={0}s'.format(end - start))
    slice_time = end - start
    return tiles


class VideoToTile(threading.Thread):
    def __init__(self, tid, tile_name, addr):
        threading.Thread.__init__(self)
        self.tid = tid
        self.tile_name = tile_name
        self.remote_addr = addr

    def run(self):
        try:
            conn = socket.socket()  # Create a socket object
            conn.connect(self.remote_addr)

            util.send_file(conn, self.tile_name)
            util.recv_file(conn, "tile_" + str(self.tid) + ".mp4")
            conn.close()
            end_time = time.time()
            print('thread{0} done, process_time={1}s'.format(self.tid, end_time - start_time))
            time_list.append(end_time - start_time)
        except Exception as e:
            print(e)


def run_server(thread_num = 2) -> None:

    tiles = slice_video(util.original_name, thread_num)

    for i in range(thread_num):
        vt = VideoToTile(i, tiles[i], ip_list[i])
        vt.setDaemon(True)
        vt.start()

    print("waiting edge to transcode...")
    time.sleep(1000)


if __name__ == "__main__":
    start_time = time.time()
    run_server()
