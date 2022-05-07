# 镜像构建
docker build -t dearmc/automon:release_v1_001 -f Dockerfile .

# Docker 镜像启动方法
docker run -itd --name automon -p 23456:23456 \  
                -v /data/app/logs:/app/logs \  
                -v /data/app/keys/id_rsa:/app/keys/id_rsa \  
                -v /data/app/templates:/app/templates \  
                dearmc/automon:release_v1_001

# 错误代码
1、错误代码由7位数组成

2、错误码左起两位固定为11，格式为：11XXXXX

3、错误码左起第三位和四位用于表示错误类型

    1) 21 代表参数错误
    2) 22 网络连接错误

4、错误码左起第五位和六位用于表示错误类型

    1）00 代表webapi返回值
    2）01 代表蓝鲸接口模块
    3) 02 代表ssh模块

5、错误码最后一位代表错误代号

