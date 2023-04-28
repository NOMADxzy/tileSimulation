# 全景视频 集中式/分布式 切片转码仿真
## 一、central：集中式处理模式
cp video_4k.mp4 central
python main.py
## 二、edge1、2、3、4：分布式处理模式
cd edge1、2、3、4
python edge.py
python server.py
