# 镜像构建
docker build -t dearmc/automon:release_v1_001 -f Dockerfile .

# Docker 镜像启动方法
docker run -itd --name automon -p 23456:23456 -v /data/app/logs:/app/logs dearmc/automon:release_v1_001
