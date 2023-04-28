original_name = "video.mp4"
recv_tile_name = "recv_tile_name.mp4"
transcode_tile_name = "transcode_tile_name.mp4"
tmp_folder = "tmp/"


def recv_file(sock ,filename):
    with open(filename, "wb") as out_file:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            out_file.write(data)  # Write data to a file
            if len(data)<1024: #读到文件末尾
                break

    print("Done receiving")


def send_file(sock ,filename):
    with open(filename, "rb") as in_file:
        data = in_file.read(1024)
        while data:
            sock.send(data)
            data = in_file.read(1024)

    print("Done sending")
