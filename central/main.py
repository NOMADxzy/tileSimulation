# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess


# Press the green button in the gutter to run the script.
import time,os
import util

def slice_video(filename, n):
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
    return tiles

if __name__ == '__main__':
    start = time.time()
    tile_num = 2

    tiles = slice_video(util.original_name, tile_num)
    for tile in tiles:
        if os.path.exists("out_"+tile):
            os.remove("out_"+tile)
        subprocess.call(
            'ffmpeg -i {0} -vf scale=640:360 {1} -hide_banner'.format(tile, "out_"+tile),
            stdout=subprocess.PIPE, shell=True)

    end = time.time()
    print("main process time={0}".format(end - start))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
