
# 不务正业的Day 6

## 2019/07/13

### docker部署mc服务器

mc服务端默认端口为25565，所以在腾讯云上添加新的安全组

![img1](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/0713_1.png)

![img2](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/0713_2.png)

`systemctl enable docker.service`

把docker设置为开机启动

从https://hub.docker.com/r/itzg/minecraft-server/这个仓库把服务端的镜像拉过来

用下面的命令可以自动拉取

```
docker run -d -e EULA=TRUE \   

    -v /mcworld1_data:/data \   

    -e TYPE=PAPER \

    -e VERSION=1.13.2 \

    -e OPS=willminec \

    -e ONLINE_MODE=FALSE \

    -e difficulty=3 \

    -p 25566:25565 \

    --restart always \

    --name mcworld1 \

    itzg/minecraft-server --noconsole 
```

启动的同时更改几个参数，按照喜好来即可

运行mcbungeecord群组服务器，方便分配不同类型的游戏房间

```
docker run -d -v /mcbg_data:/server \
    -p 25565:25577 \
    --name mcbungeecord \
    --restart always \
    itzg/bungeecord
```

然后一个1.13.2的纯净服就开好了


### rar

```
以下的内容或多或少来自：
http://www.freev.cc/2016/09/08/ctf%E4%B9%8B%E5%8E%8B%E7%BC%A9%E6%96%87%E4%BB%B6/
https://ctf-wiki.github.io/ctf-wiki/misc/archive/rar-zh/
https://bbs.ichunqiu.com/thread-50835-1-1.html

```

文件头：52 61 72 21 1A 07 00


每一段文件块都有以下字段

名称 | 大小	| 描述
  -|-|-
HEAD_CRC | 2 |全部块或块部分的 CRC
HEAD_TYPE | 1 | 块类型
HEAD_FLAGS | 2 | 阻止标志
HEAD_SIZE | 2 | 块大小
ADD_SIZE | 4 |可选字段 - 添加块大小

举个例子：

![rar_0](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_0.png)

其实这些都还算是比较浅显的部分，更多的可以参考《RAR文件格式的研究》

rar就目前来说还是比较玄学的一种压缩格式，导致目前的挖掘其实都还不怎么深入，一下是我的一丢丢发现

#### 重点

对比一下几种不同的情况的rar

![rar_importance_1](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_1.png)

> 未加密的rar

![rar_importance_2](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_2.png)

> rar标准加密过的rar

但是如果把文件名也给加密的话，那么文件头的内容则会产生变化

![rar_importance_2_1](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_2_1.png)

![rar_importance_3](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_3.png)

> rar5标准加密过后的文件

重点来了，众所周知rar，7z这些压缩格式都是可以在加密的同时把文件名也给加密上的。

加密文件名的效果如下：

![rar_importance_4](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_4.png)
![rar_importance_5](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_5.png)
> 使用rar标准加密文件名的效果

注意打红圈的地方

这个部位是之前都没有出现的东西(HEAD_TYPE)，它的作用其实是把加密的文件分开来处理

其实在未加密的rar中也会出现类似的部分，只不过它的值为`XX 74`

也就是说只有当压缩包里面的文件数量大于1的时候才会出现

具体的可以参考bugku里面的某一道题

在这个题目中，我们可以发现这个压缩包里面其实放入了两个文件，但是用压缩软件打开的话却只能读取其中的一个文件，实际上就是压缩包的这一个部位被修改以后出现了问题

![rar_importance_6](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_6.png)

将打红圈的地方修正为`3C 74`即可正常打开压缩包

但是经过我多次测验发现，如果用rar标准将多个文件打包并且设置文件名加密的话

那么这个**分隔符**的值将会是固定的`8B 74`，也就是HEAD_TYPE的长度由2变为了4，所以能够更加准确地判断出压缩包内文件的数量

同时如果修改这个**分隔符**的话，那么压缩包也会出现像上面那道题的情况，可以自己去确认一下


![rar_importance_7](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/rar_importance_7.png)

> 图里是我将4张图片打包以后检索出来的结果，所以可以认定上边的论证是成立的

综上，如果一个rar并没有使用rar5标准加密的话，那么就算把文件名也加密了，也可以从中得知压缩包中文件的大致数量
