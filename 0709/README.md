# Day2

## 2019/07/09  

### zsh+oh-my-zsh的安装
`sudo apt-get install -y zsh `
> -y的意思是安装的默认选项都为yes  

`sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"`
> wget安装oh-my-zsh，下载安装一部搞定

`sudo apt-get install fonts-powerline`
> 安装某些主题可能要用到的字体库

`vim ~/.zshrc`
> 编辑配置文件，锁定到 `ZSH_THEME="robbyrussell"` 这一行 引号内即为主题，后来我把主题换掉了

`chsh -s /bin/zsh`
> 设置为默认系统终端，重启后生效

### 安装htop
 `sudo apt-get install htop`
### 部署lnmp
https://lnmp.org/install.html
一键安装完事
### docker
`service docker restart`
> 重启docker，方便之后再部署
`docker search sqli-labs`
> 搜索需要部署的靶机
`docker pull acgpiano/sqli-labs`
> 拉取镜像到本地，然后等下载
`docker images`
> 查看本地存在的镜像
`docker run -dt --name sqli-labs -p 233:80 --rm acgpiano/sqli-labs`
`ip -a`
> 233为物理机上的端口号，通过ip -a指令寻找物理机应该访问的ip

