## 管理员文档

### 部署

该repo提供了docker部署方式，docker的安装详见其[官方文档](https://docs.docker.com/install/overview/)

1. 新建文件夹
2. 下载该repo的[tools/docker-deploy](https://github.com/Botbattle-net/BOTBattle.net/tree/master/tools/docker-deploy)文件夹下的两个文件 ```Dockerfile``` ```sources.list```到该文件夹中
3. 在文件所在目录输入 ```docker build --build-arg KEY=这里填你的secretkey -t botbattle:latest .```
4. 待image拉取成功后启动 ```docker run -p 8001:8001 --name botbattle botbattle```
5. 访问 ```服务器ip:8001/goldennum``` 进入游戏页面
6. 停止游戏 ```docker stop botbattle```