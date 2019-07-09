# Day1

## 2019/07/08

### git基本命令

git init         //新建git类型的仓库  
git add .        //把所有文件添加进仓库  
git commit -m "first commit"     //提交修改的信息，引号里面写描述  
git remote add origin https://github.com/largewaste/cqr.git    //添加到自己的仓库  
git push -u origin master   //分配到远程服务器  




ssh-keygen -t rsa -C "邮箱地址"

这里的邮箱地址即为你的github账号邮箱。  

在资源管理器中打开这个.ssh文件夹，在它下面会看到两个文件，

选择后缀名为.pub的文件并用记事本打开，复制这个文件中的所有内容。

然后在git上的设置李淼导入此密钥  

ssh git@github.com  

连接认证